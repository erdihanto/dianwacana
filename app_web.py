import streamlit as st

import random



# 1. Konfigurasi Halaman Browser

st.set_page_config(page_title="Absensi Intra Coding", page_icon="🏫", layout="wide")



# 2. SUNTIKAN CSS UNTUK TAMPILAN SUPER CERIA & WARNA-WARNI (KIDS THEME)

st.markdown("""

    <style>

    .stApp {

        background: linear-gradient(135deg, #FEF08A 0%, #E0F2FE 50%, #FBCFE8 100%);

    }

    

    .judul-utama {

        font-family: 'Comic Sans MS', 'Segoe UI', sans-serif;

        color: #FF6B6B;

        text-align: center;

        font-size: 42px;

        font-weight: bold;

        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);

        margin-bottom: 5px;

    }



    .nama-sekolah {

        font-family: 'Segoe UI', sans-serif;

        color: #4B5563;

        text-align: center;

        font-size: 24px;

        font-weight: 600;

        margin-bottom: 2px;

    }

    

    .sub-judul {

        font-family: 'Segoe UI', sans-serif;

        color: #4D96FF;

        text-align: center;

        font-size: 18px;

        font-weight: bold;

        margin-bottom: 5px;

    }



    .guru-mapel {

        font-family: 'Comic Sans MS', sans-serif;

        color: #8B5CF6;

        text-align: center;

        font-size: 20px;

        font-weight: bold;

        margin-bottom: 25px;

    }

    

    .kartu-absen {

        background-color: #FFFDE7;

        border: 4px solid #FFF59D;

        border-radius: 25px;

        padding: 25px;

        box-shadow: 0px 8px 16px rgba(0,0,0,0.05);

    }

    

    .kartu-game {

        background-color: #F0FDF4;

        border: 4px solid #BBF7D0;

        border-radius: 25px;

        padding: 25px;

        box-shadow: 0px 8px 16px rgba(0,0,0,0.05);

    }

    

    .stButton>button {

        border-radius: 50px !important;

        font-size: 18px !important;

        font-weight: bold !important;

        padding: 12px 25px !important;

        transition: transform 0.2s;

        box-shadow: 0 4px 6px rgba(0,0,0,0.1);

    }

    

    .stButton>button:hover {

        transform: scale(1.08);

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



# --- HEADER APLIKASI ---

st.markdown('<div class="judul-utama">🏫 ABSENSI INTRA CODING</div>', unsafe_allow_html=True)

st.markdown('<div class="nama-sekolah">KB-TK Kristen Dian Wacana</div>', unsafe_allow_html=True)

st.markdown('<div class="sub-judul">🎈 🌈 KASIH • INTEGRITAS • PEDULI • TAAT 🌈 🎈</div>', unsafe_allow_html=True)

st.markdown('<div class="guru-mapel">👩‍🏫 Guru Mapel: Ms. Siska</div>', unsafe_allow_html=True)



# --- LAYOUT DUA KOLOM UTAMA ---

kolom_kiri, kolom_kanan = st.columns([1, 1.1], gap="large")



# ==================== PANEL KIRI: ABSENSI CERIA ====================

with kolom_kiri:

    st.markdown('<div class="kartu-absen">', unsafe_allow_html=True)

    st.markdown("### ✨ 1. Ayo Pilih Kelas & Namamu! ✨")

    

    # Pilih Kelas

    kelas = st.selectbox("Pilih Kelas Di Sini ya:", ["KB", "TK A", "TK B"])

    info_usia = {"KB": "Usia 3-4 Tahun (Kelompok Bermain)", "TK A": "Usia 4-5 Tahun (TK Kecil)", "TK B": "Usia 5-6 Tahun (TK Besar)"}

    st.info(f"👶 {info_usia[kelas]}")

    

    # Pilih Nama

    daftar_nama = sorted(list(st.session_state.database_siswa[kelas].keys()))

    nama_terpilih = st.selectbox("Siapa Namamu Sayang?", ["-- Klik Pilihan Nama --"] + daftar_nama)

    

    if nama_terpilih != "-- Klik Pilihan Nama --":

        hadir = st.session_state.status_hadir[kelas][nama_terpilih]

        bintang = st.session_state.database_siswa[kelas][nama_terpilih]

        

        if hadir:

            st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 0;'>🥰</h1>", unsafe_allow_html=True)

            st.success(f"Selamat Datang {nama_terpilih}! Kamu sudah hadir. Bintangmu: {bintang} ⭐")

        else:

            st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 0;'>🙂</h1>", unsafe_allow_html=True)

            st.warning(f"Halo {nama_terpilih}, kamu belum absen hari ini.")

            if st.button("✋ SAYA HADIR! 🎈", type="primary"):

                st.session_state.status_hadir[kelas][nama_terpilih] = True

                st.session_state.game_aktif = get_game(kelas)

                st.session_state.umpan_balik_game = None

                st.rerun()

    else:

        st.markdown(f"<h1 style='text-align: center; font-size: 70px; margin: 0;'>😶</h1>", unsafe_allow_html=True)

        st.write("Silakan klik kolom di atas untuk mencari namamu ya!")

        

    st.markdown('</div>', unsafe_allow_html=True)



# ==================== PANEL KANAN: GAME ZONA BERMAIN ====================

with kolom_kanan:

    st.markdown('<div class="kartu-game">', unsafe_allow_html=True)

    st.markdown(f"### 🎮 ZONA BERMAIN KELAS {kelas} 🎮")

    

    if nama_terpilih == "-- Klik Pilihan Nama --" or not st.session_state.status_hadir[kelas][nama_terpilih]:

        st.info("Kamu harus **Absen Hadir** ✋ dulu di sebelah kiri sebelum bisa membuka permainan seru ini! 😊")

    else:

        if st.button("🎲 MAIN / GANTI GAME BARU", type="secondary"):

            st.session_state.game_aktif = get_game(kelas)

            st.session_state.umpan_balik_game = None

            st.rerun()



        if st.session_state.umpan_balik_game == "benar":

            st.balloons()

            st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🏆 HEBAT! JAWABANMU BENAR! 🎉</h2>", unsafe_allow_html=True)

            st.session_state.umpan_balik_game = None 

        elif st.session_state.umpan_balik_game == "salah":

            st.markdown("<h4 style='text-align: center; color: #FF5722;'>💪 Hampir tepat! Ayo coba lagi, kamu pasti bisa!</h4>", unsafe_allow_html=True)



        if st.session_state.game_aktif:

            visual, pertanyaan, opsi, jawaban_benar = st.session_state.game_aktif

            

            st.markdown(f"<h1 style='text-align: center; font-size: 85px; background-color: #FFF9C4; border: 3px dashed #FFD93D; border-radius: 20px; padding: 20px; margin-bottom: 15px;'>{visual}</h1>", unsafe_allow_html=True)

            st.markdown(f"<h4 style='text-align: center; color: #2E7D32;'>{pertanyaan}</h4>", unsafe_allow_html=True)

            

            kol_opsi = st.columns(len(opsi))

            for i, alternatif in enumerate(opsi):

                with kol_opsi[i]:

                    if st.button(alternatif, key=f"btn_{alternatif}_{i}"):

                        if alternatif == jawaban_benar:

                            st.session_state.database_siswa[kelas][nama_terpilih] += 1

                            st.session_state.umpan_balik_game = "benar"

                            st.session_state.game_aktif = get_game(kelas) 

                            st.rerun()

                        else:

                            st.session_state.umpan_balik_game = "salah"

                            st.rerun()

        else:

            st.write("Klik tombol **🎲 MAIN / GANTI GAME BARU** di atas untuk mulai bermain!")

                    

    st.markdown('</div>', unsafe_allow_html=True) 

