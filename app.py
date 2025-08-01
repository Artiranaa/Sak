import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import datetime

# Page config
st.set_page_config(page_title="📈 Live Stock Market Dashboard", layout="wide")
st.title("📊 Live Stock Market Dashboard")
st.markdown("View real-time stock prices, trends, and trading volume interactively.")

# Sidebar
symbols = st.sidebar.multiselect(
    "Select Stocks to View",
    ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "IBM", "INTC"],
    default=["AAPL", "MSFT", "GOOGL"]
)

start_date = st.sidebar.date_input("Start Date", datetime.date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())
chart_type = st.sidebar.selectbox("Select Chart Type", ["Line", "Area", "Bar"])

# Load data
if symbols:
    data = yf.download(symbols, start=start_date, end=end_date)
    data.columns = ['_'.join(col).strip('_') if isinstance(col, tuple) else col for col in data.columns]
    data.reset_index(inplace=True)

    st.subheader("📅 Raw Data Preview")
    st.dataframe(data.head(), use_container_width=True)

    # Tabs for visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Closing Price", 
        "📉 Open Price", 
        "📊 Volume Traded", 
        "📈 % Daily Change"
    ])

    # --- Charting Functions ---
    def plot_price(data, col_prefix, title, chart_type):
        fig = px.line() if chart_type == "Line" else px.area() if chart_type == "Area" else px.bar()
        for sym in symbols:
            fig.add_scatter(
                x=data['Date'],
                y=data[f'{col_prefix}_{sym}'],
                mode='lines' if chart_type != 'Bar' else 'markers',
                name=sym
            )
        fig.update_layout(title=title, xaxis_title="Date", yaxis_title="Price (USD)")
        return fig

    def plot_volume(data, chart_type):
        fig = px.area() if chart_type == "Area" else px.line() if chart_type == "Line" else px.bar()
        for sym in symbols:
            fig.add_scatter(
                x=data['Date'],
                y=data[f'Volume_{sym}'],
                stackgroup='one' if chart_type == "Area" else None,
                mode='lines' if chart_type != 'Bar' else 'markers',
                name=sym
            )
        fig.update_layout(title="Daily Volume Traded", xaxis_title="Date", yaxis_title="Volume")
        return fig

    def plot_daily_change(data):
        fig = px.line()
        for sym in symbols:
            daily_return = data[f'Close_{sym}'].pct_change() * 100
            fig.add_scatter(
                x=data['Date'],
                y=daily_return,
                mode='lines',
                name=sym
            )
        fig.update_layout(title="📈 % Daily Change", xaxis_title="Date", yaxis_title="Change (%)")
        return fig

    # --- Tabs Content ---
    with tab1:
        st.plotly_chart(plot_price(data, "Close", "Closing Price Trend", chart_type), use_container_width=True)

    with tab2:
        st.plotly_chart(plot_price(data, "Open", "Open Price Trend", chart_type), use_container_width=True)

    with tab3:
        st.plotly_chart(plot_volume(data, chart_type), use_container_width=True)

    with tab4:
        st.plotly_chart(plot_daily_change(data), use_container_width=True)

    # Option to download
    st.sidebar.markdown("### 📥 Download Data")
    csv = data.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button("Download CSV", csv, "stock_data.csv", "text/csv")

else:
    st.warning("👈 Please select at least one stock symbol to view data.")
