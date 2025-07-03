import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import joblib
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Monitor de fallas del metro", layout="wide"
)  # opcional: título de la pestaña y layout
st.title("Monitor en tiempo real de fallas")

# Cargar modelo y features
modelo = joblib.load("modelo.pkl")
features = joblib.load("features.pkl")


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


def estandarizar(df):
    nulos = df.isnull().values.any()
    duplicados = df.duplicated().any()
    if nulos == False:
        print("No hay datos nulos en el dataset.")
    else:
        print("Revisar nulos por columna.")
    if duplicados == False:
        print("No hay filas duplicadas en el dataset.")
    else:
        print("Revisar duplicados.")
    df["estado"] = df["timestamp"].apply(estado)


def preparar_datos(df):
    df = df.copy()
    df["DV_pressure_ma6"] = df["DV_pressure"].rolling(window=6, min_periods=1).mean()
    df["DV_pressure_var6"] = df["DV_pressure"].rolling(window=6, min_periods=1).var()
    df = df.dropna(subset=features)
    return df


def predecir(df, threshold=0.6):
    df_proc = preparar_datos(df)
    X = df_proc[features]
    probs = modelo.predict_proba(X)[:, 1]
    pred = (probs >= threshold).astype(int)
    df_proc["probabilidad"] = probs
    df_proc["prediccion"] = pred
    return df_proc[["timestamp", "probabilidad", "prediccion"]]


# Cargar los datos
data = pd.read_csv("metro_dataset.csv.gz")
data = data.drop(columns=["Unnamed: 0"])
data = preparar_datos(data)
data["timestamp"] = pd.to_datetime(data["timestamp"])
data = data[data["timestamp"] >= pd.Timestamp("2020-04-18 00:00:01")]
prediccion = predecir(data)
prediccion["timestamp"] = pd.to_datetime(prediccion["timestamp"])
prediccion["estado"] = prediccion["timestamp"].apply(estado)
prediccion = prediccion.set_index("timestamp")

# Convertimos la serie en listas para simular en vivo
timestamps = prediccion.index.to_list()
probabilidades = prediccion["probabilidad"].to_list()


def generar_datos_en_vivo_real(i):
    if i < len(timestamps):
        return timestamps[i], probabilidades[i]
    else:
        return None, None


def actualizar_grafico():
    global x_data, y_data

    chart_placeholder = st.empty()
    alerta_activa = False  # bandera para controlar el envío de alertas

    for i in range(len(timestamps)):
        tiempo, probabilidad = generar_datos_en_vivo_real(i)
        if tiempo is None:
            break

        x_data.append(tiempo)
        y_data.append(probabilidad)

        if len(x_data) > 10:
            x_data = x_data[1:]
            y_data = y_data[1:]

        ax.clear()
        ax.plot(x_data, y_data, label="Probabilidad de Falla", color="b")
        ax.axhline(y=umbral, color="r", linestyle="--", label="Umbral (0.90)")
        # ax.set_title("Probabilidad de Falla en Tiempo Real")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Probabilidad de Falla")
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
        plt.xticks(rotation=45)
        plt.tight_layout()

        chart_placeholder.pyplot(fig)

        # Control de alerta única
        if probabilidad > umbral and not alerta_activa:
            st.warning(
                f"¡Alerta! Posible falla detectada a las {tiempo.strftime('%Y-%m-%d %H:%M:%S')}. Probabilidad: {probabilidad:.2f}"
            )
            alerta_activa = True  # activa la bandera para no repetir la alerta
        elif probabilidad <= umbral:
            alerta_activa = False  # resetea la bandera cuando baja la probabilidad

        time.sleep(1)


x_data = []  # Lista de tiempos
y_data = []  # Lista de probabilidades
fig, ax = plt.subplots(figsize=(12, 6))
umbral = 0.90  # Ya lo usás dentro de la función

actualizar_grafico()
