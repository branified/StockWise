# Import Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
from keras.models import load_model
import streamlit as st

start = '2010-01-01'
end = '2019-12-31'

st.title("StockWise")

user_input = st.text_input("Enter Stock Ticker", "AAPL")
df = pdr.get_data_yahoo(user_input, start=start, end=end)

# Describing Data
st.subheader("Data from 2010 - 2019")
st.write(df.describe())

# Data Visualizations
st.subheader("Closing Price vs Time Chart")
fig = plt.figure(figsize = (12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader("Closing Price vs Time Chart with 100 days Rolling Average")
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader("Closing Price vs Time Chart with 100 & 200 days Rolling Average")
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(ma200)
plt.plot(df.Close)
st.pyplot(fig)

# Splitting Data into Training and Testing
data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.7)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.7):int(len(df))])

# Scaling down training data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

# Fitting training data to scaler as an array. It is scaling down training data into values bewteen 0 and 1
data_training_array = scaler.fit_transform(data_training)

# Load pretrained model
model = load_model('keras_model.h5')

# Testing the model using the 30%
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index = True)

# Scaling data
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
  x_test.append(input_data[i-100: i])
  y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)

scaler = scaler.scale_
scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

#Final Visualization
st.subheader("Predictions vs Original")
fig2 = plt.figure(figsize = (12,6))
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(y_predicted, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)