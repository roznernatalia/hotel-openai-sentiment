import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generuj_opis_ai(opinie, nazwa_hotelu):
    # Ograniczenie liczby opinii do 50 (można zmienić)
    tekst = "\n".join(f"- {op}" for op in opinie[:50])

    # Prompt po polsku – generuje profesjonalny opis, listę zalet i wad
    prompt = f"""Jesteś ekspertem ds. marketingu w branży hotelarskiej.

Na podstawie prawdziwych opinii klientów o hotelu „{nazwa_hotelu}”, stwórz:
- Profesjonalny i atrakcyjny opis hotelu (4–6 zdań)
- Wypunktowaną listę największych zalet hotelu
- Wypunktowaną listę ewentualnych wad (sformułowanych uprzejmie)

Opinie klientów:
{tekst}
"""

    # Wygeneruj opis po polsku
    opis_pl = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1200
    ).choices[0].message.content

    # Tłumaczenie na angielski
    prompt_en = f"""Przetłumacz poniższy tekst na profesjonalny język angielski (styl marketingowy):

{opis_pl}
"""

    opis_en = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_en}],
        temperature=0.7,
        max_tokens=1200
    ).choices[0].message.content

    return opis_en, opis_pl