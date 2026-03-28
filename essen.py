import streamlit as st
import random
import os

# Datei für deine persönlichen Ergänzungen
DATA_FILE = "meine_extra_gerichte.txt"

# 1. Die große Datenbank (100 gesunde & machbare Gerichte)
datenbank = {
    "Nudeln & Pasta 🍝": [
        "Vollkorn-Pasta mit Avocado-Pesto", "Zucchini-Zitronen-Spaghetti", "Linsennudeln mit Bolognese",
        "Penne mit Brokkoli und Pinienkernen", "Spaghetti Aglio e Olio mit Garnelen", "Tagliatelle mit Lachs-Spinat-Soße",
        "Gnocchi-Pfanne mit Kirschtomaten", "Kürbis-Salbei-Pasta", "Dinkel-Lasagne mit viel Gemüse",
        "Glasnudelsalat mit Erdnuss-Dressing", "Tortellini in leichter Tomaten-Ricotta-Soße", "Nudelsalat mit Feta und Oliven",
        "Makkaroni-Auflauf (fettarm mit Blumenkohlsoße)", "Reisnudeln mit Tofu und Gemüse", "Pasta mit gerösteter Paprikasoße",
        "Dinkel-Spaghetti mit Walnuss-Gorgonzola (wenig Käse)", "One-Pot-Pasta mit Pilzen", "Nudeln mit Erbsen-Minz-Pesto",
        "Vollkorn-Fusilli mit Thunfisch und Kapern", "Süßkartoffel-Gnocchi"
    ],
    "Reis & Bowls 🍚": [
        "Gemüse-Curry mit Kokosmilch", "Hähnchen-Teriyaki-Bowl", "Mexikanische Burrito-Bowl",
        "Lachs-Poke-Bowl mit Edamame", "Gefüllte Paprika mit Reis", "Risotto mit grünem Spargel",
        "Eierreis mit knackigem Gemüse", "Paella mit Meeresfrüchten", "Indisches Linsen-Dal mit Reis",
        "Quinoa-Bowl mit gerösteten Kichererbsen", "Hähnchen-Curry mit Ananas", "Wildreis-Salat mit Granatapfel",
        "Thailändisches Basilikum-Hähnchen (Pad Krapow)", "Reispfanne mit Hackfleisch und Zucchini", "Sushi-Selbstbau-Set",
        "Bibimbap (Koreanische Reis-Bowl)", "Zitronen-Hähnchen-Reis-Topf", "Gefüllte Zucchini mit Reis und Feta",
        "Reis-Bowl mit Halloumi und Hummus", "Mediterrane Reispfanne"
    ],
    "Low Carb / Fleisch & Fisch 🥩🐟": [
        "Hähnchenbrust in Tomaten-Mozzarella-Kruste", "Gebratenes Lachsfilet auf Blattspinat", "Rinderstreifen mit buntem Paprika",
        "Zucchini-Puffer mit Kräuterquark", "Putensteak mit Ofengemüse", "Dorade vom Blech mit Zitrone",
        "Frikadellen aus Geflügelhack mit Salat", "Omelett mit Pilzen und Speck", "Hähnchen-Spieße mit Erdnusssoße",
        "Garnelen-Pfanne mit Knoblauch", "Rinder-Steak mit Bohnen im Speckmantel", "Gebratene Forelle mit Mandeln",
        "Gefüllte Auberginen mit Hackfleisch", "Shakshuka (Eier in Tomatensoße)", "Hähnchen-Geschnetzeltes 'Züricher Art' (leicht)",
        "Thunfisch-Steak mit Sesam", "Saltimbocca vom Huhn", "Gebackener Feta mit Gemüse",
        "Wok-Pfanne mit Rind und Brokkoli", "Kabeljau in Senfsoße"
    ],
    "Vegetarisch & Vegan 🥗": [
        "Kichererbsen-Curry", "Süßkartoffel-Kumpir", "Linsensuppe 'Omas Art'",
        "Gebackener Blumenkohl mit Tahini", "Falafel-Wraps mit Minz-Dip", "Gemüse-Lasagne ohne Fleisch",
        "Kürbissuppe mit Ingwer", "Vegetarische Paella", "Gefüllte Champignons",
        "Rote-Linsen-Bolognese", "Sommerrollen mit Erdnuss-Dip", "Ratatouille",
        "Bunter Bohnensalat", "Hirsepfanne mit Gemüse", "Flammkuchen mit Lauch und Äpfeln",
        "Kürbis-Curry", "Gefüllte Tomaten mit Couscous", "Gebratener Tofu mit Pak Choi",
        "Halloumi-Burger mit Grillgemüse", "Kartoffel-Möhren-Eintopf"
    ],
    "Schnelle Küche & Snacks 🥪": [
        "Avocado-Brot mit pochiertem Ei", "Vollkorn-Wraps mit Putenbrust", "Griechischer Salat mit Oliven",
        "Tomate-Mozzarella mit Basilikum", "Strammer Max (Vollkornbrot)", "Quesadillas mit Käse und Mais",
        "Überbackene Baguette-Hälften", "Thunfisch-Salat mit Zwiebeln", "Rührei mit Schinken auf Brot",
        "Couscous-Salat (5-Minuten-Rezept)", "Gesunde Pizza-Toasties", "Rote-Beete-Salat mit Walnüssen",
        "Wraps mit Frischkäse und Lachs", "Warmer Ziegenkäse auf Salat", "Pizzaschnecken (Vollkorn)",
        "Lachs-Tartar auf Pumpernickel", "Gefüllte Pita-Taschen", "Nacho-Salat (gesunde Version)",
        "Bauernfrühstück (leicht)", "Süßkartoffel-Toast"
    ]
}

# 2. Laden der persönlichen Extra-Gerichte aus der Datei
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        f.write("")

def load_extras():
    with open(DATA_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# --- APP LAYOUT ---
st.set_page_config(page_title="Küchen-Chef 2.0", page_icon="👨‍🍳", layout="centered")

st.title("👨‍🍳 Der Küchen-Chef 2.0")
st.write("Wählt eine Kategorie oder lasst euch überraschen!")

# --- KATEGORIE-AUSWAHL ---
kategorien = ["Alles", "Nudeln & Pasta 🍝", "Reis & Bowls 🍚", "Low Carb / Fleisch & Fisch 🥩🐟", "Vegetarisch & Vegan 🥗", "Schnelle Küche & Snacks 🥪"]
auswahl_kat = st.selectbox("Was habt ihr im Haus / Worauf habt ihr Lust?", kategorien)

# --- GENERATOR LOGIK ---
if st.button("🎲 Gericht vorschlagen"):
    # Liste zusammenstellen
    pool = []
    if auswahl_kat == "Alles":
        for k in datenbank:
            pool.extend(datenbank[k])
        pool.extend(load_extras())
    else:
        pool = datenbank[auswahl_kat]
    
    if pool:
        gericht = random.choice(pool)
        st.balloons()
        st.info("Der Chef empfiehlt:")
        st.markdown(f"## {gericht}")
    else:
        st.warning("Keine Gerichte in dieser Kategorie gefunden.")

# --- PERSÖNLICHE LISTE ERWEITERN ---
with st.expander("📝 Eigenes Gericht hinzufügen"):
    neu = st.text_input("Gericht-Name:")
    if st.button("Hinzufügen"):
        if neu:
            with open(DATA_FILE, "a") as f:
                f.write(f"\n{neu}")
            st.success(f"'{neu}' wurde gespeichert!")
            st.rerun()

# --- ÜBERSICHT ---
if st.checkbox("Zeige alle 100+ Gerichte"):
    for kat, essen in datenbank.items():
        st.write(f"**{kat}**")
        st.write(", ".join(essen))