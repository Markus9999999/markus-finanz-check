import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# 1. Grund-Einstellungen
st.set_page_config(page_title="Markus' Dashboard", layout="wide")
st.title("Markus' Finanz-Zentrale 📈")

# --- ZEITRAUM-WAHL (Zentral oben zum Klicken) ---
st.write("### Globalen Zeitraum wählen")
tab_namen = ["1 Tag", "5 Tage", "1 Monat", "1 Jahr", "5 Jahre", "Max"]
auswahl_zeit = st.radio("Zeitraum für alle Charts:", tab_namen, horizontal=True, index=2)

zeit_liste = {
    "1 Tag": ("1d", "1m"),
    "5 Tage": ("5d", "5m"),
    "1 Monat": ("1mo", "1d"),
    "1 Jahr": ("1y", "1d"),
    "5 Jahre": ("5y", "1wk"),
    "Max": ("max", "1mo")
}
period, interval = zeit_liste[auswahl_zeit]

# --- SEITENLEISTE (Für die Suche) ---
st.sidebar.header("Suche & Einstellungen")
user_ticker = st.sidebar.text_input("Zusatz-Aktie suchen (z.B. TSLA, NVDA):", "").upper()

# --- FUNKTION FÜR DIE CHARTS ---
def draw_chart(ticker_symbol, title):
    try:
        data = yf.Ticker(ticker_symbol)
        hist = data.history(period=period, interval=interval)
        
        if not hist.empty:
            aktuell = hist['Close'].iloc[-1]
            start = hist['Close'].iloc[0]
            diff_pct = ((aktuell - start) / start) * 100
            
            # WÄHRUNGSERKENNUNG
            waehrung_raw = data.info.get('currency', 'USD')
            waehrung = "€" if waehrung_raw == "EUR" else "$" if waehrung_raw == "USD" else waehrung_raw
            
            # Farbe
            color = "green" if diff_pct >= 0 else "red"
            
            st.subheader(title)
            # Metrik mit Währungssymbol
            st.metric(label=f"Kurs ({auswahl_zeit})", value=f"{aktuell:.2f} {waehrung}", delta=f"{diff_pct:.2f}%")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hist.index, y=hist['Close'], 
                line=dict(color=color, width=2.5),
                fill='tozeroy', fillcolor=f'rgba({0 if color=="green" else 255}, {255 if color=="green" else 0}, 0, 0.1)'
            ))
            
            # Dynamischer Zoom
            y_min = hist['Close'].min() * 0.99
            y_max = hist['Close'].max() * 1.01
            
            fig.update_layout(
                height=230, # Etwas kleiner für bessere Übersicht
                margin=dict(l=0, r=0, t=10, b=0), 
                template="plotly_dark",
                yaxis=dict(range=[y_min, y_max], showgrid=True, title=waehrung),
                xaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"Keine Daten")
    except:
        st.error("Fehler")

# --- DASHBOARD LAYOUT ---

# 1. Reihe: AKTIEN
st.markdown("---")
st.header("🏢 Aktien")
col1, col2 = st.columns(2)
with col1:
    draw_chart("SAP.DE", "SAP (XETRA)")
with col2:
    if user_ticker:
        draw_chart(user_ticker, f"Suche: {user_ticker}")
    else:
        draw_chart("AAPL", "Apple (USA)")

# 2. Reihe: EDELMETALLE
st.markdown("---")
st.header("🪙 Edelmetalle")
col3, col4 = st.columns(2)
with col3:
    draw_chart("SI=F", "Silber (Unze)")
with col4:
    draw_chart("GC=F", "Gold (Unze)")

# 3. Reihe: KRYPTO
st.markdown("---")
st.header("₿ Krypto")
col5, col6 = st.columns(2)
with col5:
    draw_chart("BTC-EUR", "Bitcoin")
with col6:
    draw_chart("ETH-EUR", "Ethereum")

st.sidebar.caption(f"Letztes Update: {period}")