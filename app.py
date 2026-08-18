import streamlit as st
from google import genai
import tempfile
import os
import time

# Konfigurasi Tampilan Halaman
st.set_page_config(
    page_title="AI Video Content Director",
    page_icon="🎬",
    layout="wide"
)

# Ambil API Key dari Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Custom CSS Dashboard Modern & Bersih
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
        padding: 15px 0 10px 0;
    }
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #0F172A !important;
        letter-spacing: -0.5px;
    }
    .main-subtitle {
        font-size: 14px;
        color: #64748B !important;
        margin-top: -5px;
        margin-bottom: 20px;
    }
    .feature-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        height: 100%;
    }
    .icon-box { font-size: 22px; margin-bottom: 4px; }
    .card-title { font-size: 15px; font-weight: 700; color: #0F172A !important; margin-bottom: 2px; }
    .card-desc { font-size: 12px; color: #64748B !important; line-height: 1.3; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <div class="main-title">🎬 AI Video Content Director</div>
        <div class="main-subtitle">Asisten Kurasi Visual CapCut, Voice Over & Caption Otomatis untuk Semua Produk</div>
    </div>
""", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">✂️</div>
            <div class="card-title">CapCut Cut Guide (X.Xs)</div>
            <div class="card-desc">Deteksi detik terbaik dengan format durasi desimal CapCut & deskripsi visual video.</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">🎙️</div>
            <div class="card-title">Voice Over Script</div>
            <div class="card-desc">Skrip durasi fleksibel berstruktur Hook, Isi & CTA, siap dibaca ElevenLabs / TTS.</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">📱</div>
            <div class="card-title">TikTok / Reels Copy</div>
            <div class="card-desc">Caption menggugah rasa penasaran, CTA keranjang kuning, dan hashtag terarah.</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Form Informasi Produk (Universal)
with st.container(border=True):
    st.markdown("##### 📌 Informasi Produk & Target Konten")
    c_nama, c_usp = st.columns(2)
    with c_nama:
        nama_produk = st.text_input("Nama & Kategori Produk:", placeholder="Contoh: Sumpia Udang / Kemeja Linen Pria / Serum Wajah")
    with c_usp:
        usp_produk = st.text_input("Keunggulan Utama (USP):", placeholder="Contoh: Super renyah isian gurih / Bahan adem anti kusut / Mencerahkan 7 hari")

    c_audiens, c_tone, c_durasi = st.columns(3)
    with c_audiens:
        target_audiens = st.selectbox(
            "Target Audiens:",
            ["Penyuka Camilan / Ibu Rumah Tangga", "Gen-Z / Remaja", "Karyawan & Profesional", "Umum / Semua Kalangan"]
        )
    with c_tone:
        tone_suara = st.selectbox(
            "Gaya Bahasa / Tone:",
            ["Santai & Menggoda Selera (Camilan/Kuliner)", "Enerjik & Persuasif (Hard Selling / Promo)", "Elegan & Storytelling (Lifestyle/Skincare)", "Informatif & Edukatif"]
        )
    with c_durasi:
        target_durasi = st.selectbox(
            "Target Durasi Video:",
            [
                "20 - 30 Detik (Standar Review / Selling)",
                "10 - 15 Detik (Cepat / Fast Hook)",
                "45 - 60 Detik (Storytelling / Edukasi Mendalam)"
            ]
        )

# Area Upload Video
st.markdown("##### 📤 Upload Klip Video Mentah")
uploaded_files = st.file_uploader(
    "Pilih 2 hingga 5 video (.mp4, .mov, .avi):", 
    type=["mp4", "mov", "avi"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.error("⚠️ Maksimal 5 video saja ya Uda!")
    else:
        # Preview Video di Web
        st.markdown("###### 🎬 Video yang Dipilih:")
        cols = st.columns(len(uploaded_files))
        for i, file in enumerate(uploaded_files):
            with cols[i]:
                st.caption(f"**Video {i+1}** ({file.name})")
                st.video(file)

        st.write("")
        if st.button("🚀 Analisa Video & Buat Konten", use_container_width=True, type="primary"):
            if not nama_produk:
                st.warning("Mohon isi Nama Produk terlebih dahulu agar AI bisa menyesuaikan naskah dan caption-nya ya!")
            else:
                with st.spinner("Gemini sedang membedah frame video, menghitung durasi CapCut, dan meracik naskah..."):
                    gemini_files = []
                    file_info_list = []
                    try:
                        for i, file in enumerate(uploaded_files):
                            label = f"Video {i+1} ({file.name})"
                            file_info_list.append(label)
                            suffix = f".{file.name.split('.')[-1]}"
                            
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
                        Kamu adalah Video Director, Video Editor CapCut, dan Copywriter profesional.
                        
                        Informasi Produk:
                        - Nama & Kategori: {nama_produk}
                        - Keunggulan Utama (USP): {usp_produk}
                        - Target Audiens: {target_audiens}
                        - Gaya Bahasa: {tone_suara}
                        - Target Total Durasi: {target_durasi}
                        
                        Pengguna telah mengunggah {total_file} video mentah: {daftar_file_str}.
                        
                        Tugasmu:
                        1. **Panduan Potongan CapCut (CapCut Cut Guide)**:
                           - WAJIB gunakan minimal 1 potongan terbaik dari SETIAP file video yang diunggah ({daftar_file_str}).
                           - Sesuaikan total durasi video gabungan agar pas dengan target: {target_durasi}.
                           - Untuk setiap video, berikan:
                             * Label Video (contoh: Video 1, Video 2, dst).
                             * **Ciri Visual Utama Video**: Deskripsikan objek/adegan utama video tersebut secara gamblang sebagai tanda pengenal saat memilih video di galeri HP.
                             * **Rentang Waktu**: `[00:0X - 00:0Y]`
                             * **Durasi CapCut**: Wajib dalam format desimal standar CapCut: **X.Xs** (contoh: `4.5s`, `5.2s`, `6.0s`).
                             * **Deskripsi Aksi**: Alasan visual kenapa detik tersebut dipotong.
                           - Alur potongan: Hook (detik paling memikat) -> Isi (detail/keunggulan produk) -> CTA (stok/kemasan siap kirim).
                           - Hitung Total Durasi Gabungan dalam format desimal (contoh: `Total Durasi Gabungan: 24.5s`).

                        2. **Skrip Voice Over (ElevenLabs / TTS Ready)**:
                           - Sesuaikan jumlah kata naskah dengan target durasi:
                             * Jika durasi 10-15 detik: 25 - 35 kata.
                             * Jika durasi 20-30 detik: 50 - 70 kata.
                             * Jika durasi 45-60 detik: 110 - 140 kata.
                           - Bahasa natural, menggugah minat sesuai target audiens.
                           - Alur: Hook kuat -> Penjelasan keunggulan & detail produk -> Ajakan beli (CTA).
                           - Tulis teks naskah polos tanpa tanda kurung [Hook]/[Isi] agar langsung siap di-copy ke software TTS.

                        3. **Caption TikTok / Reels & Hashtags**:
                           - Hook baris pertama, benefit singkat produk, ajakan transaksi keranjang kuning / DM.
                           - ATURAN HASHTAG: Jumlah hashtag MAKSIMAL 5 hashtag, dan WAJIB menyertakan tagar #lesasnack sebagai tagar utama (contoh: #lesasnack #sumpiaudang #camilanviral #snackgurih #kuliner).

                        Format Output:
                        ---
                        ### ✂️ 1. Panduan Potongan Video (CapCut)
                        * Klip 1 (Hook) - **[Video X]** (🔍 *Ciri Video: ...*): `[00:0X - 00:0Y]` $\\rightarrow$ **Durasi CapCut: X.Xs**
                          *(Aksi Visual: ...)*
                        * Klip 2 (Isi) - **[Video Y]** (🔍 *Ciri Video: ...*): `[00:0X - 00:0Y]` $\\rightarrow$ **Durasi CapCut: X.Xs**
                          *(Aksi Visual: ...)*
                        ...dst hingga ke-{total_file} video terpakai.
                        *(Total Durasi Video Jadi: XX.Xs)*

                        ---
                        ### 🎙️ 2. Skrip Voice Over (ElevenLabs Ready)
                        *(Estimasi: XX Detik / XX Kata)*
                        (Tulis naskah teks polos di sini)

                        ---
                        ### 📱 3. Caption Postingan & Hashtags
                        (Tulis caption lengkap dengan maksimal 5 hashtag termasuk #lesasnack)
                        """

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
                            st.success("✨ Konten Berhasil Dianalisa & Dibuat!")
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
