#@title 🛠️ Panel Konfiguracyjny Analizatora { display-mode: "form" }
import os
import requests
import json
import time
from IPython.display import display, Markdown

#@markdown ### 🔑 Autoryzacja i Konfiguracja
#@markdown Wprowadź swój klucz API z Google AI Studio (wartość zostanie zamaskowana):
api_key = "" #@param {type:"string"}

#@markdown ### 📝 Dane Wejściowe
#@markdown Wklej tutaj tekst, który chcesz poddać analizie:
input_text = "None" #@param {type:"string"}

#@markdown Poziom szczegółowości notatki (1 - najprostszy, 5 - najpełniejszy):
level = 3 #@param {type:"slider", min:1, max:5, step:1}

def call_gemini(model_name):
    # Użycie klucza z formularza, a w przypadku jego braku próba pobrania ze zmiennych środowiskowych
    active_key = api_key if api_key else os.environ.get("GEMINI_API_KEY", "")
    
    if not active_key:
        raise ValueError("Brak klucza API! Wpisz go w polu 'api_key' powyżej.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={active_key}"
    headers = {'Content-Type': 'application/json'}

    payload = {
        "system_instruction": {
            "parts": [{
                "text": f"""Jesteś precyzyjnym analitykiem tekstów edukacyjnych.
ZASADY KRYTYCZNE:
1. WALIDACJA KOMPLETNOŚCI: Jeśli tekst jest wyraźnie urwany, odpowiedz: "BŁĄD: Przesłany tekst jest niekompletny".
2. FAKT-CHECKING: Odmawiaj analizy treści o niskiej wiarygodności (Komunikat: "BŁĄD: Treści niewiarygodne").
3. ZAKRES: Nie wykonuj zadań kreatywnych (Komunikat: "BŁĄD: Zapytanie poza zakresem").

FORMATOWANIE (Poziom {level}/5):
- Nagłówek głównego tematu, pod nim nagłówki pomniejszych zagadnień
- Stosowanie streszczenia zależnego od mocy i listy od myślników
- Długość tekstu zależna od poziomu uproszczenia
- Zakaz znaków specjalnych ($, \\, [ ]).
- Format notatki
- Poziom {level} dostosowany do stopnia edukacji
- Format streszczonej notatki, ale nadal zawierającej nagłówki zagadnień i rozbudowane podpunkty
- Zakaz powitań i wstępów."""
            }]
        },
        "contents": [{
            "parts": [{
                "text": f"Format: Lista punktowa. Poziom szczegółowości: {level}/5. Przeanalizuj poniższy tekst: {input_text}"
            }]
        }]
    }

    return requests.post(url, headers=headers, data=json.dumps(payload))

def start():
    if not api_key and not os.environ.get("GEMINI_API_KEY"):
        print("❌ BŁĄD: Proszę wprowadzić klucz API w formularzu powyżej!")
        return

    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.5-pro"]

    for model in models_to_try:
        print(f"⏳ Próba połączenia z {model}...")
        try:
            response = call_gemini(model)
        except Exception as e:
            print(f"❌ Błąd: {e}")
            return

        if response.status_code == 200:
            result = response.json()
            output = result['candidates'][0]['content']['parts'][0]['text']
            print(f"\n✅ REZULTAT ({model}):")
            print("-" * 40)
            display(Markdown(output))
            print("-" * 40)
            return
        elif response.status_code == 503:
            print(f"⚠️ Model {model} jest przeciążony. Próbuję następny...")
            time.sleep(1)
        else:
            print(f"❌ Błąd {response.status_code} dla {model}: {response.text}")
            time.sleep(1)

start()
