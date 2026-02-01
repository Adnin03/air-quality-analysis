import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

# Set style seaborn
sns.set(style='dark')

# Function untuk menyiapkan monthly_trend_df
def create_monthly_trend_df(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    monthly_trend_df = df.resample(rule='M', on='datetime').agg({
        'PM2.5':'mean'
    }).reset_index()
    return monthly_trend_df

# Membaca file csv
current_dir = os.path.dirname(os.path.abspath(__file__))
main_df = pd.read_csv(os.path.join(current_dir, 'main_df.csv'))
main_df['datetime'] = pd.to_datetime(main_df['datetime'])

# Menyiapkan DataFrame
monthly_trend_df = create_monthly_trend_df(main_df)

# Filter Waktu
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>Air Quality Analysis</h1>", unsafe_allow_html=True)
    img_path = os.path.join(current_dir, 'awan.png')
    st.image(img_path)
    
    min_date = main_df['datetime'].min()
    max_date = main_df['datetime'].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df_fitered = main_df[(
    (main_df['datetime'] >= str(start_date)) &
    (main_df['datetime'] <= str(end_date))
)]

# Filter Stasiun 
with st.sidebar:
    selected_stations = st.multiselect(
        label='Pilih Stasiun',
        options=main_df['station'].unique(),
        default=[]
    )
    
main_df_fitered = main_df_fitered[main_df_fitered['station'].isin(selected_stations)]

st.header('Air Quality Analysis Dashboard ☁️')

st.subheader('Informasi Ringkas Kualitas Udara')

col1, col2 = st.columns(2)
with col1:
    avg_pm25 = main_df['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", value=f"{avg_pm25:.2f} µg/m³")

with col2:
    max_temp = main_df['TEMP'].max()
    st.metric("Suhu Maksimum", value=f"{max_temp:.1f} °C")

# Menampilkan pertanyaan pertama
st.subheader('Tren Rata-rata PM2.5 Seluruh Stasiun (2013-2017)')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_trend_df['datetime'],
    monthly_trend_df['PM2.5'],
    marker='o',
    linewidth=2,
    color='#3498db'
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_ylabel('Rata-rata Konsentrasi', fontsize=20)
st.pyplot(fig)

with st.expander('Lihat Insight Tren'):
    st.write(
        """Grafik menunjukkan pola musiman di mana kadar PM2.5 melonjak tinggi pada awal tahun (Januari-Maret) dan cenderung menurun di pertengahan tahun. Puncak tertinggi terjadi pada awal 2014, 2016, dan 2017"""
    )
    
# Menampilkan pertanyaan kedua
st.subheader('Korelasi antara Suhu (TEMP) dan Konsentrasi PM2.5 di Aotizhongxin')
df_aoti = main_df[main_df['station'] == 'Aotizhongxin']
correlation = df_aoti['TEMP'].corr(df_aoti['PM2.5'])

fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(
    data=df_aoti,
    x='TEMP',
    y='PM2.5',
    scatter_kws={'alpha': 0.3, 'color': 'skyblue'},
    line_kws={'color': 'red'},
    ax=ax
)

ax.set_title(f'Koefisien Korelasi: {correlation:.2f}', fontsize=14)
ax.set_xlabel('Suhu (Celsius)', fontsize=12)
ax.set_ylabel('Konsentrasi PM2.5 (µg/m³)', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)
with st.expander('Lihat Insight Korelasi'):
    st.write(
        f"""
        Berdasarkan grafik di atas, ditemukan korelasi **negatif yang lemah ({correlation:.2f})** antara suhu udara dan konsentrasi PM2.5 di stasiun Aotizhongxin. 
        
        Hal ini menunjukkan bahwa peningkatan suhu cenderung diikuti oleh sedikit penurunan kadar PM2.5. Hal ini kemungkinan disebabkan oleh kondisi atmosfer yang lebih tidak stabil saat suhu panas, sehingga memudahkan penyebaran polutan. Namun, karena nilainya mendekati nol, suhu bukanlah faktor tunggal utama yang menentukan kualitas udara di lokasi ini.
        """
    )
    
st.caption('Copyright (c) Dicoding 2026')