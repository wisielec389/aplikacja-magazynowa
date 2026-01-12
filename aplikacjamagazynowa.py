import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="System Magazynowy 1.0", layout="wide")

url = "https://twoje-id.supabase.co"
key = "twój-anon-public-key"

# Stałe
MAX_MIEJSC = 10
MAX_OBCIAZENIE_KG = 1000

# Inicjalizacja stanu magazynu
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = [None] * MAX_MIEJSC

st.title("📦 Inteligentny Magazyn (Limit 1t)")

# --- BOCZNY PANEL ---
st.sidebar.header("Zarządzanie")

with st.sidebar.expander("➕ Dodaj produkt", expanded=True):
    nazwa = st.text_input("Nazwa")
    ilosc = st.number_input("Ilość (szt.)", min_value=1, step=1)
    waga_jedn = st.number_input("Waga jedn. (kg)", min_value=0.1, step=0.1)
    
    if st.button("Zatwierdź dostawę"):
        wolne = [i for i, m in enumerate(st.session_state.magazyn) if m is None]
        total_waga = ilosc * waga_jedn
        
        if not wolne:
            st.error("Magazyn pełny!")
        elif total_waga > MAX_OBCIAZENIE_KG:
            st.error(f"Przeciążenie! {total_waga}kg > {MAX_OBCIAZENIE_KG}kg")
        elif nazwa:
            idx = wolne[0]
            st.session_state.magazyn[idx] = {
                "Nazwa": nazwa,
                "Ilość": ilosc,
                "Waga_Total": total_waga
            }
            st.success(f"Dodano na miejsce {idx+1}")
            st.rerun()

with st.sidebar.expander("🗑️ Usuń produkt"):
    zajete = [i+1 for i, m in enumerate(st.session_state.magazyn) if m is not None]
    miejsce = st.selectbox("Numer miejsca", zajete if zajete else ["Pusto"])
    
    if st.button("Usuń") and miejsce != "Pusto":
        st.session_state.magazyn[miejsce - 1] = None
        st.rerun()

# --- PRZYGOTOWANIE DANYCH ---
miejsca_numery = [f"Miejsce {i+1}" for i in range(MAX_MIEJSC)]
wagi_dane = [m['Waga_Total'] if m else 0 for m in st.session_state.magazyn]
produkty_nazwy = [m['Nazwa'] if m else "WOLNE" for m in st.session_state.magazyn]

df_magazyn = pd.DataFrame({
    "Miejsce": miejsca_numery,
    "Produkt": produkty_nazwy,
    "Obciążenie (kg)": wagi_dane
})

# --- GŁÓWNY PANEL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Status slotów")
    st.table(df_magazyn)

with col2:
    st.subheader("📊 Wykorzystanie limitu wagowego")
    # Streamlitowy natywny wykres słupkowy
    st.bar_chart(df_magazyn.set_index("Miejsce")["Obciążenie (kg)"])
    
    # Dodatkowa informacja o limicie
    st.info(f"Maksymalne dopuszczalne obciążenie każdego slotu to {MAX_OBCIAZENIE_KG} kg.")

# Statystyki na dole
st.divider()
zajete_count = sum(1 for m in st.session_state.magazyn if m is not None)
c1, c2, c3 = st.columns(3)
c1.metric("Obłożenie slotów", f"{zajete_count}/{MAX_MIEJSC}")
c2.metric("Suma ładunku", f"{sum(wagi_dane):.1f} kg")
c3.metric("Średnie dociążenie", f"{sum(wagi_dane)/MAX_MIEJSC:.1f} kg")
