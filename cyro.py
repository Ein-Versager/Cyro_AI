import streamlit as st
import google.generativeai as genai

st.title("TEST POŁĄCZENIA")
klucz = st.text_input("Wklej nowy klucz API:", type="password")

if st.button("TESTUJ"):
    try:
        genai.configure(api_key=klucz)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Odpowiedz jednym słowem: Działam")
        st.write(f"ODPOWIEDŹ AI: {response.text}")
    except Exception as e:
        st.error(f"BŁĄD: {e}")
