    # python -m pip install --upgrade pip
    # pip install plotly
    # pip install cufflinks
    # pip install chart_studio
    # pip install yfinance --upgrade --no-cache-dir
import streamlit as st # retrieve the web application 
import yfinance as yf # retrieve the stock data and company information 
import pandas as pd # dataframe visuals 
import cufflinks as cf # creating the nice plots
import datetime # able us to input date information
import numpy as np
import plotly
import plotly.graph_objects as go


# App Title
st.markdown('''
#   TT WEALTH MANAGEMENT 

INCREASES YOUR LIFE QUALITY!

''')
st.write('---')

# Sidebar
st.sidebar.subheader('Requested Information')
start_date = st.sidebar.date_input("Start date", datetime.date(2021, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2023, 3, 9))
ticker_list = pd.read_csv('StocksFull.csv')
tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list)

# Retrieving tickers data
st.write(tickerSymbol)
final_df = pd.DataFrame({})
ticker = tickerSymbol
tickerData = yf.Ticker(ticker) # get ticker data
tickerDf = tickerData.history(period='1d', start='2023-01-01', end='2023-02-28') # get the history of ticker
tickerDf['ticker']=ticker
if final_df.shape[0]==0:
    final_df = tickerDf
else:
    final_df = pd.concat([final_df, tickerDf])
final_df
    
# Bollinger Bands
st.header('**Bollinger Bands**')
qf = cf.QuantFig(tickerDf, title=ticker, legend='top', name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

# Candle Stick Bar
st.header('**Candle Sticks**')
qf.add_sma([10,20],width=2,color=['green','lightgreen'],legendgroup=True)
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

# RSI
st.header('**RSI**')
qf.add_rsi(periods=20,color='java')
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

qf.add_volume()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

qf.add_macd()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)



