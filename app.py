import streamlit as st
import google.generativeai as genai
import yfinance as yf
import plotly.graph_objects as go
import os

# Initialize the Gemini API key (using secrets or environment variable)
api_key = os.getenv("AIzaSyCYglyfcX2HUAgjCZ2M6gARfC-zoPg2txc")
genai.configure(api_key=api_key)

# Function to fetch stock data from Yahoo Finance
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    history = stock.history(period="1y")
    
    return info, history

# Function to plot stock price chart
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

# Function to generate LLM-based stock insights
def generate_llm_insights(stock_data):
    prompt = f"""
    Please provide an insightful summary of the stock performance based on the following details:

    Stock Information:
    - PE Ratio: {stock_data.get('trailingPE', 'N/A')}
    - PB Ratio: {stock_data.get('priceToBook', 'N/A')}
    - EPS: {stock_data.get('trailingEps', 'N/A')}
    - Market Cap: {stock_data.get('marketCap', 'N/A')}
    - Volume: {stock_data.get('volume', 'N/A')}
    
    Financial Trends:
    - Describe the overall performance and trends based on the above information. Consider market conditions, growth potential, and any possible future outlook.

    Provide your response in a concise, informative manner.
    """
    
    try:
        # Generate LLM Insights using Gemini API
        response = genai.Completion.create(
            model="google/generative-ai", 
            prompt=prompt,
            max_output_tokens=300
        )
        insights = response['choices'][0]['text']
        return insights.strip()
    except Exception as e:
        return f"Error generating insights: {e}"

# Streamlit Layout
st.set_page_config(page_title="Stock Search Engine", page_icon="📈", layout="wide")

# Title and ticker input
st.title("📈 Stock Search Engine")
ticker = st.text_input("Enter Stock Ticker", "AAPL")

if ticker:
    # Fetch stock data
    info, history = get_stock_data(ticker)

    # Create columns for different sections
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
        st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
        st.write(f"**Volume:** {info.get('volume', 'N/A')}")

    # Column 3: Holdings
    with col3:
        st.markdown("<h3 style='color: #FFD700;'>🏢 Holdings</h3>", unsafe_allow_html=True)
        st.write("Here you can see information about major institutional holdings.")

    # Column 4: Peers
    with col4:
        st.markdown("<h3 style='color: #32CD32;'>🔗 Peers</h3>", unsafe_allow_html=True)
        st.write("Here you can see information about competitors or similar stocks.")

    # LLM Insights Section
    st.subheader("✨ LLM Stock Insights")
    insights = generate_llm_insights(info)
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
