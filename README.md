# 🍄 Mushroom KNN Classifier

Aplikasi web berbasis Flask untuk mengklasifikasikan jamur sebagai **Edible (dapat dimakan)** atau **Poisonous (beracun)** menggunakan algoritma **K-Nearest Neighbors (KNN)**.

## 📋 Deskripsi

Tugas 9 – Penerapan Algoritma K-Nearest Neighbors (KNN) pada Aplikasi Berbasis Web Menggunakan Flask.

Dataset yang digunakan adalah **UCI Mushroom Dataset** dengan 8.124 sampel dan 22 fitur kategorikal.

## 🎯 Akurasi Model
- **99.75%** pada data uji (test set 20%)

## 🚀 Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Model
```bash
python train_model.py
```

### 3. Jalankan Aplikasi
```bash
python app.py
```

Buka browser di `http://localhost:5000`

## 📁 Struktur Project
```
mushroom_knn_app/
├── static/
│   ├── css/style.css
│   └── js/main.js
├── templates/
│   ├── index.html
│   └── about.html
├── app.py
├── model.pkl
├── Procfile
├── README.md
├── requirements.txt
├── train_model.py
└── mushrooms.csv
```

## 🛠️ Tech Stack
- **Backend**: Python, Flask, Scikit-Learn
- **Frontend**: HTML5, Bootstrap 5, Font Awesome
- **Deployment**: Render / Railway (Gunicorn)

## 📊 Dataset
- **Sumber**: UCI Machine Learning Repository
- **Total Sampel**: 8.124
- **Fitur**: 22 atribut kategorikal
- **Label**: Edible (e) / Poisonous (p)
