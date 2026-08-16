import streamlit as st
from google import genai
import tempfile
import os

# Konfigurasi Tampilan Halaman
st.set_page_config(
    page_title="Lesa Snack - Sumpia Content Creator",
    page_icon="🍤",
    layout="wide"
)

# Ambil API Key dari Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Custom CSS Dashboard Modern
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA !important;
    }
    
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
            <div class="card-desc">Deteksi otomatis timestamp dari setiap video yang diunggah untuk dipotong di CapCut.</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">🎙️</div>
            <div class="card-title">Voice Over Script</div>
            <div class="card-desc">Skrip 10-15 detik berstruktur Hook, Isi & CTA, siap dibaca ElevenLabs.</div>
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

# Area Upload Video
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
                file_names = []
                try:
                    for file in uploaded_files:
                        file_names.append(file.name)
                        suffix = f".{file.name.split('.')[-1]}"
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                            tmp_file.write(file.read())
                            tmp_path = tmp_file.name
                        
                        g_file = client.files.upload(file=tmp_path)
                        gemini_files.append(g_file)
                        os.remove(tmp_path)

                    daftar_file_str = ", ".join(file_names)
                    total_file = len(file_names)

                    prompt = f"""
                    Kamu adalah Content Strategist & Copywriter profesional kuliner snack UMKM Indonesia.
                    Pengguna telah mengunggah persis {total_file} file video dengan daftar nama file berikut:
                    {daftar_file_str}

                    Tugasmu adalah menganalisa SEMUA video tersebut dan menyusun panduan konten TikTok:

                    1. **Panduan Potongan Video (CapCut Guide)**:
                       - ATURAN MUTLAK: Kamu WAJIB mengambil minimal 1 potongan klip (durasi 2-3 detik) dari SETIAP file yang diunggah ({daftar_file_str}). TIDAK BOLEH ada file video yang dilewati atau diabaikan!
                       - Urutkan videonya berdasarkan alur bercerita yang logis:
                         * Video untuk Hook (misal adegan renyah / mematahkan sumpia).
                         * Video untuk Isi (detail kemasan, butiran sumpia, atau tekstur isian udang).
                         * Video untuk CTA (stok melimpah / kemasan siap kirim).
                       - Tuliskan nama file asli yang jelas di setiap baris potongan klip beserta timestamp-nya.
                       - Total durasi gabungan seluruh potongan klip harus berkisar 10 - 15 detik.

                    2. **Skrip Voice Over (ElevenLabs Ready)**:
                       - Panjang naskah WAJIB antara 25 - 35 kata (disesuaikan dengan total durasi visual gabungan).
                       - Target: Ibu-ibu / penyuka camilan gurih renyah.
                       - Alur kalimat:
                         * [Hook]: 1 kalimat menarik perhatian di detik pertama.
                         * [Isi]: 1-2 kalimat rasa gurih renyah udang sumpia Lesa Snack.
                         * [CTA]: 1 kalimat ajakan beli di keranjang kuning.
                       - Tulis teks polos tanpa embel-embel label agar langsung siap dibaca mesin ElevenLabs.

                    3. **Caption TikTok & Hashtags**:
                       - Hook, detail produk, ajakan transaksi keranjang kuning, serta 5-8 hashtag kuliner viral.

                    Format Output:
                    ---
                    ### ✂️ 1. Panduan Potongan Video (CapCut)
                    (Tuliskan daftar potongan untuk ke-{total_file} video yang diunggah secara urut)
                    * Klip 1 (Hook) - [Nama_File_Asli]: [00:0X - 00:0Y] -> (Keterangan Visual)
                    * Klip 2 (Isi) - [Nama_File_Asli]: [00:0X - 00:0Y] -> (Keterangan Visual)
                    ...dst hingga semua file terpakai.
                    *(Total Durasi Gabungan: XX Detik)*

                    ---
                    ### 🎙️ 2. Skrip Voice Over (ElevenLabs Ready)
                    *(Estimasi: XX Detik / XX Kata)*
                    (Tulis naskah VO di sini)

                    ---
                    ### 📱 3. Caption TikTok & Hashtags
                    (Tulis caption lengkap di sini)
                    """

                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[*gemini_files, prompt]
                    )

                    st.success("✨ Konten Berhasil Dibuat!")
                    with st.container(border=True):
                        st.markdown(response.text)

                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses konten: {e}")

                finally:
                    for gf in gemini_files:
                        try:
                            client.files.delete(name=gf.name)
                        except Exception:
                            pass
