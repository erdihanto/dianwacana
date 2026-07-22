import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px

# 1. Konfigurasi Halaman Browser
st.set_page_config(page_title="Misi Tata Surya Dian Wacana", page_icon="🚀", layout="wide")

# 2. SUNTIKAN CSS UNTUK STYLE GALAXY / SPACE
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0C10;
        background-image: radial-gradient(circle at center, #1F2833 0%, #0B0C10 100%);
        color: #C5C6C7;
    }
    .header-kontainer {
        text-align: center;
        background-color: rgba(31, 40, 51, 0.8);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #45A29E;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(69, 162, 158, 0.3);
    }
    .judul-utama {
        font-family: 'Courier New', Courier, monospace;
        color: #66FCF1;
        font-size: 34px;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 0 10px rgba(102, 252, 241, 0.5);
    }
    .sub-judul {
        color: #F8E9A1;
        font-size: 14px;
        font-weight: 700;
        margin-top: 5px;
        letter-spacing: 2px;
    }
    .guru-mapel {
        color: #A0B2C6;
        font-size: 15px;
        margin-top: 4px;
    }
    .stElementContainer div[data-testid="stVerticalBlockBorderContainer"] {
        background-color: rgba(31, 40, 51, 0.6) !important;
        border: 1px solid #45A29E !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
    }
    .kotak-soal {
        text-align: center; 
        font-size: 60px; 
        background-color: rgba(11, 12, 16, 0.8); 
        border: 1px solid #66FCF1; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 15px;
        color: #FFFFFF;
    }
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: 1px solid #45A29E !important;
        background-color: rgba(11, 12, 16, 0.8) !important;
        color: #66FCF1 !important;
        width: 100%;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        border-color: #F8E9A1 !important;
        color: #0B0C10 !important;
        background-color: #F8E9A1 !important;
        box-shadow: 0 0 10px rgba(248, 233, 161, 0.6);
    }
    .metric-card {
        background-color: rgba(11, 12, 16, 0.8);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid #45A29E;
        color: #E0E0E0;
    }
    .stSelectbox label, .stRadio label, h2, h3, h4 {
        color: #66FCF1 !important;
    }
    p, li {
        color: #C5C6C7;
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
                "Status": "❌ Belum Mendarat",
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
            df["Total Hadir Sesi"] = df["Status"].apply(lambda x: 1 if "🚀" in str(x) else 0)
        return df
    else:
        return buat_database_baru()

def simpan_data(df):
    df.to_csv(DATA_FILE, index=False)

if 'df_master' not in st.session_state:
    st.session_state.df_master = muat_data()

if 'nama_aktif' not in st.session_state:
    st.session_state.nama_aktif = "-- Pilih Astronot --"

if 'game_aktif' not in st.session_state:
    st.session_state.game_aktif = None

if 'umpan_balik_game' not in st.session_state:
    st.session_state.umpan_balik_game = None

# --- GENERATOR SOAL OTOMATIS TEMA TATA SURYA ---
def get_game(kategori):
    tipe_game = random.choice(["hitung", "pola", "logika", "arah"])
    if kategori == "KB":
        if tipe_game == "hitung":
            emoji = random.choice(["🌎", "🪐", "🚀", "👽", "⭐"])
            jumlah = random.randint(1, 4)
            return (" ".join([emoji] * jumlah), f"Ada berapa jumlah benda angkasa {emoji} di atas?", [str(jumlah), str(jumlah+1), "5"], str(jumlah))
        else:
            return random.choice([
                ("⭐", "Warna apakah bintang di atas?", ["Kuning", "Biru", "Hijau"], "Kuning"),
                ("👽", "Makhluk apakah gambar di atas?", ["Alien", "Kucing", "Astronot"], "Alien"),
                ("🔴", "Bentuk apakah planet berwarna merah di atas?", ["Kotak", "Lingkaran", "Segitiga"], "Lingkaran")
            ])
    elif kategori == "TK A":
        if tipe_game == "hitung":
            a, b = random.randint(1, 3), random.randint(1, 2)
            return (f"{a} 🚀 + {b} 🚀 = ?", "Berapa total roket yang meluncur?", [str(a+b), str(a+b+1), str(a+b-1)], str(a+b))
        elif tipe_game == "pola":
            e1, e2 = random.sample(["🌎", "🪐", "☄️", "☀️"], 2)
            return (f"{e1} {e2} {e1} {e2} ?", "Benda angkasa apa setelahnya sesuai pola orbit?", [e1, e2, "❓"], e1)
        else:
            return random.choice([
                ("☀️ ... 🌕", "Siapa yang ukurannya LEBIH BESAR di angkasa?", ["Matahari ☀️", "Bulan 🌕"], "Matahari ☀️"),
                ("M, A, R, _", "Huruf apa yang hilang pada kata MARS?", ["S", "T", "B"], "S")
            ])
    else: # TK B
        if tipe_game == "hitung":
            mode = random.choice(["+", "-"])
            a, b = (random.randint(3, 6), random.randint(1, 3)) if mode == "+" else (random.randint(6, 9), random.randint(1, 4))
            kunci = a + b if mode == "+" else a - b
            return (f"{a} {mode} {b} = ?", "Berapa hasil perhitungan rute roket di atas?", [str(kunci), str(kunci+1), str(kunci-1)], str(kunci))
        elif tipe_game == "arah":
            awal = random.randint(1, 3)
            langkah = random.randint(1, 2)
            return (f"Sektor {awal} ➔ " + ("🚀 " * langkah), f"Jika roket di sektor {awal} maju {langkah} sektor, di sektor nomor berapa roket sekarang?", [str(awal+langkah), str(awal+langkah+1), "0"], str(awal+langkah))
        else:
            return random.choice([
                ("☀️", "Apa LAWAN KATA dari keadaan TERANG di siang hari?", ["GELAP", "PANAS", "DINGIN"], "GELAP"),
                ("🔴 🟡 🔵 🔴 🟡 _", "Lanjutkan pola warna planet berikut!", ["Merah", "Kuning", "Biru"], "Biru")
            ])

# --- TAMPILAN HEADER ---
st.markdown("""
    <div class="header-kontainer">
        <div class="judul-utama">🌌 MISI TATA SURYA: ABSENSI & GAME CODING</div>
        <div class="sub-judul">STASIUN LUAR ANGKASA KB-TK DIAN WACANA</div>
        <div class="guru-mapel">👩‍🚀 Komandan Misi: Ms. Siska</div>
    </div>
""", unsafe_allow_html=True)

# GRID UTAMA: Panel Input & Game
kolom_absen, kolom_game = st.columns(2, gap="large")

# FRAME 1: PANEL ABSENSI (KIRI)
with kolom_absen:
    with st.container(border=True):
        st.subheader("🛰️ Radar Deteksi Astronot")
        
        if 'kelas_lama' not in st.session_state:
            st.session_state.kelas_lama = "KB"
        
        kelas = st.selectbox("1. Pilih Skuadron (Kelas):", ["KB", "TK A", "TK B"])
        
        if kelas != st.session_state.kelas_lama:
            st.session_state.nama_aktif = "-- Pilih Astronot --"
            st.session_state.kelas_lama = kelas
        
        df_kelas = st.session_state.df_master[st.session_state.df_master["Kelas"] == kelas]
        daftar_nama_asli = sorted(df_kelas["Nama Siswa"].tolist())
        
        opsi_selectbox = ["-- Pilih Astronot --"]
        mapping_nama = {"-- Pilih Astronot --": "-- Pilih Astronot --"}
        indeks_default = 0
        
        for i, nama in enumerate(daftar_nama_asli):
            status_siswa = df_kelas[df_kelas["Nama Siswa"] == nama]["Status"].values[0]
            if "🚀" in str(status_siswa):
                label_tampilan = f"🚀 {nama} (Sudah Mendarat)"
            else:
                label_tampilan = f"🧑‍🚀 {nama}"
            
            opsi_selectbox.append(label_tampilan)
            mapping_nama[label_tampilan] = nama
            
            if nama == st.session_state.nama_aktif:
                indeks_default = i + 1
        
        pilihan_tampilan = st.selectbox("2. Panggil Namamu ke Stasiun:", opsi_selectbox, index=indeks_default)
        nama_terpilled = mapping_nama[pilihan_tampilan]
        st.session_state.nama_aktif = nama_terpilled
        
        st.write("---")
        
        if nama_terpilled != "-- Pilih Astronot --":
            idx_anak = st.session_state.df_master[(st.session_state.df_master["Kelas"] == kelas) & (st.session_state.df_master["Nama Siswa"] == nama_terpilled)].index[0]
            row_anak = st.session_state.df_master.loc[idx_anak]
            
            hadir = "🚀" in str(row_anak["Status"])
            bintang = row_anak["Bintang"]
            tgl_absen = row_anak["Tanggal Presensi"]
            jam_absen = row_anak["Jam Presensi"]
            
            if hadir:
                st.markdown("<h1 style='text-align: center; margin:0;'>👨‍🚀</h1>", unsafe_allow_html=True)
                st.success(f"Selamat Mendarat, Astronot {nama_terpilled}! Deteksi masuk tanggal {tgl_absen} jam {jam_absen}. Bintang galaksimu: {bintang} ⭐")
            else:
                st.markdown("<h1 style='text-align: center; margin:0;'>🛸</h1>", unsafe_allow_html=True)
                st.warning(f"Halo Astronot {nama_terpilled}, kapalmu belum terdeteksi masuk stasiun.")
                if st.button("🚀 SAYA SIAP MELUNCUR HARI INI!", type="primary"):
                    waktu_wib = datetime.utcnow() + timedelta(hours=7)
                    
                    st.session_state.df_master.loc[idx_anak, "Status"] = "🚀 Sudah Mendarat"
                    st.session_state.df_master.loc[idx_anak, "Tanggal Presensi"] = waktu_wib.strftime("%d-%m-%Y")
                    st.session_state.df_master.loc[idx_anak, "Jam Presensi"] = waktu_wib.strftime("%H:%M:%S")
                    st.session_state.df_master.loc[idx_anak, "Total Hadir Sesi"] += 1
                    
                    simpan_data(st.session_state.df_master)
                    
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
        else:
            st.markdown("<h1 style='text-align: center; margin:0;'>🌍</h1>", unsafe_allow_html=True)
            st.info("Sistem navigasi siap. Silakan identifikasi dirimu terlebih dahulu di atas.")

# FRAME 2: PANEL GAME (KANAN)
with kolom_game:
    with st.container(border=True):
        st.subheader("🎮 Simulator Pelatihan Antariksa")
        
        status_absen_siswa = ""
        if nama_terpilled != "-- Pilih Astronot --":
            status_absen_siswa = st.session_state.df_master[(st.session_state.df_master["Kelas"] == kelas) & (st.session_state.df_master["Nama Siswa"] == nama_terpilled)]["Status"].values[0]
        
        if nama_terpilled == "-- Pilih Astronot --" or not ("🚀" in str(status_absen_siswa)):
            st.markdown("<h1 style='text-align: center; margin: 30px 0;'>🔒</h1>", unsafe_allow_html=True)
            st.info("Simulator Terkunci. Silakan **Siap Meluncur** di radar sebelah kiri untuk membuka kode akses!")
        else:
            idx_anak = st.session_state.df_master[(st.session_state.df_master["Kelas"] == kelas) & (st.session_state.df_master["Nama Siswa"] == nama_terpilled)].index[0]
            
            if st.session_state.umpan_balik_game == "benar":
                st.balloons()
                st.markdown("<h3 style='text-align: center; color: #66FCF1;'>🌟 KODE BENAR! +1 BINTANG GALAKSI</h3>", unsafe_allow_html=True)
                if st.button("☄️ LANJUTKAN MISI BERIKUTNYA", type="primary"):
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
            else:
                if st.session_state.game_aktif:
                    if st.button("🔄 GANTI KOORDINAT SOAL"):
                        st.session_state.game_aktif = get_game(kelas)
                        st.session_state.umpan_balik_game = None
                        st.rerun()
                
                if st.session_state.umpan_balik_game == "salah":
                    st.error("❌ Hitungan kurang tepat, roket meleset! Ayo coba lagi, Astronot!")

                if st.session_state.game_aktif:
                    visual, pertanyaan, opsi, jawaban_benar = st.session_state.game_aktif
                    
                    st.markdown(f'<div class="kotak-soal">{visual}</div>', unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align:center; font-weight:600; font-size:18px;">{pertanyaan}</p>', unsafe_allow_html=True)
                    
                    kol_opsi = st.columns(len(opsi))
                    for i, alternatif in enumerate(opsi):
                        with kol_opsi[i]:
                            if st.button(alternatif, key=f"btn_{alternatif}_{i}"):
                                if alternatif == jawaban_benar:
                                    st.session_state.df_master.loc[idx_anak, "Bintang"] += 1
                                    simpan_data(st.session_state.df_master)
                                    st.session_state.umpan_balik_game = "benar"
                                    st.rerun()
                                else:
                                    st.session_state.umpan_balik_game = "salah"
                                    st.rerun()
                else:
                    if st.button("🎲 MULAI SIMULASI", type="primary"):
                        st.session_state.game_aktif = get_game(kelas)
                        st.session_state.umpan_balik_game = None
                        st.rerun()

st.write("<br><br>", unsafe_allow_html=True)

# ==================== COMPONENT UTAMA: LOG & GRAFIK LAPORAN AKHIR ====================
st.write("---")
with st.container(border=True):
    st.markdown("<h2 style='margin-top:0;'>📊 Pusat Komando: Laporan Misi Kelas</h2>", unsafe_allow_html=True)
    
    total_siswa = len(st.session_state.df_master)
    total_hadir = len(st.session_state.df_master[st.session_state.df_master["Status"].str.contains("🚀", na=False)])
    total_belum = total_siswa - total_hadir
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"<div class='metric-card'>🧑‍🚀 <b>Kapasitas Kru Skuadron</b><br><span style='font-size:24px; font-weight:700; color:#66FCF1;'>{total_siswa} Kru</span></div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"<div class='metric-card'>🛸 <b>Roket Mendarat Hari Ini</b><br><span style='font-size:24px; font-weight:700; color:#45A29E;'>{total_hadir} Kapal</span></div>", unsafe_allow_html=True)
    with col_m3:
        persentase = round((total_hadir / total_siswa) * 100) if total_siswa > 0 else 0
        st.markdown(f"<div class='metric-card'>📈 <b>Keberhasilan Misi Kehadiran</b><br><span style='font-size:24px; font-weight:700; color:#F8E9A1;'>{persentase}%</span></div>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    
    pilih_log_kelas = st.radio("Pilih frekuensi sinyal skuadron:", ["Semua Skuadron", "KB", "TK A", "TK B"], horizontal=True, key="filter_laporan")
    df_filtered = st.session_state.df_master if pilih_log_kelas == "Semua Skuadron" else st.session_state.df_master[st.session_state.df_master["Kelas"] == pilih_log_kelas]

    # --- 1. SEKSI GRAFIK LINGKARAN (PIE CHART) ---
    st.markdown("### 🔭 Radar Proporsi Kehadiran Misi")
    
    hadir_filter = len(df_filtered[df_filtered["Status"].str.contains("🚀", na=False)])
    belum_filter = len(df_filtered) - hadir_filter
    
    if len(df_filtered) > 0:
        kol_grafik, kol_info_detail = st.columns([3, 2], gap="large")
        
        with kol_grafik:
            df_pie = pd.DataFrame({
                "Status Presensi": ["Sudah Mendarat (🚀)", "Belum Terdeteksi (❌)"],
                "Jumlah Anak": [hadir_filter, belum_filter]
            })
            
            fig = px.pie(
                df_pie, 
                values="Jumlah Anak", 
                names="Status Presensi",
                color="Status Presensi",
                color_discrete_map={"Sudah Mendarat (🚀)": "#45A29E", "Belum Terdeteksi (❌)": "#E27D60"},
                hole=0.4
            )
            
            # Ubah layout agar cocok dengan dark mode
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#C5C6C7"),
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with kol_info_detail:
            st.markdown("#### 📡 Detail Komunikasi Skuadron")
            persen_hadir = round((hadir_filter / len(df_filtered)) * 100) if len(df_filtered) > 0 else 0
            persen_belum = 100 - persen_hadir
            
            st.markdown(f"""
            * 🟢 **Terkoneksi ke Stasiun:** `{hadir_filter} Astronot` ({persen_hadir}%)
            * 🔴 **Belum Memasuki Orbit:** `{belum_filter} Astronot` ({persen_belum}%)
            * 🏢 **Kapasitas Skuadron Saat Ini:** `{len(df_filtered)} Astronot`
            
            ---
            💡 *Pesan Komando: Pantauan radar interaktif ini mempermudah Komandan Ms. Siska mengecek kru sebelum lepas landas menuju pelajaran.*
            """)
    else:
        st.info("ℹ️ Tidak ada sinyal data yang tersedia untuk skuadron ini.")

    # --- 2. SEKSI TABEL LOG AUDIT ---
    st.write("---")
    st.markdown("### 📋 Log Penerbangan (Riwayat Presensi)")
    
    df_tampilan_tabel = df_filtered.copy()
    df_tampilan_tabel["Bintang"] = df_tampilan_tabel["Bintang"].apply(lambda x: f"{x} ⭐")
    df_tampilan_tabel["Total Hadir Sesi"] = df_tampilan_tabel["Total Hadir Sesi"].apply(lambda x: f"{x} Misi")
    
    st.dataframe(
        df_tampilan_tabel[["Kelas", "Nama Siswa", "Status", "Tanggal Presensi", "Jam Presensi", "Bintang", "Total Hadir Sesi"]], 
        use_container_width=True, 
        hide_index=True
    )

    # --- FITUR ADMIN GURU (DENGAN TOMBOL RESET DATABASE TOTAL) ---
    st.write("---")
    with st.expander("⚙️ Konsol Kontrol Pusat (Ms. Siska)"):
        st.markdown("### 🔄 Sinkronisasi Orbit Sesi Baru")
        
        if st.button("🔄 Mulai Sesi Hari Baru (Reset Status Harian Saja)"):
            st.session_state.df_master["Status"] = "❌ Belum Mendarat"
            st.session_state.df_master["Tanggal Presensi"] = "-"
            st.session_state.df_master["Jam Presensi"] = "-"
            simpan_data(st.session_state.df_master)
            st.success("Sistem harian di-reset! Siklus rotasi bumi baru dimulai, data bintang kru tetap aman.")
            st.rerun()
            
        st.write("<br>", unsafe_allow_html=True)
        st.write("---")
        
        st.markdown("### ⚠️ Area Lubang Hitam (Blackhole / Reset Pabrik)")
        st.error("Perhatian: Tombol di bawah ini akan menghisap semua riwayat secara PERMANEN ke dalam Blackhole. Bintang galaksi dan total misi seluruh kru akan hangus menjadi 0.")
        
        konfirmasi_reset = st.checkbox("Saya mengotorisasi penghapusan seluruh data penerbangan (Bintang & Presensi kembali ke 0)")
        
        if st.button("🚨 FORMAT TOTAL SISTEM DATABASE", type="secondary"):
            if konfirmasi_reset:
                st.session_state.df_master = buat_database_baru()
                st.session_state.nama_aktif = "-- Pilih Astronot --"
                st.session_state.game_aktif = None
                st.session_state.umpan_balik_game = None
                st.success("💥 Ledakan Supernova! Seluruh database dan perolehan bintang telah diformat ulang.")
                st.rerun()
            else:
                st.warning("Silakan centang otorisasi di atas untuk membuka kunci protokol reset total!")
