import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Cartera Óptima", layout="centered")

st.title("📈 Simulador de Cartera Óptima para la Jubilación")
st.markdown("Simula tu capital a la jubilación con diferentes escenarios y ajustes por inflación.")

# ----------- Entradas del usuario -------------
edad_actual = st.slider("Edad actual", min_value=18, max_value=60, value=30)
edad_jubilacion = st.slider("Edad de jubilación", min_value=60, max_value=70, value=67)
aporte_mensual = st.number_input("Aportación mensual (€)", min_value=0, value=200, step=25)
perfil_riesgo = st.selectbox("Perfil de riesgo", ["Conservador", "Moderado", "Agresivo"])
inflacion = st.number_input("Inflación anual estimada (%)", min_value=0.0, max_value=10.0, value=2.0) / 100

horizonte = edad_jubilacion - edad_actual
aporte_anual = aporte_mensual * 12
capital_inicial = 10000

# ----------- Supuestos de rentabilidad por perfil y escenarios -------------
escenarios = {
    'Conservador': [0.025, 0.035, 0.045],
    'Moderado':    [0.05,  0.07,  0.09],
    'Agresivo':    [0.07,  0.09,  0.12],
}

nombres_escenarios = ['Pesimista', 'Medio', 'Optimista']
colores = ['#e74c3c', '#f1c40f', '#2ecc71']

# ----------- Portafolios por perfil (rebalanceo implícito) -------------
portafolios = {
    'Conservador': {'Renta fija': 0.85, 'Fondo global': 0.01, 'Acciones S&P500': 0.14},
    'Moderado':    {'Renta fija': 0.36, 'Fondo global': 0.19, 'Acciones S&P500': 0.45},
    'Agresivo':    {'Renta fija': 0.01, 'Fondo global': 0.01, 'Acciones S&P500': 0.98},
}

pesos = portafolios[perfil_riesgo]

# ----------- Simulación de capital acumulado por escenario -------------
historicos = {}
for i, esc in enumerate(escenarios[perfil_riesgo]):
    capital = capital_inicial
    historico = [capital]
    for _ in range(horizonte):
        capital = capital * (1 + esc) + aporte_anual
        historico.append(capital)
    historicos[nombres_escenarios[i]] = historico

# ----------- Ajuste por inflación -------------
def ajustar_inflacion(valor, inflacion, años):
    return valor / ((1 + inflacion) ** años)

# ----------- Visualización -------------
st.subheader("📊 Evolución del capital acumulado (con rebalanceo anual)")
df_edad = np.arange(edad_actual, edad_jubilacion + 1)
df_capital = pd.DataFrame(historicos, index=df_edad)

st.line_chart(df_capital)

# Capital final ajustado por inflación (valor real)
capital_real = {
    escenario: ajustar_inflacion(historico[-1], inflacion, horizonte)
    for escenario, historico in historicos.items()
}

st.subheader("💸 Capital estimado al jubilarte (ajustado por inflación)")
for esc in nombres_escenarios:
    st.write(f"**{esc}**: {capital_real[esc]:,.2f} € (en euros de hoy)")

# ----------- Composición de cartera -------------
st.subheader("🧱 Composición de cartera (con rebalanceo anual)")
df_pesos = pd.DataFrame.from_dict(pesos, orient='index', columns=['Peso']).sort_values('Peso', ascending=False)
st.bar_chart(df_pesos)

# Nota sobre rebalanceo
st.caption("🔄 Se asume rebalanceo anual automático para mantener los pesos constantes a lo largo del tiempo.")