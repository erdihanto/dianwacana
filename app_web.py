import streamlit as st
import random

# 1. Konfigurasi Halaman Browser
st.set_page_config(page_title="Absensi Intra Coding", page_icon="🤖", layout="wide")

# 2. SUNTIKAN CSS UNTUK TAMPILAN FUTURISTIK & MODERN (CYBER-TECH THEME)
st.markdown("""
    <style>
    /* Background Utama dengan Gradasi Gelap Futuristik */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #121829 0%, #060814 100%);
        color: #E2E8F0;
    }
    
    /* Judul Utama dengan Efek Glow Neon */
    .judul-utama {
        font-family: 'Orbitron', 'Segoe UI', sans-serif;
        color: #00F2FE;
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.6), 0 0 20px rgba(0, 242, 254, 0.3);
        margin-bottom: 2px;
    }

    .nama-sekolah {
        font-family: 'Segoe UI', sans-serif;
        color: #94A3B8;
        text-align: center;
        font-size: 20px;
        font-weight: 400;
        letter-spacing: 1px;
        margin-bottom: 2px;
    }
    
    .sub-judul {
        font-family: 'Segoe UI', sans-serif;
        color: #4FACFE;
        text-align: center;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 3px;
        margin-bottom: 5px;
        text-transform: uppercase;
    }

    .guru-mapel {
        font-family: 'Segoe UI', sans-serif;
        color: #A78BFA;
        text-align: center;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 35px;
    }
    
    /* Efek Kaca (Glassmorphism) untuk Kartu Absen & Game */
    .kartu-absen {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    .kartu-game {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(0, 242, 254, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.1);
        margin-bottom: 20px;
    }
    
    /* Mengubah Gaya Teks Header di Dalam Kartu */
    .kartu-absen h3, .kartu-game h3 {
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    /* Desain Tombol ala Sci-Fi */
    .stButton>button {
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        padding: 10px 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        color: #E2E8F0 !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Efek Hover Tombol */
    .stButton>button:hover {
        transform: translateY(-2px);
        border-color: #00F2FE !important;
        color: #00F2FE !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
    }
    
    /* Khusus Tombol Primary (Tombol Aksi Utama) */
    .stButton>button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #0072FF 0%, #00F2FE 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    
    .stButton>button[data-testid="baseButton-primary"]:hover {
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
    }
    
    /* Penyesuaian Elemen Input Streamlit agar Senada */
    div[data-baseweb="select"] {
        background-color: #0F172A !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INI DATABASE SISWA ---
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

# --- BANK DATA GAME ---
def get_game(kategori):
    if kategori == "KB":
        return random.choice([
            ("🍎 🍎 🍎", "Ada berapa jumlah buah apel merah di atas?", ["1", "2", "3"], "3"),
            ("🐱", "Suara hewan apakah di atas?", ["Guk-Guk 🐕", "Meong 🐈", "Kwek-Kwek 🦆"], "Meong 🐈"),
            ("💛", "Warna apakah balon hati di atas?", ["Merah ❤️", "Biru 💙", "Kuning 💛"], "Kuning 💛"),
            ("🍌", "Buah apa yang paling disukai monyet?", ["Pisang 🍌", "Anggur 🍇", "Semangka 🍉"], "Pisang 🍌")
        ])
    elif kategori == "TK A":
        return random.choice([
            ("🐘 ... 🐁", "Siapa yang ukuran badannya LEBIH BESAR?", ["Gajah 🐘", "Tikus 🐁", "Semut 🐜"], "Gajah 🐘"),
            ("A, B, _, D", "Huruf apa yang hilang di tengah?", ["C", "M", "Q"], "C"),
            ("🚗 🚗 🚕 🚗", "Mobil ke berapa yang warnanya BERBEDA sendiri?", ["Ke-1", "Ke-2", "Ke-3"], "Ke-3"),
            ("🌧️", "Bagaimana cuaca pada gambar awan di atas?", ["Cerah ☀️", "Hujan 🌧️", "Petir ⛈️"], "Hujan 🌧️")
        ])
    else: # TK B
        return random.choice([
            ("4 + 3 = ?", "Berapakah hasil penjumlahan di atas?", ["6", "7", "8"], "7"),
            ("R _ M A H", "Huruf vokal apa yang hilang untuk melengkapi kata?", ["A", "I", "U"], "U"),
            ("✈️", "Kendaraan di atas tempat jalannya di mana ya?", ["Darat 🛣️", "Laut 🌊", "Udara ☁️"], "Udara ☁️"),
            ("🔥 (PANAS)", "Apa LAWAN KATA dari benda PANAS?", ["DINGIN ❄️", "MALAM 🌙", "KOTOR 🪰"], "DINGIN ❄️")
        ])

# --- HEADER APLIKASI INTERAKTIF SYNCED WITH CYBER LOOK ---
st.markdown('<div class="judul-utama">⚡ CODING INTERACTIVE CORE ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="nama-sekolah">KB-TK Kristen Dian Wacana Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-judul">// KASIH • INTEGRITAS • PEDULI • TAAT //</div>', unsafe_allow_html=True)
st.markdown('<div class="guru-mapel">System Instructor: Ms. Siska</div>', unsafe_allow_html=True)

# --- LAYOUT DUA KOLOM UTAMA ---
kolom_kiri, kolom_kanan = st.columns([1, 1.1], gap="large")

# ==================== PANEL KIRI: TERMINAL ABSENSI ====================
with kolom_kiri:
    st.markdown('<div class="kartu-absen">', unsafe_allow_html=True)
    st.markdown("### 🎛️ SYSTEM VERIFICATION")
    
    # Pilih Kelas
    kelas = st.selectbox("Pilih Parameter Kelas:", ["KB", "TK A", "TK B"])
    info_usia = {"KB": "Level 1: Usia 3-4 Tahun (Kelompok Bermain)", "TK A": "Level 2: Usia 4-5 Tahun (TK Kecil)", "TK B": "Level 3: Usia 5-6 Tahun (TK Besar)"}
    st.caption(f"⚙️ Status: {info_usia[kelas]}")
    
    # Pilih Nama
    daftar_nama = sorted(list(st.session_state.database_siswa[kelas].keys()))
    nama_terpilih = st.selectbox("Identifikasi User (Pilih Nama):", ["-- Pilih ID Nama --"] + daftar_nama)
    
    if nama_terpilih != "-- Pilih ID Nama --":
        hadir = st.session_state.status_hadir[kelas][nama_terpilih]
        bintang = st.session_state.database_siswa[kelas][nama_terpilih]
        
        if hadir:
            st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 10px 0;'>🤖</h1>", unsafe_allow_html=True)
            st.success(f"ACCESS GRANTED. Halo {nama_terpilih}! Data kehadiran tersimpan. Reward: {bintang} Data-Stars ⭐")
        else:
            st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 10px 0;'>🔒</h1>", unsafe_allow_html=True)
            st.warning(f"USER STANDBY. Halo {nama_terpilih}, silakan verifikasi kehadiran Anda.")
            if st.button("INITIALIZE PRESENCE ⚡", type="primary"):
                st.session_state.status_hadir[kelas][nama_terpilih] = True
                st.session_state.game_aktif = get_game(kelas)
                st.session_state.umpan_balik_game = None
                st.rerun()
    else:
        st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 10px 0;'>🌐</h1>", unsafe_allow_html=True)
        st.info("Menunggu input user. Silakan pilih ID nama di atas.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PANEL KANAN: CORE MODULE GAME ====================
with kolom_kanan:
    st.markdown('<div class="kartu-game">', unsafe_allow_html=True)
    st.markdown(f"### 🚀 GAMIFICATION INTERACTION (CLASS {kelas})")
    
    if nama_terpilih == "-- Pilih ID Nama --" or not st.session_state.status_hadir[kelas][nama_terpilih]:
        st.info("🔒 Sinyal Terkunci. Selesaikan verifikasi kehadiran di panel kiri untuk membuka modul ini.")
    else:
        # Jika jawaban benar, kita tampilkan layar kemenangan khusus
        if st.session_state.umpan_balik_game == "benar":
            st.balloons()
            st.markdown("<h2 style='text-align: center; color: #00F2FE;'>🎉 ARCHIVEMENT UNLOCKED! 🎉</h2>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: #A78BFA;'>+1 Core Star Berhasil Ditambahkan ke Database!</h4>", unsafe_allow_html=True)
            
            # Tombol untuk lanjut tantangan berikutnya
            if st.button("NEXT LEVEL CHALLENGE 🚀", type="primary"):
                st.session_state.game_aktif = get_game(kelas)
                st.session_state.umpan_balik_game = None
                st.rerun()
        else:
            # Tampilkan tombol ganti game jika game sedang aktif
            if st.session_state.game_aktif:
                if st.button("🔄 RE-GENERATE QUEST", type="secondary"):
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
            
            # Umpan balik jika jawaban salah
            if st.session_state.umpan_balik_game == "salah":
                st.markdown("<h4 style='text-align: center; color: #EF4444;'>⚡ System Error: Jawaban Kurang Tepat. Inisiasi Percobaan Ulang...</h4>", unsafe_allow_html=True)

            # Menampilkan area pertanyaan game jika game aktif tersedia
            if st.session_state.game_aktif:
                visual, pertanyaan, opsi, jawaban_benar = st.session_state.game_aktif
                
                # Visual Box Hologram bergaya futuristik
                st.markdown(f"<h1 style='text-align: center; font-size: 85px; background: rgba(15, 23, 42, 0.6); border: 2px solid #00F2FE; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: inset 0 0 15px rgba(0,242,254,0.2);'>{visual}</h1>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align: center; color: #38BDF8;'>[QUEST] : {pertanyaan}</h4>", unsafe_allow_html=True)
                
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
                if st.button("🎮 BOOT GAME ENGINE", type="primary"):
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
                    
    st.markdown('</div>', unsafe_allow_html=True)
