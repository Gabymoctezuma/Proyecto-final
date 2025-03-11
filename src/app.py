import streamlit as st
import requests
from pickle import load
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el modelo
ruta_modelo = os.path.join(os.path.dirname(__file__), "../models/LinearRegression_default_42.sav")
model = load(open(ruta_modelo, "rb"))

# Configuración de página
st.set_page_config(page_title="Predicción de Humedad en Casa", page_icon="🌡️", layout="wide")

# Encabezado
st.title("🌡️ Aplicación de Predicción de Humedad en Casa")
st.write("Esta aplicación predice la humedad de tu casa y te da recomendaciones para mejorar la calidad del aire.")

# Entrada de datos con sliders
st.subheader("🔍 Ingresa los valores de los siguientes parámetros:")
col1, col2 = st.columns(2)

with col1:
    Consumo_electrico = st.slider("Consumo electrico (Watts)", 0.0, 5000.0, 1000.0, 10.0)
    Temp_exterior = st.slider("Temp_exterior: Temperatura exterior (°C)", -10.0, 40.0, 20.0, 0.1)
    Presion_exterior = st.slider("Presión exterior (hPa)", 900.0, 1100.0, 1013.0, 1.0)

with col2:
    Hum_exterior = st.slider("Humedad exterior (%)", 10.0, 100.0, 50.0, 1.0)
    Vel_viento = st.slider("Velocidad del viento (m/s)", 0.0, 30.0, 5.0, 0.1)
    Punto_rocio = st.slider("Punto de rocío (°C)", -10.0, 30.0, 10.0, 0.1)
    Temp_casa = st.slider("Temp_casa: Temperatura casa (°C)", -10.0, 40.0, 20.0, 0.1)

# Botón de predicción
if st.button("✨ Predecir Humedad en Casa"):
    input_data = np.array([[Consumo_electrico, Temp_exterior, Presion_exterior, Hum_exterior, Vel_viento, Punto_rocio, Temp_casa]])
    humedad_predicha = model.predict(input_data)[0]
    
    # Mostrar resultado con colores
    if humedad_predicha < 40:
        st.error(f"⚠️ La humedad en casa es baja: {humedad_predicha:.2f}%. Puede causar problemas respiratorios y favorecer virus y bacterias.")
        st.write("💡 **Consejos:** Usa humidificadores, coloca plantas y evita calefacción excesiva.")
    elif humedad_predicha > 50:
        st.warning(f"⚠️ La humedad en casa es alta: {humedad_predicha:.2f}%. Puede favorecer hongos y alergias.")
        st.write("💡 **Consejos:** Ventila tu casa, usa deshumidificadores y revisa filtraciones.")
    else:
        st.success(f"✅ La humedad en casa es óptima: {humedad_predicha:.2f}%.")
        st.write("🌿 Tu ambiente es saludable, ¡sigue así!")
    
    # Graficar los valores de entrada
    fig, ax = plt.subplots(figsize=(8, 4))
    valores = [Consumo_electrico, Temp_exterior, Presion_exterior, Hum_exterior, Vel_viento Punto_rocio, Temp_casa]
    etiquetas = ["Electrodom.", "Luces", "Temp_ext", "Presión_ext", "Hum_ext", "Viento", "Punto_rocio", "Temp_casa"]
    sns.barplot(x=etiquetas, y=valores, palette="viridis", ax=ax)
    ax.set_ylabel("Valor")
    ax.set_title("Valores de Entrada")
    st.pyplot(fig)

