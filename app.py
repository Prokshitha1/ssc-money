import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from model import predict_prices
from fundamentals import get_fundamentals
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="📈 Stock Analyzer by Shiva Sai Chakradhar", layout="wide")

# CSS Styling
st.markdown("""
    <style>
        .main { background-color: #f0f2f6; }
        .block-container { padding-top: 2rem; }
        .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 18px; font-weight: bold; animation: colorchange 3s infinite; }
        @keyframes colorchange {
            0% { color: red; }
            25% { color: blue; }
            50% { color: green; }
            75% { color: orange; }
            100% { color: red; }
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Stock Price & Financial Status Analyzer")

# Sidebar for ticker input
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)", value="AAPL")
search_btn = st.button("🔍 Search")

if search_btn and ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")

        # Charts Column
        col1, col2, col3, col4 = st.columns([2.5, 2, 1.5, 2])

        with col1:
            st.subheader(f"📈 {ticker} Stock Price Chart")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close'))
            fig.update_layout(title=f"{ticker} Closing Price", xaxis_title="Date", yaxis_title="Price", height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📊 Financial Indicators")
            metrics = get_fundamentals(stock)
            for key, value in metrics.items():
                st.metric(label=key, value=value)

        with col3:
            st.subheader("📈 Predicted Prices (Next 7 Days)")
            predicted = predict_prices(hist['Close'])
            for i, price in enumerate(predicted):
                st.write(f"Day {i+1}: ${price:.2f}")

        with col4:
            st.subheader("🧍 Peers & Holdings")
            st.write("(Static/Optional for now)")
            st.write("Peers: MSFT, GOOG, AMZN")
            st.write("Holdings: BlackRock, Vanguard")

    except Exception as e:
        st.error(f"Failed to fetch data: {e}")

# Footer
st.markdown('<div class="footer">This app is made by Shiva Sai Chakradhar 💡</div>', unsafe_allow_html=True)
