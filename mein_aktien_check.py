import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 1. Grund-Einstellungen
st.set_page_config(page_title="Markus' Terminal Pro", layout="wide")

st.title("Markus' Terminal Pro 📱📈")

# --- 1. SUCHE GANZ OBEN ---
user_ticker = st.text_input("🔍 Aktie suchen (z.B. NVDA, TSLA, MSFT):", "").upper()

# --- FUNKTION FÜR EINZEL-CHARTS ---
def draw_smart_chart(ticker_symbol, title):
    key_suffix = f"btn_{ticker_symbol}"
    st.markdown(f"### {title}")
    
    zeit_wahl = st.radio("Zeitraum:", ["1T", "5T", "1M", "1J", "Max"], horizontal=True, key=key_suffix, label_visibility="collapsed")
    
    mapping = {"1T": ("2d", "5m"), "5T": ("7d", "15m"), "1M": ("1mo", "1d"), "1J": ("1y", "1d"), "Max": ("max", "1mo")}
    read_period, interval = mapping[zeit_wahl]

    try:
        data = yf.Ticker(ticker_symbol)
        # Wir laden immer etwas mehr, um Wochenenden zu überbrücken
        hist = data.history(period=read_period, interval=interval)
        
        if hist.empty:
            # Zweiter Versuch mit mehr Puffer für das Wochenende
            hist = data.history(period="5d", interval="15m")

        if not hist.empty:
            # Für 1-Tages-Ansicht: Nur den aktuellsten Handelstag filtern
            if zeit_wahl == "1T":
                last_date = hist.index.date[-1]
                hist_plot = hist[hist.index.date == last_date]
            else:
                hist_plot = hist

            aktuell = hist_plot['Close'].iloc[-1]
            start = hist_plot['Close'].iloc[0]
            diff_pct = ((aktuell - start) / start) * 100
            waehrung = "€" if data.info.get('currency') == "EUR" else "$"
            
            st.metric(label=f"Kurs", value=f"{aktuell:.2f} {waehrung}", delta=f"{diff_pct:.2f}%")
            
            # --- DER CHART ---
            fig = go.Figure()
            color = "green" if diff_pct >= 0 else "red"
            
            fig.add_trace(go.Scatter(
                x=hist_plot.index, y=hist_plot['Close'], 
                line=dict(color=color, width=3),
                fill='tozeroy', 
                fillcolor=f'rgba({0 if color=="green" else 255}, {255 if color=="green" else 0}, 0, 0.1)',
                hoverinfo='y'
            ))
            
            # --- MANUELLER ZOOM-FIX ---
            y_min = hist_plot['Close'].min() * 0.999 # Nur 0.1% Puffer
            y_max = hist_plot['Close'].max() * 1.001
            
            fig.update_layout(
                height=250, margin=dict(l=0, r=0, t=0, b=0), template="plotly_dark",
                xaxis=dict(showgrid=False, fixedrange=True),
                yaxis=dict(
                    range=[y_min, y_max], # ERZWUNGENER ZOOM
                    autorange=False, 
                    fixedrange=True, # Verhindert versehentliches Zoomen am Handy
                    showgrid=True,
                    zeroline=False
                ),
                hovermode='x'
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.error(f"Keine Daten für {ticker_symbol} verfügbar.")
    except:
        st.error("Ladefehler...")

# --- LAYOUT ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    if user_ticker:
        draw_smart_chart(user_ticker, f"Suche: {user_ticker}")
    else:
        st.info("Kürzel oben eingeben")

with col2:
    # SAP.BE (Berlin) liefert am Wochenende oft nichts, daher "SAP" (USA) als Backup-Logik
    draw_smart_chart("SAP.DE", "SAP (XETRA/L&S)")

st.header("🪙 Edelmetalle")
col3, col4 = st.columns(2)
with col3: draw_smart_chart("SI=F", "Silber")
with col4: draw_smart_chart("GC=F", "Gold")

st.header("₿ Krypto")
col5, col6 = st.columns(2)
with col5: draw_smart_chart("BTC-EUR", "Bitcoin")
with col6: draw_smart_chart("ETH-EUR", "Ethereum")