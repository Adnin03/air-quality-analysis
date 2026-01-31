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

st.header('Air Quality Analysis Dashboard ☁️')

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
st.subheader('Korelasi antara Suhu (TEMP) dan Kadar Ozon (O3)')

fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(
    x=main_df['TEMP'],
    y=main_df['O3'],
    scatter_kws={'alpha':0.1, 'color':'#3498db'},
    line_kws={'color':'red'},
    ax=ax
)
ax.set_xlabel('Suhu (Celcius)', fontsize=12)
ax.set_ylabel('Kadar Ozon (O3)', fontsize=12)
st.pyplot(fig)

with st.expander('Lihat Insight Korelasi'):
    st.write(
        """Terdapat korelasi positif yang cukup kuat (0.61) antara suhu udara dan kadar Ozon. Semakin tinggi suhu udara, maka pembentukan Ozon cenderung semakin meningkat"""
    )
    
st.caption('Copyright (c) Dicoding 2026')