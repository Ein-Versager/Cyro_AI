import streamlit as st
import google.generativeai as genai
import time

# 1. Konfiguracja strony
st.set_page_config(page_title="CYRO_AI", page_icon="🧠", layout="centered")

# 2. Styl CSS (poprawiony - bez 'rfr')
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
    model_choice = st.selectbox("Model główny:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.divider()
    st.info("Agent sprawdzi alternatywne modele w razie przeciążenia.")

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

# 5. Logika generowania (Oficjalna biblioteka)
if st.button("🚀 Generuj notatkę"):
    if not api_key:
        st.error("Brak klucza API!")
    elif not input_text:
        st.warning("Najpierw wklej tekst.")
    else:
        with st.spinner("Agent analizuje dane przez oficjalny protokół..."):
            # Konfiguracja biblioteki
            genai.configure(api_key=api_key)
            
            # Lista modeli do sprawdzenia
            models_to_try = [model_choice, "gemini-1.5-flash", "gemini-1.5-flash-8b"]
            success = False
            
            for m_name in models_to_try:
                try:
                    # Wybór modelu
                    model = genai.GenerativeModel(m_name)
                    
                    # Przygotowanie promptu
                    full_prompt = f"Rola: Edytor. Cel: {levels_map[level]}. Format: lista punktowa, język polski. Tekst: {input_text}"
                    
                    # Generowanie (z timeoutem wbudowanym w bibliotekę)
                    response = model.generate_content(full_prompt)
                    
                    # Wyświetlenie wyniku
                    st.markdown("---")
                    st.balloons()
                    st.subheader(f"📝 Wynik (Model: {m_name}):")
                    st.write(response.text)
                    
                    success = True
                    break # Wyjście z pętli po sukcesie
                    
                except Exception as e:
                    st.toast(f"Model {m_name} nie odpowiedział. Próbuję kolejny...")
                    time.sleep(1)
            
            if not success:
                st.error("Wszystkie modele AI są obecnie zajęte lub klucz API jest nieaktywny.")
                with st.expander("Dlaczego to się dzieje?"):
                    st.write("""
                    1. **Region:** Darmowe klucze czasem nie działają na serwerach w USA/UE.
                    2. **Limity:** Przekroczono liczbę słów na minutę dla planu 'Free'.
                    3. **Bezpieczeństwo:** Google zablokował odpowiedź, bo tekst zawiera wrażliwe dane.
                    """)
