import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf 
import plotly.express as px

st.title("Stock Market Trend Prediction Using Sentiment Analysis")

ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Check if the ticker and start date are provided
if ticker and start_date:
    # Fetch historical stock data
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Check if data is available
    if not data.empty:
        # Display the fetched data in a line chart
        fig = px.line(data, x=data.index, y='Close', title=f'{ticker} Stock Price')
        st.plotly_chart(fig)
        
        pricing_data, predictions = st.tabs(["Pricing Data", "Predictions"])
        
        with pricing_data:
            st.header("Price Movement")
            data2 = data.copy()
            data2['% Change'] = data['Adj Close'] / data2['Adj Close'].shift(1)
            data2.dropna(inplace=True)
            st.write(data2)
            annual_return = data2['% Change'].mean() * 252 * 100 - 1
            st.write('Annual Return:', annual_return, '%')
            stdev = np.std(data2['% Change']) * np.sqrt(252)
            st.write('Standard Deviation:', stdev * 100, '%')
            st.write('Risk-Adjusted Return:', annual_return / (stdev * 100))
        
        with predictions:
            st.header("Predictions")
            st.plotly_chart(fig)
    
    else:
        st.write("No data available for the specified ticker and date range.")
        
else:
    st.write("Please enter a valid ticker and start date.")
