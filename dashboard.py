import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load data yang dibutuhkan
url_df = "https://drive.google.com/file/d/1bOac5gyltTxFWbSAGFZoEeLcJneJx5tI/view?usp=drive_link"
air_df = pd.read_csv(url_df)
air_df["datetime"] = pd.to_datetime(air_df["datetime"])

# Sidebar untuk filter data sesuai keinginan
with st.sidebar:
    st.header("Filter Data")
    stations = st.multiselect("Pilih Daerah", air_df["station"].unique(), default=air_df["station"].unique())
    date_range = st.date_input("Pilih Rentang Tanggal", [air_df["datetime"].min(), air_df["datetime"].max()])
    gas = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]

# Mengambil pilihan dari sidebar untuk dipakai dalam dataframe
filter_df = air_df[
    (air_df["station"].isin(stations)) &
    (air_df["datetime"] >= pd.to_datetime(date_range[0])) &
    (air_df["datetime"] <= pd.to_datetime(date_range[1]))
]
filter_df = filter_df.sort_values("station")
date_df = air_df[
    (air_df["datetime"] >= pd.to_datetime(date_range[0])) &
    (air_df["datetime"] <= pd.to_datetime(date_range[1]))
]
date_df = date_df.sort_values("station")

st.title("⛅️ Air Quality Dataset ⛅️")

# Data Min Mean Max dari polutan
st.subheader("Rangkuman Data")
rangkuman = st.radio(
    label="Pilih Polutan untuk Rangkuman Data",
    options=("PM2.5", "PM10", "SO2", "NO2", "CO", "O3"),
    index=0,
    horizontal=True
)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Polutan", rangkuman)
col2.metric("Terkecil", f"{filter_df[rangkuman].min():.2f}")
col3.metric("Rata-rata", f"{filter_df[rangkuman].mean():.2f}")
col4.metric("Terbesar", f"{filter_df[rangkuman].max():.2f}")

st.subheader("Sebaran Data Kualitas Udara")
mean_gas = filter_df[gas].mean()
mean_gas_wo_co = mean_gas.drop("CO")
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

sns.barplot(x=mean_gas.index, y=mean_gas.values, palette=["#ff6678", "#ff6678", "#ff6678", "#ff6678", "#c9061d", "#ff6678"], ax=ax[0])
ax[0].set_title("Rata-rata Kadar Polutan di Semua Daerah", fontsize = 18)
ax[0].set_ylabel("Kadar Rata-rata")
ax[0].set_xlabel("Polutan")

sns.barplot(x=mean_gas_wo_co.index, y=mean_gas_wo_co.values, palette=["#ff6678", "#c9061d", "#ff6678", "#ff6678", "#ff6678"], ax=ax[1])
ax[1].set_title("Kadar Polutan tanpa CO", fontsize = 18)
ax[1].set_ylabel("Kadar Rata-rata")
ax[1].set_xlabel("Polutan")

st.pyplot(fig)

select_gas = st.radio(
    label="Pilih Polutan untuk Distribusi Tiap Daerah",
    options=("PM2.5", "PM10", "SO2", "NO2", "CO", "O3"),
    index=0,
    horizontal=True,
    key="gas1"
)

fig, ax = plt.subplots(figsize=(14, 8))
sns.boxplot(data=date_df, x="station", y=select_gas, color="#ff6678", ax=ax)
ax.set_title(f"Distribusi Kadar {select_gas} di Tiap Daerah", fontsize=25)
ax.set_ylabel(f"Kadar {select_gas}", fontsize=14)
ax.set_xlabel("Daerah", fontsize=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

st.subheader("Tingkat Polutan di Tiap Daerah")

select2_gas = st.radio(
    label="Pilih Polutan",
    options=("PM2.5", "PM10", "SO2", "NO2", "CO", "O3"),
    index=0,
    horizontal=True,
    key="gas2"
)
fig, ax = plt.subplots(figsize=(14, 8))
sns.lineplot(data=date_df, x="station", y=select2_gas, label=select2_gas, ci=None, marker="o", color="#ff6678", ax=ax)
ax.set_title(f"Tingkat Polutan {select2_gas} di Tiap Daerah", fontsize=25)
ax.set_ylabel(f"Kadar {select2_gas}", fontsize=14)
ax.set_ylim(0)
ax.set_xlabel("Daerah", fontsize=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)
             
st.subheader("Korelasi Antar Variabel")
correlation = filter_df[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "DEWP"]].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt='.2f', linewidths=0.5)
plt.gca().xaxis.set_ticks_position('top')
plt.gca().tick_params(labeltop=True) 
plt.title('Korelasi Antara Suhu, Kelembapan, dan Polutan')
st.pyplot(plt)
