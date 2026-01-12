import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="System Zarządzania Magazynem", layout="wide")

# Stałe
MAX_MIEJSC = 10
MAX_OBCIAZENIE_KG = 1000

# Inicjalizacja stanu magazynu w sesji (żeby dane nie znikały przy odświeżaniu)
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = [None] * MAX_MIEJSC

st.title("📦 System Zarządzania Magazynem (1.0t / Miejsce)")

# --- BOCZNY PANEL: ZARZĄDZANIE ---
st.sidebar.header("Zarządzanie produktami")

# 1. Dodawanie produktów
with st.sidebar.expander("➕ Dodaj nowy produkt", expanded=True):
    nazwa = st.text_input("Nazwa produktu")
    ilosc = st.number_input("Ilość (szt.)", min_value=1, step=1)
    waga_jedn = st.number_input("Waga jednostkowa (kg)", min_value=0.1, step=0.1)
    
    if st.button("Dodaj do magazynu"):
        wolne_indeksy = [i for i, m in enumerate(st.session_state.magazyn) if m is None]
        
        total_waga = ilosc * waga_jedn
        
        if not wolne_indeksy:
            st.error("Brak wolnych miejsc w magazynie!")
        elif total_waga > MAX_OBCIAZENIE_KG:
            st.error(f"Przekroczono limit wagi! (Próba: {total_waga}kg / Limit: {MAX_OBCIAZENIE_KG}kg)")
        elif nazwa == "":
            st.warning("Podaj nazwę produktu.")
        else:
            idx = wolne_indeksy[0]
            st.session_state.magazyn[idx] = {
                "nazwa": nazwa,
                "ilosc": ilosc,
                "waga_jedn": waga_jedn,
                "waga_total": total_waga
            }
            st.success(f"Dodano {nazwa} na miejsce {idx+1}")

# 2. Usuwanie produktów
with st.sidebar.expander("🗑️ Usuń produkt"):
    zajete_miejsca = [i+1 for i, m in enumerate(st.session_state.magazyn) if m is not None]
    miejsce_do_usuniecia = st.selectbox("Wybierz numer miejsca", zajete_miejsca if zajete_miejsca else ["Brak"])
    
    if st.button("Usuń zaznaczone"):
        if miejsce_do_usuniecia != "Brak":
            st.session_state.magazyn[miejsce_do_usuniecia - 1] = None
            st.rerun()

# --- GŁÓWNY PANEL: WIDOK MAGAZYNU ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Tabela stanów")
    data = []
    for i, m in enumerate(st.session_state.magazyn):
        if m:
            data.append([i+1, m['nazwa'], m['ilosc'], m['waga_total'], f"{(m['waga_total']/MAX_OBCIAZENIE_KG)*100:.1f}%"])
        else:
            data.append([i+1, "WOLNE", 0, 0, "0%"])
    
    df = pd.DataFrame(data, columns=["Miejsce", "Produkt", "Ilość", "Waga (kg)", "Obciążenie"])
    st.table(df)

with col2:
    st.subheader("📊 Wykres obciążenia")
    
    miejsca = [f"M.{i+1}" for i in range(MAX_MIEJSC)]
    wagi = [m['waga_total'] if m else 0 for m in st.session_state.magazyn]
    
    # Dobór kolorów
    kolory = []
    for w in wagi:
        if w > 900: kolory.append('#ff4b4b') # Czerwony
        elif w > 500: kolory.append('#ffa500') # Pomarańczowy
        else: kolory.append('#2eb82e') # Zielony

    fig, ax = plt.subplots()
    bars = ax.bar(miejsca, wagi, color=kolory)
    ax.axhline(y=MAX_OBCIAZENIE_KG, color='red', linestyle='--', label='Limit 1t')
    ax.set_ylabel("Waga (kg)")
    ax.set_ylim(0, 1100)
    ax.legend()
    
    st.pyplot(fig)

# Statystyki na dole
total_zajete = sum(1 for m in st.session_state.magazyn if m is not None)
st.divider()
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Zajęte miejsca", f"{total_zajete} / {MAX_MIEJSC}")
kpi2.metric("Wolne miejsca", MAX_MIEJSC - total_zajete)
kpi3.metric("Całkowita waga", f"{sum(wagi):.1f} kg")
  
