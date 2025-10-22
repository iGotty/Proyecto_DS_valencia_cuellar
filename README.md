# Proyecto Final - Ciencia de Datos Aplicada

**Curso:** MINE-4101: Ciencia de Datos Aplicada
**Semestre:** 2025-20
**Universidad:** Universidad de los Andes

## Integrantes

- **Juan David Valencia** – 201728857
- **Juan Esteban Cuellar** – 202014258

---

## 📑 Índice de Contenidos

1. [📦 Entregables Primera Entrega](#-entregables-primera-entrega)
2. [📋 Descripción del Proyecto](#-descripción-del-proyecto)
3. [🎯 Producto de Datos](#-producto-de-datos)
4. [📊 Dataset](#-dataset)
5. [🔍 Hallazgos Principales](#-hallazgos-principales)
6. [📁 Estructura del Proyecto](#-estructura-del-proyecto)
7. [🚀 Instrucciones de Ejecución](#-instrucciones-de-ejecución)
8. [📈 Resultados del Análisis](#-resultados-del-análisis)
9. [🔬 Próximos Pasos](#-próximos-pasos)
10. [📝 Resumen de Cumplimiento](#-resumen-de-cumplimiento---primera-entrega)

---

## 📦 Entregables Primera Entrega

> **📌 IMPORTANTE:** Los siguientes son los entregables principales de la primera entrega. Haz clic en los enlaces para acceder directamente a cada documento.

### Documentos Principales

| Entregable | Descripción | Ubicación |
|------------|-------------|-----------|
| 📄 **Documento PDF** | Documento ejecutivo de 5 páginas | [Ver PDF](documento/PRIMERA%20ENTREGA%20Proyecto%20Final%20_%20Ciencia%20de%20datos%20(1)%20(1).pdf) |
| 📊 **Notebook** | Análisis exploratorio completo (ejecutable sin errores) | [Ver Notebook](notebooks/entendimiento_datos.ipynb) |
| 🎥 **Video** | Sustentación de 5 minutos del equipo | [Ver Video](video/videoprimeraentrega.mp4) |
| 📊 **Presentación** | Diapositivas utilizadas en el video | [Ver Presentación](video/Presentacion%20-%20Primera%20Entrega%20Proyecto%20Ciencia%20de%20datos.pdf) |

---

## 📋 Descripción del Proyecto

Este proyecto desarrolla una solución de ciencia de datos para una **plataforma de delivery de comida**, enfocándose en la caracterización y segmentación de usuarios nuevos del equipo de Engagement para optimizar estrategias de retención y crecimiento.

### Problemática

El equipo de Engagement no cuenta con un esquema claro para priorizar recursos y definir qué usuarios recientes tienen mayor probabilidad de seguir creciendo en órdenes, limitando la efectividad de las estrategias de retención.

### Objetivo

Caracterizar y segmentar a los nuevos usuarios (aquellos que alcanzaron su cuarta orden) para identificar perfiles de alto potencial, entendiendo su comportamiento en los tres meses posteriores.

### Alcance

**Primera Entrega:**
- ✅ Entendimiento del negocio y definición de la problemática
- ✅ Diseño del producto de datos (dashboard + modelo + recomendaciones)
- ✅ Identificación de aspectos éticos y de privacidad
- ✅ Definición del enfoque analítico (hipótesis, técnicas, métricas)
- ✅ Recolección y documentación de fuentes de datos
- ✅ Análisis exploratorio exhaustivo (univariado, multivariado, gráfico)
- ✅ Conclusiones iniciales y próximos pasos

**Segunda Entrega:**
- Preparación y limpieza de datos
- Modelado predictivo (Random Forest, XGBoost, LightGBM)
- Construcción del producto de datos funcional
- Evaluación y retroalimentación con stakeholders

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
│   └── PRIMERA ENTREGA Proyecto Final _
│       Ciencia de datos (1) (1).pdf               # 📄 DOCUMENTO PDF EJECUTIVO
│
├── 📁 notebooks/
│   └── entendimiento_datos.ipynb                  # 📊 NOTEBOOK DE ANÁLISIS
│
├── 📁 video/
│   ├── videoprimeraentrega.mp4                    # 🎥 VIDEO DE SUSTENTACIÓN
│   └── Presentacion - Primera Entrega
│       Proyecto Ciencia de datos.pdf              # 📊 PRESENTACIÓN PDF
│
├── 📁 scripts/                                     # Scripts Python de análisis
│   ├── README.md                                  # Guía de scripts
│   ├── data_quality.py                            # Análisis de calidad
│   ├── affinity_analysis.py                       # Análisis de afinidades
│   ├── univariate_analysis.py                     # Análisis univariado
│   ├── multivariate_analysis.py                   # Análisis multivariado
│   └── visualizations.py                          # Generación de gráficas
│
├── 📁 visualizations/                              # Gráficas generadas (11 PNGs)
│
└── 📄 dataset_protegido (1).csv                    # Dataset original
```

---

## 🚀 Instrucciones de Ejecución

### Dependencias

```bash
pip install pandas numpy scipy matplotlib seaborn jupyter
```

### Opción 1: Ejecutar Notebook Principal (Recomendado)

El análisis completo está consolidado en el notebook ejecutable:

```bash
jupyter notebook notebooks/entendimiento_datos.ipynb
```

**Nota:** El notebook se ejecuta secuencialmente sin errores. Contiene todo el análisis exploratorio de datos requerido para la primera entrega.

### Opción 2: Ejecutar Scripts Individuales

Alternativamente, se pueden ejecutar los scripts modulares:

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

## 📝 Resumen de Cumplimiento - Primera Entrega

### Checklist de Requisitos ✅

| Requisito | Peso | Estado | Evidencia |
|-----------|------|--------|-----------|
| Definición de problemática y negocio | 10% | ✅ | [Ver PDF](documento/PRIMERA%20ENTREGA%20Proyecto%20Final%20_%20Ciencia%20de%20datos%20(1)%20(1).pdf) |
| Ideación del producto de datos | 10% | ✅ | [Ver PDF](documento/PRIMERA%20ENTREGA%20Proyecto%20Final%20_%20Ciencia%20de%20datos%20(1)%20(1).pdf) |
| Aspectos éticos y responsables | 10% | ✅ | [Ver PDF](documento/PRIMERA%20ENTREGA%20Proyecto%20Final%20_%20Ciencia%20de%20datos%20(1)%20(1).pdf) |
| Enfoque analítico | 15% | ✅ | [Ver PDF](documento/PRIMERA%20ENTREGA%20Proyecto%20Final%20_%20Ciencia%20de%20datos%20(1)%20(1).pdf) |
| Recolección de datos | 10% | ✅ | [Ver Notebook](notebooks/entendimiento_datos.ipynb) |
| Análisis exploratorio de datos | 35% | ✅ | [Ver Notebook](notebooks/entendimiento_datos.ipynb) |
| Conclusiones iniciales | 10% | ✅ | [Ver PDF](documento/PRIMERA%20ENTREGA%20Proyecto%20Final%20_%20Ciencia%20de%20datos%20(1)%20(1).pdf) |

### Formatos de Entrega ✅

- ✅ **Repositorio GitHub público** con código auto-contenido
- ✅ **README completo** con integrantes, objetivo, alcance, conclusiones e instrucciones
- ✅ **Notebook ejecutable** sin errores ([notebooks/entendimiento_datos.ipynb](notebooks/entendimiento_datos.ipynb))
- ✅ **Documento PDF ejecutivo** de 5 páginas, Arial 12
- ✅ **Video de sustentación** de 5 minutos con todos los integrantes
- ✅ **Diapositivas** incluidas en el repositorio

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
