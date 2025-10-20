# Proyecto Final - Ciencia de Datos Aplicada

**Curso:** MINE-4101: Ciencia de Datos Aplicada
**Semestre:** 2025-20
**Universidad:** Universidad de los Andes

## Integrantes

- **Juan David Valencia** – 201728857
- **Juan Esteban Cuellar** – 202014258

---

## 📋 Descripción del Proyecto

Este proyecto desarrolla una solución de ciencia de datos para una **plataforma de delivery de comida**, enfocándose en la caracterización y segmentación de usuarios nuevos del equipo de Engagement para optimizar estrategias de retención y crecimiento.

### Problemática

El equipo de Engagement no cuenta con un esquema claro para priorizar recursos y definir qué usuarios recientes tienen mayor probabilidad de seguir creciendo en órdenes, limitando la efectividad de las estrategias de retención.

### Objetivo

Caracterizar y segmentar a los nuevos usuarios (aquellos que alcanzaron su cuarta orden) para identificar perfiles de alto potencial, entendiendo su comportamiento en los tres meses posteriores.

---

## 🎯 Producto de Datos

El proyecto propone construir:

1. **Dashboard interactivo** con métricas clave (órdenes totales, delta de órdenes, recencia, segmentación)
2. **Modelo predictivo** que calcule la probabilidad de crecimiento del usuario
3. **Sistema de recomendación** que priorice usuarios según su potencial y afinidades

---

## 📊 Dataset

- **Total de usuarios:** 41,667
- **Período:** Usuarios que alcanzaron su 4ta orden entre marzo y septiembre 2025
- **Variables:** 15 columnas (actividad, fechas, afinidades, segmentación)
- **Calidad:** 100/100 (sin valores faltantes ni duplicados)

---

## 🔍 Hallazgos Principales

### Top 5 Insights

1. **⚡ Velocidad de Adopción Predice Crecimiento**
   - Correlación: -0.201 (p < 0.001)
   - Usuarios rápidos crecen **2.3x más** que lentos

2. **🔥 Recencia es el Factor MÁS Crítico**
   - Usuarios activos vs perdidos: **diferencia de 7x**
   - ANOVA p < 0.001, efecto mediano (η² = 0.073)

3. **🏆 r_segment002 es Superior**
   - Mejor en crecimiento (7.12 vs 6.53-6.97 órdenes)
   - Mejor en órdenes totales (7.44)
   - Adopción más rápida (14.58 días)

4. **🛍️ Alta Exploración, Baja Lealtad**
   - 96.9% compran en múltiples tiendas
   - Solo 6 categorías = 80% de órdenes

5. **📅 Patrón de Fin de Semana**
   - 35.8% de actividad en sábado-domingo
   - Pico de nuevos usuarios en julio-agosto (66%)

---

## 📁 Estructura del Proyecto

```
Proyecto_DS/
│
├── 📄 README.md                                    # Este archivo
├── 📄 .gitignore                                   # Archivos ignorados por git
│
├── 📁 documento/
│   ├── Proyecto_Final.md                          # Requisitos del proyecto
│   └── Primera_Entrega_Proyecto_Final.md          # Documento principal de entrega
│
├── 📁 scripts/                                     # Scripts Python de análisis
│   ├── README.md                                  # Guía de scripts
│   ├── data_quality.py                            # Análisis de calidad
│   ├── affinity_analysis.py                       # Análisis de afinidades
│   ├── univariate_analysis.py                     # Análisis univariado
│   ├── multivariate_analysis.py                   # Análisis multivariado
│   └── visualizations.py                          # Generación de gráficas
│
├── 📁 notebooks/
│   └── entendimiento_datos.ipynb                  # Notebook consolidado
│
├── 📁 visualizations/                              # Gráficas generadas (11 PNGs)
│
├── 📄 dataset_protegido (1).csv                    # Dataset original
├── 📄 HALLAZGOS_CLAVE.md                          # Insights ejecutivos
├── 📄 RESUMEN_TRABAJO_REALIZADO.md                # Guía del proyecto
└── 📄 ENTREGA_COMPLETA.md                         # Checklist de entrega
```

---

## 🚀 Instrucciones de Ejecución

### Requisitos

```bash
pip install pandas numpy scipy matplotlib seaborn
```

### Ejecutar Análisis Completo

```bash
cd scripts

# 1. Análisis de calidad (~30 segundos)
python data_quality.py

# 2. Análisis de afinidades (~1 minuto)
python affinity_analysis.py

# 3. Análisis univariado (~1 minuto)
python univariate_analysis.py

# 4. Análisis multivariado (~1 minuto)
python multivariate_analysis.py

# 5. Generación de visualizaciones (~30 segundos)
python visualizations.py
```

### Ejecutar Notebook

```bash
cd notebooks
jupyter notebook entendimiento_datos.ipynb
```

---

## 📈 Resultados del Análisis

### Validación de Hipótesis

| Hipótesis | Estado | Evidencia |
|-----------|--------|-----------|
| H1: Velocidad de adopción predice crecimiento | ✅ VALIDADA | r=-0.201 (p<0.001), diferencia 2.3x |
| H2: Recencia predice volumen de órdenes | ✅ VALIDADA | ANOVA p<0.001, η²=0.073, diferencia 7x |
| H3: Afinidades orientan estrategias | ✅ VALIDADA | 6 categorías = 80%, diversidad 3.67 |

### Técnicas de Análisis Utilizadas

**Univariadas:**
- Estadísticas descriptivas (media, mediana, std, CV, asimetría, curtosis)
- Tests de normalidad (Shapiro-Wilk, Anderson-Darling)
- Índice de diversidad de Shannon

**Multivariadas:**
- Correlaciones (Pearson, Spearman)
- ANOVA y Kruskal-Wallis
- Chi-cuadrado de independencia
- Cramér's V

**Visualizaciones:**
- 11 gráficas profesionales (300 DPI)
- Histogramas, boxplots, scatter plots, heatmaps

---

## 🎯 KPIs del Proyecto

- **Delta de órdenes** entre periodos (Δ órdenes)
- **Tasa de actividad** por recencia (≤7d, 8-14d, 15-30d, 31-90d)
- **Retención** posterior a la cuarta orden
- **Costo por orden incremental** (CPOI)

---

## 📊 Métricas de Calidad

- **Calidad del dataset:** 100/100
- **Valores faltantes:** 0 (0%)
- **Duplicados:** 0 (0%)
- **Reglas de negocio validadas:** 4/4 (100%)

---

## 🔬 Próximos Pasos

### Segunda Entrega

1. **Preparación de Datos**
   - Feature engineering
   - Tratamiento de outliers
   - Codificación de variables

2. **Modelado**
   - Modelo de clasificación (usuarios de alto crecimiento)
   - Modelo de regresión (predicción de delta_orders)
   - Algoritmos: Random Forest, XGBoost, LightGBM

3. **Construcción del Producto**
   - Dashboard interactivo (Streamlit/Dash)
   - Sistema de recomendación
   - API REST

4. **Evaluación**
   - Validación cruzada
   - Métricas: AUC-ROC, RMSE, MAE
   - Retroalimentación con stakeholders

---

## 📚 Referencias

1. Superintendencia de Industria y Comercio. "Guía oficial de protección de datos personales." SIC, 2023.
   [Enlace](https://habeasdata.todoenuno.net.co/wp-content/uploads/2023/10/SuperIndustria-publico-la-Guia-oficial-de-proteccion-de-datos-personales_compressed.pdf)

---

## 📝 Notas

- **Fecha de Primera Entrega:** 19 de octubre de 2025
- **Fecha de Entrega Final:** 30 de noviembre de 2025
- **Estado:** Primera entrega COMPLETA ✅

---

## 📧 Contacto

Para consultas sobre el proyecto:
- Juan David Valencia: jd.valencia@uniandes.edu.co
- Juan Esteban Cuellar: je.cuellar@uniandes.edu.co

---

**Universidad de los Andes**
**Facultad de Ingeniería**
**Maestría en Ingeniería - Ciencia de Datos**
**2025-20**
