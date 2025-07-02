import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import matplotlib.dates as mdates


# Simulación de datos (sustituir por tu propio flujo de datos en vivo)
def generar_datos_en_vivo():
    tiempo_actual = pd.to_datetime("now")
    probabilidad_falla = np.random.rand()  # Simulamos probabilidades entre 0 y 1
    return tiempo_actual, probabilidad_falla


# Crear la interfaz de Streamlit
st.title("Monitoreo en Vivo de Probabilidad de Falla")

# Inicializar las listas para almacenar los datos del gráfico
x_data = []
y_data = []

# Configuración del gráfico
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title("Probabilidad de Falla en Tiempo Real")
ax.set_xlabel("Tiempo")
ax.set_ylabel("Probabilidad de Falla")
ax.axhline(y=0.7, color="r", linestyle="--", label="Umbral (0.7)")

# Actualizar el gráfico en vivo
for _ in range(100):  # Esto simula 100 iteraciones de datos en vivo
    # Generar un nuevo dato de probabilidad de falla
    tiempo, probabilidad = generar_datos_en_vivo()

    # Agregar los nuevos datos al gráfico
    x_data.append(tiempo)
    y_data.append(probabilidad)

    # Limpiar el gráfico anterior y graficar los datos actualizados
    ax.clear()

    # Graficar la probabilidad de falla
    ax.plot(x_data, y_data, label="Probabilidad de Falla", color="b")

    # Añadir la línea de umbral
    ax.axhline(y=0.7, color="r", linestyle="--", label="Umbral (0.7)")

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

    # Hacer una pausa para simular la llegada de nuevos datos
    time.sleep(1)  # Actualizar cada segundo o el intervalo que desees
