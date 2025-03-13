import streamlit as st
import requests
from pickle import load
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import load

# 🔹 `st.set_page_config()` debe ser la primera instrucción de Streamlit
st.set_page_config(page_title="Mi App en Render 🚀", page_icon="🌡️", layout="wide")
import os
import streamlit as st

PORT = os.getenv("PORT", "8501")  # Usa el puerto de Render si está disponible
os.environ["STREAMLIT_SERVER_PORT"] = PORT
os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"


# Cargar el modelo comprimido
ruta_modelo = os.path.join(os.path.dirname(__file__), "../models/RandomForestRegressor_default_42_compressed.joblib")
model = load(ruta_modelo)

# Encabezado
st.title("🫁 HomeHumidity IA")
st.write("Esta aplicación predice la humedad de tu casa y te da recomendaciones para mejorar la calidad del aire.")

# Entrada de datos con sliders
st.subheader("🔍 Ingresa los valores de los siguientes parámetros:")
col1, col2 = st.columns(2)

with col1:
    Hum_exterior = st.slider("Humedad exterior (%)", 10.0, 100.0, 50.0, 1.0)
    st.markdown("[🔍 Consultar humedad exterior en Google](https://www.google.com/search?q=humedad+exterior+actual)")

    Temp_exterior = st.slider("Temperatura exterior (°C)", -10.0, 40.0, 20.0, 0.1)
    st.markdown("[🔍 Consultar temperatura exterior en Google](https://www.google.com/search?q=temperatura+exterior+actual)")

    Presion_exterior = st.slider("Presión exterior (hPa)", 900.0, 1100.0, 1013.0, 1.0)
    st.markdown("[🔍 Consultar presión atmosférica en Google](https://www.google.com/search?q=presion+atmosferica+actual)")

with col2:
    Vel_viento = st.slider("Velocidad del viento (m/s)", 0.0, 30.0, 5.0, 0.1)
    st.markdown("[🔍 Consultar velocidad del viento en Google](https://www.google.com/search?q=velocidad+del+viento+actual)")

    Punto_rocio = st.slider("Punto de rocío (°C)", -10.0, 30.0, 10.0, 0.1)
    st.markdown("[🔍 Consultar punto de rocío en Google](https://www.google.com/search?q=punto+de+rocío+actual)")

    Temp_casa = st.slider("Temperatura casa (°C)", -10.0, 40.0, 20.0, 0.1)
    st.caption("🏠 **Cómo medir:** Usa un termómetro ambiental para conocer la temperatura dentro de casa.")

# Botón de predicción
if st.button("✨ Predecir Humedad en Casa"):
    input_data = np.array([[Temp_exterior, Presion_exterior, Hum_exterior, Vel_viento, Punto_rocio, Temp_casa]])
    humedad_predicha = model.predict(input_data)[0]

    # Mostrar resultado con colores
    if humedad_predicha < 40:
        st.error(f"🟥⬇️ La humedad en casa es baja: {humedad_predicha:.2f}%. Puede causar problemas respiratorios y favorecer virus y bacterias.")
        st.write("💡 **Consejos:** Usa humidificadores, coloca plantas y evita calefacción excesiva.")

        # Mostrar enlace a venta de plantas
        st.subheader("🌿 Tiendas donde puedes comprar plantas para mejorar la humedad:")
        st.markdown("""
        - [Amazon: Plantas para el hogar](https://www.amazon.com/s?k=plantas+para+el+hogar)
        - [Mercado Libre: Plantas de interior](https://www.mercadolibre.com.ar/plantas-de-in
        """)

    else:
        st.success(f"😃 La humedad en casa es óptima: {humedad_predicha:.2f}%.")
        st.write("🌿 Tu ambiente es saludable, ¡sigue así!")