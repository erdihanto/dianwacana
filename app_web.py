import streamlit as st
import random

# 1. Konfigurasi Halaman Browser
st.set_page_config(page_title="Absensi Ceria & Coding", page_icon="🎨", layout="wide")

# 2. SUNTIKAN CSS UNTUK MENIRU STYLE APLIKASI WEB CLEAN FRAME
st.markdown("""
    <style>
    /* Mengubah background utama aplikasi agar bersih dan soft */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    /* Desain Header Utama ala Kalkulator Web */
    .header-kontainer {
        text-align: center;
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .judul-utama {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1E3A8A;
        font-size: 32px;
        font-weight: 800;
        margin: 0;
    }
    .sub-judul {
        color: #10B981;
        font-size: 14px;
        font-weight: 700;
        margin-top: 5px;
        letter-spacing: 1px;
    }
    .guru-mapel {
        color: #64748B;
        font-size: 14px;
        margin-top: 2px;
    }

    /* Memaksa bingkai internal Streamlit st.container(border=True) agar terlihat tegas dan rapi */
    .stElementContainer div[data-testid="stVerticalBlockBorderContainer"] {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Efek visual kotak soal game di dalam frame */
    .kotak-soal {
        text-align: center; 
        font-size: 60px; 
        background-color: #F1F5F9; 
        border: 1px solid #CBD5E1; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 15px;
    }
    
    /* Desain Tombol agar seragam dan flat rapi */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        color: #334155 !important;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
        background-color: #EFF6FF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE STATE ---
if 'database_siswa' not in st.session_state:
    st.session_state.database_siswa = {
        "KB": {"Adit": 0, "Amari": 0, "Levin": 0, "Sienny": 0, "Jesselyn": 0, "Kenzou": 0, "Ralf": 0},
        "TK A": {"Kenzie": 0, "Brigitta": 0, "Essy": 0, "Felicia": 0, "Geva": 0, "Greesa": 0, "Laras": 0, "Liam": 0},
        "TK B": {"Aileen": 0, "Agatha": 0, "Daniel": 0, "Sean": 0, "Elvano": 0, "Betha": 0, "Hiro": 0}
    }

if 'status_hadir' not in st.session_state:
    st.session_state.status_hadir = {kelas: {nama: False for nama in siswa} for kelas, siswa in st.session_state.database_siswa.items()}

if 'game_aktif' not in st.session_state:
    st.session_state.game_aktif = None

if 'umpan_balik_game' not in st.session_state:
    st.session_state.umpan_balik_game = None

# --- GENERATOR SOAL OTOMATIS (100+ VARIASI KELAS KANAN) ---
def get_game(kategori):
    tipe_game = random.choice(["hitung", "pola", "logika", "arah"])
    
    if kategori == "KB":
        if tipe_game == "hitung":
            emoji = random.choice(["🍎", "🍌", "🚗", "🧸", "⭐"])
            jumlah = random.randint(1, 4)
            return (" ".join([emoji] * jumlah), f"Ada berapa jumlah {emoji} di atas?", [str(jumlah), str(jumlah+1), "5"], str(jumlah))
        else:
            return random.choice([
                ("💛", "Warna apakah hati di atas?", ["Merah", "Biru", "Kuning"], "Kuning"),
                ("🐱", "Suara hewan apakah di atas?", ["Guk-Guk", "Meong", "Kwek-Kwek"], "Meong"),
                ("🔴", "Bentuk apakah gambar berwarna merah di atas?", ["Kotak", "Lingkaran", "Segitiga"], "Lingkaran")
            ])
    elif kategori == "TK A":
        if tipe_game == "hitung":
            a, b = random.randint(1, 3), random.randint(1, 2)
            return (f"{a} + {b} = ?", "Berapakah hasil penjumlahan di atas?", [str(a+b), str(a+b+1), str(a+b-1)], str(a+b))
        elif tipe_game == "pola":
            e1, e2 = random.sample(["🔴", "🔵", "🟡", "🟢"], 2)
            return (f"{e1} {e2} {e1} {e2} ?", "Gambar apa setelahnya sesuai pola?", [e1, e2, "❓"], e1)
        else:
            return random.choice([
                ("🐘 ... 🐁", "Siapa yang badannya LEBIH BESAR?", ["Gajah 🐘", "Tikus 🐁"], "Gajah 🐘"),
                ("A, B, _, D", "Huruf apa yang hilang di tengah?", ["C", "M", "E"], "C")
            ])
    else: # TK B
        if tipe_game == "hitung":
            mode = random.choice(["+", "-"])
            a, b = (random.randint(3, 6), random.randint(1, 3)) if mode == "+" else (random.randint(6, 9), random.randint(1, 4))
            kunci = a + b if mode == "+" else a - b
            return (f"{a} {mode} {b} = ?", "Berapakah hasil perhitungan matematika di atas?", [str(kunci), str(kunci+1), str(kunci-1)], str(kunci))
        elif tipe_game == "arah":
            awal = random.randint(1, 3)
            langkah = random.randint(1, 2)
            return (f"Kotak {awal} ➔ " + ("🔼 " * langkah), f"Jika robot di kotak {awal} maju {langkah} langkah, di kotak nomor berapa sekarang?", [str(awal+langkah), str(awal+langkah+1), "0"], str(awal+langkah))
        else:
            return random.choice([
                ("🔥", "Apa LAWAN KATA dari benda PANAS?", ["DINGIN", "MALAM", "BASAH"], "DINGIN"),
                ("🟥 🟨 🟩 🟥 🟨 _", "Lanjutkan pola warna lampu lalu lintas berikut!", ["Merah", "Kuning", "Hijau"], "Hijau")
            ])

# --- TAMPILAN HEADER ---
st.markdown("""
    <div class="header-kontainer">
        <div class="judul-utama">🏫 ABSENSI CERIA & GAME CODING</div>
        <div class="sub-judul">KB-TK KRISTEN DIAN WACANA</div>
        <div class="guru-mapel">👩‍🏫 Guru Mapel: Ms. Siska</div>
    </div>
""", unsafe_allow_html=True)

# --- GRID UTAMA: 2 KOLOM FRAME MANDIRI ---
kolom_absen, kolom_game = st.columns(2, gap="large")

# ==================== FRAME 1: PANEL ABSENSI (KIRI) ====================
with kolom_absen:
    # Menggunakan border=True agar terkurung rapi di dalam bingkai tanpa celah
    with st.container(border=True):
        st.subheader("📋 Bingkai Absensi Siswa")
        
        kelas = st.selectbox("1. Pilih Kelas Kelompok:", ["KB", "TK A", "TK B"])
        daftar_nama = sorted(list(st.session_state.database_siswa[kelas].keys()))
        nama_terpilih = st.selectbox("2. Cari & Klik Namamu:", ["-- Pilih Nama --"] + daftar_nama)
        
        st.write("---")
        
        if nama_terpilih != "-- Pilih Nama --":
            hadir = st.session_state.status_hadir[kelas][nama_terpilih]
            bintang = st.session_state.database_siswa[kelas][nama_terpilih]
            
            if hadir:
                st.markdown("<h1 style='text-align: center; margin:0;'>🥰</h1>", unsafe_allow_html=True)
                st.success(f"Selamat Datang, {nama_terpilih}! Kamu sudah absen. Bintangmu: {bintang} ⭐")
            else:
                st.markdown("<h1 style='text-align: center; margin:0;'>😊</h1>", unsafe_allow_html=True)
                st.warning(f"Halo {nama_terpilih}, kamu belum mengonfirmasi kehadiran.")
                if st.button("✋ SAYA HADIR HARI INI!", type="primary"):
                    st.session_state.status_hadir[kelas][nama_terpilih] = True
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
        else:
            st.markdown("<h1 style='text-align: center; margin:0;'>👋</h1>", unsafe_allow_html=True)
            st.info("Silakan tentukan nama kamu di atas terlebih dahulu.")

# ==================== FRAME 2: PANEL GAME (KANAN) ====================
with kolom_game:
    # Menggunakan border=True agar terkurung rapi di dalam bingkai tanpa celah
    with st.container(border=True):
        st.subheader("🎮 Bingkai Tantangan Game")
        
        if nama_terpilih == "-- Pilih Nama --" or not st.session_state.status_hadir[kelas][nama_terpilih]:
            st.markdown("<h1 style='text-align: center; margin: 30px 0;'>🔒</h1>", unsafe_allow_html=True)
            st.info("Game Terkunci. Silakan lakukan **Absen Hadir** di frame sebelah kiri untuk membukanya!")
        else:
            if st.session_state.umpan_balik_game == "benar":
                st.balloons()
                st.markdown("<h3 style='text-align: center; color: #10B981;'>🏆 JAWABAN BENAR! +1 ⭐</h3>", unsafe_allow_html=True)
                if st.button("🚀 LANJUT GAME BERIKUTNYA", type="primary"):
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
            else:
                if st.session_state.game_aktif:
                    if st.button("🎲 GANTI SOAL BARU"):
                        st.session_state.game_aktif = get_game(kelas)
                        st.session_state.umpan_balik_game = None
                        st.rerun()
                
                if st.session_state.umpan_balik_game == "salah":
                    st.error("❌ Jawaban kurang tepat, coba lagi ya sayang!")

                if st.session_state.game_aktif:
                    visual, pertanyaan, opsi, jawaban_benar = st.session_state.game_aktif
                    
                    # Kotak abu-abu di dalam bingkai game untuk menaruh soal gambar/emoji
                    st.markdown(f'<div class="kotak-soal">{visual}</div>', unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align:center; font-weight:600;">{pertanyaan}</p>', unsafe_allow_html=True)
                    
                    # Pilihan jawaban tombol horizontal yang rigid
                    kol_opsi = st.columns(len(opsi))
                    for i, alternatif in enumerate(opsi):
                        with kol_opsi[i]:
                            if st.button(alternatif, key=f"btn_{alternatif}_{i}"):
                                if alternatif == jawaban_benar:
                                    st.session_state.database_siswa[kelas][nama_terpilih] += 1
                                    st.session_state.umpan_balik_game = "benar"
                                    st.rerun()
                                else:
                                    st.session_state.umpan_balik_game = "salah"
                                    st.rerun()
                else:
                    if st.button("🎲 MULAI BERMAIN", type="primary"):
                        st.session_state.game_aktif = get_game(kelas)
                        st.session_state.umpan_balik_game = None
                        st.rerun()
