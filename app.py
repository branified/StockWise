# Import Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
from keras.models import load_model
import streamlit as streamlit

start = '2010-01-01'
end = '2019-12-31'

st.title("StockWise")

user_input = st.text_input("Enter Stock Ticker", "AAPL")
df = pdr.get_data_yahoo(user_input, start=start, end=end)

# Describing Data
st.subheader("Data from 2010 - 2019")
st.write(df.describe())