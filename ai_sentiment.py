import openai
import os
from dotenv import load_dotenv

# Załaduj klucz API z pliku .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Funkcja klasyfikująca sentyment opinii z użyciem OpenAI
def klasyfikuj_sentyment_ai(opinia):
    prompt = f"""Przyporządkuj poniższą opinię do jednej z kategorii: pozytywny, neutralny, negatywny. 
    Zwróć wyłącznie jedno słowo — bez znaków interpunkcyjnych i dodatków.

Opinia:
{opinia}

Odpowiedź:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=5
        )
        wynik = response.choices[0].message.content.strip().lower()
        if "pozytywny" in wynik:
            return "pozytywny"
        elif "neutralny" in wynik:
            return "neutralny"
        elif "negatywny" in wynik:
            return "negatywny"
        else:
            return "nieokreślony"
    except Exception as e:
        print("Błąd:", e)
        return "błąd"

# Funkcja tłumacząca opinię z języka angielskiego na polski
def tlumacz_opinie_na_polski(opinia):
    prompt = f"""Przetłumacz poniższą opinię klienta hotelowego na język polski. 
    Nie dodawaj cudzysłowów, znaków interpunkcyjnych na końcu zdania i dodatków. 
    Zadbaj o naturalny, swobodny i zrozumiały styl.

Opinia:
{opinia}

Tłumaczenie:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=150
        )
        wynik = response.choices[0].message.content.strip().strip('"“”')

        # Dodaj kropkę, jeśli jej nie ma
        if not wynik.endswith((".", "!", "?", "…")):
            wynik += "."

        return wynik

    except Exception as e:
        print("Błąd podczas tłumaczenia:", e)
        return "błąd"
