# app.py
import streamlit as st
from parameter_data import sampling_data, baku_mutu

# -----------------------------------------------------------------------------
# KONFIGURASI HALAMAN & CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EcoSurface - Pemantau Kualitas Air",
    page_icon="💧",
    layout="wide"
)

# CSS Custom untuk Tampilan Modern
st.markdown("""
    <style>
    /* Import Font Google */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Pengaturan Font Global */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        color: #333;
    }

    /* Custom Card Style */
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 5px solid #2E8B57; /* Green Accent */
    }

    .custom-card-blue {
        border-left: 5px solid #1E90FF; /* Blue Accent */
    }
    
    .custom-card-red {
        border-left: 5px solid #FF6B6B;
    }

    /* Headers */
    h1, h2, h3 {
        color: #2E8B57;
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #F0F8FF;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #2E8B57;
        color: white;
        border-radius: 8px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# NAVIGASI SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.title("🌊 EcoSurface")
st.sidebar.markdown("### Sistem Pendukung Pemantauan Kualitas Air")
st.sidebar.markdown("---")

menu_options = [
    "🏠 Beranda", 
    "🧪 Panduan Sampling", 
    "📊 Evaluasi Baku Mutu", 
    "ℹ️ Tentang Aplikasi"
]
selection = st.sidebar.radio("Navigasi Menu:", menu_options)

# -----------------------------------------------------------------------------
# 1. HALAMAN BERANDA
# -----------------------------------------------------------------------------
if selection == "🏠 Beranda":
    st.title("🌊 EcoSurface")
    st.markdown("## Sistem Pendukung Pemantauan Kualitas Air Permukaan")
    st.markdown("---")
    
    # Dashboard Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📋 Parameter Sampling",
            value=len(sampling_data),
            delta="Tersedia"
        )
    with col2:
        st.metric(
            label="⚖️ Baku Mutu",
            value=len(baku_mutu),
            delta="Regulasi"
        )
    with col3:
        st.metric(
            label="📈 Fiturnya",
            value="2",
            delta="Utama"
        )
    
    st.markdown("---")
    st.markdown("""
    ### 👋 Selamat Datang di EcoSurface!
    
    Aplikasi ini dibuat untuk membantu mahasiswa dan praktisi lingkungan dalam melakukan:
    1. **Panduan Sampling** : Menentukan metode pengawetan, volume, dan wadah yang tepat.
    2. **Evaluasi Baku Mutu** : Membandingkan hasil analisis dengan standar yang berlaku.
    
    Silakan pilih menu di sidebar untuk memulai.
    """)
    
    # Container Informasi tambahan
    with st.expander("ℹ️ Cara Menggunakan Aplikasi"):
        st.write("""
        1. Pilih menu **Panduan Sampling** untuk melihat detail teknis pengambilan sampel.
        2. Pilih menu **Evaluasi Baku Mutu** untuk menginput hasil lab dan cek kepatuhan.
        3. Aplikasi ini dirancang untuk pembelajaran dan literasi lingkungan.
        """)

# -----------------------------------------------------------------------------
# 2. HALAMAN PANDUAN SAMPLING
# -----------------------------------------------------------------------------
elif selection == "🧪 Panduan Sampling":
    st.title("🧪 Panduan Sampling Air Permukaan")
    st.markdown("Pilih parameter untuk melihat prosedur teknis pengambilan dan pengawetan sampel.")
    st.markdown("---")

    # Selectbox Parameters
    list_param = sorted(sampling_data.keys())
    param_choice = st.selectbox("Pilih Parameter:", list_param)

    if param_choice:
        data = sampling_data[param_choice]
        
        # Layout 2 Kolom
        c1, c2 = st.columns([1, 3])
        
        with c1:
            st.markdown(f"### 🔬 {param_choice}")
            st.metric("Volume Minimal", data['volume'])
        
        with c2:
            # Tampilkan Detail dalam Card
            st.markdown(f"""
            <div class="custom-card">
                <h4>📦 Detail Pengawasan</h4>
                <table style="width:100%;">
                    <tr>
                        <td><b>🫙 Jenis Wadah</b></td>
                        <td>:</td>
                        <td>{data['wadah']}</td>
                    </tr>
                    <tr>
                        <td><b>🧪 Bahan Pengawet</b></td>
                        <td>:</td>
                        <td>{data['pengawet']}</td>
                    </tr>
                    <tr>
                        <td><b>❄️ Suhu Penyimpanan</b></td>
                        <td>:</td>
                        <td>{data['penyimpanan']}</td>
                    </tr>
                    <tr>
                        <td><b>⏳ Holding Time</b></td>
                        <td>:</td>
                        <td>{data['holding_time']}</td>
                    </tr>
                </table>
                <br>
                <p><b>📝 Catatan:</b> <i>{data['catatan']}</i></p>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. HALAMAN EVALUASI BAKU MUTU
# -----------------------------------------------------------------------------
elif selection == "📊 Evaluasi Baku Mutu":
    st.title("📊 Evaluasi Baku Mutu Kualitas Air")
    st.markdown("-input hasil analisis dan bandingkan dengan standar regulasi.")
    st.markdown("---")

    # Filter parameter yang memiliki baku mutu (exclude Suhu/pH khusus jika perlu, tapi kita gunakan semua yang ada di dict)
    list_baku_mutu = list(baku_mutu.keys())
    
    # Layout Input
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        selected_param = st.selectbox("Pilih Parameter", list_baku_mutu)
    
    with col_input2:
        # Input nilai, tentikan float
        input_value = st.number_input(
            f"Masukkan Nilai {selected_param}", 
            min_value=0.0, 
            value=0.0, 
            step=0.01,
            format="%.3f"
        )

    # AMBIL NILAI BAKU MUTU
    standar = baku_mutu.get(selected_param, 0)
    
    st.markdown("---")
    
    # LOGIKA EVALUASI
    # Jika parameter DO, logikanya Minimum (>=), selebihnya Maximum (<=)
    
    if selected_param == "DO":
        # Logika DO: Harus >= Standar
        status_ok = input_value >= standar
        operator_symbol = "≥"
    else:
        # Logika Umum: Harus <= Standar (Tidak melebihi)
        status_ok = input_value <= standar
        operator_symbol = "≤"
    
    # Hitung Selisih
    selisih = abs(input_value - standar)
    
    # TAMPILKAN HASIL
    if status_ok:
        # Tampilan MEMENUHI (Hijau)
        st.markdown(f"""
        <div class="custom-card" style="border-left-color: #2E8B57;">
            <h2 style="color: #2E8B57; text-align: center;">✅ MEMENUHI BAKU MUTU</h2>
            <p style="text-align: center;">Nilai analisis <b>{input_value}</b> {operator_symbol} Standar <b>{standar}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detail metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Hasil Analisis", f"{input_value}")
        m2.metric("Baku Mutu", f"{standar}")
        m3.metric("Selisih", f"{selisih} (Aman)")
        
    else:
        # Tampilan TIDAK MEMENUHI (Merah)
        st.markdown(f"""
        <div class="custom-card custom-card-red" style="border-left-color: #FF6B6B;">
            <h2 style="color: #FF6B6B; text-align: center;">❌ TIDAK MEMENUHI BAKU MUTU</h2>
            <p style="text-align: center;">Nilai analisis <b>{input_value}</b> {operator_symbol} Standar <b>{standar}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detail metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Hasil Analisis", f"{input_value}", delta_color="inverse")
        m2.metric("Baku Mutu", f"{standar}")
        m3.metric("Selisih", f"+{selisih} (Melebihi)", delta="over_limit")

    # Catatan bawah
    st.info(f"""
    📌 Catatan Logika:
    - Parameter <b>{selected_param}</b> menggunakan acuan baku mutu = **{standar}**.
    - Status "Memenuhi"意味着 nilai tidak melampaui (atau tidak lebih rendah untuk DO) baku mutu.
    """)

# -----------------------------------------------------------------------------
# 4. TENTANG APLIKASI
# -----------------------------------------------------------------------------
elif selection == "ℹ️ Tentang Aplikasi":
    st.title("ℹ️ Tentang EcoSurface")
    st.markdown("---")
    
    st.markdown("""
    <div class="custom-card custom-card-blue">
        <h2>🌊 EcoSurface v1.0</h2>
        <p><b>Sistem Pendukung Pemantauan Kualitas Air Permukaan</b></p>
        <br>
        <table>
            <tr>
                <td><b>Nama Aplikasi</b></td>
                <td>:</td>
                <td>EcoSurface</td>
            </tr>
            <tr>
                <td><b>Versi</b></td>
                <td>:</td>
                <td>1.0</td>
            </tr>
            <tr>
                <td><b>Developer</b></td>
                <td>:</td>
                <td>Mahasiswa Politeknik AKA Bogor</td>
            </tr>
            <tr>
                <td><b>Teknologi</b></td>
                <td>:</td>
                <td>Python & Streamlit</td>
            </tr>
        </table>
        <br>
        <h4>Deskripsi</h4>
        <p>Aplikasi ini kedepankan kegiatan pemantauan kualitas air permukaan dengan menyediakan panduan sampling (metode pengawetan, wadah, holding time) dan evaluasi hasil analisis berdasarkan baku mutuair yang berlaku (PerMenLH No. 5 Tahun 2014).</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.success("Terima kasih telah menggunakan EcoSurface! 💧")
