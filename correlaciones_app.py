
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📈 Correlaciones Móviles entre Activos Financieros")

# Sidebar - Selección de activos
tickers_default = ['^GSPC', '^IXIC', 'BTC-USD', 'GC=F', 'EURUSD=X', '^TNX']
ticker_names = {
    '^GSPC': 'SP500',
    '^IXIC': 'NASDAQ',
    'BTC-USD': 'BTC',
    'GC=F': 'Gold',
    'EURUSD=X': 'EURUSD',
    '^TNX': 'US10Y'
}

st.sidebar.header("Opciones")
tickers = st.sidebar.multiselect("Selecciona activos:", options=tickers_default, default=tickers_default)
window = st.sidebar.slider("Tamaño de la ventana (días):", min_value=30, max_value=180, value=90, step=15)

# Descarga de datos
data = yf.download(tickers, start="2018-01-01", end="2025-01-01")['Close']
data = data.rename(columns=ticker_names)
data.dropna(inplace=True)

# Calcular retornos
daily_returns = data.pct_change().dropna()

# Selección de pares para analizar
columns = list(data.columns)
pairs = [(a, b) for i, a in enumerate(columns) for b in columns[i+1:]]
default_pairs = [pair for pair in [('SP500', 'BTC'), ('SP500', 'US10Y')] if pair in pairs]
selected_pairs = st.sidebar.multiselect(
    "Selecciona pares a analizar:",
    options=pairs,
    default=default_pairs
)

# Graficar correlaciones móviles
st.subheader(f"Correlaciones Móviles ({window} días)")
fig, ax = plt.subplots(figsize=(14, 7))

for a, b in selected_pairs:
    rolling_corr = daily_returns[a].rolling(window).corr(daily_returns[b])
    ax.plot(rolling_corr, label=f"{a} vs {b}")

ax.axhline(0, color='black', linestyle='--', linewidth=0.7)
ax.set_title("Correlaciones en el tiempo")
ax.set_xlabel("Fecha")
ax.set_ylabel("Correlación")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Mostrar datos opcionales
with st.expander("Mostrar datos crudos"):
    st.dataframe(data.tail())
