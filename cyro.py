import streamlit as st
import requests
import json
import time

# Konfiguracja strony
st.set_page_config(page_title="CYRO_AI", page_icon="🧠", layout="centered")

# Style CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 CYRO_AI")
st.markdown("### Profesjonalny asystent upraszczania tekstów naukowych")

# --- PASEK BOCZNY ---
with st.sidebar:
    st.header("⚙️ Ustawienia")
    api_key = st.text_input("Gemini API Key:", type="password", value="AIzaSyCCg4KdxaJFFQkP3r37EGGnwua4t0vgrrI")
    model_choice = st.selectbox("Model główny:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.divider()
    st.info("Agent automatycznie sprawdzi alternatywne modele w razie przeciążenia.")

# --- INTERFEJS GŁÓWNY ---
input_text = st.text_area("Wklej tekst naukowy:", height=250, placeholder="Wklej tutaj treść publikacji...")
level = st.select_slider("Skala uproszczenia:", options=[1, 2, 3, 4, 5], value=3)

levels_map = {
    1: "Poziom Ekspert: Streszczenie akademickie, zachowaj terminologię.",
    2: "Poziom Student: Język formalny, skup się na konkretach.",
    3: "Poziom Standard: Język potoczny, wyjaśnij trudne pojęcia.",
    4: "Poziom Prosty: Używaj metafor, unikaj żargonu.",
    5: "Poziom ELI5: Wyjaśnij jak dziecku, maksimum obrazowych porównań."
}
st.caption(f"🎯 **Cel:** {levels_map[level]}")

def call_gemini(model_name, level_val, text):
    # Ważne: używamy v1beta dla lepszej kompatybilności z darmowymi kluczami
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    prompt = f"Jesteś edytorem. Cel: {levels_map[level_val]}. Format: lista punktowa, język polski. Przetransformuj ten tekst: {text}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        return response
    except Exception:
        return None

if st.button("🚀 Generuj notatkę"):
    if not api_key:
        st.error("Brak klucza API!")
    elif not input_text:
        st.warning("Najpierw wklej tekst.")
    else:
        with st.spinner("Agent analizuje dane..."):
            # Lista modeli poza pętlą
            models_to_try = [model_choice, "gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.0-pro"]
            success = False
            last_res = None
            
            for m in models_to_try:
                res = call_gemini(m, level, input_text)
                last_res = res
                
                if res and res.status_code == 200:
                    try:
                        data = res.json()
                        output = data['candidates'][0]['content']['parts'][0]['text']
                        st.markdown("---")
                        st.balloons()
                        st.subheader("📝 Wynik transformacji:")
                        st.write(output)
                        success = True
                        break
                    except:
                        st.warning(f"Błąd danych z modelu {m}. Próbuję dalej...")
                else:
                    st.toast(f"Model {m} niedostępny. Szukam dalej...")
                    time.sleep(1) # Chwila przerwy przed kolejnym modelem
            
            if not success:
                st.error("Wszystkie modele AI są obecnie zajęte.")
                if last_res:
                    with st.expander("Szczegóły błędu"):
                        st.write(f"Kod: {last_res.status_code}")
                        st.write(last_res.text)
