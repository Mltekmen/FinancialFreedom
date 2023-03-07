import streamlit as st
import warnings
import yfinance as yf
import riskfolio as rp
import pandas as pd
import matplotlib.pyplot as plt

# Disable warnings
warnings.filterwarnings("ignore")

# Set format for displaying float values
pd.options.display.float_format = '{:.4%}'.format

# Set default start and end dates
start = '2013-03-09'
end = '2023-03-09'

# Define tickers of assets
assets = ['AAPL', 'GE', 'TSLA', 'KRP', 'NMM', 'CVX', 'ET', 'JPM']
assets.sort()

# Define optimization parameters
model='Classic'
rm = 'MV'
obj = 'Sharpe'
hist = True
rf = 0
l = 0
points = 50

# Set up Streamlit app
st.set_page_config(page_title='Portfolio Optimization',
                   page_icon=':money_with_wings:',
                   layout='wide')
st.title('Portfolio Optimization')
st.write('Our portfolio optimization strategy is based on a comprehensive analysis of historical data for selected assets. By leveraging the power of advanced analytics and data-driven insights, we can help you optimize your portfolio for maximum returns and minimum risk. With our proven track record of success, you can trust us to help you achieve your investment goals and maximize your returns')

# Add sidebar for selecting options
st.sidebar.title('Select Options')
ticker_list = st.sidebar.multiselect('Select Tickers', assets, default=assets)
start_date = st.sidebar.date_input('Start Date', value=pd.to_datetime(start))
end_date = st.sidebar.date_input('End Date', value=pd.to_datetime(end))
rm = st.sidebar.selectbox('Risk Measure', ['MV', 'MAD', 'MDD', 'ADD', 'CDaR', 'EDaR', 'CVaR', 'WR', 'MWR', 'UWR', 'SWR', 'DR', 'MDR'], index=0)
obj = st.sidebar.selectbox('Objective Function', ['MinRisk', 'MaxRet', 'Utility', 'Sharpe'], index=3)
model = st.sidebar.selectbox('Model', ['Classic', 'BL', 'FM', 'BL_FM'], index=0)
l = st.sidebar.slider('Risk Aversion Factor', min_value=0.0, max_value=10.0, step=0.5, value=0.0)

# Download data, calculate returns, and estimate optimal portfolio
data = yf.download(ticker_list, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
data = data.loc[:,('Adj Close', slice(None))]
data.columns = ticker_list
Y = data[ticker_list].pct_change().dropna()
port = rp.Portfolio(returns=Y)
method_mu='hist'
method_cov='hist'
port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

# Estimate optimal portfolio:
model='Classic' # Could be Classic(historical), BL(Black Litterman), FM(Factor Model) or BL_FM(Black litterman with factors)
rm = 'MV' # Risk measure used, there are 13 available risk measures
obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
hist = True # Use historical scenarios for risk measures that depend on scenarios
rf = 0 # Risk free rate
l = 0 # Risk aversion factor, only useful when obj is 'Utility'

w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
w = pd.DataFrame(w)
# st.write(w)

st.header("Portfolio Allocation")
st.write("Portfolio weights:")
st.dataframe(w)

# Create a pie chart with portfolio weights.
fig, ax = plt.subplots(figsize=(10, 6))
rp.plot_pie(w=w, title='Portfolio Allocation', others=0.05, nrow=25, cmap="tab20", height=6, width=10, ax=ax)

st.pyplot(fig)

points = 50 # Number of points of the frontier
frontier = port.efficient_frontier(model=model, rm=rm, points=points, rf=rf, hist=hist)

label = 'Max Risk Adjusted Return Portfolio' # Title of plot
mu = port.mu # Expected returns
cov = port.cov # Covariance matrix
returns = port.returns # Returns of the assets

# Plot the efficient frontier
fig, ax = plt.subplots(figsize=(10, 6))
rp.plot_frontier(w_frontier=frontier, mu=mu, cov=cov, returns=returns, rm=rm, rf=rf, alpha=0.05, cmap='viridis', w=w, label=label, marker='*', s=16, c='r', height=6, width=10, ax=ax)
st.pyplot(fig)

rp.plot_frontier_area(w_frontier=frontier, cmap="tab20", height=4, width=12, ax=ax)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
w1 = port.optimization(model='Classic', rm=rm, obj='Sharpe', rf=0.0, l=0, hist=True)
ax = rp.plot_hist(returns=Y, w=w1, alpha=0.05, bins=50, height=6,
                  width=10, ax=None)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
ax = rp.plot_network(returns=Y, codependence="pearson",
                     linkage="ward", k=None, max_k=10,
                     alpha_tail=0.05, leaf_order=True,
                     kind='spring', ax=None)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
ax = rp.plot_clusters(returns=Y, codependence='pearson',
                      linkage='ward', k=None, max_k=10,
                      leaf_order=True, dendrogram=True, ax=None)
st.pyplot(fig)