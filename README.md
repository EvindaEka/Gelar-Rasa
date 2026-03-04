## Dashboard Analisis Finansial Generasi Z di Indonesia

Dashboard interaktif berbasis Streamlit yang menganalisis profil keuangan, literasi, dan perilaku finansial Generasi Z di Indonesia.
Dashboard ini mengintegrasikan data individu dan indikator ekonomi regional untuk menghasilkan insight berbasis data mengenai kondisi finansial Gen Z di era digital.

---

## Deskripsi Proyek
Dashboard ini mengintegrasikan tiga dataset utama yaitu:
1. **Profil Keuangan Gen Z**
2. **Survei Literasi & Perilaku Keuangan**
3. **Indikator Ekonomi Regional (PDRB, Kredit, Urbanisasi, dll.)**

---

## ⚙️ Fitur Dashboard
## 🔹 1. Ringkasan Umum
Menampilkan:
* ✅ Jumlah responden
* ✅ Rata-rata usia
* ✅ Pendapatan rata-rata
* ✅ Pengeluaran rata-rata

Visualisasi:
* Distribusi responden per provinsi
* Komposisi gender
* Distribusi status pekerjaan

---

## 🔹 2. Profil Keuangan
Analisis mendalam terkait:
* Distribusi pendapatan & pengeluaran (Histogram)
* Rata-rata pendapatan & pengeluaran per provinsi
* Rata-rata pengeluaran per gender
* Distribusi penggunaan e-wallet
* Scatter plot hubungan pendapatan vs pengeluaran (dengan trendline OLS)

---

## 🔹 3. Literasi & Perilaku Keuangan
### Analisis Literasi Keuangan
* Rata-rata skor literasi (skala 1–4)
* Visualisasi skor per aspek
* Insight otomatis aspek tertinggi & terendah

### Analisis Perilaku & Pengambilan Keputusan
* Skor perilaku finansial
* Evaluasi impulsivitas & kontrol keuangan
* Interpretasi naratif otomatis

---

## 🔹 4. Indikator Ekonomi Regional (Integrasi Dataset)
Analisis lanjutan dengan menggabungkan data mikro & makro:

### PDRB vs Outstanding Pinjaman
Bubble scatter:
* Size → jumlah penerima pinjaman
* Color → urbanisasi

### Urbanisasi vs Dana yang Diberikan
Scatter dengan trendline OLS

### Integrasi PDRB vs Pendapatan Gen Z
Grouped bar chart antar provinsi

### Literasi vs Risiko Kredit (TWP 90%)
Bar chart horizontal untuk melihat hubungan literasi dan risiko kredit regional

---

## 🛠️ Teknologi yang Digunakan
* **Python**
* **Streamlit**
* **Pandas**
* **NumPy**
* **Plotly (Express & Graph Objects)**
* **Statsmodels (OLS via Plotly trendline)**

---

## 🧹 Data Processing
Beberapa proses yang dilakukan dalam kode:
* Parsing range Rupiah menjadi nilai rata-rata numerik
* Cleaning karakter non-numerik pada data regional
* Normalisasi nama kolom
* Perhitungan skor literasi & perilaku (mean aggregation)
* Integrasi dataset menggunakan merge berdasarkan provinsi

---

## 🚀 Cara Menjalankan
```bash
git clone https://github.com/EvindaEka/Gelar-Rasa
cd Gelar-Rasa
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Struktur Proyek

```
Gelar-Rasa/
│
├── app.py
├── data/
│   ├── GenZ_Financial_Profile.csv
│   ├── GenZ_Financial_Literacy_Survey.csv
│   └── Regional_Economic_Indicators.csv
├── requirements.txt
└── README.md
```

---

## 🎯 Insight Utama yang Dihasilkan
* Karakteristik finansial Gen Z per provinsi
* Hubungan pendapatan dan pengeluaran
* Tingkat literasi keuangan digital
* Pola perilaku finansial & impulsivitas
* Hubungan kondisi ekonomi regional dengan kondisi finansial Gen Z

---

## 👩‍💻 Pengembang
* **Evinda Eka Ayudia Lestari**
* **R. Aj Maria Shovia Fadinda**

---
