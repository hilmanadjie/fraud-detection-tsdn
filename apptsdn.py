import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import base64

# Judul Aplikasi Web
st.markdown('''
# **FRAUD DETECTION PADA SALDO AKHIR NASABAH BPR**
---

**Credit:** App built in `Python` + `Streamlit` by [CUCU JENDRAL TEAMS]

---
''')

# Menambahkan gambar pada aplikasi
image_url = 'https://img.freepik.com/free-photo/fraud-word-magnifying-glass_23-2148783089.jpg?size=626&ext=jpg&ga=GA1.1.335645936.1700024977&semt=aisg'
st.image(image_url, caption='Gambar Ilustrasi', use_column_width=True)

# Fitur Keamanan: Otentikasi
# Accessing the secrets
USERNAME = st.secrets["username"]
PASSWORD = st.secrets["password"]


# Otentikasi Pengguna
user_auth = st.sidebar.text_input("username:")
password_auth = st.sidebar.text_input("password:", type="password")

# Validasi Otentikasi
if user_auth == USERNAME and password_auth == PASSWORD:
    st.success("Otentikasi berhasil! Anda dapat mengakses aplikasi.")
else:
    st.error("Otentikasi gagal. Silakan coba lagi atau hubungi administrator.")
    st.stop()

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

# Definisi fungsi untuk mendapatkan tautan unduhan CSV
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convert to base64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="fraud_audit.csv">Download CSV</a>'
    return href

# Load your dataset from the uploaded file
if uploaded_file is not None:
    # Validasi Nama Kolom
    required_columns = ['NASABAH ID', 'SALDO AKHIR', 'TRANS TERAKHIR']

    data = pd.read_csv(uploaded_file)

    if set(required_columns).issubset(data.columns):
        st.success("Dataset berisi kolom yang diperlukan.")
    else:
        st.error(f"Dataset tidak memiliki kolom yang diperlukan. Kolom yang diperlukan: {', '.join(required_columns)}")
        st.stop()

    # Pilih fitur yang akan digunakan untuk clustering (misalnya, hanya saldo akhir)
    X = data[['SALDO AKHIR']]

    # Standarisasi fitur menggunakan StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Menentukan jumlah cluster (bisa disesuaikan sesuai kebutuhan)
    num_clusters = 2

    # Membuat model k-means
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(X_scaled)

    # Menampilkan nasabah yang berada di cluster minoritas (potensial fraud)
    fraudulent_customers = data[data['cluster'] != data['cluster'].mode().iloc[0]]

    # Menampilkan hasil di Streamlit dengan fitur audit
    st.header("Nasabah yang berpotensi mengalami fraud:")
    
    for index, row in fraudulent_customers.iterrows():
        st.write(f"**Nasabah ID:** {row['NASABAH ID']}")
        st.write(f"**Saldo Akhir:** {row['SALDO AKHIR']}")
        st.write(f"**Detail Transaksi Terakhir:** {row['TRANS TERAKHIR']}")  # Ganti dengan kolom yang sesuai
        st.write("---")  # Garis pemisah antara nasabah

    # Tambahkan opsi untuk mengunduh data audit dalam format CSV
    st.markdown("### Download Audit Data")
    st.write("Anda bisa mengunduh data audit nasabah yang berpotensi mengalami fraud.")
    st.markdown(get_table_download_link(fraudulent_customers), unsafe_allow_html=True)
else:
    st.warning("Silakan unggah file CSV untuk melanjutkan.")
