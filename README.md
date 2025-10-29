# 🎵 Sistem Rekomendasi Lagu Berdasarkan Mood Pengguna

Sistem rekomendasi lagu yang menggunakan **Content-Based Filtering** untuk memberikan rekomendasi lagu berdasarkan mood pengguna yang diinput melalui formulir web.

## 📋 Fitur Utama

- ✅ **Content-Based Filtering**: Menggunakan cosine similarity untuk menghitung kemiripan lagu
- ✅ **Formulir Input Sederhana**: Hanya 2 input - Mood dan Level Energi
- ✅ **Filter Ganda**: Filter berdasarkan mood dan energi pengguna
- ✅ **Responsive Design**: Tampilan yang responsif di berbagai perangkat
- ✅ **Real-time Statistics**: Menampilkan statistik dataset secara real-time
- ✅ **Beautiful UI**: Desain modern dengan gradient dan animasi
- ✅ **No Duplicate Songs**: Sistem memastikan setiap lagu unik dalam hasil rekomendasi

## 🛠️ Teknologi yang Digunakan

### Backend

- **Flask**: Web framework Python
- **Pandas**: Data manipulation dan analysis
- **NumPy**: Komputasi numerik
- **Scikit-learn**: Machine learning (Cosine Similarity, LabelEncoder, StandardScaler)

### Frontend

- **HTML5**: Struktur halaman web
- **CSS3**: Styling dengan gradient dan animasi
- **JavaScript**: Interaksi dan AJAX requests

## 📊 Dataset

Dataset `music_sentiment_dataset.csv` berisi informasi lagu dengan fitur:

- **User_ID**: ID pengguna
- **User_Text**: Teks input pengguna
- **Sentiment_Label**: Label sentimen (Happy, Sad, Relaxed, Motivated)
- **Recommended_Song_ID**: ID lagu yang direkomendasikan
- **Song_Name**: Nama lagu
- **Artist**: Nama artis
- **Genre**: Genre musik (Pop, Rock, Classical, Hip-Hop, dll)
- **Tempo (BPM)**: Kecepatan lagu dalam Beats Per Minute
- **Mood**: Mood lagu (Joyful, Melancholic, Soothing, Energetic, dll)
- **Energy**: Level energi (High, Medium, Low)
- **Danceability**: Level danceability (High, Medium, Low)

## 🚀 Cara Menjalankan

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi

```powershell
python app.py
```

### 3. Buka Browser

Buka browser dan akses:

```
http://127.0.0.1:5000
```

## 📖 Cara Menggunakan

1. **Pilih Mood**: Pilih mood Anda saat ini (Happy, Sad, Relaxed, atau Motivated)
2. **Pilih Level Energi**: Pilih level energi yang diinginkan (High, Medium, Low)
3. **Klik "Dapatkan Rekomendasi"**: Sistem akan menampilkan 10 lagu yang sesuai dengan mood dan energi Anda

## 🎯 Metodologi Content-Based Filtering

### 1. Preprocessing Data

- Menggunakan seluruh dataset (1000+ entries) untuk variasi rekomendasi
- Encoding fitur kategorikal (Genre, Mood, Energy, Danceability) menggunakan LabelEncoder
- Normalisasi tempo menggunakan StandardScaler

### 2. Feature Engineering

- Membuat feature matrix dari fitur yang telah diencode:
  - Genre_Encoded
  - Mood_Encoded
  - Energy_Encoded
  - Danceability_Encoded
  - Tempo_Normalized

### 3. Similarity Calculation

- Menghitung **Cosine Similarity** antara semua lagu berdasarkan feature matrix
- Menghasilkan similarity matrix untuk menemukan lagu-lagu yang mirip

### 4. Recommendation Process

- Filter lagu berdasarkan Sentiment_Label yang sesuai dengan mood pengguna
- Filter tambahan berdasarkan level energi yang dipilih
- Hapus duplikasi berdasarkan kombinasi Song_Name + Artist
- Shuffle hasil untuk menambah variasi
- Menghitung similarity score dengan random factor untuk variasi hasil
- Mengurutkan lagu berdasarkan similarity score tertinggi
- Mengembalikan 10 rekomendasi lagu unik

## 📐 Formula Cosine Similarity

```
similarity = (A · B) / (||A|| × ||B||)
```

Dimana:

- A dan B adalah feature vectors dari dua lagu
- A · B adalah dot product dari kedua vectors
- ||A|| dan ||B|| adalah magnitude (panjang) dari vectors

## 🌟 Keunggulan Sistem

1. **Akurat**: Menggunakan multiple features untuk similarity calculation
2. **Sederhana**: Hanya 2 input yang diperlukan (Mood & Energy)
3. **Cepat**: Menggunakan pre-computed similarity matrix
4. **User-Friendly**: Interface yang sangat mudah digunakan
5. **No Duplicates**: Memastikan setiap lagu yang direkomendasikan unik
6. **Varied Results**: Menggunakan random factor untuk hasil yang bervariasi setiap request
7. **Scalable**: Mudah untuk menambah fitur atau dataset

## 📁 Struktur Project

```
project/
│
├── app.py                      # Flask application (backend)
├── music_sentiment_dataset.csv # Dataset lagu
├── requirements.txt            # Python dependencies
├── README.md                   # Dokumentasi
│
├── templates/
│   └── index.html             # HTML template
│
└── static/
    ├── style.css              # CSS styling
    └── script.js              # JavaScript frontend logic
```

## 🔧 API Endpoints

### 1. GET `/`

Menampilkan halaman utama dengan formulir input

### 2. POST `/recommend`

Mendapatkan rekomendasi lagu

**Request Body:**

```json
{
  "mood": "Happy",
  "energy": "High"
}
```

**Response:**

```json
{
  "message": "Found 10 recommendations for you!",
  "recommendations": [
    {
      "song_id": "S2",
      "song_name": "Happy",
      "artist": "Pharrell Williams",
      "genre": "Pop",
      "tempo": 160,
      "mood": "Joyful",
      "energy": "High",
      "danceability": "High",
      "sentiment": "Happy"
    }
  ]
}
```

### 3. GET `/stats`

Mendapatkan statistik dataset

**Response:**

```json
{
  "total_songs": 1000,
  "genres": {
    "Pop": 150,
    "Rock": 120,
    "Hip-Hop": 100,
    "Classical": 90,
    "Funk": 80,
    "Ambient": 70
  },
  "moods": {
    "Joyful": 200,
    "Melancholic": 180,
    "Emotional": 150,
    "Energetic": 170,
    "Soothing": 140,
    "Calm": 90,
    "Powerful": 70
  },
  "energy_levels": { "High": 400, "Low": 350, "Medium": 250 }
}
```

## 🎓 Use Case

Sistem ini cocok untuk:

- 📱 Aplikasi streaming musik
- 🎧 Playlist generator
- 💡 Music therapy applications
- 🎵 Personal music assistant
- 📊 Music analytics platform

## 👨‍💻 Developer

Dibuat untuk tugas **Sistem Pemberi Rekomendasi** - Semester 7 (2025)

## 📝 License

Educational purposes only.

## 🙏 Acknowledgments

- Dataset: Music Sentiment Dataset
- Method: Content-Based Filtering dengan Cosine Similarity
- Framework: Flask, Scikit-learn

---

**Selamat mencoba! 🎵✨**
