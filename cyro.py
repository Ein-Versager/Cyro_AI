import streamlit as st
import google.generativeai as genai
import time

# 1. Konfiguracja strony
st.set_page_config(page_title="CYRO_AI", page_icon="🧠", layout="centered")

# 2. Styl CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 CYRO_AI")
st.markdown("### Profesjonalny asystent upraszczania tekstów naukowych")

# 3. Pasek boczny
with st.sidebar:
    st.header("⚙️ Ustawienia")
    api_key = st.text_input("Gemini API Key:", type="password", value="")
    model_choice = st.selectbox("Model główny:", ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"])
    st.divider()
    st.info("Agent automatycznie sprawdzi alternatywne modele w razie przeciążenia.")

# 4. Interfejs główny
input_text = st.text_area("Wklej tekst naukowy:", height=250, placeholder="Wklej tutaj treść publikacji...")

level = st.select_slider(
    "Skala uproszczenia:",
    options=[1, 2, 3, 4, 5],
    value=3
)

levels_map = {
    1: "Poziom Ekspert: Streszczenie akademickie, zachowaj terminologię.",
    2: "Poziom Student: Język formalny, skup się na konkretach.",
    3: "Poziom Standard: Język potoczny, wyjaśnij trudne pojęcia.",
    4: "Poziom Prosty: Używaj metafor, unikaj żargonu.",
    5: "Poziom ELI5: Wyjaśnij jak dziecku, maksimum obrazowych porównań."
}

st.caption(f"🎯 **Cel:** {levels_map[level]}")

# 5. Logika generowania
if st.button("🚀 Generuj notatkę"):
    if not api_key:
        st.error("Brak klucza API!")
    elif not input_text:
        st.warning("Najpierw wklej tekst.")
    else:
        with st.spinner("Agent analizuje dane..."):
            try:
                # Konfiguracja API
                genai.configure(api_key=api_key)
                
                # Wyłączenie filtrów (blokady tekstów naukowych)
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]

                # Lista modeli do przetestowania
                models_to_try = [model_choice, "gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-2.0-flash-exp"]
                success = False
                
                for m_name in models_to_try:
                    try:
                        # Próba wywołania konkretnego modelu
                        model = genai.GenerativeModel(model_name=m_name, safety_settings=safety_settings)
                        
                        full_prompt = f"Rola: Edytor. Cel: {levels_map[level]}. Format: lista punktowa, język polski. Tekst: {input_text}"
                        
                        response = model.generate_content(full_prompt)
                        
                        # Sprawdzenie czy AI coś zwróciło
                        if response and response.text:
                            st.markdown("---")
                            st.balloons()
                            st.subheader(f"📝 Wynik (Model: {m_name}):")
                            st.write(response.text)
                            success = True
                            break
                    except Exception as e:
                        st.toast(f"Model {m_name} niedostępny, sprawdzam kolejny...")
                        continue

                if not success:
                    st.error("Wszystkie modele AI odmówiły odpowiedzi (prawdopodobnie błąd regionu lub klucza).")
                    with st.expander("Zobacz co możesz zrobić:"):
                        st.write("1. Sprawdź, czy Twój klucz API jest poprawny (bez spacji).")
                        st.write("2. Jeśli jesteś w szkole, sieć może blokować serwery Google.")
                        st.write("3. Spróbuj udostępnić internet z telefonu (hotspot).")

            except Exception as e:
                st.error(f"Błąd krytyczny: {e}")
