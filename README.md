# 🛒 Proyek Analisis Data: E-Commerce Public Dataset

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://e-commerce-public-analysis-farrel-farica-f.streamlit.app/)

Proyek akhir analisis data menggunakan dataset publik e-commerce Brazil (Olist) dari Dicoding Indonesia (Kursus: **Belajar Analisis Data dengan Python**). Proyek ini mencakup proses data wrangling, exploratory data analysis (EDA), visualisasi data, analisis lanjutan RFM, kesimpulan bisnis, serta dashboard interaktif berbasis Streamlit.

- **Nama:** Farrel Farica Firjaturazza
- **ID Dicoding:** DS284B6Y0580
- **Live Dashboard:** [e-commerce-public-analysis-farrel-farica-f.streamlit.app](https://e-commerce-public-analysis-farrel-farica-f.streamlit.app/)
- **GitHub Repository:** [github.com/farrelfaricaf/e-commerce-public-analysis](https://github.com/farrelfaricaf/e-commerce-public-analysis)

---

## 📁 Struktur Direktori

```text
submission/
├───dashboard/
│   ├───dashboard.py
│   └───main_data.csv
├───data/
│   ├───customers_dataset.csv
│   ├───geolocation_dataset.csv
│   ├───order_items_dataset.csv
│   ├───order_payments_dataset.csv
│   ├───order_reviews_dataset.csv
│   ├───orders_dataset.csv
│   ├───product_category_name_translation.csv
│   ├───products_dataset.csv
│   └───sellers_dataset.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt (tautan dashboard Streamlit Cloud publik)
```

---

## 📌 Pertanyaan Bisnis yang Dijawab (SMART Framework)
1. **Tren Pendapatan & Pesanan Bulanan**: Bagaimana tren pertumbuhan total pendapatan (*revenue*) dan volume pesanan (*orders*) e-commerce per bulan sepanjang periode **Januari 2017 hingga Agustus 2018**?
2. **Karakteristik Parameter RFM Pelanggan**: Bagaimana segmentasi pelanggan berdasarkan analisis RFM (*Recency, Frequency, Monetary*) pada transaksi e-commerce sepanjang periode **Januari 2017 hingga Agustus 2018** untuk menentukan karakteristik kelompok pelanggan loyal (*Champions*) dan pelanggan yang membutuhkan retensi (*At-Risk*)?
3. **Persebaran Geografis Pelanggan & Pesanan**: Negara bagian (*state*) mana saja di Brazil yang mendominasi aktivitas e-commerce berdasarkan **indikator total pelanggan unik (*unique customers*) dan total volume pesanan (*order volume*)** sepanjang periode **Januari 2017 hingga Agustus 2018**?

---

## 🚀 Panduan Menjalankan Dashboard

### Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Setup Environment - Shell/Terminal
```bash
pipenv install
pipenv shell
pip install -r requirements.txt
```

### Run Steamlit App
```bash
streamlit run dashboard/dashboard.py
```
Atau jika menggunakan Python launcher:
```bash
python -m streamlit run dashboard/dashboard.py
```
Aplikasi dashboard akan otomatis terbuka di browser pada alamat default: `http://localhost:8501`.

---

## 🌐 Panduan Deploy ke Streamlit Community Cloud (Bonus Bintang 5)
1. Buat repository publik baru di GitHub (misal: `e-commerce-public-analysis`).
2. Upload seluruh isi folder `submission/` ini ke dalam repository tersebut.
3. Kunjungi [share.streamlit.io](https://share.streamlit.io) dan masuk dengan akun GitHub Anda.
4. Klik tombol **Create app** atau **New app**.
5. Pilih repository, branch `main`, dan set path **Main file path** ke: `dashboard/dashboard.py`.
6. Klik **Deploy!** Aplikasi akan langsung ter-build dan aktif secara publik dalam 1-2 menit.
7. Salin tautan URL aplikasi Anda dan tempelkan ke dalam file `url.txt`.
