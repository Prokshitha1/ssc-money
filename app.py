import streamlit as st
import google.generativeai as genai
import yfinance as yf
import plotly.graph_objects as go

# Initialize the Gemini API key
genai.configure(api_key="AIzaSyCYglyfcX2HUAgjCZ2M6gARfC-zoPg2txc")

# Function to fetch stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    history = stock.history(period="1y")
    
    return info, history

# Function to display stock chart
def plot_stock_chart(history):
    fig = go.Figure(data=[go.Candlestick(
        x=history.index,
        open=history['Open'],
        high=history['High'],
        low=history['Low'],
        close=history['Close'],
        name="Stock Price"
    )])
    fig.update_layout(title="Stock Price Chart", xaxis_title="Date", yaxis_title="Price", template="plotly_dark")
    st.plotly_chart(fig)

# Function to get peers and holdings (stubbed for now)
def get_peers_and_holdings(ticker):
    peers = ["Peer 1", "Peer 2", "Peer 3"]
    holdings = {"Institution A": 10.0, "Institution B": 5.0}
    
    return peers, holdings

# Function to generate insights using Gemini AI
def get_stock_insights(ticker):
    try:
        response = genai.Completion.create(
            model="google/generative-ai", 
            prompt=f"Provide an analysis and summary for the stock {ticker} based on its recent performance, including its financials, trends, and market sentiment.",
            max_output_tokens=200
        )
        return response['choices'][0]['text']
    except Exception as e:
        return f"Error generating insights: {e}"

# Streamlit layout
st.set_page_config(page_title="Stock Search Engine", page_icon="📈", layout="wide")

# Title
st.title("📈 Stock Search Engine")

# Stock search box
ticker = st.text_input("Enter Stock Ticker", "AAPL")

if ticker:
    # Fetch stock data
    info, history = get_stock_data(ticker)

    # Create columns with color styling and descriptions on the left
    col1, col2, col3, col4 = st.columns(4)

    # Column 1: Stock Chart
    with col1:
        st.markdown("<h3 style='color: #00bfae;'>📊 Stock Chart</h3>", unsafe_allow_html=True)
        plot_stock_chart(history)

    # Column 2: Key Metrics
    with col2:
        st.markdown("<h3 style='color: #FF6347;'>📊 Key Metrics</h3>", unsafe_allow_html=True)
        st.write(f"**PE Ratio:** {info.get('trailingPE', 'N/A')}")
        st.write(f"**PB Ratio:** {info.get('priceToBook', 'N/A')}")
        st.write(f"**EPS:** {info.get('trailingEps', 'N/A')}")
        st.write(f"**Book Value:** {info.get('bookValue', 'N/A')}")
        st.write(f"**Volume:** {info.get('volume', 'N/A')}")
        st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")

    # Column 3: Holdings
    with col3:
        st.markdown("<h3 style='color: #FFD700;'>🏢 Holdings</h3>", unsafe_allow_html=True)
        holdings = get_peers_and_holdings(ticker)[1]
        for institution, percent in holdings.items():
            st.write(f"{institution}: {percent}%")

    # Column 4: Peers
    with col4:
        st.markdown("<h3 style='color: #32CD32;'>🔗 Peers</h3>", unsafe_allow_html=True)
        peers = get_peers_and_holdings(ticker)[0]
        for peer in peers:
            st.write(peer)

    # Stock Insights (below the columns)
    st.subheader("✨ Stock Insights")
    insights = get_stock_insights(ticker)
    st.write(insights)

# Footer with color animation
footer_html = """
<style>
/* Keyframe animation for changing colors */
@keyframes colorChange {
  0% {color: #FF6347;}   /* Tomato */
  25% {color: #FFD700;}  /* Gold */
  50% {color: #00bfae;}  /* Teal */
  75% {color: #32CD32;}  /* Lime Green */
  100% {color: #FF6347;} /* Tomato */
}

/* Style for footer */
footer {
  position: fixed;
  bottom: 10px;
  width: 100%;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  animation: colorChange 3s infinite;
  font-family: 'Arial', sans-serif;
  background-color: rgba(0, 0, 0, 0.8); /* semi-transparent background */
  padding: 10px;
  color: white;
  border-radius: 5px;
}
</style>
<footer>
    <p>This app is made by Shiva Sai Chakradhar</p>
</footer>
"""

st.markdown(footer_html, unsafe_allow_html=True)
