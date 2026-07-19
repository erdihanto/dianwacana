import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# 1. Konfigurasi Halaman Browser
st.set_page_config(page_title="Dashboard Absensi Dian Wacana", page_icon="📊", layout="wide")

# 2. SUNTIKAN CSS UNTUK STYLE PREMIUM & PROFESIONAL
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    .header-kontainer {
        text-align: center;
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .judul-utama {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1E3A8A;
        font-size: 34px;
        font-weight: 800;
        margin: 0;
    }
    .sub-judul {
        color: #10B981;
        font-size: 14px;
        font-weight: 700;
        margin-top: 5px;
        letter-spacing: 1.5px;
    }
    .guru-mapel {
        color: #64748B;
        font-size: 15px;
        margin-top: 4px;
    }
    .stElementContainer div[data-testid="stVerticalBlockBorderContainer"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    .kotak-soal {
        text-align: center; 
        font-size: 60px; 
        background-color: #F1F5F9; 
        border: 1px solid #CBD5E1; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 15px;
    }
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
    .metric-card {
        background-color: #F1F5F9;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# --- KONFIGURASI FILE PENYIMPANAN DATA (DATABASE CSV) ---
DATA_FILE = "database_absensi_dian_wacana.csv"

# Daftar Master Siswa Tetap
MASTER_SISWA = {
    "KB": ["Adit", "Amari", "Levin", "Sienny", "Jesselyn", "Kenzou", "Ralf"],
    "TK A": ["Kenzie", "Brigitta", "Essy", "Felicia", "Geva", "Greesa", "Laras", "Liam"],
    "TK B": ["Aileen", "Agatha", "Daniel", "Sean", "Elvano", "Betha", "Hiro"]
}

# Fungsi Membuat Data Awal dari Nol
def buat_database_baru():
    rows = []
    for kelas, daftar_nama in MASTER_SISWA.items():
        for nama in daftar_nama:
            rows.append({
                "Kelas": kelas,
                "Nama Siswa": nama,
                "Status": "❌ Belum Absen",
                "Tanggal Presensi": "-",
                "Jam Presensi": "-",
                "Bintang": 0,
                "Total Hadir Sesi": 0
            })
    df_awal = pd.DataFrame(rows)
    df_awal.to_csv(DATA_FILE, index=False)
    return df_awal

# Fungsi Memuat Data dari CSV
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

# Fungsi Menyimpan Perubahan Data Kembali ke CSV
def simpan_data(df):
    df.to_csv(DATA_FILE, index=False)

# Memuat data secara persisten ke dalam session_state agar sinkron dengan Streamlit
if 'df_master' not in st.session_state:
    st.session_state.df_master = muat_data()

if 'nama_aktif' not in st.session_state:
    st.session_state.nama_aktif = "-- Pilih Nama --"

if 'game_aktif' not in st.session_state:
    st.session_state.game_aktif = None

if 'umpan_balik_game' not in st.session_state:
    st.session_state.umpan_balik_game = None

# --- GENERATOR SOAL OTOMATIS ---
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

# GRID UTAMA: Panel Input & Game
kolom_absen, kolom_game = st.columns(2, gap="large")

# FRAME 1: PANEL ABSENSI (KIRI)
with kolom_absen:
    with st.container(border=True):
        st.subheader("📋 Bingkai Absensi Siswa")
        
        if 'kelas_lama' not in st.session_state:
            st.session_state.kelas_lama = "KB"
        
        kelas = st.selectbox("1. Pilih Kelas Kelompok:", ["KB", "TK A", "TK B"])
        
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
                label_tampilan = f"✅ {nama} (Sudah Hadir)"
            else:
                label_tampilan = nama
            
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
                st.success(f"Selamat Datang, {nama_terpilled}! Masuk tanggal {tgl_absen} pukul {jam_absen}. Bintangmu: {bintang} ⭐")
            else:
                st.markdown("<h1 style='text-align: center; margin:0;'>😊</h1>", unsafe_allow_html=True)
                st.warning(f"Halo {nama_terpilled}, kamu belum mengonfirmasi kehadiran.")
                if st.button("✋ SAYA HADIR HARI INI!", type="primary"):
                    sekarang = datetime.now()
                    
                    st.session_state.df_master.loc[idx_anak, "Status"] = "✅ Hadir"
                    st.session_state.df_master.loc[idx_anak, "Tanggal Presensi"] = sekarang.strftime("%d-%m-%Y")
                    st.session_state.df_master.loc[idx_anak, "Jam Presensi"] = sekarang.strftime("%H:%M:%S")
                    st.session_state.df_master.loc[idx_anak, "Total Hadir Sesi"] += 1
                    
                    simpan_data(st.session_state.df_master)
                    
                    st.session_state.game_aktif = get_game(kelas)
                    st.session_state.umpan_balik_game = None
                    st.rerun()
        else:
            st.markdown("<h1 style='text-align: center; margin:0;'>👋</h1>", unsafe_allow_html=True)
            st.info("Silakan tentukan nama kamu di atas terlebih dahulu.")

# FRAME 2: PANEL GAME (KANAN)
with kolom_game:
    with st.container(border=True):
        st.subheader("🎮 Bingkai Tantangan Game")
        
        status_absen_siswa = ""
        if nama_terpilled != "-- Pilih Nama --":
            status_absen_siswa = st.session_state.df_master[(st.session_state.df_master["Kelas"] == kelas) & (st.session_state.df_master["Nama Siswa"] == nama_terpilled)]["Status"].values[0]
        
        if nama_terpilled == "-- Pilih Nama --" or not ("✅" in str(status_absen_siswa)):
            st.markdown("<h1 style='text-align: center; margin: 30px 0;'>🔒</h1>", unsafe_allow_html=True)
            st.info("Game Terkunci. Silakan lakukan **Absen Hadir** di frame sebelah kiri untuk membukanya!")
        else:
            idx_anak = st.session_state.df_master[(st.session_state.df_master["Kelas"] == kelas) & (st.session_state.df_master["Nama Siswa"] == nama_terpilled)].index[0]
            
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
                    
                    st.markdown(f'<div class="kotak-soal">{visual}</div>', unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align:center; font-weight:600;">{pertanyaan}</p>', unsafe_allow_html=True)
                    
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
                    if st.button("🎲 MULAI BERMAIN", type="primary"):
                        st.session_state.game_aktif = get_game(kelas)
                        st.session_state.umpan_balik_game = None
                        st.rerun()

st.write("<br><br>", unsafe_allow_html=True)

# ==================== COMPONENT UTAMA: LOG & GRAFIK LAPORAN AKHIR ====================
st.write("---")
with st.container(border=True):
    st.markdown("<h2 style='color:#1E3A8A; margin-top:0;'>📊 Papan Analisis & Laporan Kelas Modern</h2>", unsafe_allow_html=True)
    
    total_siswa = len(st.session_state.df_master)
    total_hadir = len(st.session_state.df_master[st.session_state.df_master["Status"].str.contains("✅", na=False)])
    total_belum = total_siswa - total_hadir
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"<div class='metric-card'>🔑 <b>Total Siswa Terdaftar</b><br><span style='font-size:24px; font-weight:700;'>{total_siswa} Anak</span></div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"<div class='metric-card'>📈 <b>Total Hadir Hari Ini</b><br><span style='font-size:24px; font-weight:700; color:#10B981;'>{total_hadir} Anak</span></div>", unsafe_allow_html=True)
    with col_m3:
        persentase = round((total_hadir / total_siswa) * 100) if total_siswa > 0 else 0
        st.markdown(f"<div class='metric-card'>🎯 <b>Rasio Kehadiran Kelas</b><br><span style='font-size:24px; font-weight:700; color:#3B82F6;'>{persentase}%</span></div>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    
    pilih_log_kelas = st.radio("Pilih filter laporan kelompok kelas:", ["Semua Kelas", "KB", "TK A", "TK B"], horizontal=True, key="filter_laporan")
    df_filtered = st.session_state.df_master if pilih_log_kelas == "Semua Kelas" else st.session_state.df_master[st.session_state.df_master["Kelas"] == pilih_log_kelas]

    # --- 1. SEKSI GRAFIK LINGKARAN (PIE CHART) ---
    st.markdown("### 🎯 Grafik Proporsi Status Kehadiran Siswa")
    
    hadir_filter = len(df_filtered[df_filtered["Status"].str.contains("✅", na=False)])
    belum_filter = len(df_filtered) - hadir_filter
    
    if len(df_filtered) > 0:
        kol_grafik, kol_info_detail = st.columns([3, 2], gap="large")
        
        with kol_grafik:
            df_pie = pd.DataFrame({
                "Status Presensi": ["Sudah Hadir (✅)", "Belum Absen (❌)"],
                "Jumlah Anak": [hadir_filter, belum_filter]
            })
            
            fig = px.pie(
                df_pie, 
                values="Jumlah Anak", 
                names="Status Presensi",
                color="Status Presensi",
                color_discrete_map={"Sudah Hadir (✅)": "#10B981", "Belum Absen (❌)": "#EF4444"},
                hole=0.4
            )
            
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with kol_info_detail:
            st.markdown("#### 📝 Detail Status Eksekutif")
            persen_hadir = round((hadir_filter / len(df_filtered)) * 100) if len(df_filtered) > 0 else 0
            persen_belum = 100 - persen_hadir
            
            st.markdown(f"""
            * 🟢 **Sudah Mengonfirmasi Hadir:** `{hadir_filter} Anak` ({persen_hadir}%)
            * 🔴 **Belum Mengonfirmasi/Absen:** `{belum_filter} Anak` ({persen_belum}%)
            * 🏢 **Total Kapasitas Kelas Terfilter:** `{len(df_filtered)} Anak`
            
            ---
            💡 *Pemberitahuan: Grafik interaktif ini membantu Ms. Siska memantau rasio kedatangan kelas secara cepat sebelum aktivitas belajar mengajar dimulai.*
            """)
    else:
        st.info("ℹ️ Tidak ada data yang tersedia untuk filter kelas ini.")

    # --- 2. SEKSI TABEL LOG AUDIT ---
    st.write("---")
    st.markdown("### 📋 Tabel Log Riwayat Audit Presensi Resmi")
    
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
    with st.expander("⚙️ Menu Admin Guru (Ms. Siska)"):
        st.markdown("### 🔄 Kontrol Sembuh & Siklus Sesi")
        
        if st.button("🔄 Mulai Sesi Hari Baru (Reset Status Harian Saja)"):
            st.session_state.df_master["Status"] = "❌ Belum Absen"
            st.session_state.df_master["Tanggal Presensi"] = "-"
            st.session_state.df_master["Jam Presensi"] = "-"
            simpan_data(st.session_state.df_master)
            st.success("Sesi harian berhasil di-reset! Besok anak-anak bisa absen ulang, rekam data lama aman.")
            st.rerun()
            
        st.write("<br>", unsafe_allow_html=True)
        st.write("---")
        
        st.markdown("### ⚠️ Area Bahaya (Reset Pabrik)")
        st.error("Perhatian: Tombol di bawah ini akan menghapus semua riwayat secara PERMANEN. Bintang dan total hari masuk seluruh siswa akan kembali menjadi 0.")
        
        konfirmasi_reset = st.checkbox("Saya benar-benar ingin mengosongkan seluruh database (Bintang & Absen kembali ke 0)")
        
        if st.button("🚨 RESET TOTAL DATA DATABASE (Kembali ke Nol)", type="secondary"):
            if konfirmasi_reset:
                st.session_state.df_master = buat_database_baru()
                st.session_state.nama_aktif = "-- Pilih Nama --"
                st.session_state.game_aktif = None
                st.session_state.umpan_balik_game = None
                st.success("💥 Sukses! Seluruh database absensi dan perolehan bintang telah dibersihkan kembali ke pengaturan awal.")
                st.rerun()
            else:
                st.warning("Silakan centang kotak konfirmasi di atas terlebih dahulu untuk membuka kunci tombol reset total!")
