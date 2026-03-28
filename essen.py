import streamlit as st
import random
import os
import urllib.parse

# --- APP SETUP ---
st.set_page_config(
    page_title="Küchen-Chef Pro", 
    page_icon="👨‍🍳", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- DATENBANK (100+ GESUNDE GERICHTE) ---
# Format: "Name": ["Zutaten", "Tageszeit", "Kategorie"]
rezepte = {
    # FRÜHSTÜCK
    "Vollkorn-Omelett mit Spinat": ["3 Eier, Handvoll Blattspinat, 2 Scheiben Vollkornbrot, 50g Feta", "Frühstück", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Beeren-Quark mit Haferflocken": ["250g Magerquark, 100g Beeren, 4 EL Haferflocken, 1 TL Honig", "Frühstück", "Schnelle Küche & Snacks 🥪"],
    "Avocado-Brot mit pochiertem Ei": ["2 Scheiben Vollkornbrot, 1 Avocado, 2 Eier, Prise Chili", "Frühstück", "Vegetarisch & Vegan 🥗"],
    "Griechischer Joghurt mit Nüssen": ["250g Joghurt, 30g Walnüsse, 1 Apfel, Zimt", "Frühstück", "Schnelle Küche & Snacks 🥪"],
    "Bananen-Pancakes": ["1 reife Banane, 2 Eier, 30g Haferflocken", "Frühstück", "Vegetarisch & Vegan 🥗"],
    "Hüttenkäse mit Gurke & Lachs": ["200g Hüttenkäse, halbe Gurke, 50g Räucherlachs, Knäckebrot", "Frühstück", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Chia-Pudding mit Mango": ["3 EL Chia-Samen, 200ml Hafermilch, halbe Mango", "Frühstück", "Vegetarisch & Vegan 🥗"],
    "Rührei mit Tomaten & Feta": ["4 Eier, 5 Kirschtomaten, 50g Feta, Vollkornbrot", "Frühstück", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Vollkorn-Sandwich mit Pute": ["2 Scheiben Vollkornbrot, Putenbrust, Frischkäse, Salat", "Frühstück", "Schnelle Küche & Snacks 🥪"],
    "Smoothie-Bowl": ["1 Banane, TK-Beeren, 100ml Hafermilch, Topping: Müsli & Kerne", "Frühstück", "Vegetarisch & Vegan 🥗"],

    # NUDELN & PASTA
    "Pasta mit Avocado-Pesto": ["200g Vollkorn-Pasta, 1 Avocado, Basilikum, Knoblauch, Pinienkerne", "Abendessen", "Nudeln & Pasta 🍝"],
    "Linsennudeln Bolognese": ["250g Linsennudeln, 200g Rinderhack (oder Veggie), Passierte Tomaten, Karotten", "Mittagessen", "Nudeln & Pasta 🍝"],
    "Zucchini-Spaghetti mit Garnelen": ["2 Zucchini (Zoodles), 150g Garnelen, Knoblauch, Olivenöl, Zitrone", "Abendessen", "Nudeln & Pasta 🍝"],
    "Spaghetti Aglio e Olio": ["200g Spaghetti, Olivenöl, 3 Knoblauchzehen, Petersilie, Chili", "Abendessen", "Nudeln & Pasta 🍝"],
    "Penne mit Brokkoli & Feta": ["200g Penne, 1 Brokkoli, 100g Feta, Mandelsplitter", "Mittagessen", "Nudeln & Pasta 🍝"],
    "Gnocchi-Tomaten-Pfanne": ["500g Gnocchi, 1 Packung Kirschtomaten, frischer Basilikum, Parmesan", "Mittagessen", "Nudeln & Pasta 🍝"],
    "Pasta Carbonara (Light)": ["200g Spaghetti, 100g Schinkenwürfel, 2 Eier, Parmesan, Pfeffer", "Abendessen", "Nudeln & Pasta 🍝"],
    "Tortellini in Salbeibutter": ["1 Pkg Tortellini, frischer Salbei, 20g Butter, Parmesan", "Abendessen", "Nudeln & Pasta 🍝"],
    "Dinkel-Lasagne": ["Lasagneplatten, Zucchini, Paprika, Tomatensoße, Mozzarella", "Abendessen", "Nudeln & Pasta 🍝"],
    "Reisnudeln mit Tofu": ["150g Reisnudeln, 200g Tofu, Erdnusssoße, Paprika", "Mittagessen", "Nudeln & Pasta 🍝"],

    # REIS & BOWLS
    "Gemüse-Curry mit Kokosmilch": ["1 Dose Kokosmilch, Brokkoli, Paprika, Kichererbsen, Reis", "Abendessen", "Reis & Bowls 🍚"],
    "Hähnchen-Teriyaki-Bowl": ["200g Hähnchen, Reis, Edamame, geraspelte Möhren, Teriyaki-Soße", "Mittagessen", "Reis & Bowls 🍚"],
    "Lachs-Poke-Bowl": ["150g Lachs, Reis, Avocado, Gurke, Sesam", "Mittagessen", "Reis & Bowls 🍚"],
    "Mexikanische Reis-Pfanne": ["150g Reis, 1 Dose Mais, 1 Dose schwarze Bohnen, Paprika, Avocado", "Abendessen", "Reis & Bowls 🍚"],
    "Risotto mit grünem Spargel": ["200g Risottoreis, 1 Bund grüner Spargel, Zwiebel, Parmesan", "Abendessen", "Reis & Bowls 🍚"],
    "Paella mit Meeresfrüchten": ["200g Reis, TK-Meeresfrüchte-Mix, Paprika, Safran/Kurkuma", "Abendessen", "Reis & Bowls 🍚"],
    "Bunter Quinoa-Salat": ["150g Quinoa, Paprika, Gurke, Petersilie, Feta", "Mittagessen", "Reis & Bowls 🍚"],
    "Indisches Linsen-Dal": ["200g rote Linsen, Kokosmilch, Kurkuma, Reis", "Abendessen", "Reis & Bowls 🍚"],
    "Eierreis mit Gemüse": ["150g Reis, 2 Eier, TK-Erbsen, Frühlingszwiebeln, Sojasoße", "Mittagessen", "Reis & Bowls 🍚"],
    "Gefüllte Paprika mit Reis": ["2 Paprika, Reis-Gemüse-Füllung, Tomatensoße", "Abendessen", "Reis & Bowls 🍚"],

    # LOW CARB / FLEISCH & FISCH
    "Lachsfilet vom Blech": ["2 Lachsfilets, 1 Bund Spargel oder Brokkoli, Zitrone, Olivenöl", "Abendessen", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Hähnchenbrust mit Tomate-Mozzarella": ["2 Hähnchenbrüste, 1 Mozzarella, 2 Tomaten, Basilikum", "Abendessen", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Rinderstreifen mit Paprika": ["300g Rinderstreifen, 3 bunte Paprika, Sojasoße, Ingwer", "Mittagessen", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Gebackener Feta mit Gemüse": ["200g Feta, Zucchini, Kirschtomaten, Oliven", "Abendessen", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Puten-Geschnetzeltes mit Pilzen": ["300g Pute, 250g Champignons, 1 Zwiebel, Schuss Sahne", "Mittagessen", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Forelle Müllerin Art": ["2 Forellen, Kartoffeln, Zitrone, Petersilie", "Abendessen", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Steak mit grünen Bohnen": ["2 Rindersteaks, 300g grüne Bohnen, Kräuterbutter", "Abendessen", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Zucchini-Puffer mit Lachs": ["2 Zucchini, 1 Ei, 50g Mehl, Räucherlachs, Quark", "Mittagessen", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Garnelen-Knoblauch-Pfanne": ["250g Garnelen, viel Knoblauch, Petersilie, Zitrone", "Abendessen", "Low Carb / Fleisch & Fisch 🥩🐟"],
    "Wok-Pfanne mit Rind": ["200g Rind, Brokkoli, Karotten, Sojasoße, Chili", "Mittagessen", "Low Carb / Fleisch & Fisch 🥩🐟"],

    # VEGETARISCH & VEGAN
    "Süßkartoffel-Kumpir": ["2 große Süßkartoffeln, Hummus, Rotkohl, Mais, Feta", "Abendessen", "Vegetarisch & Vegan 🥗"],
    "Kichererbsen-Salat": ["1 Dose Kichererbsen, Gurke, Tomate, Petersilie, Zitrone", "Mittagessen", "Vegetarisch & Vegan 🥗"],
    "Shakshuka": ["1 Dose Tomaten, 3 Eier, Paprika, Kreuzkümmel", "Frühstück", "Vegetarisch & Vegan 🥗"],
    "Linsensuppe": ["200g rote Linsen, Karotten, Kartoffeln, Brühe", "Mittagessen", "Vegetarisch & Vegan 🥗"],
    "Flammkuchen mit Lauch": ["1 Flammkuchenteig, Schmand, Lauch, Zwiebeln", "Abendessen", "Vegetarisch & Vegan 🥗"],
    "Gebackener Blumenkohl": ["1 Blumenkohl, Tahini, Zitrone, Kichererbsen", "Abendessen", "Vegetarisch & Vegan 🥗"],
    "Vegetarische Burrito-Bowl": ["Reis, schwarze Bohnen, Avocado, Mais, Salsa", "Abendessen", "Vegetarisch & Vegan 🥗"],
    "Kartoffel-Möhren-Eintopf": ["500g Kartoffeln, 3 Möhren, Zwiebel, Petersilie", "Mittagessen", "Vegetarisch & Vegan 🥗"],
    "Hirsepfanne mit Gemüse": ["150g Hirse, Zucchini, Paprika, Pinienkerne", "Mittagessen", "Vegetarisch & Vegan 🥗"],
    "Falafel-Wrap": ["Wraps, Falafel, Hummus, Salat, Gurke", "Mittagessen", "Vegetarisch & Vegan 🥗"],

    # SCHNELLE KÜCHE
    "Wraps mit Putenbrust": ["2 Vollkorn-Wraps, 100g Putenbrust, Salat, Frischkäse", "Mittagessen", "Schnelle Küche & Snacks 🥪"],
    "Thunfisch-Salat 'Quick'": ["1 Dose Thunfisch, Mix-Salat aus der Tüte, Mais, Ei", "Mittagessen", "Schnelle Küche & Snacks 🥪"],
    "Strammer Max": ["2 Scheiben Brot, Schinken, 2 Spiegeleier, Gewürzgurke", "Abendessen", "Schnelle Küche & Snacks 🥪"],
    "Avocado-Toast mit Tomaten": ["2 Scheiben Brot, 1 Avocado, Kirschtomaten", "Frühstück", "Schnelle Küche & Snacks 🥪"],
    "Couscous-Salat (5 Min)": ["150g Couscous, Brühe, Tomaten, Gurke, Feta", "Mittagessen", "Schnelle Küche & Snacks 🥪"],
    "Tomate-Mozzarella": ["2 große Tomaten, 1 Mozzarella, Basilikum, Olivenöl", "Abendessen", "Schnelle Küche & Snacks 🥪"],
    "Quesadillas": ["2 Tortillas, Käse, Mais, rote Bohnen", "Abendessen", "Schnelle Küche & Snacks 🥪"],
    "Überbackene Baguettes": ["Vollkorn-Baguette, Schinken, Käse, Paprika", "Abendessen", "Schnelle Küche & Snacks 🥪"],
    "Griechischer Salat": ["Gurke, Tomate, Oliven, Feta, Zwiebeln", "Mittagessen", "Schnelle Küche & Snacks 🥪"],
    "Rührei auf Brot": ["3 Eier, Schnittlauch, 2 Scheiben Vollkornbrot", "Frühstück", "Schnelle Küche & Snacks 🥪"]
}

# --- LOGIK FÜR EXTRA GERICHTE ---
DATA_FILE = "meine_extra_gerichte.txt"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f: f.write("")

def load_extras():
    with open(DATA_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# --- UI ANZEIGE ---
st.title("👨‍🍳 Küchen-Chef Pro")
st.markdown("### Was essen wir heute?")

# Filter-Bereich
col1, col2 = st.columns(2)
with col1:
    auswahl_zeit = st.selectbox("Zeitpunkt 🕒", ["Egal", "Frühstück", "Mittagessen", "Abendessen"])
with col2:
    kat_liste = ["Alles", "Nudeln & Pasta 🍝", "Reis & Bowls 🍚", "Low Carb / Fleisch & Fisch 🥩🐟", "Vegetarisch & Vegan 🥗", "Schnelle Küche & Snacks 🥪"]
    auswahl_kat = st.selectbox("Kategorie 📂", kat_liste)

# Filter-Logik
pool = []
for name, info in rezepte.items():
    zutaten, zeit, kat = info
    if (auswahl_zeit == "Egal" or zeit == auswahl_zeit) and (auswahl_kat == "Alles" or kat == auswahl_kat):
        pool.append((name, zutaten))

# --- GENERATOR (OHNE ANIMATION) ---
st.write("---")
if st.button("🎲 Gericht vorschlagen", use_container_width=True):
    if pool:
        gericht_name, zutaten_liste = random.choice(pool)
        
        st.subheader(f"🍴 {gericht_name}")
        
        with st.container():
            st.markdown("#### 🛒 Einkaufsliste:")
            for item in zutaten_liste.split(","):
                st.write(f"- {item.strip()}")
            
        # WhatsApp Link
        text = f"Vorschlag für heute: {gericht_name}\n\nEinkaufsliste:\n{zutaten_liste}"
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(text)}"
        st.divider()
        st.markdown(f"[📲 **Per WhatsApp an Freundin schicken**]({whatsapp_url})")
    else:
        st.warning("Kein passendes Rezept gefunden. Ändere die Filter!")

# --- EXTRAS ---
with st.expander("➕ Eigenes Gericht hinzufügen"):
    neu_n = st.text_input("Gericht Name")
    neu_z = st.text_input("Zutaten (mit Komma)")
    if st.button("Speichern"):
        if neu_n and neu_z:
            with open(DATA_FILE, "a") as f:
                f.write(f"\n{neu_n} ({neu_z})")
            st.success("Gespeichert!")

st.caption("Tipp: Zum Home-Bildschirm hinzufügen!")