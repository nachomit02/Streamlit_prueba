import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.dates as mdates
import pandas as pd


# Simulación de los datos de probabilidad de falla (debe ser reemplazada por el modelo real)
def generar_datos_en_vivo():
    # Simulamos una probabilidad de falla entre 0 y 1
    probabilidad_falla = np.random.rand()  # Simulamos probabilidades entre 0 y 1
    tiempo_actual = pd.to_datetime("now")  # Obtenemos el tiempo actual
    return tiempo_actual, probabilidad_falla


# Inicializar la interfaz de Streamlit
st.title("Monitoreo en Vivo de Probabilidad de Falla")

# Configuración del gráfico
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title("Probabilidad de Falla en Tiempo Real")
ax.set_xlabel("Tiempo")
ax.set_ylabel("Probabilidad de Falla")
ax.axhline(y=0.7, color="r", linestyle="--", label="Umbral (0.7)")  # Umbral de alerta

# Lista para almacenar los datos
x_data = []  # Lista de tiempos
y_data = []  # Lista de probabilidades

# Variable de umbral
umbral = 0.90

# Crear el gráfico inicial
ax.set_xlim(
    pd.to_datetime("now") - pd.Timedelta(minutes=5),
    pd.to_datetime("now") + pd.Timedelta(minutes=1),
)  # Últimos 5 minutos de datos


# Función para actualizar el gráfico en tiempo real
def actualizar_grafico():
    global x_data, y_data

    for _ in range(100):  # Esto simula 100 iteraciones de datos en vivo
        # Generar un nuevo dato de probabilidad de falla
        tiempo, probabilidad = generar_datos_en_vivo()

        # Agregar los nuevos datos al gráfico
        x_data.append(tiempo)
        y_data.append(probabilidad)

        # Limitar el gráfico a los últimos 5 minutos
        if (
            len(x_data) > 10
        ):  # Mostrar solo los últimos 10 puntos (equivalente a 5 minutos)
            x_data = x_data[1:]
            y_data = y_data[1:]

        # Limpiar el gráfico anterior y graficar los datos actualizados
        ax.clear()
        ax.plot(x_data, y_data, label="Probabilidad de Falla", color="b")

        # Añadir la línea de umbral
        ax.axhline(y=umbral, color="r", linestyle="--", label="Umbral (0.90)")

        # Mejorar la visualización
        ax.set_title("Probabilidad de Falla en Tiempo Real")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Probabilidad de Falla")
        ax.legend()

        # Formato de las fechas en el eje X
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

        # Ajustar la visualización
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

        # Alerta si la probabilidad de falla supera el umbral
        if probabilidad > umbral:
            st.warning("¡Alerta! Se predice una posible falla.")

        # Pausa para simular la llegada de nuevos datos (1 segundo)
        time.sleep(1)  # Actualización cada 1 segundo


# Llamar la función para actualizar el gráfico en vivo
actualizar_grafico()
