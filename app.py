import streamlit as st
import pandas as pd
import plotly.express as px
from gtts import gTTS
import os
from datetime import datetime
import google.generativeai as genai # Import library Gemini AI

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Mood x Productivity Journal AI",
    page_icon="✨",
    layout="wide"
)

# --- Integrasi Google Gemini AI ---
# Mengambil API Key dari Streamlit Secrets.
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_ENABLED = True
except (KeyError, FileNotFoundError):
    st.warning("API Key Gemini tidak ditemukan. Fitur motivasi AI dinonaktifkan. Silakan lihat cara setup di README.")
    AI_ENABLED = False

# --- Nama File untuk Menyimpan Data ---
DATA_FILE = "data.csv"
DF_COLUMNS = ["Tanggal", "Mood Pilihan", "Jam Belajar", "Jurnal", "Sentimen AI", "Emosi AI", "Motivasi AI"]

# --- Fungsi untuk Memuat atau Membuat DataFrame ---
def load_data():
    """Memuat data dari file CSV, atau membuat file baru jika belum ada."""
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE, parse_dates=['Tanggal'])
            # Pastikan semua kolom yang diperlukan ada
            for col in DF_COLUMNS:
                if col not in df.columns:
                    df[col] = None
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=DF_COLUMNS)
    else:
        return pd.DataFrame(columns=DF_COLUMNS)

# --- FUNGSI ANALISIS & MOTIVASI DENGAN AI (PENGGANTI FUNGSI LAMA) ---
def analyze_and_motivate_with_ai(journal_text):
    """Menganalisis sentimen, emosi, dan membuat motivasi dengan satu panggilan AI."""
    if not AI_ENABLED:
        return "Netral", "Tidak Terdeteksi", "Fitur AI tidak aktif. Semangat selalu!"

    # Prompt yang detail untuk mendapatkan output yang terstruktur
    prompt = f"""
    Kamu adalah seorang psikolog AI yang empatik dan juga teman yang suportif.
    Analisis teks jurnal berikut dari seorang pengguna.

    Teks Jurnal: "{journal_text}"

    Tugasmu adalah melakukan 3 hal dan memberikan jawaban HANYA dalam format yang ditentukan di bawah ini:
    1.  **Analisis Sentimen**: Tentukan apakah sentimen teks ini 'Positif', 'Negatif', atau 'Netral'.
    2.  **Deteksi Emosi**: Identifikasi satu emosi yang paling dominan dari teks tersebut (contoh: Senang, Sedih, Lelah, Kecewa, Semangat, Marah, Takut).
    3.  **Buat Motivasi**: Tulis satu atau dua kalimat motivasi yang personal, singkat, relevan, dan membangkitkan semangat berdasarkan isi jurnal. Gunakan bahasa Indonesia yang santai.

    Format Jawaban (HARUS SEPERTI INI, jangan tambahkan teks lain):
    Sentimen: [Hasil Analisis Sentimenmu]
    Emosi: [Hasil Deteksi Emosimu]
    Motivasi: [Kalimat Motivasimu]
    """
    try:
        # PEMBARUAN: Menambahkan timeout 30 detik untuk mencegah aplikasi macet
        request_options = {"timeout": 30}
        response = model.generate_content(prompt, request_options=request_options)
        text_response = response.text

        # Parsing respons terstruktur dari AI
        # Pengecekan sederhana untuk memastikan format respons benar
        if "Sentimen:" in text_response and "Emosi:" in text_response and "Motivasi:" in text_response:
            sentiment = text_response.split("Sentimen:")[1].split("Emosi:")[0].strip()
            emotion = text_response.split("Emosi:")[1].split("Motivasi:")[0].strip()
            motivation = text_response.split("Motivasi:")[1].strip()
            return sentiment, emotion, motivation
        else:
            st.error("Format respons dari AI tidak sesuai. Menampilkan respons mentah.")
            # Jika format salah, kembalikan respons mentah untuk debugging
            return "Error Parsing", "Error Parsing", text_response

    except Exception as e:
        # PEMBARUAN: Menampilkan pesan error yang lebih spesifik
        st.error(f"Gagal menghubungi AI: {e}")
        return "Error", "Error", "Maaf, terjadi kesalahan saat menghubungi AI. Periksa koneksi internet atau API Key Anda."


# --- Tampilan Utama Aplikasi ---
st.title("✨ Mood x Productivity Journal (Full AI)")
st.markdown("Catat _mood_, progres belajar, dan pikiranmu setiap hari. Dapatkan analisis & motivasi personal dari AI!")

# --- Memuat Data ---
df = load_data()

# --- Layout Aplikasi ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.header("📝 Input Jurnal Harian")
    with st.form(key="journal_form", clear_on_submit=True):
        mood_options = ["Pilih satu...", "Senang", "Semangat", "Biasa Aja", "Lelah", "Stress", "Sedih"]
        mood = st.selectbox("Bagaimana perasaanmu hari ini (menurutmu)?", mood_options)
        hours = st.number_input("Berapa jam kamu belajar/coding hari ini?", min_value=0.0, max_value=24.0, step=0.5, format="%.1f")
        journal_text = st.text_area("Tuliskan catatan singkatmu di sini:", "Contoh: Hari ini berhasil menyelesaikan fitur X, tapi masih ada bug di bagian Y.")
        
        submit_button = st.form_submit_button(label="Simpan & Dapatkan Analisis AI")

        if submit_button:
            if mood == "Pilih satu..." or not journal_text:
                st.warning("Mohon isi mood dan jurnal terlebih dahulu.")
            else:
                with st.spinner("AI sedang menganalisis jurnal dan merangkai kata-kata terbaik untukmu..."):
                    # Panggil fungsi AI tunggal untuk mendapatkan semuanya
                    sentiment_ai, emotion_ai, motivation_ai = analyze_and_motivate_with_ai(journal_text)

                # Buat entri baru
                new_entry = pd.DataFrame([{
                    "Tanggal": datetime.now(),
                    "Mood Pilihan": mood,
                    "Jam Belajar": hours,
                    "Jurnal": journal_text,
                    "Sentimen AI": sentiment_ai,
                    "Emosi AI": emotion_ai,
                    "Motivasi AI": motivation_ai,
                }])
                
                # Gabungkan dengan data lama dan simpan
                df = pd.concat([df, new_entry], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("Jurnal berhasil dianalisis dan disimpan!")

with col2:
    st.header("🔍 Analisis & Motivasi dari AI")
    if not df.empty:
        last_entry = df.iloc[-1]
        
        st.subheader("Analisis Jurnal Terakhir")
        st.info(f"**Jurnal:** *{last_entry['Jurnal']}*")
        
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("Sentimen (Menurut AI)", last_entry['Sentimen AI'])
        metric_col2.metric("Emosi Dominan (Menurut AI)", last_entry['Emosi AI'])
        
        st.subheader("💬 Kata Penyemangat dari AI Untukmu")
        motivation_text = last_entry['Motivasi AI']
        st.markdown(f"> *{motivation_text}*")
        
        try:
            tts = gTTS(text=motivation_text, lang='id', slow=False)
            tts.save("motivasi_ai.mp3")
            st.audio("motivasi_ai.mp3")
            os.remove("motivasi_ai.mp3")
        except Exception as e:
            st.warning(f"Gagal membuat audio: {e}") # Diubah jadi warning agar tidak terlalu mengganggu
            
    else:
        st.info("Belum ada data jurnal. Silakan isi form di sebelah kiri untuk memulai.")

# --- Garis pemisah dan Visualisasi ---
st.markdown("---")
st.header("📊 Visualisasi Datamu")
if not df.empty and len(df) >= 1:
    df_filtered = df.copy() # Mulai dengan data lengkap
    
    # Grafik: Hubungan Jam Belajar dan Sentimen dari Waktu ke Waktu
    st.subheader("Perkembangan Jam Belajar & Mood")
    
    # Buat kolom numerik untuk sentimen agar bisa digrafikkan
    sentiment_map = {"Positif": 1, "Netral": 0, "Negatif": -1}
    df_filtered['Skor Sentimen AI'] = df_filtered['Sentimen AI'].map(sentiment_map).fillna(0)

    fig = px.line(
        df_filtered, 
        x='Tanggal', 
        y='Jam Belajar', 
        title='Jam Belajar vs. Sentimen AI',
        markers=True,
        labels={'Jam Belajar': 'Jumlah Jam Belajar', 'Tanggal': 'Tanggal'},
        hover_data={'Jurnal': True, 'Sentimen AI': True, 'Emosi AI': True}
    )
    fig.add_scatter(x=df_filtered['Tanggal'], y=df_filtered['Skor Sentimen AI'], mode='lines+markers', name='Sentimen AI', yaxis='y2')

    fig.update_layout(
        yaxis=dict(title="Jumlah Jam Belajar"),
        yaxis2=dict(
            title="Skor Sentimen AI",
            overlaying="y",
            side="right",
            range=[-1.5, 1.5],
            tickvals=[-1, 0, 1],
            ticktext=["Negatif", "Netral", "Positif"]
        ),
        legend=dict(yanchor="top", y=0.9, xanchor="left", x=0.1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tambahan: Distribusi Emosi AI
    st.subheader("Distribusi Emosi (Menurut AI)")
    emotion_counts = df_filtered['Emosi AI'].value_counts().reset_index()
    emotion_counts.columns = ['Emosi', 'Jumlah']
    fig_pie = px.pie(emotion_counts, names='Emosi', values='Jumlah', title='Proporsi Emosi yang Kamu Rasakan')
    st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.info("Grafik akan muncul di sini setelah kamu memiliki data jurnal.")

# --- Menampilkan Riwayat Data ---
with st.expander("Lihat Semua Riwayat Jurnal"):
    st.dataframe(df.sort_values(by="Tanggal", ascending=False), use_container_width=True)

