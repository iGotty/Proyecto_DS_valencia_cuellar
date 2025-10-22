# Proyecto Final - Ciencia de Datos Aplicada

Universidad de los Andes
MINE-4101: Ciencia de Datos Aplicada
Semestre 2025-20

## Integrantes

- Juan David Valencia – 201728857
- Juan Esteban Cuellar – 202014258

---

## Entregables

Todos los documentos de la primera entrega están en este repositorio:

- **Documento PDF**: [documento/PRIMERA ENTREGA Proyecto Final _ Ciencia de datos (1) (1).pdf](documento/PRIMERA%20ENTREGA%20Proyecto%20Final%20_%20Ciencia%20de%20datos%20(1)%20(1).pdf)
- **Notebook de análisis**: [notebooks/entendimiento_datos.ipynb](notebooks/entendimiento_datos.ipynb)
- **Video**: [video/videoprimeraentrega.mp4](video/videoprimeraentrega.mp4)
- **Presentación**: [video/Presentacion - Primera Entrega Proyecto Ciencia de datos.pdf](video/Presentacion%20-%20Primera%20Entrega%20Proyecto%20Ciencia%20de%20datos.pdf)

---

## Sobre el proyecto

### El problema

Trabajamos con una plataforma de delivery de comida que tiene un desafío: no saben cómo identificar qué usuarios nuevos tienen más probabilidad de convertirse en clientes frecuentes. Esto dificulta priorizar recursos y diseñar estrategias de retención efectivas.

### Nuestro objetivo

Analizar el comportamiento de usuarios que alcanzaron su cuarta orden para identificar patrones que nos permitan predecir quiénes tienen mayor potencial de crecimiento.

### Alcance

**Primera entrega (ya completada):**
- Entender el problema de negocio
- Diseñar la solución propuesta
- Analizar aspectos éticos
- Definir el enfoque analítico
- Recolectar y explorar los datos
- Sacar conclusiones iniciales

**Segunda entrega:**
- Preparar los datos
- Construir modelos predictivos
- Desarrollar el producto final
- Validar con stakeholders

---

## La solución propuesta

Queremos construir un sistema que ayude al equipo de Engagement a tomar mejores decisiones. Este sistema tendría:

1. Un **dashboard** para visualizar métricas clave de cada usuario
2. Un **modelo predictivo** que calcule la probabilidad de que un usuario siga creciendo
3. Un **sistema de recomendación** que priorice a qué usuarios enfocarse

---

## Los datos

Analizamos 41,667 usuarios que alcanzaron su cuarta orden entre marzo y septiembre de 2025. El dataset tiene 15 variables que incluyen información de actividad, fechas, preferencias y segmentación.

La calidad de los datos es buena: no hay valores faltantes ni duplicados.

---

## Lo que encontramos

Estos son los hallazgos más importantes del análisis exploratorio:

**1. La velocidad importa**
Los usuarios que llegan rápido a su cuarta orden terminan haciendo 2.3 veces más órdenes que los usuarios lentos. Hay una correlación significativa entre qué tan rápido adoptan la plataforma y cuánto crecen después.

**2. La recencia es crítica**
Los usuarios activos tienen 7 veces más órdenes que los inactivos. Esta es la variable más importante para predecir el comportamiento futuro.

**3. Un segmento destaca sobre los demás**
El segmento r_segment002 tiene mejor desempeño en todas las métricas: más crecimiento, más órdenes totales y adopción más rápida.

**4. Exploran mucho pero son poco leales**
El 96.9% de los usuarios compra en múltiples tiendas, pero solo 6 categorías concentran el 80% de las órdenes. Hay oportunidad de trabajar en lealtad a tiendas específicas.

**5. Los fines de semana son clave**
Más de un tercio de la actividad ocurre en fin de semana, y julio-agosto concentran el 66% de los nuevos usuarios.

---

## Cómo ejecutar el análisis

### Requisitos

```bash
pip install pandas numpy scipy matplotlib seaborn jupyter
```

### Opción 1: Notebook (recomendado)

```bash
jupyter notebook notebooks/entendimiento_datos.ipynb
```

El notebook se ejecuta sin errores y contiene todo el análisis.

### Opción 2: Scripts individuales

```bash
cd scripts
python data_quality.py
python affinity_analysis.py
python univariate_analysis.py
python multivariate_analysis.py
python visualizations.py
```

---

## Metodología

**Análisis univariado:**
- Estadísticas descriptivas
- Tests de normalidad
- Análisis de distribuciones

**Análisis multivariado:**
- Correlaciones (Pearson y Spearman)
- ANOVA y Kruskal-Wallis
- Chi-cuadrado
- Cramér's V

**Visualizaciones:**
- 11 gráficas en alta resolución que muestran patrones clave

---

## Validación de hipótesis

| Hipótesis | Estado | Evidencia |
|-----------|--------|-----------|
| La velocidad de adopción predice el crecimiento | Validada | Correlación -0.201, diferencia 2.3x |
| La recencia predice el volumen de órdenes | Validada | ANOVA significativo, diferencia 7x |
| Las afinidades ayudan a personalizar | Validada | 6 categorías = 80% de órdenes |

---

## Próximos pasos

Para la segunda entrega vamos a:

1. Preparar los datos para modelado
2. Entrenar modelos con Random Forest, XGBoost y LightGBM
3. Construir el producto completo (dashboard + API + modelo)
4. Validar todo con los stakeholders

