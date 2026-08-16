import streamlit as st
from google import genai
import tempfile
import os
import time

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
        font-size: 34px;
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
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        height: 100%;
    }
    .icon-box { font-size: 24px; margin-bottom: 6px; }
    .card-title { font-size: 16px; font-weight: 700; color: #0F172A !important; margin-bottom: 4px; }
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
            <div class="card-title">CapCut Visual Guide</div>
            <div class="card-desc">Panduan potongan video dengan ciri visual thumbnail agar mudah dicari di galeri iPhone.</div>
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
        # Menampilkan Preview Video yang diupload
        st.markdown("#### 🎬 Preview Video Terpilih:")
        cols = st.columns(len(uploaded_files))
        for i, file in enumerate(uploaded_files):
            with cols[i]:
                st.caption(f"**Video {i+1}** ({file.name})")
                st.video(file)

        st.write("")
        if st.button("🚀 Process & Generate Content", use_container_width=True, type="primary"):
            with st.spinner("Sedang menganalisa visual video, membuat skrip, dan meracik caption..."):
                gemini_files = []
                file_info_list = []
                try:
                    for i, file in enumerate(uploaded_files):
                        label = f"Video {i+1} ({file.name})"
                        file_info_list.append(label)
                        suffix = f".{file.name.split('.')[-1]}"
                        
                        # Reset file pointer sebelum dibaca
                        file.seek(0)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                            tmp_file.write(file.read())
                            tmp_path = tmp_file.name
                        
                        g_file = client.files.upload(file=tmp_path)
                        gemini_files.append(g_file)
                        os.remove(tmp_path)

                    daftar_file_str = ", ".join(file_info_list)
                    total_file = len(file_info_list)

                    prompt = f"""
                    Kamu adalah Content Strategist & Copywriter profesional kuliner snack UMKM Indonesia.
                    Pengguna telah mengunggah persis {total_file} file video dengan urutan:
                    {daftar_file_str}

                    Tugasmu adalah menganalisa SEMUA video tersebut dan menyusun panduan konten TikTok:

                    1. **Panduan Potongan Video (CapCut Visual Guide)**:
                       - Pengguna mengedit di iPhone (galeri tidak menampilkan nama file, hanya gambar awal video / thumbnail).
                       - OLEH KARENA ITU, di setiap baris potongan, kamu WAJIB menuliskan:
                         1. Label urutan video (contoh: Video 1, Video 2, dst).
                         2. **Ciri Gambar Pertama / Thumbnail** (contoh: *Thumbnail: Tangan memegang toples*, atau *Thumbnail: Tumpukan karung coklat*).
                         3. Timestamp detik potongannya [00:0X - 00:0Y].
                         4. Keterangan visual saat dipotong.
                       - WAJIB gunakan minimal 1 potongan dari SETIAP video yang diunggah.
                       - Total durasi gabungan seluruh klip: 10 - 15 detik.

                    2. **Skrip Voice Over (ElevenLabs Ready)**:
                       - Panjang naskah WAJIB 25 - 35 kata (pas untuk 10-15 detik).
                       - Target: Ibu-ibu / penyuka camilan gurih renyah.
                       - Alur: Hook -> Deskripsi rasa gurih renyah udang sumpia -> Ajakan checkout.
                       - Tulis teks polos tanpa label [Hook]/[Isi].

                    3. **Caption TikTok & Hashtags**:
                       - Hook, deskripsi produk, CTA keranjang kuning, dan 5-8 hashtag relevan.

                    Format Output:
                    ---
                    ### ✂️ 1. Panduan Potongan Video (CapCut)
                    * Klip 1 (Hook) - **[Video X]** (🖼️ *Ciri Awal/Thumbnail: ...*): `[00:0X - 00:0Y]` -> (Keterangan Visual)
                    * Klip 2 (Isi) - **[Video Y]** (🖼️ *Ciri Awal/Thumbnail: ...*): `[00:0X - 00:0Y]` -> (Keterangan Visual)
                    ...dst hingga semua video terpakai.
                    *(Total Durasi Gabungan: XX Detik)*

                    ---
                    ### 🎙️ 2. Skrip Voice Over (ElevenLabs Ready)
                    *(Estimasi: XX Detik / XX Kata)*
                    (Tulis naskah VO di sini)

                    ---
                    ### 📱 3. Caption TikTok & Hashtags
                    (Tulis caption lengkap di sini)
                    """

                    # Auto Retry jika terjadi high demand / 503
                    models_to_try = [
                        "gemini-3.7-flash",
                        "gemini-3.7-flash-lite",
                        "gemini-flash-latest"
                    ]
                    response = None
                    last_error = None

                    for model_name in models_to_try:
                        for attempt in range(3):
                            try:
                                response = client.models.generate_content(
                                    model=model_name,
                                    contents=[*gemini_files, prompt]
                                )
                                break
                            except Exception as err:
                                last_error = err
                                if "503" in str(err) or "UNAVAILABLE" in str(err):
                                    time.sleep(3)
                                    continue
                                else:
                                    break
                        if response:
                            break

                    if response:
                        st.success("✨ Konten Berhasil Dibuat!")
                        with st.container(border=True):
                            st.markdown(response.text)
                    else:
                        raise last_error

                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses konten: {e}")

                finally:
                    for gf in gemini_files:
                        try:
                            client.files.delete(name=gf.name)
                        except Exception:
                            pass
