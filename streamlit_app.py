import streamlit as  st
import yfinance as yf
import datetime

st.write("# Stock Price Analyser")
# symbol = 'AAPL'
symbol = st.selectbox('Which stock symbol would you analyse?', 
                      ['AAPL','GOOG','TSLA'])

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input('Please enter start date ', datetime.date(2019,7,6))

with col2:
    end_date = st.date_input('Please enter end date ', datetime.date(2022,12,31))

ticker_data = yf.Ticker(symbol)
ticker_df = ticker_data.history(period='1d', start=start_date, end=end_date)

st.write("### Stock Price Data")

st.dataframe(ticker_df)

# st.write("### Apple's Chart - Closing Prices")
st.write(f"### {symbol}'s Chart - Closing Prices")

st.line_chart(ticker_df['Close'])
            #   , x=None, y=None, width=0, height=0, use_container_width=True)

st.write("### Apple's Chart - Volume")

st.line_chart(ticker_df['Volume'])


