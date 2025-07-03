import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import matplotlib.dates as mdates

st.set_page_config(page_title="Predicción de Fallas en Trenes", layout="wide")

# Título principal
st.title("🔧 Monitoreo en Tiempo Real de Probabilidad de Falla")
st.subheader(
    "Sistema de Predicción Preventiva (Ventana móvil de 5 minutos hacia adelante)"
)
st.caption("Frecuencia de muestreo: 1 Hz | Umbral crítico: 0.9")

# Variables simuladas
x_data = []
y_data = []
alerta_activada = st.session_state.get("alerta_activada", False)

# Crear el contenedor para el gráfico
grafico = st.empty()

# Botón para reanudar después de alerta
if alerta_activada:
    if st.button("✅ Ya se revisó el sistema, continuar monitoreo"):
        st.session_state.alerta_activada = False
        alerta_activada = False


# Simulador de datos reales
def generar_dato():
    tiempo_actual = pd.to_datetime("now")
    # Simular un patrón creciente con algo de ruido
    base = len(x_data) / 200
    probabilidad = np.clip(0.4 + 0.6 * np.sin(base) + np.random.normal(0, 0.05), 0, 1)
    return tiempo_actual, probabilidad


# Loop principal solo si no hay alerta
if not alerta_activada:
    for _ in range(300):  # Cambiar a 3600 para simular una hora entera
        tiempo, prob = generar_dato()
        x_data.append(tiempo)
        y_data.append(prob)

        if prob > 0.9:
            st.session_state.alerta_activada = True
            st.error("⚠️ ALERTA: CHEQUEAR SISTEMA", icon="🚨")
            break

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(
            x_data, y_data, label="Probabilidad de Falla", color="blue", linewidth=2
        )
        ax.axhline(
            y=0.9,
            color="red",
            linestyle="--",
            linewidth=1.5,
            label="Umbral crítico (0.9)",
        )
        ax.set_ylabel("Probabilidad", fontsize=12)
        ax.set_xlabel("Tiempo", fontsize=12)
        ax.set_title("Probabilidad de Falla a Futuro (Próximos 5 minutos)", fontsize=14)
        ax.set_ylim([0, 1.05])
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        ax.legend()
        ax.grid(True)

        plt.xticks(rotation=45)
        plt.tight_layout()

        grafico.pyplot(fig)
        time.sleep(1)
