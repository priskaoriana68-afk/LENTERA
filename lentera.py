import streamlit as st
import os

# Konfigurasi Halaman Utama
st.set_page_config(page_title="LENTERA", page_icon="🕯️", layout="centered")

# Inisialisasi Session State agar data tidak hilang saat pindah menu
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'kelas' not in st.session_state:
    st.session_state.kelas = ""

# --- FUNGSI SIMPAN FILE ---
def simpan_ke_file(nama_file, teks):
    with open(nama_file, "a", encoding="utf-8") as f:
        f.write(teks + "\n")

def baca_file(nama_file):
    if os.path.exists(nama_file):
        with open(nama_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Belum ada data riwayat aktivitas."

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
                    st.warning("🟡 **Tingkat Risiko: SEDANG**\n\nKamu mulai menunjukkan tanda-tanda kelelahan akademik. Disarankan membuka menu Pijar atau Jembatan.")
                    kategori = "Sedang"
                else:
                    st.error("🔴 **Tingkat Risiko: TINGGI**\n\nLENTERA mendeteksi adanya risiko burnout akademik. Segera manfaatkan layanan konseling melalui menu Jembatan.")
                    kategori = "Tinggi"
                
                st.caption("Hasil ini merupakan skrining awal dan bukan diagnosis medis.")
                
                log_teks = f"==================================\nUsername : {st.session_state.username}\nFitur    : Refleksi\nSkor     : {skor_total}/75\nKategori : {kategori}\n==================================\n"
                simpan_ke_file("jejak.txt", log_teks)
                st.success("Hasil refleksi berhasil disimpan ke riwayat Jejak.")

        # 2. FITUR NYALA
        elif "2. Nyala" in menu_siswa:
            st.write("### 🕯️ NYALA (Weekly Mood Tracker)")
            st.write("1 = Sangat Buruk, 2 = Buruk, 3 = Biasa, 4 = Baik, 5 = Sangat Baik")
            
            pertanyaan_nyala = [
                "Bagaimana suasana hatimu hari ini?",
                "Bagaimana kualitas tidurmu tadi malam?",
                "Bagaimana tingkat energimu hari ini?",
                "Seberapa semangat kamu menjalani aktivitas hari ini?",
                "Seberapa mampu kamu mengelola stres hari ini?"
            ]
            
            jawaban_nyala = []
            for i, q in enumerate(pertanyaan_nyala):
                jawaban_nyala.append(st.radio(f"{i+1}. {q}", [1, 2, 3, 4, 5], index=2, key=f"nyala_{i}"))
                
            if st.button("Submit Mood"):
                total_mood = sum(jawaban_nyala)
                st.write(f"**Skor Mood:** {total_mood}/25")
                
                if total_mood <= 10:
                    st.error("Mood hari ini kurang baik. Kami menyarankan kamu beristirahat dan mencari dukungan.")
                elif total_mood <= 18:
                    st.warning("Mood hari ini cukup stabil. Tetap jaga keseimbangan antara belajar dan istirahat.")
                else:
                    st.success("Mood hari ini baik! Semangat menjalani aktivitas hari ini. ✨")
                
                log_nyala = f"==================================\nUsername : {st.session_state.username}\nFitur    : Nyala\nMood     : {total_mood}/25\n==================================\n"
                simpan_ke_file("nyala.txt", log_nyala)

        # 3. FITUR RUANG
        elif "3. Ruang" in menu_siswa:
            st.write("### 💬 RUANG (Curhat Anonim)")
            st.write("Di sini kamu bebas bercerita. Identitasmu akan tetap rahasia/anonim.")
            isi_curhat = st.text_area("Tuliskan apa yang sedang kamu rasakan di sini:")
            
            if st.button("Kirim Cerita"):
                if isi_curhat:
                    log_curhat = f"====================================\nUsername : {st.session_state.username}\nKelas    : {st.session_state.kelas}\nCurhat   :\n{isi_curhat}\n------------------------------------\n"
                    simpan_ke_file("curhat.txt", log_curhat)
                    st.success("Terima kasih sudah berbagi cerita. Ceritamu aman bersama kami.")
                else:
                    st.warning("Jangan lupa tulis ceritamu dulu ya.")

        # 4. FITUR PIJAR
        elif "4. Pijar" in menu_siswa:
            st.write("### 💡 PIJAR (Tips & Edukasi)")
            st.info('"Istirahat bukan berarti menyerah, melainkan memberi diri kesempatan untuk kembali bersinar."')
            
            materi = st.selectbox("Pilih materi edukasi:", ["Pilih Materi", "Mengenal Burnout Akademik", "Manajemen Stres", "Tips Belajar Sehat", "Sleep Hygiene"])
            
            if materi == "Mengenal Burnout Akademik":
                st.markdown("**Burnout Akademik** merupakan kondisi kelelahan fisik, emosional, dan mental yang disebabkan oleh tekanan belajar secara terus-menerus.")
            elif materi == "Manajemen Stres":
                st.markdown("- Atur waktu belajar dan istirahat.\n- Luangkan waktu untuk hobi.\n- Jangan ragu bercerita kepada orang terpercaya.\n- Lakukan latihan pernapasan saat cemas.")
            elif materi == "Tips Belajar Sehat":
                st.markdown("- Gunakan metode Pomodoro (25 menit belajar, 5 menit istirahat).\n- Fokus pada proses, bukan hasil.\n- Hindari sistem kebut semalam (SKS).\n- Buat target belajar realistis.")
            elif materi == "Sleep Hygiene":
                st.markdown("- Tidur 7-9 jam semalam.\n- Hindari gadget 30 menit sebelum tidur.\n- Kurangi kafein di malam hari.\n- Jadwal tidur yang konsisten.")

        # 5. FITUR JEMBATAN
        elif "5. Jembatan" in menu_siswa:
            st.write("### 🤝 JEMBATAN (Konsultasi dengan Guru BK)")
            opsi_jembatan = st.selectbox("Pilih Layanan:", ["Pilih Layanan", "Konseling Online (Anonim)", "Ajukan Pertemuan Tatap Muka", "Informasi Ruang BK"])
            
            if opsi_jembatan == "Konseling Online (Anonim)":
                keluhan = st.text_area("Tuliskan keluhan atau hal yang ingin dikonsultasikan:")
                if st.button("Kirim Keluhan"):
                    log_konsel = f"==================================\nUsername : {st.session_state.username}\nKelas    : {st.session_state.kelas}\nJenis    : Konseling Online\nKeluhan  : {keluhan}\n==================================\n"
                    simpan_ke_file("konseling_online.txt", log_konsel)
                    
                    simpan_ke_file("jejak.txt", f"==================================\nUsername : {st.session_state.username}\nFitur    : Jembatan\nStatus   : Menunggu Konfirmasi\n==================================\n")
                    st.success("Permintaan berhasil dikirim! Guru BK akan segera menindaklanjuti.")
                    
            elif opsi_jembatan == "Ajukan Pertemuan Tatap Muka":
                hari = st.selectbox("Pilih Hari:", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
                jam = st.selectbox("Pilih Jam:", ["09.00", "10.00", "11.00", "13.00", "14.00"])
                if st.button("Ajukan Jadwal"):
                    log_jadwal = f"==================================\nUsername : {st.session_state.username}\nKelas    : {st.session_state.kelas}\nHari     : {hari}\nJam      : {jam}\n==================================\n"
                    simpan_ke_file("jadwalBK.txt", log_jadwal)
                    st.success(f"Jadwal berhasil diajukan untuk hari {hari} jam {jam}. Silakan tunggu konfirmasi.")
                    
            elif opsi_jembatan == "Informasi Ruang BK":
                st.markdown("**Jam Operasional:**\nSenin - Jumat | 07.00 - 15.00\n\n**Lokasi:**\nRuang BK Lantai 1\n\n**Kontak:**\nEmail: bk@sman.sch.id")

        # 6. FITUR TEMAN
        elif "6. Teman" in menu_siswa:
            st.write("### 🧑‍🤝‍🧑 TEMAN (Peer Support)")
            opsi_teman = st.radio("Pilih Opsi:", ["Ajukan Pendamping Sebaya", "Tentang Peer Support"])
            
            if opsi_teman == "Ajukan Pendamping Sebaya":
                kebutuhan = st.selectbox("Apa yang sedang kamu butuhkan?", 
                                         ["Ingin Didengarkan", "Teman Belajar (Tutor Sebaya)", "Motivasi Belajar", "Pendamping Akademik (Ujian)", "Teman Berbagi Cerita"])
                if st.button("Kirim Pengajuan"):
                    log_peer = f"==================================\nUsername : {st.session_state.username}\nKelas    : {st.session_state.kelas}\nKebutuhan : {kebutuhan}\nStatus   : Menunggu Persetujuan Guru BK\n==================================\n"
                    simpan_ke_file("peer_support.txt", log_peer)
                    
                    simpan_ke_file("jejak.txt", f"==================================\nUsername : {st.session_state.username}\nFitur    : Peer Support\nStatus   : Menunggu Persetujuan\n==================================\n")
                    st.success("Permintaan berhasil dikirim! Guru BK akan meninjau.")
                    
            elif opsi_teman == "Tentang Peer Support":
                st.write("Peer Support merupakan layanan pendampingan oleh siswa yang telah mendapat pelatihan langsung dari Guru BK.")

        # 7. FITUR JEJAK
        elif "7. Jejak" in menu_siswa:
            st.write("### 📜 JEJAK (Riwayat Aktivitas Anda)")
            konten_jejak = baca_file("jejak.txt")
            st.text(konten_jejak)

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
        st.success("Selamat Datang di Dashboard Guru BK")
        menu_bk = st.selectbox("Pilih Data yang Ingin Dilihat:", 
                               ["Pilih Menu Dashboard", "1. Curhat Anonim", "2. Jadwal Konseling", "3. Peer Support", "4. Hasil Refleksi", "5. Early Warning (Risiko Tinggi)", "6. Statistik Layanan", "7. Cetak Laporan"])
        
        if menu_bk == "1. Curhat Anonim":
            st.write("### 💬 Daftar Curhat Siswa (Murni Anonim)")
            konten_curhat = baca_file("curhat.txt")
            
            # Memisahkan file per blok postingan curhat
            blok_curhat = konten_curhat.split("====================================")
            ada_curhat = False
            
            for blok in blok_curhat:
                if "Curhat   :" in blok:
                    ada_curhat = True
                    # Memotong teks hanya mengambil bagian di bawah label Curhat :
                    bagian_isi = blok.split("Curhat   :")[-1].split("------------------------------------")[0].strip()
                    if bagian_isi:
                        st.info(f"“ {bagian_isi} ”")
                        
            if not ada_curhat:
                st.write("Belum ada data curhat masuk.")
                
        elif menu_bk == "2. Jadwal Konseling":
            st.text(baca_file("jadwalBK.txt"))
            
        elif menu_bk == "3. Peer Support":
            st.text(baca_file("peer_support.txt"))
            
        elif menu_bk == "4. Hasil Refleksi":
            st.text(baca_file("jejak.txt"))
            
        elif menu_bk == "5. Early Warning (Risiko Tinggi)":
            st.write("### ⚠️ Siswa Butuh Penanganan Segera:")
            jejak_data = baca_file("jejak.txt").split("==================================")
            ada_warning = False
            for block in jejak_data:
                if "Kategori : Tinggi" in block:
                    st.error(block.strip())
                    st.write("Status: *Perlu Tindak Lanjut Segera oleh BK*")
                    st.markdown("---")
                    ada_warning = True
            if not ada_warning:
                st.success("Aman! Tidak ada siswa dengan indikasi tingkat burnout tinggi.")
                
        elif menu_bk == "6. Statistik Layanan":
            def hitung_entri(nama_file, keyword="Username"):
                if os.path.exists(nama_file):
                    with open(nama_file, "r", encoding="utf-8") as f:
                        return f.read().count(keyword)
                return 0

            c = hitung_entri("curhat.txt", "====================================")
            bk = hitung_entri("jadwalBK.txt", "==================================")
            p = hitung_entri("peer_support.txt", "==================================")
            t = hitung_entri("jejak.txt", "Kategori : Tinggi")
            
            st.metric("Total Curhat Anonim", c)
            st.metric("Total Pengajuan Konseling", bk)
            st.metric("Total Request Peer Support", p)
            st.metric("Jumlah Kasus Risiko Tinggi ⚠️", t)
            
        elif menu_bk == "7. Cetak Laporan":
            simpan_ke_file("laporanBK.txt", "Laporan LENTERA berhasil dibuat secara otomatis oleh sistem web.")
            st.success("Laporan berhasil dicetak dan disimpan ke dalam file `laporanBK.txt`!")