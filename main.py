from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Wczytaj dane
df = pd.read_csv("Hotel_Reviews.csv")

# Lista unikalnych hoteli
lista_hoteli = sorted(df['Hotel_Name'].unique())

@app.route("/", methods=["GET", "POST"])
def index():
    wybrany_hotel = None
    if request.method == "POST":
        wybrany_hotel = request.form.get("hotel")
    return render_template("index.html", hotele=lista_hoteli, wybrany_hotel=wybrany_hotel)

if __name__ == "__main__":
    app.run(debug=True)
