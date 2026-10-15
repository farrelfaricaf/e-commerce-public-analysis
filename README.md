# 🛒 Proyek Analisis Data: E-Commerce Public Dataset

Proyek akhir analisis data menggunakan dataset publik e-commerce Brazil (Olist) dari Dicoding Indonesia (Kursus: **Belajar Analisis Data dengan Python**). Proyek ini mencakup proses data wrangling, exploratory data analysis (EDA), visualisasi data, analisis lanjutan RFM, kesimpulan bisnis, serta dashboard interaktif berbasis Streamlit.

- **Nama:** Farrel Farica Firjaturazza
- **ID Dicoding:** DS284B6Y0580

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
├───Proyek_Analisis_Data.ipynb
├───README.md
├───requirements.txt
└───url.txt (tautan dashboard Streamlit Cloud publik)
```

---

## 📌 Pertanyaan Bisnis yang Dijawab
1. **Tren Pendapatan & Pesanan Bulanan**: Bagaimana tren pertumbuhan total pendapatan (*revenue*) dan volume pesanan (*orders*) e-commerce per bulan sepanjang periode Januari 2017 hingga Agustus 2018?
2. **Karakteristik Parameter RFM Pelanggan Terbaik**: Bagaimana segmentasi pelanggan berdasarkan analisis RFM (*Recency, Frequency, Monetary*) untuk menentukan karakteristik pelanggan loyal (*Champions*) dan pelanggan yang membutuhkan retensi (*At-Risk*)?
3. **Persebaran Geografis Pelanggan & Pesanan**: Negara bagian (*state*) mana saja di Brazil yang mendominasi persebaran pelanggan dan total transaksi e-commerce?

---

## 🚀 Panduan Menjalankan Dashboard Secara Lokal

### 1. Prasyarat Lingkungan
Pastikan Python (versi 3.9+) telah terpasang di komputer Anda.

### 2. Instalasi Dependensi
Buka terminal / command prompt di direktori proyek ini, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard Streamlit
Jalankan perintah berikut pada terminal:
```bash
streamlit run dashboard/dashboard.py
```
Atau jika perintah `streamlit` tidak dikenali:
```bash
python -m streamlit run dashboard/dashboard.py
```
Aplikasi dashboard akan otomatis terbuka di browser Anda pada alamat default: `http://localhost:8501`.

---

## 🌐 Panduan Deploy ke Streamlit Community Cloud (Bonus Bintang 5)
1. Buat repository publik baru di GitHub (misal: `e-commerce-public-analysis`).
2. Upload seluruh isi folder `submission/` ini ke dalam repository tersebut.
3. Kunjungi [share.streamlit.io](https://share.streamlit.io) dan masuk dengan akun GitHub Anda.
4. Klik tombol **Create app** atau **New app**.
5. Pilih repository, branch `main`, dan set path **Main file path** ke: `dashboard/dashboard.py`.
6. Klik **Deploy!** Aplikasi akan langsung ter-build dan aktif secara publik dalam 1-2 menit.
7. Salin tautan URL aplikasi Anda dan tempelkan ke dalam file `url.txt`.
