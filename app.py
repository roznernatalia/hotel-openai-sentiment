from flask import Flask, render_template, request
import pandas as pd
import openai
import os
from dotenv import load_dotenv
from ranking import ocen_jakosc_hotelu

# === Import funkcji AI ===
from ai_sentiment import klasyfikuj_sentyment_ai, tlumacz_opinie_na_polski
from opis import generuj_opis_ai

# === Załadowanie klucza OpenAI z pliku .env ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Inicjalizacja aplikacji Flask ===
app = Flask(__name__)

# === Wczytanie danych z pliku CSV ===
df = pd.read_csv("Hotel_Reviews.csv")
lista_hoteli = sorted(df['Hotel_Name'].unique())  # Lista unikalnych hoteli do formularza

# === Główna strona z analizą sentymentu i tłumaczeniem opinii ===
@app.route("/", methods=["GET", "POST"])
def index():
    hotel = ""
    opinie = []

    if request.method == "POST":
        hotel = request.form.get("hotel")
        hotel_df = df[df["Hotel_Name"] == hotel].copy()

        # Losowe 20 opinii (szybkość działania)
        for _, row in hotel_df.sample(n=min(20, len(hotel_df))).iterrows():
            tekst = row["Positive_Review"] if row["Positive_Review"] != "No Positive" else row["Negative_Review"]
            tekst = tekst.strip('"“”')  # usuwa nadmiarowe cudzysłowy
            sentyment = klasyfikuj_sentyment_ai(tekst)
            tlumaczenie = tlumacz_opinie_na_polski(tekst)
            opinie.append({
                "tekst": tekst,
                "sentyment": sentyment,
                "tlumaczenie": tlumaczenie
            })

    return render_template("index.html", hotele=lista_hoteli, wybrany_hotel=hotel, opinie=opinie)

# === Strona z profesjonalnym opisem marketingowym hotelu ===
@app.route("/opis", methods=["POST"])
def opis():
    hotel = request.form.get("hotel")
    hotel_df = df[df["Hotel_Name"] == hotel].copy()

    # Połączenie wszystkich pozytywnych i negatywnych opinii
    teksty = hotel_df["Positive_Review"].tolist() + hotel_df["Negative_Review"].tolist()
    teksty = [t for t in teksty if t not in ["No Positive", "No Negative"]]

    # Generowanie: opis marketingowy + tłumaczenie
    opis_en, opis_pl = generuj_opis_ai(teksty, hotel)

    return render_template("opis.html", hotel=hotel, opis_en=opis_en, opis_pl=opis_pl)


# === Ranking hotelii ===
@app.route("/ranking")
def ranking():
    wyniki = []
    for hotel in lista_hoteli[:25]:  # można zmienić zakres
        hotel_df = df[df["Hotel_Name"] == hotel]
        teksty = hotel_df["Positive_Review"].tolist() + hotel_df["Negative_Review"].tolist()
        teksty = [t for t in teksty if t not in ["No Positive", "No Negative"]]
        ocena = ocen_jakosc_hotelu(hotel, teksty)
        wyniki.append((hotel, ocena))

    # Posortowanie po ocenie malejąco (jeśli się da)
    try:
        wyniki.sort(key=lambda x: float(x[1]), reverse=True)
    except:
        pass

    return render_template("ranking.html", wyniki=wyniki)


# === Uruchomienie aplikacji lokalnie ===
if __name__ == "__main__":
    app.run(debug=True)