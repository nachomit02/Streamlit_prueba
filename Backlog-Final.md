# Backlog Final – Mantenimiento Predictivo de Compresores (MetroPT3)

---

## Actividades Finalizadas

### Dataset & EDA

- Elección del dataset `MetroPT3 (AirCompressor).csv`
- Análisis exploratorio (EDA) de variables continuas y categóricas
- Revisión de registros faltantes y duplicados
- Creación de una variable binaria `estado` para identificar fallas (según 4 intervalos definidos)
- Visualización temporal y detección de patrones previos a fallas

---

### Preprocesamiento de datos

- Cálculo de variables estadísticas (media móvil y varianza)
- Resampleo a 10 segundos y 10 minutos para entrenamiento y visualización
- Eliminación de columnas irrelevantes
- Ingeniería de features adicionales (`DV_pressure_var6`)
- Selección de variables por correlación + Random Forest
- Normalización y escalado cuando fue necesario
- División en `train/test` con balanceo 50/50 (falla/no falla)

---

### Modelado y Evaluación

- Entrenamiento con `RandomForestClassifier`
- Optimización de hiperparámetros con `RandomizedSearchCV`
- Evaluación con métricas: accuracy, precision, recall, F1-score
- Selección de umbral óptimo (`threshold = 0.6`) en función de FN/FP
- Validación final sobre datos completos (`df_10min`)
- Guardado del modelo en `modelo.pkl` y features en `features.pkl`

---

### Visualización Interactiva (Streamlit)

- Desarrollo de `script.py` para visualización en tiempo real
- Lectura del modelo + simulación de datos históricos
- Predicción en ventanas móviles de 20 minutos con horizonte de predicción de 5 minutos
- Alertas visuales (`st.warning`) ante probabilidades > 0.9
- Control con botón para continuar la simulación tras una alerta
- Visualización única continua (no múltiples gráficos)
