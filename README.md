# Monitoreo Predictivo de Falla en Compresores de Trenes

Proyecto desarrollado como simulación de consultoría en el marco de la materia **Laboratorio de Datos con IA**. Utiliza datos reales del dataset MetroPT3 para construir un sistema de predicción de fallas en el sistema de compresión de un tren.

---

## Objetivo

El sistema busca **anticipar fallas** en los compresores neumáticos de un tren mediante el análisis de sensores en tiempo real. Para ello:

- Se construyó un modelo de machine learning entrenado con datos históricos etiquetados
- Se aplicó una lógica de predicción sobre ventanas temporales
- Se desarrolló una interfaz de monitoreo en vivo usando Streamlit

---

## Stakeholders simulados

- **Operadores ferroviarios**: necesitan conocer en tiempo real si un tren está en riesgo de falla.
- **Ingenieros de mantenimiento**: usan el sistema para activar intervenciones preventivas.
- **Área de operaciones**: puede tomar decisiones logísticas a partir del riesgo estimado.

---

## Modelo implementado

- Algoritmo: `RandomForestClassifier`
- Variables utilizadas:
  - `DV_pressure` – Caída de presión al descargar
  - `DV_pressure_var6` – Varianza móvil de DV_pressure
  - `Oil_temperature`
  - `TP2` – Presión en el compresor
- Ingeniería de características con ventanas móviles
- Entrenamiento sobre histórico etiquetado con variable `estado`
- Umbral de alerta: `p > 0.6` para señal de riesgo
