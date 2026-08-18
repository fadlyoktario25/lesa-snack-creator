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

# Inisialisasi Klien Gemini
gemini_key = st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_key)

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
        <div class="main-subtitle">Panduan CapCut, Naskah Natural ElevenLabs & Caption TikTok Otomatis</div>
    </div>
""", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">✂️</div>
            <div class="card-title">CapCut Cut Guide (X.Xs)</div>
            <div class="card-desc">Deteksi detik terbaik tiap video mentah sesuai format desimal CapCut.</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">🎙️</div>
            <div class="card-title">Voice Over Script</div>
            <div class="card-desc">Naskah otomatis atau tempel dari ChatGPT, siap 1-klik copy ke ElevenLabs.</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-box">📱</div>
            <div class="card-title">TikTok Post Kit</div>
            <div class="card-desc">Caption menggugah rasa penasaran, CTA keranjang kuning & tagar #lesasnack.</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Form Informasi Produk
with st.container(border=True):
    st.markdown("##### 📌 1. Informasi Produk & Target Konten")
    c_nama, c_usp = st.columns(2)
    with c_nama:
        nama_produk = st.text_input("Nama & Kategori Produk:", placeholder="Contoh: Sumpia Udang / Kemeja Linen / Keripik Pedas")
    with c_usp:
        usp_produk = st.text_input("Keunggulan Utama (USP):", placeholder="Contoh: Super renyah isian gurih padat, bumbu medok")

    c_audiens, c_tone, c_durasi = st.columns(3)
    with c_audiens:
        target_audiens = st.selectbox(
            "Target Audiens:",
            ["Penyuka Camilan / Ibu Rumah Tangga", "Gen-Z / Anak Muda", "Karyawan & Profesional", "Umum / Semua Kalangan"]
        )
    with c_tone:
        tone_suara = st.selectbox(
            "Gaya Bahasa:",
            ["Santai & Bikin Ngiler (Kuliner Gaul)", "Storytelling Ringan & Akrab", "Enerjik Racun Belanja (Hard Selling)", "Elegan & Informatif"]
        )
    with c_durasi:
        target_durasi = st.selectbox(
            "Target Durasi Video:",
            ["10 - 15 Detik (Fast Hook)", "20 - 30 Detik (Standar Review)", "45 - 60 Detik (Storytelling Panjang)"]
        )

# Opsi Skrip
with st.container(border=True):
    st.markdown("##### ✍️ 2. Metode Naskah Voice Over")
    mode_skrip = st.radio(
        "Pilih cara pembuatan naskah:",
        ["🤖 Buat Otomatis (Gaya Santai & Natural)", "📝 Tempel Naskah Manual (Hasil dari ChatGPT)"],
        horizontal=True
    )
    manual_script = ""
    if mode_skrip == "📝 Tempel Naskah Manual (Hasil dari ChatGPT)":
        manual_script = st.text_area(
            "Tempel naskah voice over dari ChatGPT di sini:",
            placeholder="Contoh: Gak nyangka cemilan sekecil ini isian udangnya nendang banget...",
            height=120
        )

# Area Upload Video
st.markdown("##### 📤 3. Upload Klip Video Mentah")
uploaded_files = st.file_uploader(
    "Pilih 2 hingga 5 video (.mp4, .mov, .avi):", 
    type=["mp4", "mov", "avi"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.error("⚠️ Maksimal 5 video saja ya Uda!")
    else:
        st.markdown("###### 🎬 Video Terpilih:")
        cols = st.columns(len(uploaded_files))
        for i, file in enumerate(uploaded_files):
            with cols[i]:
                st.caption(f"**Video {i+1}** ({file.name})")
                st.video(file)

        st.write("")
        if st.button("🚀 Analisa Video & Buat Konten", use_container_width=True, type="primary"):
            if not nama_produk:
                st.warning("Mohon isi Nama Produk terlebih dahulu ya Uda!")
            elif mode_skrip == "📝 Tempel Naskah Manual (Hasil dari ChatGPT)" and not manual_script.strip():
                st.warning("Mohon tempelkan naskah dari ChatGPT terlebih dahulu ya Uda!")
            else:
                with st.spinner("Gemini sedang membedah frame video, menyusun potongan CapCut, dan meracik naskah natural..."):
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

                        durasi_kata = "25 - 35 kata" if "10 - 15" in target_durasi else ("50 - 70 kata" if "20 - 30" in target_durasi else "110 - 140 kata")

                        # Instruksi Sesuai Pilihan Mode Naskah
                        if mode_skrip == "📝 Tempel Naskah Manual (Hasil dari ChatGPT)":
                            naskah_instruction = f"""
                            PENGGUNA SUDAH MENYEDIAKAN NASKAH VOICE OVER SENDIRI DARI CHATGPT:
                            \"\"\"{manual_script.strip()}\"\"\"

                            TUGAS UTAMA:
                            - Gunakan naskah di atas secara persis pada tag [VOICE_OVER].
                            - Pecah naskah tersebut menjadi beberapa kalimat, lalu cari potongan adegan dari {total_file} video yang diunggah ({daftar_file_str}) yang paling pas secara visual untuk mengilustrasikan tiap kalimat naskah tersebut.
                            """
                        else:
                            naskah_instruction = f"""
                            BUATKAN NASKAH VOICE OVER BARU:
                            - Panjang naskah: {durasi_kata}.
                            - JANGAN PERNAH gunakan bahasa iklan kaku seperti: 'manjakan lidah Anda', 'kelezatan tiada tara', 'sensasi tak terlupakan', 'perpaduan sempurna'.
                            - Gunakan gaya bahasa santai sehari-hari seperti kreator TikTok Indonesia yang mengulas produk secara jujur dan bikin ngiler penonton.
                            - Tulis naskah polos tanpa tanda kurung [Hook]/[Isi] agar siap dibaca ElevenLabs.
                            """

                        prompt = f"""
                        Kamu adalah Video Director CapCut dan Copywriter TikTok kuliner/UMKM nomor satu di Indonesia.
                        
                        Informasi Produk:
                        - Produk: {nama_produk}
                        - Keunggulan (USP): {usp_produk}
                        - Target Audiens: {target_audiens}
                        - Gaya Bicara: {tone_suara}
                        - Target Durasi Video: {target_durasi}
                        
                        Daftar file video mentah ({total_file} video): {daftar_file_str}.

                        {naskah_instruction}

                        TUGAS KAMU:
                        1. **Naskah Voice Over (ElevenLabs Ready)**:
                           - Sediakan naskah teks polos yang siap dibaca mesin ElevenLabs.
                        
                        2. **Panduan Potongan Video (CapCut Guide)**:
                           - WAJIB gunakan minimal 1 potongan klip terbaik dari SETIAP video yang diunggah ({daftar_file_str}).
                           - Cocokkan adegan visual dengan kalimat naskah yang sedang dibaca pada detik tersebut.
                           - Tuliskan:
                             * Nomor Klip & Video yang dipakai.
                             * Ciri Visual Utama Video (sebagai pengenal saat memilih video di galeri HP).
                             * Detik potongan `[00:0X - 00:0Y]`.
                             * Durasi potong dalam format desimal standar CapCut: **X.Xs** (contoh: 2.8s, 3.5s).
                             * Naskah yang dibaca & Aksi visual.
                           - Hitung Total Durasi Gabungan.

                        3. **Caption TikTok & Hashtags**:
                           - Hook pemancing rasa penasaran, penjelasan singkat, ajakan checkout di keranjang kuning.
                           - Maksimal 5 hashtag relevan dan WAJIB menyertakan tagar #lesasnack.

                        Format Balasan:
                        [VOICE_OVER]
                        (Tulis naskah VO polos di sini)
                        [/VOICE_OVER]

                        [CAPCUT_GUIDE]
                        ### ✂️ Panduan Potongan Video (CapCut B-Roll Matching)
                        * **Klip 1** - **[Video X]** (🔍 *Ciri Video: ...*): `[00:0X - 00:0Y]` -> **Durasi CapCut: X.Xs**
                          * 🗣️ *Naskah:* "..."
                          * 🎯 *Aksi Visual:* ...
                        * **Klip 2** - **[Video Y]** (🔍 *Ciri Video: ...*): `[00:0X - 00:0Y]` -> **Durasi CapCut: X.Xs**
                          * 🗣️ *Naskah:* "..."
                          * 🎯 *Aksi Visual:* ...
                        ...dst hingga semua video terpakai.
                        *(Total Durasi Video Jadi: XX.Xs)*
                        [/CAPCUT_GUIDE]

                        [CAPTION]
                        (Tulis caption lengkap dengan maksimal 5 hashtag termasuk #lesasnack)
                        [/CAPTION]
                        """

                        models_to_try = ["gemini-3.7-flash", "gemini-3.7-flash-lite", "gemini-flash-latest"]
                        response = None
                        last_err = None

                        for model_name in models_to_try:
                            for attempt in range(3):
                                try:
                                    response = client.models.generate_content(
                                        model=model_name,
                                        contents=[*gemini_files, prompt]
                                    )
                                    break
                                except Exception as err:
                                    last_err = err
                                    if "503" in str(err) or "UNAVAILABLE" in str(err):
                                        time.sleep(3)
                                        continue
                                    else:
                                        break
                            if response:
                                break

                        if not response:
                            raise last_err

                        raw_output = response.text

                        # Parsing output
                        vo_text = ""
                        capcut_text = ""
                        caption_text = ""

                        if "[VOICE_OVER]" in raw_output and "[/VOICE_OVER]" in raw_output:
                            vo_text = raw_output.split("[VOICE_OVER]")[1].split("[/VOICE_OVER]")[0].strip()
                        if "[CAPCUT_GUIDE]" in raw_output and "[/CAPCUT_GUIDE]" in raw_output:
                            capcut_text = raw_output.split("[CAPCUT_GUIDE]")[1].split("[/CAPCUT_GUIDE]")[0].strip()
                        if "[CAPTION]" in raw_output and "[/CAPTION]" in raw_output:
                            caption_text = raw_output.split("[CAPTION]")[1].split("[/CAPTION]")[0].strip()

                        if not vo_text and not capcut_text:
                            capcut_text = raw_output

                        st.success("✨ Konten Berhasil Dianalisa & Disinkronkan!")

                        # 1. Box Skrip ElevenLabs (Tinggal 1-Klik Copy)
                        if vo_text:
                            st.markdown("### 🎙️ 1. Skrip Voice Over (Siap Copy ke ElevenLabs)")
                            st.code(vo_text, language="text")

                        # 2. Panduan Potong CapCut
                        if capcut_text:
                            st.markdown("---")
                            st.markdown(capcut_text)

                        # 3. Caption TikTok & Hashtags
                        if caption_text:
                            st.markdown("---")
                            st.markdown("### 📱 3. Caption TikTok & Hashtags (Siap Copy)")
                            st.code(caption_text, language="text")

                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat memproses visual: {e}")

                    finally:
                        for gf in gemini_files:
                            try:
                                client.files.delete(name=gf.name)
                            except Exception:
                                pass
