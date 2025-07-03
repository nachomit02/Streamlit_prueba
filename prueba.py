import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import joblib
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

# --- PARÁMETROS ---
umbral = 0.90
pausa = 0.5  # segundos entre actualizaciones

# --- CARGA DE MODELO Y DATOS ---
modelo = joblib.load("modelo.pkl")
features = joblib.load("features.pkl")
data = pd.read_csv("metro_dataset.csv").drop(columns=["Unnamed: 0"])
data["timestamp"] = pd.to_datetime(data["timestamp"])


# --- FUNCIONES DE PROCESAMIENTO ---
def estado(fecha):
    if isinstance(fecha, datetime):
        fallas = [
            (datetime(2020, 4, 18, 0, 0), datetime(2020, 4, 18, 23, 59)),
            (datetime(2020, 5, 29, 23, 30), datetime(2020, 5, 30, 6, 0)),
            (datetime(2020, 6, 5, 10, 0), datetime(2020, 6, 7, 14, 30)),
            (datetime(2020, 7, 15, 14, 30), datetime(2020, 7, 15, 19, 0)),
        ]
        for inicio, fin in fallas:
            if inicio <= fecha <= fin:
                return 1
        return 0
    else:
        return 0


def preparar_datos(df):
    df = df.copy()
    df["DV_pressure_ma6"] = df["DV_pressure"].rolling(window=6, min_periods=1).mean()
    df["DV_pressure_var6"] = df["DV_pressure"].rolling(window=6, min_periods=1).var()
    df = df.dropna(subset=features)
    return df


def predecir(df):
    df_proc = preparar_datos(df)
    X = df_proc[features]
    probs = modelo.predict_proba(X)[:, 1]
    df_proc["probabilidad"] = probs
    df_proc["prediccion"] = (probs >= umbral).astype(int)
    return df_proc[["timestamp", "probabilidad", "prediccion"]]


# --- STREAMLIT SETUP ---
st.set_page_config(page_title="Sistema de Monitoreo de Falla", layout="wide")
st.title("🧠 Monitoreo de Probabilidad de Falla en Compresor del Tren")

# --- DATOS Y PREDICCIONES ---
df_pred = predecir(data)
df_pred["estado"] = df_pred["timestamp"].apply(estado)
df_pred = df_pred.set_index("timestamp")

# --- INICIALIZAR VISUALIZACIÓN ---
x_data = []
y_data = []
alertas = []

fig, ax = plt.subplots(figsize=(12, 6))
grafico = st.pyplot(fig)

st.markdown("---")

for i in range(len(df_pred)):
    tiempo = df_pred.index[i]
    prob = df_pred["probabilidad"].iloc[i]

    x_data.append(tiempo)
    y_data.append(prob)

    # Mantener 100 puntos visibles
    if len(x_data) > 100:
        x_data = x_data[1:]
        y_data = y_data[1:]

    # LIMPIAR y GRAFICAR
    ax.clear()
    ax.plot(x_data, y_data, label="Probabilidad de Falla", color="navy")
    ax.axhline(y=umbral, color="red", linestyle="--", label="Umbral (0.90)")

    ax.set_title("Probabilidad Estimada de Falla (en tiempo real)")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Probabilidad de Falla")
    ax.legend(loc="upper left")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    grafico.pyplot(fig)

    # DETECTAR ALERTA
    if prob >= umbral:
        if tiempo not in alertas:
            st.error(
                f"🚨 Posible falla detectada a las {tiempo.time()} con probabilidad {prob:.2f}"
            )
            alertas.append(tiempo)

    time.sleep(pausa)
