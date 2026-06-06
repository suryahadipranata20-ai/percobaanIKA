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

# CSS Custom (Hanya untuk elemen dasar)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; color: #333; }
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 5px solid #2E8B57;
    }
    .custom-card-blue { border-left: 5px solid #1E90FF; }
    h1, h2, h3 { color: #2E8B57; }
    [data-testid="stMetricValue"] { font-size: 1.5rem; }
    .stButton>button { background-color: #2E8B57; color: white; border-radius: 8px; border: none; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# NAVIGASI SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.title("🌊 EcoSurface")
st.sidebar.markdown("### Sistem Pendukung Pemantauan Kualitas Air")
st.sidebar.markdown("---")

menu_options = ["🏠 Beranda", "🧪 Panduan Sampling", "📊 Evaluasi Baku Mutu", "ℹ️ Tentang Aplikasi"]
selection = st.sidebar.radio("Navigasi Menu:", menu_options)

# -----------------------------------------------------------------------------
# 1. HALAMAN BERANDA
# -----------------------------------------------------------------------------
if selection == "🏠 Beranda":
    st.title("🌊 EcoSurface")
    st.markdown("## Sistem Pendukung Pemantauan Kualitas Air Permukaan")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📋 Parameter Sampling", value=len(sampling_data), delta="Tersedia")
    with col2:
        st.metric(label="⚖️ Baku Mutu", value=len(baku_mutu), delta="Regulasi")
    with col3:
        st.metric(label="📈 Fiturnya", value="2", delta="Utama")
    
    st.markdown("---")
    st.markdown("""
    ### 👋 Selamat Datang di EcoSurface!
    Aplikasi ini membantu mahasiswa dan praktisi lingkungan dalam:
    1. **Panduan Sampling** - Menentukan metode pengawetan, volume, dan wadah.
    2. **Evaluasi Baku Mutu** - Membandingkan hasil analisis dengan standar regulasi.
    """)
    with st.expander("ℹ️ Cara Menggunakan Aplikasi"):
        st.write("Pilih menu di sidebar untuk memulai.")

# -----------------------------------------------------------------------------
# 2. HALAMAN PANDUAN SAMPLING
# -----------------------------------------------------------------------------
elif selection == "🧪 Panduan Sampling":
    st.title("🧪 Panduan Sampling Air Permukaan")
    st.markdown("Pilih parameter untuk melihat prosedur teknis.")
    st.markdown("---")

    list_param = sorted(sampling_data.keys())
    param_choice = st.selectbox("Pilih Parameter:", list_param)

    if param_choice:
        data = sampling_data[param_choice]
        c1, c2 = st.columns([1, 3])
        
        with c1:
            st.markdown(f"### 🔬 {param_choice}")
            st.metric("Volume Minimal", data['volume'])
        
        with c2:
            # Card menggunakan HTML sederhana
            st.markdown(f"""
            <div class="custom-card">
                <h4>📦 Detail Pengawasan</h4>
                <p><b>🫙 Jenis Wadah:</b> {data['wadah']}</p>
                <p><b>🧪 Bahan Pengawet:</b> {data['pengawet']}</p>
                <p><b>❄️ Suhu Penyimpanan:</b> {data['penyimpanan']}</p>
                <p><b>⏳ Holding Time:</b> {data['holding_time']}</p>
                <p><b>📝 Catatan:</b> <i>{data['catatan']}</i></p>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. HALAMAN EVALUASI BAKU MUTU (PAKAI NATIVE COMPONENTS - LEBIH STABIL)
# -----------------------------------------------------------------------------
elif selection == "📊 Evaluasi Baku Mutu":
    st.title("📊 Evaluasi Baku Mutu Kualitas Air")
    st.markdown("Input hasil analisis dan bandingkan dengan standar.")
    st.markdown("---")

    list_baku_mutu = list(baku_mutu.keys())
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        selected_param = st.selectbox("Pilih Parameter", list_baku_mutu)
    with col_input2:
        input_value = st.number_input(f"Masukkan Nilai {selected_param}", min_value=0.0, value=0.0, step=0.01, format="%.3f")

    standar = baku_mutu.get(selected_param, 0)
    st.markdown("---")
    
    if selected_param == "DO":
        status_ok = input_value >= standar
        operator_symbol = "≥"
    else:
        status_ok = input_value <= standar
        operator_symbol = "≤"
    
    selisih = abs(input_value - standar)
    
    # === LINE 191: GUNAKAN ST.SUCCESS & ST.ERROR (NATIVE) ===
    if status_ok:
        st.success(f"✅ MEMENUHI BAKU MUTU | Nilai {input_value} {operator_symbol} Standar {standar}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Hasil Analisis", f"{input_value}")
        m2.metric("Baku Mutu", f"{standar}")
        m3.metric("Selisih", f"{selisih} (Aman)")
    else:
        st.error(f"❌ TIDAK MEMENUHI BAKU MUTU | Nilai {input_value} {operator_symbol} Standar {standar}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Hasil Analisis", f"{input_value}", delta_color="inverse")
        m2.metric("Baku Mutu", f"{standar}")
        m3.metric("Selisih", f"+{selisih} (Melebihi)")

    st.info(f"📌 Catatan: Parameter {selected_param} menggunakan standar = {standar}")

# -----------------------------------------------------------------------------
# 4. TENTANG APLIKASI
# -----------------------------------------------------------------------------
elif selection == "ℹ️ Tentang Aplikasi":
    st.title("ℹ️ Tentang EcoSurface")
    st.markdown("---")
    st.markdown("""
    <div class="custom-card">
        <h2>🌊 EcoSurface v1.0</h2>
        <p><b>Sistem Pendukung Pemantauan Kualitas Air Permukaan</b></p>
        <br>
        <p><b>Nama Aplikasi:</b> EcoSurface</p>
        <p><b>Versi:</b> 1.0</p>
        <p><b>Developer:</b> Mahasiswa Politeknik AKA Bogor</p>
        <p><b>Teknologi:</b> Python & Streamlit</p>
        <h4>Deskripsi</h4>
        <p>Aplikasi pendukung pemantauan kualitas air permukaan dengan panduan sampling dan evaluasi hasil analisis.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.success("Terima kasih telah menggunakan EcoSurface! 💧")
