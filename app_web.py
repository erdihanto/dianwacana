import streamlit as st
import random

# 1. Konfigurasi Halaman Browser
st.set_page_config(page_title="Absensi Ceria & Coding", page_icon="🎨", layout="wide")

# 2. SUNTIKAN CSS DENGAN DUA BINGKAI TERPISAH YANG SIMETRIS
st.markdown("""
    <style>
    /* Background Utama Terang Modern Pop */
    .stApp {
        background: linear-gradient(135deg, #F3F4F6 0%, #EFF6FF 50%, #EEF2F6 100%);
        color: #1F2937;
    }
    
    /* Judul Utama */
    .judul-utama {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: #3B82F6;
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .nama-sekolah {
        font-family: 'Segoe UI', sans-serif;
        color: #4B5563;
        text-align: center;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 2px;
    }
    
    .sub-judul {
        font-family: 'Segoe UI', sans-serif;
        color: #10B981;
        text-align: center;
        font-size: 15px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .guru-mapel {
        font-family: 'Segoe UI', sans-serif;
        color: #6B7280;
        text-align: center;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 30px;
    }
    
    /* DUA FRAME UTAMA (KIRI DAN KANAN) */
    .frame-kiri-absen {
        background-color: #FFFFFF;
        border: 4px solid #3B82F6; /* Bingkai Biru Tebal */
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.1);
        min-height: 580px; /* Menjaga tinggi agar seimbang */
    }
    
    .frame-kanan-game {
        background-color: #FFFFFF;
        border: 4px solid #10B981; /* Bingkai Hijau Tebal */
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.1);
        min-height: 580px; /* Menjaga tinggi agar seimbang */
    }
    
    .frame-kiri-absen h3 {
        color: #3B82F6 !important;
        font-weight: 800;
        border-bottom: 2px dashed #DBEAFE;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    .frame-kanan-game h3 {
        color: #10B981 !important;
        font-weight: 800;
        border-bottom: 2px dashed #D1FAE5;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Tombol Rounded Modern */
    .stButton>button {
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 10px 24px !important;
        border: 2px solid #E5E7EB !important;
        background-color: #FFFFFF !important;
        color: #4B5563 !important;
        transition: all 0.2s ease;
        width: 100%; /* Tombol menyesuaikan kolom */
    }
    
    .stButton>button:hover {
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
        background-color: #F0F6FF !important;
        transform: translateY(-1px);
    }
    
    /* Tombol Aksi Utama (Hadir & Next Game) */
    .stButton>button[data-testid="baseButton-primary"] {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    
    .stButton>button[data-testid="baseButton-primary"]:hover {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE SISWA ---
if 'database_siswa' not in st.session_state:
    st.session_state.database_siswa = {
        "KB": {"Adit": 0, "Amari": 0, "Levin": 0, "Sienny": 0, "Jesselyn": 0, "Kenzou": 0, "Ralf": 0},
        "TK A": {
            "Kenzie": 0, "Brigitta": 0, "Essy": 0, "Felicia": 0, "Geva": 0, 
            "Greesa": 0, "Laras": 0, "Liam": 0, "Lova": 0, "Nawasena": 0, 
            "Mashal": 0, "Senja": 0, "Viola": 0, "Zio": 0
        },
        "TK B": {
            "Aileen": 0, "Agatha": 0, "Daniel": 0, "Sean": 0, "Elvano": 0, 
            "Betha": 0, "Hiro": 0, "Karen": 0, "Reiga": 0, "Danis": 0, "Yura": 0
        }
    }

if 'status_hadir' not in st.session_state:
    st.session_state.status_hadir = {kelas: {nama: False for nama in siswa} for kelas, siswa in st.session_state.database_siswa.items()}

if 'game_aktif' not in st.session_state:
    st.session_state.game_aktif = None

if 'umpan_balik_game' not in st.session_state:
    st.session_state.umpan_balik_game = None

# --- MESIN GENERATOR GAME OTOMATIS (RATUSAN VARIASI SOAL) ---
def get_game(kategori):
    tipe_game = random.choice(["manual", "auto_hitung", "auto_pola", "auto_coding"])
    
    # KATEGORI KELOMPOK BERMAIN (KB)
    if kategori == "KB":
        if tipe_game == "auto_hitung":
            emoji = random.choice(["🍎", "🐱", "🍌", "🚗", "🧸", "⭐", "🎈"])
            jumlah = random.randint(1, 4)
            visual = " ".join([emoji] * jumlah)
            opsi = sorted(list(set([str(jumlah), str(random.randint(1, 5)), str(random.randint(1, 5))])))
            if len(opsi) < 3: opsi = ["1", "2", "3"]
            return (visual, f"Ada berapa jumlah {emoji} di atas?", opsi, str(jumlah))
        else:
            return random.choice([
                ("💛", "Warna apakah balon hati di atas?", ["Merah ❤️", "Biru 💙", "Kuning 💛"], "Kuning 💛"),
                ("🐱", "Suara hewan apakah di atas?", ["Guk-Guk 🐕", "Meong 🐈", "Kwek-Kwek 🦆"], "Meong 🐈"),
                ("🥛", "Minuman sehat berwarna putih dari sapi adalah...", ["Susu 🥛", "Jus 🧃", "Kopi ☕"], "Susu 🥛"),
                ("🔴", "Bentuk apakah gambar di atas?", ["Kotak 🟦", "Lingkaran 🔴", "Segitiga 🔺"], "Lingkaran 🔴"),
                ("🦖", "Dinosaurus di atas berbadan besar atau kecil?", ["Kecil Sekali", "Besar Sekali", "Setinggi Semut"], "Besar Sekali"),
                ("🍦", "Es krim di atas rasanya...", ["Asin", "Pedas", "Manis & Dingin"], "Manis & Dingin")
            ])

    # KATEGORI TK A
    elif kategori == "TK A":
        if tipe_game == "auto_hitung":
            a = random.randint(1, 3)
            b = random.randint(1, 2)
            kunci = a + b
            opsi = sorted(list(set([str(kunci), str(kunci+1), str(kunci-1 if kunci-1 > 0 else kunci+2)])))
            return (f"{a} + {b} = ?", "Ayo hitung berapa hasil penjumlahan di atas!", opsi, str(kunci))
        elif tipe_game == "auto_pola":
            e1, e2 = random.sample(["🔴", "🔵", "🟡", "🟢", "⭐", "💎"], 2)
            visual = f"{e1} {e2} {e1} {e2} __"
            return (visual, "Gambar apa selanjutnya untuk mengisi garis kosong?", [e1, e2, "❓"], e1)
        else:
            return random.choice([
                ("🐘 ... 🐁", "Siapa yang ukuran badannya LEBIH BESAR?", ["Gajah 🐘", "Tikus 🐁", "Semut 🐜"], "Gajah 🐘"),
                ("A, B, _, D", "Huruf apa yang hilang di tengah?", ["C", "M", "Q"], "C"),
                ("🚗 🚗 🔑 🚗", "Benda ke berapa yang BUKAN kendaraan?", ["Ke-1", "Ke-2", "Ke-3"], "Ke-3"),
                ("🌧️", "Bagaimana cuaca pada gambar awan di atas?", ["Cerah ☀️", "Hujan 🌧️", "Petir ⛈️"], "Hujan 🌧️"),
                ("🐸 🟩 \n 🦩 ...", "Katak itu Hijau. Kalau burung Flamingo warna apa ya?", ["Biru 💙", "Merah Muda 🦩", "Kuning 💛"], "Merah Muda 🦩")
            ])

    # KATEGORI TK B
    else:
        if tipe_game == "auto_hitung":
            mode = random.choice(["+", "-"])
            if mode == "+":
                a, b = random.randint(2, 6), random.randint(1, 4)
                kunci = a + b
            else:
                a, b = random.randint(5, 10), random.randint(1, 4)
                kunci = a - b
            opsi = sorted(list(set([str(kunci), str(kunci+1), str(kunci-1 if kunci-1 >= 0 else kunci+2)])))
            return (f"{a} {mode} {b} = ?", "Berapakah hasil perhitungan matematika di atas?", opsi, str(kunci))
        elif tipe_game == "auto_coding":
            kotak_awal = random.randint(1, 3)
            langkah = random.randint(1, 2)
            kunci = kotak_awal + langkah
            visual = "🔼 " * langkah
            return (f"Mulai: Kotak {kotak_awal} \n\n Jalan: {visual}", 
                    f"Jika robot maju {langkah} langkah ke atas, di kotak nomor berapa robot sekarang?", 
                    [f"Kotak {kunci}", f"Kotak {kunci+1}", f"Kotak {kunci-1 if kunci-1 > 0 else kunci+2}"], f"Kotak {kunci}")
        elif tipe_game == "auto_pola":
            start = random.randint(5, 10)
            visual = f"{start}, {start-1}, {start-2}, __"
            kunci = start - 3
            return (visual, "Ayo hitung mundur! Angka berapakah selanjutnya?", [str(kunci), str(kunci-1), str(kunci+1)], str(kunci))
        else:
            return random.choice([
                ("R _ M A H", "Huruf vokal apa yang hilang untuk melengkapi kata?", ["A", "I", "U"], "U"),
                ("✈️", "Kendaraan di atas tempat jalannya di mana ya?", ["Darat 🛣️", "Laut 🌊", "Udara ☁️"], "Udara ☁️"),
                ("🔥 (PANAS)", "Apa LAWAN KATA dari benda PANAS?", ["DINGIN ❄️", "MALAM 🌙", "KOTOR 🪰"], "DINGIN ❄️"),
                ("🐝 👍 🥛", "Madu dihasilkan oleh lebah. Kalau susu dihasilkan oleh...", ["Ayam 🐓", "Sapi 🐄", "Bebek 🦆"], "Sapi 🐄"),
                ("🟥 🟨 🟩 🟥 🟨 _", "Ayo lanjutkan pola warna lampu lalu lintas ini!", ["Merah 🟥", "Kuning 🟨", "Hijau 🟩"], "Hijau 🟩")
            ])

# --- HEADER APLIKASI ---
st.markdown('<div class="judul-utama">🏫 ABSENSI CERIA & CODING SMART</div>', unsafe_allow_html=True)
st.markdown('<div class="nama-sekolah">KB-TK Kristen Dian Wacana</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-judul">🎈 KASIH • INTEGRITAS • PEDULI • TAAT 🎈</div>', unsafe_allow_html=True)
st.markdown('<div class="guru-mapel">👩‍🏫 Guru Mapel: Ms. Siska</div>', unsafe_allow_html=True)

# --- LAYOUT DUA KOLOM DENGAN DUA FRAME TERPISAH TEGAS ---
kolom_kiri, kolom_kanan = st.columns([1, 1], gap="large")

# ==================== FRAME 1: PANEL ABSENSI (KIRI - BIRU) ====================
with kolom_kiri:
    st.markdown('<div class="frame-kiri-absen">', unsafe_allow_html=True)
    st.markdown("### 📋 FRAME ABSENSI SISWA")
    
    # Pilihan Kelas
    kelas = st.selectbox("1. Pilih Kelas:", ["KB", "TK A", "TK B"])
    info_usia = {"KB": "Usia 3-4 Tahun (Kelompok Bermain)", "TK A": "Usia 4-5 Tahun (TK Kecil)", "TK B": "Usia 5-6 Tahun (TK Besar)"}
    st.info(f"👶 {info_usia[kelas]}")
    
    # Pilihan Nama
    daftar_nama = sorted(list(st.session_state.database_siswa[kelas].keys()))
    nama_terpilih = st.selectbox("2. Siapa namamu?", ["-- Pilih Nama Kamu Di Sini --"] + daftar_nama)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if nama_terpilih != "-- Pilih Nama Kamu Di Sini --":
        hadir = st.session_state.status_hadir[kelas][nama_terpilih]
        bintang = st.session_state.database_siswa[kelas][nama_terpilih]
        
        if hadir:
            st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 0;'>🥰</h1>", unsafe_allow_html=True)
            st.success(f"Selamat Datang {nama_terpilih}! Kamu sudah absen hari ini. Total Bintangmu: {bintang} ⭐")
        else:
            st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 0;'>😊</h1>", unsafe_allow_html=True)
            st.warning(f"Halo {nama_terpilih}, kamu belum klik tombol kehadiran.")
            if st.button("✋ KLIK DI SINI UNTUK ABSEN HADIR 🎈", type="primary"):
                st.session_state.status_hadir[kelas][nama_terpilih] = True
                st.session_state.game_aktif = get_game(kelas)
                st.session_state.umpan_balik_game = None
                st.rerun()
    else:
        st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 0;'>👋</h1>", unsafe_allow_html=True)
        st.write("Silakan pilih namamu terlebih dahulu untuk melakukan absensi.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== FRAME 2: PANEL GAME (KANAN - HIJAU) ====================
with kolom_kanan:
    st.markdown('<div class="frame-kanan-game">', unsafe_allow_html=True)
    st.markdown(f"### 🎮 FRAME TANTANGAN GAME ({kelas})")
    
    if nama_terpilih == "-- Pilih Nama Kamu Di Sini --" or not st.session_state.status_hadir[kelas][nama_terpilih]:
        st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 20px 0;'>🔒</h1>", unsafe_allow_html=True)
        st.info("Kunci permainan masih terkunci. Silakan lakukan **Absen Hadir** di Frame Kiri terlebih dahulu untuk membukanya! 😊")
    else:
        # Kondisi Jawaban Benar
        if st.session_state.umpan_balik_game == "benar":
            st.balloons()
            st.markdown("<h2 style='text-align: center; color: #10B981;'>🏆 JAWABAN BENAR! 🎉</h2>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: #3B82F6;'>Bintangmu bertambah +1 ⭐!</h4>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 MAIN LAGI (GAME SELANJUTNYA) 🎮", type="primary"):
                st.session_state.game_aktif = get_game(kelas)
                st.session_state.umpan_balik_game = None
                st.rerun()
        else:
            # Baris kontrol game ganti soal
            if st.session_state.game_aktif:
                if st.button("🎲 GANTI SOAL BARU (ACAK)", type="secondary"):
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
            
            if st.session_state.umpan_balik_game == "salah":
                st.markdown("<h5 style='text-align: center; color: #EF4444;'>❌ Sedikit lagi tepat! Ayo coba tebak sekali lagi! 💪</h5>", unsafe_allow_html=True)

            if st.session_state.game_aktif:
                visual, pertanyaan, opsi, jawaban_benar = st.session_state.game_aktif
                
                # Box tampilan soal utama di dalam frame game
                st.markdown(f"<h1 style='text-align: center; font-size: 65px; background-color: #F8FAFC; border: 2px solid #E2E8F0; border-radius: 16px; padding: 15px; margin-bottom: 15px;'>{visual}</h1>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: #1F2937; font-size: 16px; font-weight: 500;'>{pertanyaan}</p>", unsafe_allow_html=True)
                
                # Tombol pilihan jawaban
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
                    
    st.markdown('</div>', unsafe_allow_html=True)
