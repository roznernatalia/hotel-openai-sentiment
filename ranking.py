import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def ocen_jakosc_hotelu(hotel, opinie):
    tekst = "\n".join(f"- {op}" for op in opinie[:40])

    prompt = f"""
Jesteś specjalistą ds. podróży. Przeanalizuj poniższe opinie o hotelu "{hotel}".
Na ich podstawie oceń ogólne doświadczenie klientów w skali od 1 do 10 (gdzie 10 to idealny pobyt, 1 to bardzo zły).
W odpowiedzi podaj tylko jedną liczbę – ocenę końcową.

Opinie:
{tekst}
Ocena:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Błąd przy ocenianiu hotelu {hotel}: {e}")
        return "Brak"
