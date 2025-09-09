# ✨ Mood x Productivity Journal (with Full AI)

Sebuah aplikasi web jurnal sederhana yang dibuat untuk melacak mood dan produktivitas harian.  
Ditenagai oleh **Streamlit** dan **Google Gemini AI**, aplikasi ini tidak hanya menyimpan catatanmu,  
tapi juga memberikan **analisis sentimen, deteksi emosi, dan motivasi yang dipersonalisasi** secara akurat dalam Bahasa Indonesia.

---

## 📸 Screenshot
> [Disarankan untuk menambahkan screenshot aplikasi Anda di sini]

---

## ⚡ Fitur Utama

- 📝 **Input Jurnal Harian**  
  Catat mood pilihan, jumlah jam produktif, dan catatan singkat setiap hari.

- 🧠 **Analisis Full AI**  
  Dapatkan analisis sentimen (*Positif, Negatif, Netral*) dan deteksi emosi dominan  
  yang diproses oleh **Google Gemini AI**, memberikan hasil relevan untuk teks Bahasa Indonesia.

- 💬 **Motivasi Personal dari AI**  
  Terima kata-kata penyemangat yang unik dan dibuat secara dinamis berdasarkan konteks jurnal harianmu.

- 🔊 **Motivasi dengan Suara (TTS)**  
  Dengarkan motivasi yang dihasilkan AI melalui fitur **Google Text-to-Speech (gTTS).**

- 📊 **Visualisasi Data Interaktif**  
  Pantau tren produktivitas dan perubahan mood-mu dari waktu ke waktu melalui grafik interaktif (Plotly).

- 💾 **Penyimpanan Lokal (CSV)**  
  Semua data jurnal disimpan secara sederhana dan aman di dalam file `data.csv`.

---

## 🛠️ Teknologi yang Digunakan
- **Framework**: Python, Streamlit  
- **AI & Machine Learning**: Google Gemini AI (`gemini-1.5-flash`)  
- **Analisis Data**: Pandas  
- **Visualisasi Data**: Plotly  
- **Text-to-Speech**: gTTS (Google Text-to-Speech)  

---

## 🚀 Cara Menjalankan di Komputer Lokal

### 1. Prasyarat
- Python **3.8+**  
- `pip` sudah terinstal

### 2. Clone Repository
```bash
git clone https://github.com/URL_REPOSITORY_ANDA/NAMA_PROYEK_ANDA.git
cd NAMA_PROYEK_ANDA
```
# --- Setup Environment & Run App ---

# 3. Buat Virtual Environment
python -m venv .venv

# Aktifkan Virtual Environment
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# 4. Instal Library
```
pip install -r requirements.txt 
```

# 5. Setup API Key Gemini
# Pastikan ada folder .streamlit
mkdir -p .streamlit

# Buat file secrets.toml
```
echo 'GEMINI_API_KEY = "MASUKKAN_API_KEY_ANDA_DI_SINI"' > .streamlit/secrets.toml
```

# 6. Jalankan Aplikasi
```
streamlit run app.py
```
