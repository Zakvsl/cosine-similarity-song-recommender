"""
Sistem Rekomendasi Lagu Berdasarkan Mood Pengguna
Menggunakan Metode Content-Based Filtering dengan Cosine Similarity
"""

# Import library yang diperlukan
from flask import Flask, render_template, request, jsonify  # Framework web Flask
import pandas as pd  # Untuk manipulasi data
import numpy as np  # Untuk operasi numerik dan array
from sklearn.preprocessing import LabelEncoder, StandardScaler  # Untuk encoding dan normalisasi data
from sklearn.metrics.pairwise import cosine_similarity  # Untuk menghitung similarity antar lagu
import warnings
warnings.filterwarnings('ignore')  # Menonaktifkan warning agar output lebih bersih

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Memuat dataset musik dari file CSV
df = pd.read_csv('music_sentiment_dataset.csv')

# ========== PREPROCESSING DATA ==========
def preprocess_data():
    """
    Fungsi untuk melakukan preprocessing pada dataset musik
    
    Langkah-langkah:
    1. Mengambil kolom-kolom yang diperlukan dari dataset
    2. Encoding fitur kategorikal menjadi angka (untuk perhitungan similarity)
    3. Normalisasi tempo agar skala seragam
    
    Returns:
        songs_df: DataFrame yang sudah diproses
        encoders: LabelEncoder untuk masing-masing fitur kategorikal
        scaler: StandardScaler untuk normalisasi tempo
    """
    
    # Mengambil semua baris dari dataset (tidak menghapus duplikat untuk mendapat variasi lebih banyak)
    # Kolom yang diambil: User_ID, Sentiment_Label, Song info, dan fitur-fitur musik
    songs_df = df[['User_ID', 'Sentiment_Label', 'Recommended_Song_ID', 'Song_Name', 
                    'Artist', 'Genre', 'Tempo (BPM)', 'Mood', 'Energy', 'Danceability']].copy()
    
    # Membuat encoder untuk setiap fitur kategorikal
    # LabelEncoder mengubah kategori (string) menjadi angka (integer)
    le_genre = LabelEncoder()  # Untuk Genre (Pop, Rock, Hip-Hop, dll)
    le_mood = LabelEncoder()  # Untuk Mood (Joyful, Melancholic, dll)
    le_energy = LabelEncoder()  # Untuk Energy (High, Medium, Low)
    le_dance = LabelEncoder()  # Untuk Danceability (High, Medium, Low)
    
    # Melakukan encoding pada setiap fitur kategorikal
    # Contoh: Pop=0, Rock=1, Hip-Hop=2, dst.
    songs_df['Genre_Encoded'] = le_genre.fit_transform(songs_df['Genre'])
    songs_df['Mood_Encoded'] = le_mood.fit_transform(songs_df['Mood'])
    songs_df['Energy_Encoded'] = le_energy.fit_transform(songs_df['Energy'])
    songs_df['Danceability_Encoded'] = le_dance.fit_transform(songs_df['Danceability'])
    
    # Normalisasi tempo menggunakan StandardScaler
    # StandardScaler mengubah data agar memiliki mean=0 dan std=1
    # Ini penting agar tempo (yang nilainya besar, misal 50-160 BPM) 
    # tidak mendominasi perhitungan similarity
    scaler = StandardScaler()
    songs_df['Tempo_Normalized'] = scaler.fit_transform(songs_df[['Tempo (BPM)']])
    
    return songs_df, le_genre, le_mood, le_energy, le_dance, scaler

# Memanggil fungsi preprocessing dan menyimpan hasilnya
songs_df, le_genre, le_mood, le_energy, le_dance, scaler = preprocess_data()

# ========== MEMBUAT FEATURE MATRIX ==========
# Feature matrix adalah matriks yang berisi semua fitur yang akan digunakan
# untuk menghitung similarity antar lagu
feature_columns = ['Genre_Encoded', 'Mood_Encoded', 'Energy_Encoded', 
                   'Danceability_Encoded', 'Tempo_Normalized']

# Mengambil nilai dari kolom-kolom fitur dan mengubahnya menjadi array NumPy
# Shape: (jumlah_lagu, 5) karena ada 5 fitur
feature_matrix = songs_df[feature_columns].values

# ========== MENGHITUNG SIMILARITY MATRIX ==========
# Cosine Similarity mengukur kesamaan antar dua vektor berdasarkan sudut di antara mereka
# Formula: cosine_similarity = (A · B) / (||A|| × ||B||)
# Nilai similarity berkisar antara 0 (tidak mirip) hingga 1 (sangat mirip)
# Hasil: matriks berukuran (jumlah_lagu, jumlah_lagu)
# similarity_matrix[i][j] = similarity antara lagu ke-i dan lagu ke-j
similarity_matrix = cosine_similarity(feature_matrix)

# ========== FUNGSI REKOMENDASI UTAMA ==========
def get_recommendations(user_mood, user_energy, user_genre=None, top_n=10):
    """
    Mendapatkan rekomendasi lagu berdasarkan preferensi pengguna
    Menggunakan metode Content-Based Filtering dengan Cosine Similarity
    
    Args:
        user_mood (str): Mood pengguna (Happy, Sad, Relaxed, Motivated)
        user_energy (str): Level energi yang diinginkan (High, Medium, Low)
        user_genre (str): Genre musik (opsional, default: None)
        top_n (int): Jumlah rekomendasi yang diinginkan (default: 10)
    
    Returns:
        list: List berisi dictionary informasi lagu yang direkomendasikan
    """
    
    # ===== LANGKAH 1: FILTER BERDASARKAN MOOD =====
    # Mencari lagu yang Sentiment_Label-nya cocok dengan input mood pengguna
    mood_songs = songs_df[songs_df['Sentiment_Label'].str.lower() == user_mood.lower()].copy()
    
    # Jika tidak ada hasil, coba mapping ke Mood yang lebih spesifik
    if mood_songs.empty:
        # Mapping sentiment pengguna ke mood spesifik di dataset
        # Contoh: Happy → bisa Joyful atau Energetic
        sentiment_to_mood = {
            'happy': ['joyful', 'energetic'],
            'sad': ['melancholic', 'emotional'],
            'relaxed': ['soothing', 'calm'],
            'motivated': ['energetic', 'powerful']
        }
        user_mood_lower = user_mood.lower()
        target_moods = sentiment_to_mood.get(user_mood_lower, [user_mood_lower])
        
        # Filter lagu berdasarkan mood yang sudah dimapping
        mood_songs = songs_df[songs_df['Mood'].str.lower().isin(target_moods)].copy()
    
    # Jika masih tidak ada hasil, return list kosong
    if mood_songs.empty:
        return []
    
    # ===== LANGKAH 2: FILTER BERDASARKAN ENERGI =====
    # Jika pengguna memilih level energi tertentu, filter lagi
    if user_energy:
        energy_filtered = mood_songs[mood_songs['Energy'].str.lower() == user_energy.lower()]
        # Hanya update jika ada hasil, kalau tidak ada tetap pakai yang lama
        if not energy_filtered.empty:
            mood_songs = energy_filtered
    
    # ===== LANGKAH 3: FILTER BERDASARKAN GENRE (OPSIONAL) =====
    # Filter berdasarkan genre jika user memilih genre tertentu (bukan 'All')
    if user_genre and user_genre != 'All':
        genre_filtered = mood_songs[mood_songs['Genre'].str.lower() == user_genre.lower()]
        # Hanya update jika ada hasil
        if not genre_filtered.empty:
            mood_songs = genre_filtered
    
    # Cek lagi apakah masih ada lagu setelah semua filtering
    if mood_songs.empty:
        return []
    
    # ===== LANGKAH 4: HAPUS DUPLIKASI =====
    # Menghapus lagu yang duplikat berdasarkan kombinasi Nama Lagu + Artis
    # Contoh: "Happy - Pharrell Williams" hanya muncul 1x meskipun ada berkali-kali di dataset
    unique_songs = mood_songs.drop_duplicates(subset=['Song_Name', 'Artist'], keep='first')
    
    # Mendapatkan index (posisi) dari lagu-lagu unik di DataFrame
    song_indices = unique_songs.index.tolist()
    
    # ===== LANGKAH 5: SHUFFLE UNTUK VARIASI =====
    # Mengacak urutan lagu agar tidak monoton
    np.random.shuffle(song_indices)
    
    # ===== LANGKAH 6: RANKING BERDASARKAN SIMILARITY =====
    if len(song_indices) > top_n:
        # Jika lagu lebih banyak dari yang diminta, ranking berdasarkan similarity
        similarity_scores = []
        
        for idx in song_indices:
            # Mendapatkan similarity score lagu ini dengan semua lagu lain
            # similarity_matrix[idx] adalah 1 baris berisi similarity dengan semua lagu
            scores = similarity_matrix[idx]
            
            # Menghitung rata-rata similarity sebagai score
            avg_score = np.mean(scores)
            
            # Menambahkan random factor untuk variasi hasil
            # Setiap request akan menghasilkan urutan yang sedikit berbeda
            random_factor = np.random.uniform(0.85, 1.15)
            
            # Simpan tuple (index, score) untuk sorting nanti
            similarity_scores.append((idx, avg_score * random_factor))
        
        # Mengurutkan lagu berdasarkan similarity score (tertinggi ke terendah)
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Mengambil top N lagu dengan score tertinggi
        top_indices = [i[0] for i in similarity_scores[:top_n]]
    else:
        # Jika jumlah lagu kurang dari top_n, ambil semua yang ada
        top_indices = song_indices[:top_n]
    
    # ===== LANGKAH 7: MEMBUAT LIST REKOMENDASI =====
    recommendations = []
    seen_songs = set()  # Set untuk tracking lagu yang sudah ditambahkan
    
    for idx in top_indices:
        # Mengambil data lagu berdasarkan index
        song = songs_df.iloc[idx]
        
        # Membuat key unik untuk identifikasi lagu (Nama + Artis)
        song_key = f"{song['Song_Name']}_{song['Artist']}"
        
        # Double-check: hanya tambahkan jika belum pernah ditambahkan
        if song_key not in seen_songs:
            seen_songs.add(song_key)
            
            # Membuat dictionary berisi informasi lagu
            recommendations.append({
                'song_id': song['Recommended_Song_ID'],
                'song_name': song['Song_Name'],
                'artist': song['Artist'],
                'genre': song['Genre'],
                'tempo': int(song['Tempo (BPM)']),
                'mood': song['Mood'],
                'energy': song['Energy'],
                'danceability': song['Danceability'],
                'sentiment': song['Sentiment_Label']
            })
    
    return recommendations

# ========== ROUTE: HALAMAN UTAMA ==========
@app.route('/')
def index():
    """
    Route untuk menampilkan halaman utama (index.html)
    Menyediakan pilihan mood dan energy level untuk dropdown form
    """
    # Daftar sentiment yang tersedia untuk dipilih user
    sentiment_labels = ['Happy', 'Sad', 'Relaxed', 'Motivated']
    
    # Mengambil unique values dari kolom Energy dan mengurutkannya
    energy_levels = sorted(songs_df['Energy'].unique().tolist())
    
    # Render template HTML dengan data yang diperlukan
    return render_template('index.html', moods=sentiment_labels, energy_levels=energy_levels)


# ========== ROUTE: API REKOMENDASI ==========
@app.route('/recommend', methods=['POST'])
def recommend():
    """
    API endpoint untuk mendapatkan rekomendasi lagu
    Method: POST
    Input: JSON dengan 'mood' dan 'energy'
    Output: JSON dengan list rekomendasi lagu
    """
    try:
        # Mengambil data JSON dari request
        data = request.json
        user_mood = data.get('mood')  # Mood yang dipilih user
        user_energy = data.get('energy')  # Energy level yang dipilih user
        
        # Validasi: Mood harus diisi
        if not user_mood:
            return jsonify({'error': 'Mood is required'}), 400
        
        # Validasi: Energy level harus diisi
        if not user_energy:
            return jsonify({'error': 'Energy level is required'}), 400
        
        # Memanggil fungsi get_recommendations untuk mendapatkan rekomendasi
        # Parameter: mood, energy, genre=None, top_n=10
        recommendations = get_recommendations(user_mood, user_energy, user_genre=None, top_n=10)
        
        # Jika tidak ada rekomendasi yang ditemukan
        if not recommendations:
            return jsonify({
                'message': 'No songs found matching your preferences. Try different criteria.', 
                'recommendations': []
            })
        
        # Return response dengan status success
        return jsonify({
            'message': f'Found {len(recommendations)} recommendations for you!',
            'recommendations': recommendations
        })
    
    except Exception as e:
        # Jika terjadi error, return error message
        return jsonify({'error': str(e)}), 500


# ========== ROUTE: API STATISTIK ==========
@app.route('/stats')
def stats():
    """
    API endpoint untuk mendapatkan statistik dataset
    Method: GET
    Output: JSON dengan statistik genre, mood, dan energy levels
    """
    try:
        # Membuat dictionary berisi statistik dataset
        stats_data = {
            'total_songs': len(songs_df),  # Total jumlah entries dalam dataset
            'genres': songs_df['Genre'].value_counts().to_dict(),  # Distribusi genre
            'moods': songs_df['Mood'].value_counts().to_dict(),  # Distribusi mood
            'energy_levels': songs_df['Energy'].value_counts().to_dict()  # Distribusi energy
        }
        return jsonify(stats_data)
    
    except Exception as e:
        # Jika terjadi error, return error message
        return jsonify({'error': str(e)}), 500


# ========== MENJALANKAN APLIKASI ==========
if __name__ == '__main__':
    # Menampilkan informasi saat aplikasi dimulai
    print("=" * 60)
    print("🎵 Music Recommendation System is running...")
    print("=" * 60)
    print("📊 Dataset loaded successfully!")
    print(f"📀 Total entries in dataset: {len(songs_df)}")
    print(f"🎼 Unique songs: {songs_df[['Song_Name', 'Artist']].drop_duplicates().shape[0]}")
    print(f"🎭 Available moods: {songs_df['Sentiment_Label'].unique().tolist()}")
    print(f"⚡ Energy levels: {sorted(songs_df['Energy'].unique().tolist())}")
    print("=" * 60)
    print("🌐 Open http://127.0.0.1:5000 in your browser")
    print("=" * 60)
    
    # Menjalankan Flask app dengan debug mode
    # debug=True: Auto-reload saat ada perubahan code
    app.run(debug=True)
