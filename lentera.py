import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfigurasi Halaman Utama
st.set_page_config(page_title="LENTERA", page_icon="🕯️", layout="centered")

# Alamat URL Google Sheets kamu
URL_SHEET = "https://docs.google.com/spreadsheets/d/1nD-50cq8hGjINIQN6z0-xT_rq-9tymDwjuewITK0gHU/edit?usp=sharing"

# Inisialisasi Koneksi ke Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# Inisialisasi Session State agar data tidak hilang saat pindah menu
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'kelas' not in st.session_state:
    st.session_state.kelas = ""

# --- TAMPILAN HEADER ---
st.title("🕯️ LENTERA")
st.subheader("Layanan Terintegrasi untuk Resiliensi dan Kesehatan Mental Remaja")
st.markdown("---")

# --- PROSES LOGIN (Sidebar) ---
st.sidebar.title("🔑 Menu Login")
if st.session_state.role is None:
    pilihan_role = st.sidebar.radio("Pilih Akun:", ["Belum Login", "Siswa", "Guru BK"])
    if pilihan_role == "Siswa":
        st.session_state.role = "Siswa"
    elif pilihan_role == "Guru BK":
        st.session_state.role = "Guru BK"
else:
    st.sidebar.write(f"Login sebagai: **{st.session_state.role}**")
    if st.session_state.username:
        st.sidebar.write(f"User: {st.session_state.username}")
    if st.sidebar.button("Logout 🚪"):
        st.session_state.role = None
        st.session_state.username = ""
        st.session_state.kelas = ""
        if 'bk_logged_in' in st.session_state:
            st.session_state.bk_logged_in = False
        st.rerun()

# --- HALAMAN BELUM LOGIN ---
if st.session_state.role is None or st.session_state.role == "Belum Login":
    st.info("Silakan pilih jenis login di menu sebelah kiri (sidebar) untuk memulai layanan.")

# --- HALAMAN SISWA ---
elif st.session_state.role == "Siswa":
    if not st.session_state.username or not st.session_state.kelas:
        st.write("### Hai kawan, selamat datang di LENTERA! 👋")
        st.write("Silakan masukkan username kamu secara anonim dan asal kelas kamu ya.")
        
        user_input = st.text_input("Username Anonim:")
        kelas_input = st.text_input("Asal Kelas:")
        
        if st.button("Masuk"):
            if user_input and kelas_input:
                st.session_state.username = user_input
                st.session_state.kelas = kelas_input
                st.rerun()
            else:
                st.warning("Mohon isi username dan kelas terlebih dahulu!")
    else:
        st.success(f"Halo **{st.session_state.username}** dari kelas **{st.session_state.kelas}**, apa yang kamu butuhkan hari ini?")
        
        menu_siswa = st.selectbox(
            "Pilih Layanan LENTERA:",
            ["Pilih Menu", "1. Refleksi (Mind Check)", "2. Nyala (Weekly Mood Tracker)", "3. Ruang (Curhat Anonim)", 
             "4. Pijar (Tips & Edukasi)", "5. Jembatan (Konsultasi Guru BK)", "6. Teman (Peer Support)", "7. Jejak (Riwayat)"]
        )

        # 1. FITUR REFLEKSI
        if "1. Refleksi" in menu_siswa:
            st.write("### 📊 REFLEKSI (Mind Check)")
            st.write("Jawablah sesuai indikator berikut: 1 = Tidak Pernah, 2 = Jarang, 3 = Kadang-kadang, 4 = Sering, 5 = Sangat sering.")
            
            pertanyaan_refleksi = [
                "Saya merasa lelah secara emosional setelah menjalani kegiatan belajar.",
                "Saya merasa energi saya cepat habis karena aktivitas akademik.",
                "Saya sulit merasa rileks meskipun waktu belajar telah selesai.",
                "Saya merasa kegiatan sekolah menguras kondisi mental saya.",
                "Saya merasa stres ketika memikirkan tugas, ujian, atau nilai.",
                "Saya kehilangan semangat dan motivasi untuk belajar.",
                "Saya merasa sulit berkonsentrasi saat mengikuti pelajaran.",
                "Saya menunda mengerjakan tugas karena merasa terlalu lelah.",
                "Saya merasa belajar tidak lagi memberikan kepuasan seperti sebelumnya.",
                "Saya merasa prestasi saya tidak sebanding dengan usaha yang telah saya lakukan.",
                "Saya merasa harus selalu mendapatkan nilai yang tinggi.",
                "Saya takut mengecewakan orang tua, guru, atau orang lain jika prestasi saya menurun.",
                "Saya merasa orang lain menganggap saya baik-baik saja meskipun sebenarnya sedang tertekan.",
                "Saya kesulitan menceritakan tekanan yang saya alami kepada orang lain.",
                "Saya merasa membutuhkan bantuan, tetapi ragu untuk mencarinya."
            ]
            
            jawaban = []
            for i, q in enumerate(pertanyaan_refleksi):
                jawaban.append(st.radio(f"{i+1}. {q}", [1, 2, 3, 4, 5], index=2, key=f"ref_{i}"))
            
            if st.button("Hitung Skor Refleksi"):
                skor_total = sum(jawaban)
                st.write(f"**Total Skor Anda:** {skor_total}/75")
                
                if skor_total <= 35:
                    st.success("🟢 **Tingkat Risiko: RENDAH**\n\nTetap jaga keseimbangan antara belajar dan istirahat.")
                    kategori = "Rendah"
                elif skor_total <= 56:
                    st.warning("🟡 **Tingkat Risiko: SEDANG**\n\nKamu mulai menunjukkan tanda-tanda kelelahan akademik.")
                    kategori = "Sedang"
                else:
                    st.error("🔴 **Tingkat Risiko: TINGGI**\n\nLENTERA mendeteksi adanya risiko burnout akademik. Segera konsultasi ke Guru BK.")
                    kategori = "Tinggi"
                
                # Simpan ke Google Sheets tab 'jejak'
                simpan_ke_sheets("jejak", {
                    "Username": st.session_state.username,
                    "Fitur": "Refleksi",
                    "Skor": f"{skor_total}/75",
                    "Kategori": kategori
                })
                st.success("Hasil refleksi berhasil disinkronkan ke cloud!")

        # 3. FITUR RUANG (Curhat Anonim)
        elif "3. Ruang" in menu_siswa:
            st.write("### 💬 RUANG (Curhat Anonim)")
            st.write("Di sini kamu bebas bercerita. Identitasmu tetap rahasia.")
            isi_curhat = st.text_area("Tuliskan apa yang sedang kamu rasakan di sini:")
            
            if st.button("Kirim Cerita"):
                if isi_curhat:
                    # Simpan ke Google Sheets tab 'curhat'
                    simpan_ke_sheets("curhat", {
                        "Username": st.session_state.username,
                        "Kelas": st.session_state.kelas,
                        "Isi Curhat": isi_curhat
                    })
                    st.success("Terima kasih sudah berbagi cerita. Ceritamu aman di database cloud kami.")
                else:
                    st.warning("Jangan lupa tulis ceritamu dulu ya.")

        # 5. FITUR JEMBATAN (Jadwal BK)
        elif "5. Jembatan" in menu_siswa:
            st.write("### 🤝 JEMBATAN (Konsultasi dengan Guru BK)")
            hari = st.selectbox("Pilih Hari:", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
            jam = st.selectbox("Pilih Jam:", ["09.00", "10.00", "11.00", "13.00", "14.00"])
            if st.button("Ajukan Jadwal"):
                # Simpan ke Google Sheets tab 'jadwalBK'
                simpan_ke_sheets("jadwalBK", {
                    "Username": st.session_state.username,
                    "Kelas": st.session_state.kelas,
                    "Hari": hari,
                    "Jam": jam
                })
                st.success(f"Jadwal berhasil diajukan untuk hari {hari} jam {jam}!")

        # 6. FITUR TEMAN (Peer Support)
        elif "6. Teman" in menu_siswa:
            st.write("### 🧑‍🤝‍🧑 TEMAN (Peer Support)")
            kebutuhan = st.selectbox("Apa yang sedang kamu butuhkan?", ["Ingin Didengarkan", "Teman Belajar", "Motivasi Belajar"])
            if st.button("Kirim Pengajuan"):
                # Simpan ke Google Sheets tab 'peer_support'
                simpan_ke_sheets("peer_support", {
                    "Username": st.session_state.username,
                    "Kelas": st.session_state.kelas,
                    "Kebutuhan": kebutuhan,
                    "Status": "Menunggu Persetujuan"
                })
                st.success("Permintaan peer support berhasil dikirim!")
                
        # 7. FITUR JEJAK
        elif "7. Jejak" in menu_siswa:
            st.write("### 📜 JEJAK (Riwayat Aktivitas Cloud Anda)")
            df_jejak = baca_dari_sheets("jejak")
            if not df_jejak.empty:
                # Filter data berdasarkan user aktif saat ini
                df_user = df_jejak[df_jejak["Username"] == st.session_state.username]
                if not df_user.empty:
                    st.dataframe(df_user[["Fitur", "Skor", "Kategori"]], use_container_width=True)
                else:
                    st.write("Belum ada riwayat aktivitas untuk akun ini.")
            else:
                st.write("Belum ada data.")

# --- HALAMAN GURU BK ---
elif st.session_state.role == "Guru BK":
    st.write("### 💻 LOGIN GURU BK")
    
    if 'bk_logged_in' not in st.session_state:
        st.session_state.bk_logged_in = False
        
    if not st.session_state.bk_logged_in:
        bk_user = st.text_input("Username BK:")
        bk_pass = st.text_input("Password BK:", type="password")
        if st.button("Login BK"):
            if bk_user == "BKLentera2026" and bk_pass == "123456":
                st.session_state.bk_logged_in = True
                st.session_state.username = "Guru BK"
                st.rerun()
            else:
                st.error("Username atau Password salah!")
    else:
        st.success("Selamat Datang di Dashboard Guru BK (Mode Sinkronisasi Cloud)")
        menu_bk = st.selectbox("Pilih Data yang Ingin Dilihat:", 
                               ["Pilih Menu Dashboard", "1. Curhat Anonim", "2. Jadwal Konseling", "3. Peer Support", "4. Hasil Refleksi", "5. Early Warning (Risiko Tinggi)"])
        
        if menu_bk == "1. Curhat Anonim":
            st.write("### 💬 Daftar Curhat Siswa (Murni Anonim)")
            df_curhat = baca_dari_sheets("curhat")
            if not df_curhat.empty and "Isi Curhat" in df_curhat.columns:
                for isi in df_curhat["Isi Curhat"].dropna():
                    st.info(f"“ {isi} ”")
            else:
                st.write("Belum ada data curhat masuk di Google Sheets.")
                
        elif menu_bk == "2. Jadwal Konseling":
            st.write("### 📅 Daftar Pengajuan Jadwal BK")
            df_jadwal = baca_dari_sheets("jadwalBK")
            if not df_jadwal.empty:
                st.dataframe(df_jadwal, use_container_width=True)
            else:
                st.write("Tidak ada jadwal pengajuan.")
            
        elif menu_bk == "3. Peer Support":
            st.write("### 🧑‍🤝‍🧑 Daftar Request Peer Support")
            df_peer = baca_dari_sheets("peer_support")
            if not df_peer.empty:
                st.dataframe(df_peer, use_container_width=True)
            else:
                st.write("Tidak ada data pengajuan peer support.")
            
        elif menu_bk == "4. Hasil Refleksi":
            st.write("### 📊 Semua Data Hasil Refleksi Siswa")
            df_jejak = baca_dari_sheets("jejak")
            if not df_jejak.empty:
                st.dataframe(df_jejak, use_container_width=True)
            else:
                st.write("Belum ada riwayat refleksi.")
            
        elif menu_bk == "5. Early Warning (Risiko Tinggi)":
            st.write("### ⚠️ Siswa Butuh Penanganan Segera:")
            df_jejak = baca_dari_sheets("jejak")
            if not df_jejak.empty and "Kategori" in df_jejak.columns:
                df_tinggi = df_jejak[df_jejak["Kategori"] == "Tinggi"]
                if not df_tinggi.empty:
                    st.error("Ditemukan siswa dengan tingkat Burnout TINGGI!")
                    st.dataframe(df_tinggi, use_container_width=True)
                else:
                    st.success("Aman! Tidak ada indikasi siswa dengan tingkat risiko tinggi saat ini.")