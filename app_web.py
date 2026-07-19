import streamlit as st
import random

# 1. Konfigurasi Halaman Browser
st.set_page_config(page_title="Absensi Ceria & Coding", page_icon="🎨", layout="wide")

# 2. SUNTIKAN CSS UNTUK TAMPILAN MODERN POP (BERSIH, CERIA, & RAMAH ANAK)
st.markdown("""
    <style>
    /* Background Terang Modern Pop */
    .stApp {
        background: linear-gradient(135deg, #F3F4F6 0%, #EFF6FF 50%, #EEF2F6 100%);
        color: #1F2937;
    }
    
    /* Judul Utama Estetik & Bersih */
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
    
    /* Kartu Desain Grid Minimalis & Modern */
    .kartu-absen {
        background-color: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }
    
    .kartu-game {
        background-color: #FFFFFF;
        border: 2px solid #DBEAFE;
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
        color: #2563EB !important;
        font-weight: 700;
    }
    
    /* Tombol Rounded Modern ala Duolingo */
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
    
    /* Tombol Aksi Utama (Warna Biru Cerah) */
    .stButton>button[data-testid="baseButton-primary"] {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
    }
    
    .stButton>button[data-testid="baseButton-primary"]:hover {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 10px rgba(59, 130, 246, 0.3);
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

# --- BANK DATA GAME DENGAN VARIASI LEBIH BANYAK ---
def get_game(kategori):
    if kategori == "KB":
        return random.choice([
            ("🍎 🍎 🍎", "Ada berapa jumlah buah apel merah di atas?", ["1", "2", "3"], "3"),
            ("🐱", "Suara hewan apakah di atas?", ["Guk-Guk 🐕", "Meong 🐈", "Kwek-Kwek 🦆"], "Meong 🐈"),
            ("💛", "Warna apakah balon hati di atas?", ["Merah ❤️", "Biru 💙", "Kuning 💛"], "Kuning 💛"),
            ("🍌", "Buah apa yang paling disukai monyet?", ["Pisang 🍌", "Anggur 🍇", "Semangka 🍉"], "Pisang 🍌"),
            ("🥛", "Minuman sehat berwarna putih yang dihasilkan sapi adalah...", ["Susu 🥛", "Jus 🧃", "Kopi ☕"], "Susu 🥛"),
            ("🔴", "Bentuk apakah gambar di atas?", ["Kotak 🟦", "Lingkaran 🔴", "Segitiga 🔺"], "Lingkaran 🔴"),
            ("🚗", "Kendaraan di atas memiliki roda sebanyak...", ["2 Roda", "3 Roda", "4 Roda"], "4 Roda")
        ])
    elif kategori == "TK A":
        return random.choice([
            ("🐘 ... 🐁", "Siapa yang ukuran badannya LEBIH BESAR?", ["Gajah 🐘", "Tikus 🐁", "Semut 🐜"], "Gajah 🐘"),
            ("A, B, _, D", "Huruf apa yang hilang di tengah?", ["C", "M", "Q"], "C"),
            ("🚗 🚗 🚕 🚗", "Mobil ke berapa yang warnanya BERBEDA sendiri?", ["Ke-1", "Ke-2", "Ke-3"], "Ke-3"),
            ("🌧️", "Bagaimana cuaca pada gambar awan di atas?", ["Cerah ☀️", "Hujan 🌧️", "Petir ⛈️"], "Hujan 🌧️"),
            ("🐸 🟩 \n 🦩 ...", "Katak berwarna hijau. Burung Flamingo berwarna apa ya?", ["Biru 💙", "Merah Muda 🦩", "Kuning 💛"], "Merah Muda 🦩"),
            ("🔴 🔵 🔴 🔵 _", "Ayo tebak pola! Gambar apa selanjutnya setelah lingkaran biru?", ["Lingkaran Merah 🔴", "Lingkaran Biru 🔵", "Bintang ⭐"], "Lingkaran Merah 🔴"),
            ("🧸 🧸 🧸 🧸 🧸", "Ada 5 boneka beruang. Jika diambil 2, sisanya tinggal berapa?", ["2", "3", "4"], "3"),
            ("🐢", "Jalan hewan di atas jalannya lambat atau cepat ya?", ["Lambat sekali", "Cepat sekali", "Terbang"], "Lambat sekali")
        ])
    else: # TK B (Persiapan Coding & Logika)
        return random.choice([
            ("4 + 3 = ?", "Berapakah hasil penjumlahan di atas?", ["6", "7", "8"], "7"),
            ("R _ M A H", "Huruf vokal apa yang hilang untuk melengkapi kata?", ["A", "I", "U"], "U"),
            ("✈️", "Kendaraan di atas tempat jalannya di mana ya?", ["Darat 🛣️", "Laut 🌊", "Udara ☁️"], "Udara ☁️"),
            ("🔥 (PANAS)", "Apa LAWAN KATA dari benda PANAS?", ["DINGIN ❄️", "MALAM 🌙", "KOTOR 🪰"], "DINGIN ❄️"),
            ("🔼 (Maju 1 Langkah)", "Jika robot di kotak 1 maju 2 langkah (🔼 🔼), di kotak berapa dia sekarang?", ["Kotak 2", "Kotak 3", "Kotak 4"], "Kotak 3"),
            ("☀️", "Matahari terbit di sebelah mana dan pada waktu kapan?", ["Timur - Pagi 🌅", "Barat - Sore 🌇", "Utara - Malam 🌌"], "Timur - Pagi 🌅"),
            ("10, 8, 6, _", "Ayo hitung mundur! Angka berapakah selanjutnya?", ["5", "4", "3"], "4"),
            ("🐝 👍 🥛", "Madu dihasilkan oleh lebah. Kalau susu dihasilkan oleh...", ["Ayam 🐓", "Sapi 🐄", "Bebek 🦆"], "Sapi 🐄"),
            ("🟥 🟨 🟩 🟥 🟨 _", "Ayo lanjutkan pola warna lampu lalu lintas ini!", ["Merah 🟥", "Kuning 🟨", "Hijau 🟩"], "Hijau 🟩")
        ])

# --- HEADER APLIKASI ---
st.markdown('<div class="judul-utama">🏫 ABSENSI CERIA & PLAY ZONE</div>', unsafe_allow_html=True)
st.markdown('<div class="nama-sekolah">KB-TK Kristen Dian Wacana</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-judul">🎈 KASIH • INTEGRITAS • PEDULI • TAAT 🎈</div>', unsafe_allow_html=True)
st.markdown('<div class="guru-mapel">👩‍🏫 Guru Mapel: Ms. Siska</div>', unsafe_allow_html=True)

# --- LAYOUT DUA KOLOM UTAMA ---
kolom_kiri, kolom_kanan = st.columns([1, 1.1], gap="large")

# ==================== PANEL KIRI: ABSENSI MODERN ====================
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

# ==================== PANEL KANAN: ZONA BERMAIN SERU ====================
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
            
            if st.button("🚀 MAIN LAGI! 🎮", type="primary"):
                st.session_state.game_aktif = get_game(kelas)
                st.session_state.umpan_balik_game = None
                st.rerun()
        else:
            if st.session_state.game_aktif:
                if st.button("🎲 GANTI PERMAINAN", type="secondary"):
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
            
            if st.session_state.umpan_balik_game == "salah":
                st.markdown("<h4 style='text-align: center; color: #EF4444;'>💪 Hampir tepat! Ayo coba lagi, kamu pasti bisa!</h4>", unsafe_allow_html=True)

            if st.session_state.game_aktif:
                visual, pertanyaan, opsi, jawaban_benar = st.session_state.game_aktif
                
                # Kotak pertanyaan yang bersih dan empuk di mata
                st.markdown(f"<h1 style='text-align: center; font-size: 85px; background-color: #F8FAFC; border: 2px solid #E2E8F0; border-radius: 16px; padding: 20px; margin-bottom: 20px;'>{visual}</h1>", unsafe_allow_html=True)
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
