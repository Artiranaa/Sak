import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime

# Set Streamlit page config
st.set_page_config(page_title="💰 Live Crypto Dashboard", layout="wide")

st.title("💹 Live Cryptocurrency Dashboard")
st.markdown("Track real-time prices and historical trends of popular cryptocurrencies.")

# Sidebar
coins = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    ["BTC", "ETH", "BNB", "ADA", "DOGE", "SOL", "XRP", "LTC"],
    default=["BTC", "ETH"]
)

days = st.sidebar.slider("Days of History", 1, 60, 30)

# API Base URL
def get_crypto_data(coin, limit=30):
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={coin}&tsym=USD&limit={limit}"
    response = requests.get(url)
    data = response.json()["Data"]["Data"]
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['coin'] = coin
    return df

# Fetch and display data
if coins:
    all_data = pd.concat([get_crypto_data(coin, limit=days) for coin in coins])

    st.subheader("📅 Historical Price Data")
    st.dataframe(all_data[['time', 'coin', 'close', 'volumeto']].tail(), use_container_width=True)

    st.subheader("📈 Price Trend")
    fig1 = px.line(all_data, x='time', y='close', color='coin', title='Closing Price Over Time')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📊 Volume Traded")
    fig2 = px.area(all_data, x='time', y='volumeto', color='coin', title='Trading Volume Over Time', groupnorm='percent')
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("👈 Please select at least one cryptocurrency to view data.")
