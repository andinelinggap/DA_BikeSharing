import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
hari_df = pd.read_csv('day.csv')  
hari_df['dteday'] = pd.to_datetime(hari_df['dteday'])

# Set page title and favicon
st.set_page_config(page_title="Proyek Dashboard Andine Lingga✨", page_icon="📊")

# Judul Dashboard
st.title("Proyek Dashboard Andine Lingga✨")


## Keterangan Visualisasi
st.write("Berikut merupakan Visualisasi data bloxpot pengguna sewa sepeda tiap bulan dan musim pada 2011-2012.")

## Boxplot Pengguna Sepeda setiap musim
st.header('Boxplot Pengguna Sepeda setiap musim')
df_season = hari_df.copy()
plt.figure(figsize=(16,6))
sns.boxplot(
    x="season",
    y="cnt",
    data=df_season,
    hue="season",
    palette="husl",
    dodge=False,  
    legend=False
)
plt.xlabel("Musim")
plt.ylabel("Jumlah Pengguna")
plt.title("Jumlah Pengguna Tiap Musim")
st.pyplot(plt)

## Keterangan Visualisasi
st.write("Berikut merupakan Visualisasi data bloxpot pengguna sewa sepeda tiap bulan pada 2011-2012.")

## Boxplot Pengguna Sepeda setiap bulan
st.header('Boxplot Pengguna Sepeda setiap bulan')
df_month = hari_df.copy()
plt.figure(figsize=(16,6))
sns.boxplot(
    x="mnth",
    y="cnt",
    data=df_month,
    hue="mnth",
    palette="husl",  
    dodge=False,  
    legend=False
)
plt.xlabel("Bulan")
plt.ylabel("Jumlah Pengguna")
plt.title("Jumlah Pengguna Tiap Bulan")
st.pyplot(plt)

## Keterangan Visualisasi
st.write("Berikut merupakan Visualisasi data plot korelasi antara variabel-variabel pada 2011-2012.")

## Plot Korelasi
st.header('Plot Korelasi')
df_corr = hari_df.copy()
df_corr = df_corr[[col for col in df_corr if df_corr[col].nunique() > 1]]
corr = df_corr.corr()

plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(corr, fmt=".2f", linewidths=1, linecolor='black')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
colorbar = heatmap.collections[0].colorbar
colorbar.ax.tick_params(labelsize=10)
plt.tight_layout()
st.pyplot(plt)

# Analisis pergerakan jumlah peminjaman sepeda berubah seiring waktu
st.header('Pergerakan jumlah peminjaman sepeda yang berubah seiring waktu')
df = hari_df.copy()

df_weekly = df.resample('W', on='dteday').mean()
df_weekly['moving_avg'] = df_weekly['cnt'].rolling(window=4).mean()
x = np.arange(len(df_weekly)).reshape(-1, 1)
y = df_weekly['cnt'].values.reshape(-1, 1)
slope, intercept = np.polyfit(x.flatten(), y.flatten(), 1)
df_weekly['trend'] = intercept + slope * x

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=df_weekly.index, y='cnt', data=df_weekly, label='Rata-Rata per Minggu', color='salmon', ax=ax)
sns.lineplot(x=df_weekly.index, y='moving_avg', data=df_weekly, label='Moving Average', linestyle='--', color='green', ax=ax)

plt.xlabel('')
plt.ylabel('Jumlah Peminjaman')
plt.title('Grafik Perkembangan Jumlah Peminjaman Sepeda 2011 - 2012')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
st.write(
    "Analisis data peminjaman sepeda selama 2 tahun menunjukkan fluktuasi mingguan yang kuat dan pola musiman yang jelas. Meskipun prediksi menunjukkan penurunan pada"
    "Januari 2013, tren keseluruhan menunjukkan pertumbuhan yang positif. Strategi promosi dan pemantauan musiman diperlukan untuk pertumbuhan jangka panjang.")
st.pyplot(fig)


# Analisis korelasi antara suhu terhadap total order sepeda
st.header('Korelasi antara suhu terhadap total order sepeda')
st.write("Korelasi antara suhu dan total order sepeda:")
    
# Hitung korelasi antara suhu dan total order sepeda
correlation = hari_df['temp'].corr(hari_df['cnt'])
st.write(f"Korelasi: {correlation}")

# Scatter plot
fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(x=hari_df['temp']*50, y='cnt', data=hari_df, hue='season', ax=ax)
ax.set_xlabel("Suhu (degC)")
ax.set_ylabel("Jumlah Pengguna")
ax.set_title("Pengelompokan penyewaan sepeda antara suhu dan total order sepeda (2011-2012)")
plt.tight_layout()

#Keterangan
st.write("Permintaan untuk sewa sepeda cenderung rendah pada suhu di bawah 20 derajat Celcius, namun meningkat secara signifikan pada rentang suhu 25-30 derajat Celcius. Hal ini" 
         "menunjukkan preferensi pengguna untuk bersepeda pada kondisi cuaca yang lebih hangat dan nyaman, yang dapat mempengaruhi permintaan layanan tersebut.")
# Menampilkan plot menggunakan Streamlit
st.pyplot(fig)
