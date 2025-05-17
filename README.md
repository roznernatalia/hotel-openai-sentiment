Aplikacja webowa stworzona z wykorzystaniem frameworka Flask, której celem jest analiza opinii klientów hoteli oraz generowanie opisów marketingowych z użyciem technologii sztucznej inteligencji OpenAI.

Użytkownik wybiera hotel, a aplikacja:
- analizuje treść opinii (klasyfikacja sentymentu: pozytywny / neutralny / negatywny),
- tłumaczy je automatycznie na język polski,
- generuje profesjonalny opis marketingowy (wraz z listą zalet i wad),
- tworzy ranking hoteli na podstawie ogólnej oceny AI.

Technologie:
- Python 3.9
- Flask (framework webowy)
- OpenAI GPT-3.5-turbo (API do NLP)
- Pandas (analiza danych)
- HTML + Jinja2 (renderowanie frontendowe)
- dotenv (przechowywanie klucza API)

Wymagania:
- Zarejestrowane konto w OpenAI
- Klucz API (prywatny – nie dołączony do repozytorium)

Plik .env:
W celu zachowania bezpieczeństwa klucz API nie został udostępniony. 
Aby uruchomić aplikację lokalnie, należy utworzyć plik .env z zawartością: OPENAI_API_KEY=tu_wstaw_swoj_klucz_API

