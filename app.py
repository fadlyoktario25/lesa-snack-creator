import streamlit as st
import google.generativeai as genai
import tempfile
import os

# Konfigurasi API Key Otomatis
API_KEY = "AIzaSyC17rq62C_H_9tViAzWXvGbLu6wkcVzOyo"
genai.configure(api_key=API_KEY)

# Konfigurasi Tampilan Halaman
st.set_page_config(
    page_title="Lesa Snack - Sumpia Content Creator",
    page_icon="🍤",
    layout="wide"
)

# Custom CSS Anti-Teks Putih (Memaksa semua elemen berwarna gelap yang jelas)
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA !important;
    }
    
    /* Paksa semua teks, heading, list, dan paragraf menjadi gelap */
    .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #1E293B !important;
    }

    .main-header {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    .main-title {
        font-size: 36px;
        font-weight: 800;
        color: #0F172A !important;
        letter-spacing: -0.5px;
    }
    .main-subtitle {
        font-size: 15px;
        color: #64748B !important;
        margin-top: -5px;
        margin-bottom: 25px;
    }
    .feature-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        height: 100%;
    }
    .icon-box { font-size: 26px; margin-bottom: 8px; }
    .card-title { font-size: 17px; font-weight: 700; color: #0F172A !important; margin-bottom: 4px; }
    .card-desc { font-size: 13px; color: #64748B !important; line-height: 1.4; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <div class="main-title">Lesa Snack Content Creator 🍤</div>
        <div class="main-subtitle">Platform Asisten Konten Sumpia Udang Serba Otomatis Bertenaga Gemini AI</div>
    </div>
""", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">✂️</div>
            <div class="card-title">CapCut Cut Guide</div>
            <div class="card-desc">Deteksi otomatis timestamp paling estetik & renyah dari 5 video untuk dipotong di CapCut.</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">🎙️</div>
            <div class="card-title">Voice Over Script</div>
            <div class="card-desc">Skrip naskah ramah khas ibu-ibu, natural & siap di-convert ke ElevenLabs.</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">📱</div>
            <div class="card-title">TikTok Caption</div>
            <div class="card-desc">Caption menggugah selera lengkap dengan hook, CTA penjualan, dan hashtag viral.</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Area Upload Langsung Tampil
st.markdown("### 📤 Upload Video Sumpia Udang")
uploaded_files = st.file_uploader(
    "Pilih hingga 5 video (.mp4, .mov, .avi):", 
    type=["mp4", "mov", "avi"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.error("⚠️ Maksimal 5 video saja ya!")
    else:
        if st.button("🚀 Process & Generate Content", use_container_width=True, type="primary"):
            with st.spinner("Sedang menganalisa visual video, membuat skrip, dan meracik caption..."):
                gemini_files = []
                try:
                    for file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                            tmp_file.write(file.read())
                            tmp_path = tmp_file.name
                        
                        g_file = genai.upload_file(tmp_path)
                        gemini_files.append(g_file)
                        os.remove(tmp_path)

                    prompt = """
                Kamu adalah Content Strategist & Copywriter profesional kuliner snack UMKM Indonesia.
                Tugasmu adalah menganalisa klip-klip video Sumpia Udang dari Lesa Snack dan membuat konsep video TikTok berdurasi ideal 10-15 detik.

                Hasilkan 3 komponen konten utama:

                1. **Panduan Potongan Video (CapCut Guide)**:
                   - Susun potongan klip menjadi total durasi 10 - 15 detik (rata-rata 2-3 detik per potongan adegan).
                   - Klip 1: Hook visual (adegan mematahkan sumpia / visual renyah paling menarik).
                   - Klip 2 & 3: Isi (detail isian udang, tekstur, atau tangan mengambil camilan).
                   - Klip 4 / 5: Call to Action (kemasan rapi atau stok melimpah siap kirim).
                   - Tuliskan timestamp dan total durasinya.

                2. **Skrip Voice Over (ElevenLabs Ready)**:
                   - Panjang skrip WAJIB antara 25 - 35 kata (pas untuk durasi bicara 10-15 detik).
                   - Target: Ibu-ibu / penyuka camilan gurih renyah.
                   - Struktur kalimat wajib:
                     * [Hook]: 1 kalimat pemancing rasa penasaran di awal.
                     * [Isi]: 1-2 kalimat deskripsi gurih, krispi, dan nikmatnya udang sumpia Lesa Snack.
                     * [CTA]: 1 kalimat ajakan pesan/checkout di keranjang kuning mumpung ready.
                   - Format tulisan polos tanpa tanda kurung [Hook]/[Isi] agar langsung siap dibaca ElevenLabs.

                3. **Caption TikTok & Hashtags**:
                   - Hook baris pertama, detail singkat produk, CTA, dan 5-8 hashtag kuliner viral.

                Format Output:
                ---
                ### ✂️ 1. Panduan Potongan Video (CapCut)
                * Klip 1 (Hook): [00:0X - 00:0Y] -> ...
                * Klip 2 (Isi): [00:0X - 00:0Y] -> ...
                * Klip 3 (Isi): [00:0X - 00:0Y] -> ...
                * Klip 4 (CTA): [00:0X - 00:0Y] -> ...
                *(Total Durasi: XX detik)*

                ---
                ### 🎙️ 2. Skrip Voice Over (ElevenLabs Ready)
                *(Estimasi: XX detik / XX kata)*
                (Tuliskan teks naskah langsung di sini)

                ---
                ### 📱 3. Caption TikTok & Hashtags
                (Tuliskan caption lengkap di sini)
                """
                    model = genai.GenerativeModel('models/gemini-3.7-flash')
                    response = model.generate_content([*gemini_files, prompt])

                    st.success("✨ Konten Berhasil Dibuat!")
                    
                    # Box Container Bawaan Streamlit (Aman dari Bug CSS)
                    with st.container(border=True):
                        st.markdown(response.text)

                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses konten: {e}")

                finally:
                    for gf in gemini_files:
                        try:
                            genai.delete_file(gf.name)
                        except Exception:
                            pass