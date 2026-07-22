import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px

# 1. Konfigurasi Halaman Browser
st.set_page_config(page_title="Absensi Ceria Dian Wacana", page_icon="🏫", layout="wide")

# 2. SUNTIKAN CSS UNTUK STYLE COLORFUL & PLAYFUL (KINDERGARTEN)
st.markdown("""
    <style>
    /* Latar belakang halaman bergradasi warna pastel ceria */
    .stApp {
        background-color: #F8F9FA;
        background-image: linear-gradient(135deg, #FFD1BA 0%, #FFF2CC 50%, #C1E1C1 100%);
        color: #2D3142;
    }
    
    /* Header Utama */
    .header-kontainer {
        text-align: center;
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 25px;
        border: 4px dashed #FF9AA2;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(255, 154, 162, 0.3);
    }
    .judul-utama {
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
        color: #FF6B6B;
        font-size: 38px;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 0px #FFE6E6;
    }
    .sub-judul {
        color: #4ECDC4;
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
        letter-spacing: 1px;
    }
    .guru-mapel {
        color: #FFA69E;
        font-size: 16px;
        font-weight: bold;
        margin-top: 5px;
        background-color: #FFF5F5;
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
    }
    
    /* Kontainer / Bingkai */
    .stElementContainer div[data-testid="stVerticalBlockBorderContainer"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 3px solid #84DCC6 !important;
        border-radius: 25px !important;
        padding: 25px !important;
        box-shadow: 0 8px 15px rgba(132, 220, 198, 0.2) !important;
    }
    
    /* Bingkai Game / Soal */
    .kotak-soal {
        text-align: center; 
        font-size: 70px; 
        background-color: #FFF3E0; 
        border: 3px solid #FFCC80; 
        border-radius: 20px; 
        padding: 20px; 
        margin-bottom: 20px;
        box-shadow: inset 0 0 10px rgba(255, 204, 128, 0.5);
    }
    
    /* Tombol-tombol Ceria */
    .stButton>button {
        border-radius: 30px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        border: none !important;
        background-color: #A0E8AF !important;
        color: #2D3142 !important;
        width: 100%;
        padding: 10px !important;
        transition: all 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 4px 6px rgba(160, 232, 175, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        background-color: #FF9AA2 !important;
        color: white !important;
        box-shadow: 0 6px 12px rgba(255, 154, 162, 0.5);
    }
    
    /* Kartu Metrik Laporan */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        border: 2px solid #A0C4FF;
        box-shadow: 0 4px 8px rgba(160, 196, 255, 0.3);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Teks dan Label */
    .stSelectbox label, .stRadio label, h2, h3, h4 {
        color: #6D597A !important;
        font-family: 'Comic Sans MS', sans-serif;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- KONFIGURASI FILE PENYIMPANAN DATA (DATABASE CSV) ---
DATA_FILE = "database_absensi_dian_wacana.csv"

# Daftar Master Siswa Tetap
MASTER_SISWA = {
 "KB": ["Adit", "Amari", "Levin", "Sienny", "Jesselyn", "Kenzou", "Ralf"],
 "TK A": ["Kenzie", "Brigitta", "Essy", "Felicia", "Geva", "Greesa", "Laras", "Liam","Lova","Nawasena","Mashal","Senja","Viola","Zio"],
 "TK B": ["Aileen", "Agatha", "Daniel", "Sean", "Elvano", "Betha", "Hiro","Karen","Reiga","Danis","Yura"]
}

def buat_database_baru():
    rows = []
    for kelas, daftar_nama in MASTER_SISWA.items():
        for nama in daftar_nama:
            rows.append({
                "Kelas": kelas,
                "Nama Siswa": nama,
                "Status": "❌ Belum Hadir",
                "Tanggal Presensi": "-",
                "Jam Presensi": "-",
                "Bintang": 0,
                "Total Hadir Sesi": 0
            })
    df_awal = pd.DataFrame(rows)
    df_awal.to_csv(DATA_FILE, index=False)
    return df_awal

def muat_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if "Waktu Presensi" in df.columns:
            df = df.drop(columns=["Waktu Presensi"])
        if "Tanggal Presensi" not in df.columns:
            df["Tanggal Presensi"] = "-"
        if "Jam Presensi" not in df.columns:
            df["Jam Presensi"] = "-"
        if "Total Hadir Sesi" not in df.columns:
            df["Total Hadir Sesi"] = df["Status"].apply(lambda x: 1 if "✅" in str(x) else 0)
        return df
    else:
        return buat_database_baru()

def simpan_data(df):
    df.to_csv(DATA_FILE, index=False)

if 'df_master' not in st.session_state:
    st.session_state.df_master = muat_data()

if 'nama_aktif' not in st.session_state:
    st.session_state.nama_aktif = "-- Pilih Nama --"

if 'game_aktif' not in st.session_state:
    st.session_state.game_aktif = None

if 'umpan_balik_game' not in st.session_state:
    st.session_state.umpan_balik_game = None


# =========================================================================
# --- GENERATOR SOAL OTOMATIS BERVARIASI TEMA KINDERGARTEN ---
# =========================================================================
def get_game(kategori):
    if kategori == "KB":
        tipe_game = random.choice(["hitung_dasar", "warna", "hewan", "benda"])
        if tipe_game == "hitung_dasar":
            emoji = random.choice(["🍓", "🧸", "🎈", "🐥", "🚗"])
            jumlah = random.randint(1, 3)
            return (" ".join([emoji] * jumlah), f"Ada berapa jumlah {emoji} di atas?", [str(jumlah), str(jumlah+1), "4"], str(jumlah))
        elif tipe_game == "warna":
            return random.choice([
                ("🍌", "Buah Pisang di atas warnanya apa?", ["Kuning", "Biru", "Merah"], "Kuning"),
                ("🍏", "Buah Apel ini warnanya apa?", ["Hijau", "Hitam", "Ungu"], "Hijau"),
                ("☁️", "Awan di langit warnanya apa?", ["Putih", "Coklat", "Merah"], "Putih")
            ])
        elif tipe_game == "hewan":
            return random.choice([
                ("🐄", "Hewan apa yang suaranya MOOO...?", ["Sapi 🐄", "Bebek 🦆", "Kucing 🐈"], "Sapi 🐄"),
                ("🐕", "Hewan apa yang suaranya GUK GUK...?", ["Anjing 🐕", "Ayam 🐓", "Kuda 🐎"], "Anjing 🐕"),
                ("🐸", "Hewan apa yang suka melompat dan berbunyi TEOBLUNG?", ["Katak 🐸", "Burung 🐦", "Ikan 🐟"], "Katak 🐸")
            ])
        else: # benda
            return random.choice([
                ("☂️", "Kapan kita memakai Payung?", ["Saat Hujan 🌧️", "Saat Tidur 🛏️", "Saat Makan 🍽️"], "Saat Hujan 🌧️"),
                ("🦷🪥", "Alat ini dipakai untuk membersihkan apa?", ["Gigi", "Rambut", "Sepatu"], "Gigi")
            ])
            
    elif kategori == "TK A":
        tipe_game = random.choice(["hitung", "huruf", "ukuran", "pola"])
        if tipe_game == "hitung":
            a, b = random.randint(1, 3), random.randint(1, 2)
            buah = random.choice(["🍎", "🍊", "🧁"])
            return (f"{a} {buah} + {b} {buah}", f"Berapa jumlah semua {buah} di atas?", [str(a+b), str(a+b+1), str(a+b-1)], str(a+b))
        elif tipe_game == "huruf":
            return random.choice([
                ("B - U - K - U", "Kata 'BUKU' huruf awalnya apa?", ["B", "K", "U"], "B"),
                ("A - P - E - L", "Kata 'APEL' huruf awalnya apa?", ["P", "A", "L"], "A"),
                ("M - A - T - A", "Huruf apa yang hilang? M - _ - T - A", ["A", "O", "I"], "A")
            ])
        elif tipe_game == "ukuran":
            return random.choice([
                ("🐘 ... 🐁", "Hewan manakah yang badannya PALING BESAR?", ["Gajah 🐘", "Tikus 🐁", "Sama Besar"], "Gajah 🐘"),
                ("🚌 ... 🚗", "Kendaraan manakah yang PALING PANJANG?", ["Bus 🚌", "Mobil 🚗", "Sama Panjang"], "Bus 🚌"),
                ("🍉 ... 🍓", "Buah manakah yang LEBIH BERAT?", ["Semangka 🍉", "Stroberi 🍓", "Sama Berat"], "Semangka 🍉")
            ])
        else: # pola
            e1, e2 = random.sample(["🔴", "🔵", "🟡", "🟢"], 2)
            return (f"{e1} {e2} {e1} {e2} ... ?", "Warna apa yang muncul setelah ini?", [e1, e2, "⚫"], e1)
            
    else: 
        tipe_game = random.choice(["hitung_tkb", "arah", "membaca", "logika_sifat"])
        if tipe_game == "hitung_tkb":
            mode = random.choice(["+", "-"])
            if mode == "+":
                a, b = random.randint(3, 5), random.randint(2, 4)
                soal = f"{a} 🍬 + {b} 🍬 = ?"
            else:
                a, b = random.randint(6, 9), random.randint(1, 4)
                soal = f"{a} 🍪 dimakan {b} 🍪, sisa = ?"
            kunci = a + b if mode == "+" else a - b
            return (soal, "Yuk berhitung! Berapa jawabannya?", [str(kunci), str(kunci+1), str(kunci-1)], str(kunci))
        elif tipe_game == "arah":
            awal = random.randint(1, 2)
            langkah = random.randint(2, 3)
            return (f"Rumah {awal} ➔ " + ("🐇 " * langkah), f"Kelinci mulai di Rumah {awal} lalu melompat {langkah} kali. Di rumah nomor berapakah kelinci sekarang?", [str(awal+langkah), str(awal+langkah+1), "Rumah 10"], str(awal+langkah))
        elif tipe_game == "membaca":
            return random.choice([
                ("B - O - L - A", "Jika dibaca bunyinya menjadi apa?", ["BOLA", "BALO", "BULA"], "BOLA"),
                ("S - A - P - U", "Kata ini digunakan untuk membersihkan lantai, dibaca?", ["SAPI", "SAPU", "SOPU"], "SAPU"),
                ("M - E - J - A", "Tempat kita menulis di sekolah, dibaca?", ["MAJU", "MEJA", "MATA"], "MEJA")
            ])
        else:
            return random.choice([
                ("🔥", "Lawan kata dari benda yang PANAS adalah?", ["DINGIN 🧊", "TERANG ☀️", "MANIS 🍬"], "DINGIN 🧊"),
                ("🍋 vs 🍬", "Makanan manakah yang rasanya MANIS?", ["Permen 🍬", "Jeruk Nipis 🍋", "Garam 🧂"], "Permen 🍬"),
                ("☀️ vs 🌙", "Matahari muncul pada saat hari sedang?", ["Malam", "Siang", "Hujan"], "Siang")
            ])

# Fungsi baru untuk mengacak soal dan MENGUNCI urutannya ke dalam session state
def generate_new_game(kelas):
    visual, pertanyaan, opsi, jawaban_benar = get_game(kelas)
    opsi_acak = random.sample(opsi, len(opsi)) # Acak posisi tombol hanya sekali di sini
    return (visual, pertanyaan, opsi_acak, jawaban_benar)

# --- TAMPILAN HEADER ---
st.markdown("""
    <div class="header-kontainer">
        <div class="judul-utama">🌈 ABSENSI CERIA & BERMAIN 🎨</div>
        <div class="sub-judul">KB-TK KRISTEN DIAN WACANA 🧸</div>
        <div class="guru-mapel">👩‍🏫 Guru Kelas: Ms. Siska</div>
    </div>
""", unsafe_allow_html=True)

# GRID UTAMA: Panel Input & Game
kolom_absen, kolom_game = st.columns(2, gap="large")

# FRAME 1: PANEL ABSENSI (KIRI)
with kolom_absen:
    with st.container(border=True):
        st.subheader("🎒 Buku Absen Kelas")
        
        if 'kelas_lama' not in st.session_state:
            st.session_state.kelas_lama = "KB"
        
        kelas = st.selectbox("1. Pilih Kelasmu:", ["KB", "TK A", "TK B"])
        
        if kelas != st.session_state.kelas_lama:
            st.session_state.nama_aktif = "-- Pilih Nama --"
            st.session_state.kelas_lama = kelas
        
        df_kelas = st.session_state.df_master[st.session_state.df_master["Kelas"] == kelas]
        daftar_nama_asli = sorted(df_kelas["Nama Siswa"].tolist())
        
        opsi_selectbox = ["-- Pilih Nama --"]
        mapping_nama = {"-- Pilih Nama --": "-- Pilih Nama --"}
        indeks_default = 0
        
        for i, nama in enumerate(daftar_nama_asli):
            status_siswa = df_kelas[df_kelas["Nama Siswa"] == nama]["Status"].values[0]
            if "✅" in str(status_siswa):
                label_tampilan = f"✅ {nama} (Sudah Datang)"
            else:
                label_tampilan = f"👧👦 {nama}"
            
            opsi_selectbox.append(label_tampilan)
            mapping_nama[label_tampilan] = nama
            
            if nama == st.session_state.nama_aktif:
                indeks_default = i + 1
        
        pilihan_tampilan = st.selectbox("2. Cari & Klik Namamu:", opsi_selectbox, index=indeks_default)
        nama_terpilled = mapping_nama[pilihan_tampilan]
        st.session_state.nama_aktif = nama_terpilled
        
        st.write("---")
        
        if nama_terpilled != "-- Pilih Nama --":
            idx_anak = st.session_state.df_master[(st.session_state.df_master["Kelas"] == kelas) & (st.session_state.df_master["Nama Siswa"] == nama_terpilled)].index[0]
            row_anak = st.session_state.df_master.loc[idx_anak]
            
            hadir = "✅" in str(row_anak["Status"])
            bintang = row_anak["Bintang"]
            tgl_absen = row_anak["Tanggal Presensi"]
            jam_absen = row_anak["Jam Presensi"]
            
            if hadir:
                st.markdown("<h1 style='text-align: center; margin:0;'>🥰</h1>", unsafe_allow_html=True)
                st.success(f"Pintarnya! {nama_terpilled} masuk tanggal {tgl_absen} jam {jam_absen}. Kamu punya {bintang} ⭐")
            else:
                st.markdown("<h1 style='text-align: center; margin:0;'>😊</h1>", unsafe_allow_html=True)
                st.warning(f"Halo {nama_terpilled} sayang, yuk klik tombol hadir dulu di bawah ini!")
                if st.button("🙋‍♀️🙋‍♂️ SAYA HADIR MS. SISKA!", type="primary"):
                    waktu_wib = datetime.utcnow() + timedelta(hours=7)
                    
                    st.session_state.df_master.loc[idx_anak, "Status"] = "✅ Sudah Datang"
                    st.session_state.df_master.loc[idx_anak, "Tanggal Presensi"] = waktu_wib.strftime("%d-%m-%Y")
                    st.session_state.df_master.loc[idx_anak, "Jam Presensi"] = waktu_wib.strftime("%H:%M:%S")
                    st.session_state.df_master.loc[idx_anak, "Total Hadir Sesi"] += 1
                    
                    simpan_data(st.session_state.df_master)
                    
                    # Menggunakan fungsi baru untuk mengunci opsi acak
                    st.session_state.game_aktif = generate_new_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
        else:
            st.markdown("<h1 style='text-align: center; margin:0;'>🎈</h1>", unsafe_allow_html=True)
            st.info("Pilih kelas dan namamu di atas dulu ya, Nak!")

# FRAME 2: PANEL GAME (KANAN)
with kolom_game:
    with st.container(border=True):
        st.subheader("🧩 Waktunya Bermain!")
        
        status_absen_siswa = ""
        if nama_terpilled != "-- Pilih Nama --":
            status_absen_siswa = st.session_state.df_master[(st.session_state.df_master["Kelas"] == kelas) & (st.session_state.df_master["Nama Siswa"] == nama_terpilled)]["Status"].values[0]
        
        if nama_terpilled == "-- Pilih Nama --" or not ("✅" in str(status_absen_siswa)):
            st.markdown("<h1 style='text-align: center; margin: 30px 0;'>🔒</h1>", unsafe_allow_html=True)
            st.info("Game masih terkunci! Absen hadir dulu ya di sebelah kiri untuk mulai bermain. 🎨")
        else:
            idx_anak = st.session_state.df_master[(st.session_state.df_master["Kelas"] == kelas) & (st.session_state.df_master["Nama Siswa"] == nama_terpilled)].index[0]
            
            if st.session_state.umpan_balik_game == "benar":
                st.balloons()
                st.markdown("<h3 style='text-align: center; color: #4ECDC4;'>🌟 YAY BENAR! DAPAT +1 BINTANG!</h3>", unsafe_allow_html=True)
                if st.button("🚀 MAIN LAGI YUK", type="primary"):
                    st.session_state.game_aktif = generate_new_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
            else:
                if st.session_state.game_aktif:
                    if st.button("🔄 GANTI PERTANYAAN"):
                        st.session_state.game_aktif = generate_new_game(kelas)
                        st.session_state.umpan_balik_game = None
                        st.rerun()
                
                if st.session_state.umpan_balik_game == "salah":
                    st.error("❌ Wah, masih kurang tepat. Tidak apa-apa, ayo coba lagi! 💪")

                if st.session_state.game_aktif:
                    # Opsi di sini sekarang sudah dikunci (static) dari fungsi generate_new_game
                    visual, pertanyaan, opsi_terkunci, jawaban_benar = st.session_state.game_aktif
                    
                    st.markdown(f'<div class="kotak-soal">{visual}</div>', unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align:center; font-weight:700; font-size:20px; color:#6D597A;">{pertanyaan}</p>', unsafe_allow_html=True)
                    
                    kol_opsi = st.columns(len(opsi_terkunci))
                    for i, alternatif in enumerate(opsi_terkunci):
                        with kol_opsi[i]:
                            # Tombol menggunakan key yang fix dan stabil
                            if st.button(alternatif, key=f"btn_jawab_{i}_{alternatif}"):
                                if alternatif == jawaban_benar:
                                    st.session_state.df_master.loc[idx_anak, "Bintang"] += 1
                                    simpan_data(st.session_state.df_master)
                                    st.session_state.umpan_balik_game = "benar"
                                    st.rerun()
                                else:
                                    st.session_state.umpan_balik_game = "salah"
                                    st.rerun()
                else:
                    if st.button("🎲 MULAI BERMAIN", type="primary"):
                        st.session_state.game_aktif = generate_new_game(kelas)
                        st.session_state.umpan_balik_game = None
                        st.rerun()

st.write("<br><br>", unsafe_allow_html=True)

# ==================== COMPONENT UTAMA: LOG & GRAFIK LAPORAN AKHIR ====================
st.write("---")
with st.container(border=True):
    st.markdown("<h2 style='margin-top:0;'>📊 Catatan Ms. Siska (Laporan Kelas)</h2>", unsafe_allow_html=True)
    
    total_siswa = len(st.session_state.df_master)
    total_hadir = len(st.session_state.df_master[st.session_state.df_master["Status"].str.contains("✅", na=False)])
    total_belum = total_siswa - total_hadir
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"<div class='metric-card'>🧒👧 <b>Jumlah Semua Anak</b><br><span style='font-size:26px; font-weight:900; color:#6D597A;'>{total_siswa} Anak</span></div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"<div class='metric-card'>🏫 <b>Hadir Hari Ini</b><br><span style='font-size:26px; font-weight:900; color:#4ECDC4;'>{total_hadir} Anak</span></div>", unsafe_allow_html=True)
    with col_m3:
        persentase = round((total_hadir / total_siswa) * 100) if total_siswa > 0 else 0
        st.markdown(f"<div class='metric-card'>🌟 <b>Persentase Hadir</b><br><span style='font-size:26px; font-weight:900; color:#FF9AA2;'>{persentase}%</span></div>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    
    pilih_log_kelas = st.radio("Pilih kelas yang mau dilihat:", ["Semua Kelas", "KB", "TK A", "TK B"], horizontal=True, key="filter_laporan")
    df_filtered = st.session_state.df_master if pilih_log_kelas == "Semua Kelas" else st.session_state.df_master[st.session_state.df_master["Kelas"] == pilih_log_kelas]

    # --- 1. SEKSI GRAFIK LINGKARAN (PIE CHART) ---
    st.markdown("### 🍩 Grafik Kehadiran")
    
    hadir_filter = len(df_filtered[df_filtered["Status"].str.contains("✅", na=False)])
    belum_filter = len(df_filtered) - hadir_filter
    
    if len(df_filtered) > 0:
        kol_grafik, kol_info_detail = st.columns([3, 2], gap="large")
        
        with kol_grafik:
            df_pie = pd.DataFrame({
                "Status Presensi": ["Sudah Datang (✅)", "Belum Datang (❌)"],
                "Jumlah Anak": [hadir_filter, belum_filter]
            })
            
            fig = px.pie(
                df_pie, 
                values="Jumlah Anak", 
                names="Status Presensi",
                color="Status Presensi",
                color_discrete_map={"Sudah Datang (✅)": "#A0E8AF", "Belum Datang (❌)": "#FF9AA2"}, # Pastel Green & Pink
                hole=0.4
            )
            
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Comic Sans MS", color="#2D3142"),
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with kol_info_detail:
            st.markdown("#### 📝 Detail Kelas")
            persen_hadir = round((hadir_filter / len(df_filtered)) * 100) if len(df_filtered) > 0 else 0
            persen_belum = 100 - persen_hadir
            
            st.markdown(f"""
            * 🟢 **Sudah di Sekolah:** `{hadir_filter} Anak` ({persen_hadir}%)
            * 🔴 **Belum di Sekolah:** `{belum_filter} Anak` ({persen_belum}%)
            * 🏫 **Total Murid di Kelas:** `{len(df_filtered)} Anak`
            
            ---
            💡 *Pesan Ms. Siska: Grafik donat ini membantuku melihat seberapa banyak anak hebat yang sudah datang hari ini sebelum mulai bernyanyi!*
            """)
    else:
        st.info("ℹ️ Tidak ada data murid di kelas ini.")

    # --- 2. SEKSI TABEL LOG AUDIT ---
    st.write("---")
    st.markdown("### 📋 Buku Nilai Bintang Anak Hebat")
    
    df_tampilan_tabel = df_filtered.copy()
    df_tampilan_tabel["Bintang"] = df_tampilan_tabel["Bintang"].apply(lambda x: f"{x} ⭐")
    df_tampilan_tabel["Total Hadir Sesi"] = df_tampilan_tabel["Total Hadir Sesi"].apply(lambda x: f"{x} Hari")
    
    st.dataframe(
        df_tampilan_tabel[["Kelas", "Nama Siswa", "Status", "Tanggal Presensi", "Jam Presensi", "Bintang", "Total Hadir Sesi"]], 
        use_container_width=True, 
        hide_index=True
    )

    # --- FITUR ADMIN GURU (DENGAN TOMBOL RESET DATABASE TOTAL) ---
    st.write("---")
    with st.expander("⚙️ Laci Rahasia Ms. Siska (Pengaturan)"):
        st.markdown("### 🌅 Memulai Hari Baru")
        
        if st.button("🌅 Buka Kelas Hari Baru (Reset Status Kehadiran Saja)"):
            st.session_state.df_master["Status"] = "❌ Belum Hadir"
            st.session_state.df_master["Tanggal Presensi"] = "-"
            st.session_state.df_master["Jam Presensi"] = "-"
            simpan_data(st.session_state.df_master)
            st.success("Selamat Pagi! Status absen sudah kosong untuk hari ini. Bintang anak-anak tetap tersimpan aman. 🥰")
            st.rerun()
            
        st.write("<br>", unsafe_allow_html=True)
        st.write("---")
        
        st.markdown("### 🚨 Hapus Semua Data (Kembali ke Nol)")
        st.error("Perhatian: Tombol di bawah ini akan MENGHAPUS SEMUA BINTANG dan HARI HADIR anak-anak menjadi 0 (Nol).")
        
        konfirmasi_reset = st.checkbox("Saya yakin ingin menghapus semua bintang dan kembali ke buku baru (Tahun Ajaran Baru)")
        
        if st.button("🗑️ HAPUS SEMUA DATA & BINTANG", type="secondary"):
            if konfirmasi_reset:
                st.session_state.df_master = buat_database_baru()
                st.session_state.nama_aktif = "-- Pilih Nama --"
                st.session_state.game_aktif = None
                st.session_state.umpan_balik_game = None
                st.success("Buku rapor sudah dibersihkan! Mulai mengumpulkan bintang dari nol lagi ya! ✨")
                st.rerun()
            else:
                st.warning("Centang dulu kotak persetujuan di atas ya Ms. Siska!")
