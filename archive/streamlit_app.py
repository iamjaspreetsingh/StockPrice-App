import streamlit as  st
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.write("# Stock Price Analyser")

"## by JS"

chart_data = pd.DataFrame(
    np.random.randn(200, 3),
    columns=["a", "b", "c"])

st.bar_chart(chart_data)

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)

# symbol = 'AAPL'
symbol = st.selectbox('Which stock symbol would you analyse?', 
                      ['AAPL','GOOG','TSLA'])

# Initialization
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# Session State also supports attribute based syntax
# if 'key' not in st.session_state:
#     st.session_state.key = 'value'

# Read
st.write(st.session_state.key)

# st.session_state.key2 = 'value2'     # Attribute API
st.session_state['key2'] = 'value2'  # Dictionary like API
st.write(st.session_state)

# Delete all the items in Session state
# for key in st.session_state.keys():
#     del st.session_state[key]
# st.write(st.session_state)

st.text_input("Your name", key="name")

# This exists now:
# st.session_state.name
# st.write(st.session_state)


def form_callback():
    st.write(st.session_state.my_slider)
    st.write(st.session_state.my_checkbox)
    
with st.form(key='my_form'):
    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
    submit_button = st.form_submit_button(label='Submit', on_click=form_callback)

# Only the st.form_submit_button has a callback in forms. Other widgets inside a form are not allowed to have callbacks.
# on_change and on_click events are only supported on input type widgets.
# Modifying the value of a widget via the Session state API, after instantiating it, is not allowed and will raise a StreamlitAPIException. For example:
# slider = st.slider(
#     label='My Slider', min_value=1,
#     max_value=10, value=5, key='my_slider')
# st.session_state.my_slider = 7
# # Throws an exception!


col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input('Please enter start date ', datetime.date(2019,7,6))

with col2:
    end_date = st.date_input('Please enter end date ', datetime.date(2022,12,31))

ticker_data = yf.Ticker(symbol)
ticker_df = ticker_data.history(period='1d', start=start_date, end=end_date)

st.write("### Stock Price Data")

st.dataframe(ticker_df)
# can simply write
# ticker_df

# st.write("### Apple's Chart - Closing Prices")
st.write(f"### {symbol}'s Chart - Closing Prices")

st.line_chart(ticker_df['Close'])
            #   , x=None, y=None, width=0, height=0, use_container_width=True)

st.write("### Apple's Chart - Volume")

st.line_chart(ticker_df['Volume'])

