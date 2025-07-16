
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Cartera Óptima", layout="centered")

st.title("📈 Simulador de Cartera Óptima para la Jubilación")
st.markdown("""
Calcula tu capital estimado a la jubilación y tu cartera óptima en función de tu perfil de riesgo.
""")

edad_actual = st.slider("Edad actual", min_value=18, max_value=60, value=30)
edad_jubilacion = st.slider("Edad de jubilación", min_value=60, max_value=70, value=67)
aporte_mensual = st.number_input("Aportación mensual (€)", min_value=0, value=200, step=25)
perfil_riesgo = st.selectbox("Perfil de riesgo", ["Conservador", "Moderado", "Agresivo"])

horizonte = edad_jubilacion - edad_actual
aporte_anual = aporte_mensual * 12
capital_inicial = 10000

rent_anual = {'Renta fija': 0.035, 'Fondo global': 0.07, 'Acciones S&P500': 0.09}
vol_anual = {'Renta fija': 0.05, 'Fondo global': 0.12, 'Acciones S&P500': 0.18}

portafolios = {
    'Conservador': {'Renta fija': 0.85, 'Fondo global': 0.01, 'Acciones S&P500': 0.14},
    'Moderado':    {'Renta fija': 0.36, 'Fondo global': 0.19, 'Acciones S&P500': 0.45},
    'Agresivo':    {'Renta fija': 0.01, 'Fondo global': 0.01, 'Acciones S&P500': 0.98},
}

pesos = portafolios[perfil_riesgo]
rentabilidad_esperada = sum(pesos[act] * rent_anual[act] for act in pesos)

capital = capital_inicial
historico = [capital]
for _ in range(horizonte):
    capital = capital * (1 + rentabilidad_esperada) + aporte_anual
    historico.append(capital)

df_hist = pd.DataFrame({
    "Edad": np.arange(edad_actual, edad_jubilacion + 1),
    "Capital acumulado (€)": historico
})

st.subheader("📊 Proyección del capital acumulado")
st.line_chart(df_hist.set_index("Edad"))

st.subheader("🧱 Distribución de la cartera óptima")
df_cartera = pd.DataFrame.from_dict(pesos, orient='index', columns=['Peso']).sort_values('Peso', ascending=False)
st.bar_chart(df_cartera)

st.success(f"💰 Capital estimado al jubilarte: {historico[-1]:,.2f} €")

st.caption("Simulación basada en rentabilidades históricas promedio. No constituye asesoramiento financiero.")
