## Resultados del Modelo Final

El modelo final fue entrenado con `RandomForestClassifier`, usando un umbral de **0.6** para maximizar la detección temprana de fallas (aceptando mayor tasa de falsos positivos). A continuación, se resumen las métricas de evaluación:

- **Precision (clase 1 - falla):** 0.7286
- **Recall (clase 1 - falla):** 0.9935
- **F1-score (clase 1 - falla):** 0.8407
- **Accuracy general:** 0.9926

**Matriz de confusión:**

|                    | Predicho: No Falla | Predicho: Falla |
| ------------------ | ------------------ | --------------- |
| **Real: No Falla** | 1,475,850          | 11,083          |
| **Real: Falla**    | 195                | 29,759          |

Este enfoque reduce los falsos negativos a costa de algunos falsos positivos, lo que se considera aceptable en un sistema de mantenimiento preventivo.

---

## Acceso a la App

La demostración en vivo está disponible en Streamlit Cloud:

[Ir a la app de predicción de fallas](https://metro-tp-lab1-dh55rkcuynltqwuycsnpg4.streamlit.app/)
