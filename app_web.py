import streamlit as st
import random

# 1. Konfigurasi Halaman Browser
st.set_page_config(page_title="Absensi Ceria & Coding", page_icon="🎨", layout="wide")

# 2. SUNTIKAN CSS DENGAN FRAME (BINGKAI) MODERN POP
st.markdown("""
    <style>
    /* Background Terang Modern Pop */
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
    
    /* KARTU DENGAN AKSEN FRAME (BINGKAI RAPI) */
    .kartu-absen {
        background-color: #FFFFFF;
        border: 3px solid #E5E7EB; /* Bingkai luar */
        border-top: 8px solid #3B82F6; /* Aksen warna biru di atas frame */
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .kartu-game {
        background-color: #FFFFFF;
        border: 3px solid #DBEAFE; /* Bingkai luar */
        border-top: 8px solid #10B981; /* Aksen warna hijau di atas frame */
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.05);
        margin-bottom: 20px;
    }
    
    .kartu-absen h3 {
        color: #1F2937 !important;
        font-weight: 700;
    }
    
    .kartu-game h3 {
        color: #10B981 !important;
        font-weight: 700;
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
    }
    
    .stButton>button:hover {
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
        background-color: #F0F6FF !important;
        transform: translateY(-1px);
    }
    
    /* Tombol Aksi Utama */
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
    
    # 🌟 KATEGORI KELOMPOK BERMAIN (KB) - Fokus Visual & Warna
    if kategori == "KB":
        if tipe_game == "auto_hitung":
            # Menghasilkan hitungan benda acak 1-5
            emoji = random.choice(["🍎", "🐱", "🍌", "🚗", "🧸", "⭐", "🎈"])
            jumlah = random.randint(1, 4)
            visual = " ".join([emoji] * jumlah)
            opsi = sorted(list(set([str(jumlah), str(random.randint(1, 5)), str(random.randint(1, 5))])))
            if len(opsi) < 3: opsi = ["1", "2", "3"] # Fallback jika angka duplikat
            return (visual, f"Ada berapa jumlah {emoji} di atas?", opsi, str(jumlah))
        else:
            # Bank Soal Manual Seru untuk KB
            return random.choice([
                ("💛", "Warna apakah balon hati di atas?", ["Merah ❤️", "Biru 💙", "Kuning 💛"], "Kuning 💛"),
                ("🐱", "Suara hewan apakah di atas?", ["Guk-Guk 🐕", "Meong 🐈", "Kwek-Kwek 🦆"], "Meong 🐈"),
                ("🥛", "Minuman sehat berwarna putih dari sapi adalah...", ["Susu 🥛", "Jus 🧃", "Kopi ☕"], "Susu 🥛"),
                ("🔴", "Bentuk apakah gambar di atas?", ["Kotak 🟦", "Lingkaran 🔴", "Segitiga 🔺"], "Lingkaran 🔴"),
                ("🦖", "Dinosaurus di atas berbadan besar atau kecil?", ["Kecil Sekali", "Besar Sekali", "Setinggi Semut"], "Besar Sekali"),
                ("🍦", "Es krim di atas rasanya...", ["Asin", "Pedas", "Manis & Dingin"], "Manis & Dingin")
            ])

    # 🌟 KATEGORI TK A - Fokus Hitungan Menengah & Pola Visual
    elif kategori == "TK A":
        if tipe_game == "auto_hitung":
            # Hitungan penjumlahan sederhana di bawah 5
            a = random.randint(1, 3)
            b = random.randint(1, 2)
            kunci = a + b
            opsi = sorted(list(set([str(kunci), str(kunci+1), str(kunci-1 if kunci-1 > 0 else kunci+2)])))
            return (f"{a} + {b} = ?", "Ayo hitung berapa hasil penjumlahan di atas!", opsi, str(kunci))
            
        elif tipe_game == "auto_pola":
            # Pola ABAB acak
            e1, e2 = random.sample(["🔴", "🔵", "🟡", "🟢", "⭐", "💎"], 2)
            visual = f"{e1} {e2} {e1} {e2} __"
            return (visual, "Ayo tebak! Gambar apa selanjutnya untuk mengisi garis kosong?", [e1, e2, "❓"], e1)
            
        else:
            return random.choice([
                ("🐘 ... 🐁", "Siapa yang ukuran badannya LEBIH BESAR?", ["Gajah 🐘", "Tikus 🐁", "Semut 🐜"], "Gajah 🐘"),
                ("A, B, _, D", "Huruf apa yang hilang di tengah?", ["C", "M", "Q"], "C"),
                ("🚗 🚗 🔑 🚗", "Benda ke berapa yang BUKAN kendaraan?", ["Ke-1", "Ke-2", "Ke-3"], "Ke-3"),
                ("🌧️", "Bagaimana cuaca pada gambar awan di atas?", ["Cerah ☀️", "Hujan 🌧️", "Petir ⛈️"], "Hujan 🌧️"),
                ("🐸 🟩 \n 🦩 ...", "Katak itu Hijau. Kalau burung Flamingo warna apa ya?", ["Biru 💙", "Merah Muda 🦩", "Kuning 💛"], "Merah Muda 🦩"),
                ("🐢", "Jalan hewan di atas jalannya lambat atau cepat ya?", ["Lambat", "Cepat", "Terbang"], "Lambat")
            ])

    # 🌟 KATEGORI TK B - Fokus Logika Coding, Matematika & Hitung Mundur
    else:
        if tipe_game == "auto_hitung":
            # Penjumlahan / Pengurangan acak angka 1-10
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
            # Logika Langkah Arah Grid Coding Robot
            kotak_awal = random.randint(1, 3)
            langkah = random.randint(1, 2)
            kunci = kotak_awal + langkah
            visual = "🔼 " * langkah
            return (f"Posisi Awal: Kotak {kotak_awal} \n\n Instruksi Robot: {visual}", 
                    f"Jika robot maju {langkah} langkah ke atas, di kotak nomor berapa posisi robot sekarang?", 
                    [f"Kotak {kunci}", f"Kotak {kunci+1}", f"Kotak {kunci-1 if kunci-1 > 0 else kunci+2}"], f"Kotak {kunci}")
        
        elif tipe_game == "auto_pola":
            # Urutan angka melompat (Hitung maju/mundur)
            start = random.randint(5, 10)
            visual = f"{start}, {start-1}, {start-2}, __"
            kunci = start - 3
            return (visual, "Ayo hitung mundur! Angka berapakah selanjutnya?", [str(kunci), str(kunci-1), str(kunci+1)], str(kunci))
            
            # Soal Manual Logika
        else:
            return random.choice([
                ("R _ M A H", "Huruf vokal apa yang hilang untuk melengkapi kata?", ["A", "I", "U"], "U"),
                ("✈️", "Kendaraan di atas tempat jalannya di mana ya?", ["Darat 🛣️", "Laut 🌊", "Udara ☁️"], "Udara ☁️"),
                ("🔥 (PANAS)", "Apa LAWAN KATA dari benda PANAS?", ["DINGIN ❄️", "MALAM 🌙", "KOTOR 🪰"], "DINGIN ❄️"),
                ("☀️", "Matahari terbit di sebelah mana dan pada waktu kapan?", ["Timur - Pagi 🌅", "Barat - Sore 🌇", "Utara - Malam 🌌"], "Timur - Pagi 🌅"),
                ("🐝 👍 🥛", "Madu dihasilkan oleh lebah. Kalau susu dihasilkan oleh...", ["Ayam 🐓", "Sapi 🐄", "Bebek 🦆"], "Sapi 🐄"),
                ("🟥 🟨 🟩 🟥 🟨 _", "Ayo lanjutkan pola warna lampu lalu lintas ini!", ["Merah 🟥", "Kuning 🟨", "Hijau 🟩"], "Hijau 🟩")
            ])

# --- HEADER APLIKASI ---
st.markdown('<div class="judul-utama">🏫 ABSENSI CERIA & CODING SMART</div>', unsafe_allow_html=True)
st.markdown('<div class="nama-sekolah">KB-TK Kristen Dian Wacana</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-judul">🎈 KASIH • INTEGRITAS • PEDULI • TAAT 🎈</div>', unsafe_allow_html=True)
st.markdown('<div class="guru-mapel">👩‍🏫 Guru Mapel: Ms. Siska</div>', unsafe_allow_html=True)

# --- LAYOUT DUA KOLOM UTAMA ---
kolom_kiri, kolom_kanan = st.columns([1, 1.1], gap="large")

# ==================== PANEL KIRI: ABSENSI BINGKAI RAPI ====================
with kolom_kiri:
    st.markdown('<div class="kartu-absen">', unsafe_allow_html=True)
    st.markdown("### ✨ 1. Pilih Kelas & Namamu")
    
    # Pilih Kelas
    kelas = st.selectbox("Pilih Kelas:", ["KB", "TK A", "TK B"])
    info_usia = {"KB": "Usia 3-4 Tahun (Kelompok Bermain)", "TK A": "Usia 4-5 Tahun (TK Kecil)", "TK B": "Usia 5-6 Tahun (TK Besar)"}
    st.info(f"👶 {info_usia[kelas]}")
    
    # Pilih Nama
    daftar_nama = sorted(list(st.session_state.database_siswa[kelas].keys()))
    nama_terpilih = st.selectbox("Siapa namamu?", ["-- Klik Pilihan Nama --"] + daftar_nama)
    
    if nama_terpilih != "-- Klik Pilihan Nama --":
        hadir = st.session_state.status_hadir[kelas][nama_terpilih]
        bintang = st.session_state.database_siswa[kelas][nama_terpilih]
        
        if hadir:
            st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 10px 0;'>🥰</h1>", unsafe_allow_html=True)
            st.success(f"Selamat Datang {nama_terpilih}! Kamu sudah absen. Bintangmu: {bintang} ⭐")
        else:
            st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 10px 0;'>😊</h1>", unsafe_allow_html=True)
            st.warning(f"Halo {nama_terpilih}, kamu belum absen hari ini.")
            if st.button("✋ SAYA HADIR! 🎈", type="primary"):
                st.session_state.status_hadir[kelas][nama_terpilih] = True
                st.session_state.game_aktif = get_game(kelas)
                st.session_state.umpan_balik_game = None
                st.rerun()
    else:
        st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 10px 0;'>👋</h1>", unsafe_allow_html=True)
        st.write("Silakan pilih namamu pada kolom di atas ya!")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PANEL KANAN: ZONA BERMAIN KAYA VARIASI ====================
with kolom_kanan:
    st.markdown('<div class="kartu-game">', unsafe_allow_html=True)
    st.markdown(f"### 🎮 ZONA TANTANGAN CERDAS ({kelas})")
    
    if nama_terpilih == "-- Klik Pilihan Nama --" or not st.session_state.status_hadir[kelas][nama_terpilih]:
        st.info("Kamu harus **Absen Hadir** ✋ dulu di sebelah kiri untuk membuka permainan seru ini! 😊")
    else:
        # Jika jawaban benar
        if st.session_state.umpan_balik_game == "benar":
            st.balloons()
            st.markdown("<h2 style='text-align: center; color: #10B981;'>🏆 HEBAT! JAWABANMU BENAR! 🎉</h2>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: #3B82F6;'>Kamu dapat 1 ⭐ tambahan! Hore!</h4>", unsafe_allow_html=True)
            
            if st.button("🚀 TANTANGAN SELANJUTNYA! 🎮", type="primary"):
                st.session_state.game_aktif = get_game(kelas)
                st.session_state.umpan_balik_game = None
                st.rerun()
        else:
            if st.session_state.game_aktif:
                if st.button("🎲 GANTI PERMAINAN BARU", type="secondary"):
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
            
            if st.session_state.umpan_balik_game == "salah":
                st.markdown("<h4 style='text-align: center; color: #EF4444;'>💪 Hampir tepat! Ayo coba lagi, kamu pasti bisa!</h4>", unsafe_allow_html=True)

            if st.session_state.game_aktif:
                visual, pertanyaan, opsi, jawaban_benar = st.session_state.game_aktif
                
                # Kotak visual soal di dalam frame game
                st.markdown(f"<h1 style='text-align: center; font-size: 75px; background-color: #F8FAFC; border: 2px solid #E2E8F0; border-radius: 16px; padding: 20px; margin-bottom: 20px;'>{visual}</h1>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='text-align: center; color: #1F2937; font-size: 18px; margin-bottom: 25px;'>{pertanyaan}</h5>", unsafe_allow_html=True)
                
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
