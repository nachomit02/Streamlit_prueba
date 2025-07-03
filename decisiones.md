### 📌 Decisiones tomadas en el desarrollo del modelo de predicción de fallas

---

#### 1. **Selección de Variables**

- Se analizaron las variables mediante **correlación** con la variable objetivo `estado`, identificando aquellas con mayor relación con la ocurrencia de fallas.
- Luego se aplicó **Random Forest** para realizar una selección empírica adicional, considerando la importancia de cada variable para la predicción.
- Las variables finales elegidas fueron:
  - `DV_pressure`
  - `DV_pressure_var6`
  - `Oil_temperature`
  - `TP2`

---

#### 2. **Modelo elegido**

- Se probó inicialmente con **XGBoost**, pero las métricas obtenidas no superaron a las del modelo Random Forest, por lo tanto se descartó.
- Se optó por **Random Forest** por su **robustez ante ruido**, buena capacidad de generalización y por manejar bien la mezcla de variables correlacionadas y no lineales.

---

#### 3. **Detección temprana (ventanas)**

- El modelo no fue entrenado directamente con ventanas deslizantes, pero se simuló su uso en producción dividiendo la serie en ventanas de 10 a 20 minutos, y prediciendo si habría una falla en los próximos 60 minutos.
- Esto permite una **detección anticipada** basada en el comportamiento reciente de las variables clave.

---

#### 4. **Umbral de clasificación**

- Se realizaron pruebas con distintos **thresholds** para definir cuándo una probabilidad debería considerarse una alerta de falla.
- Los resultados se evaluaron en función de la relación entre **Falsos Positivos (FP)** y **Falsos Negativos (FN)**.
- Se eligió **umbral = 0.6** como valor por defecto para la POC, buscando minimizar los FN incluso a costa de un leve aumento en FP.
- Se considera que **0.7** podría ser una opción más conservadora para una versión en producción.

| Threshold | Falsos Positivos (FP) | Falsos Negativos (FN) | Comentario clave                      |
| --------- | --------------------- | --------------------- | ------------------------------------- |
| 0.9       | 9.241                 | 339                   | Muy pocos FP, pero más FN             |
| 0.8       | 10.023                | 249                   | Ligeramente más FP, bastante menos FN |
| 0.7       | 10.680                | 227                   | FP siguen subiendo, FN bajando        |
| 0.6       | 11.083                | 195                   | Más FP, pero mínimos FN               |

---

#### 5. **Simulación y visualización**

- Se desarrolló una simulación en **Streamlit** que muestra cómo evolucionaría la probabilidad de falla en tiempo real.
- Se utiliza un sistema de umbral dinámico que genera una alerta visible si la probabilidad supera el 0.6.
- El sistema está pensado para **detener el monitoreo al detectar una alerta**, permitiendo que el operador lo verifique manualmente.
