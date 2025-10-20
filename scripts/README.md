# Scripts de Análisis Exploratorio de Datos (EDA)

**Proyecto:** Primera Entrega - Proyecto Final
**Curso:** MINE-4101: Ciencia de Datos Aplicada
**Fecha:** 2025-10-19

---

## Descripción General

Este directorio contiene **5 scripts de Python** diseñados para realizar un análisis exploratorio exhaustivo y profesional del dataset de usuarios de Engagement de una plataforma de delivery de comida.

Cada script está diseñado para ser **ejecutado de forma independiente** y genera reportes detallados en consola, permitiendo validar hallazgos antes de consolidarlos en el notebook final.

---

## Estructura de Scripts

### 1. `data_quality.py` - Análisis de Calidad de Datos

**Propósito:** Evaluar la calidad y consistencia del dataset.

**Análisis realizados:**
- ✅ Valores faltantes y duplicados
- ✅ Tipos de datos y consistencia
- ✅ Validación de reglas de negocio
- ✅ Detección de outliers (método IQR)
- ✅ Puntuación de calidad general

**Resultado Clave:**
- **Calidad del dataset: 100/100** ✅
- Sin valores faltantes
- Sin duplicados
- Todas las reglas de negocio validadas

**Ejecutar:**
```bash
cd scripts
python data_quality.py
```

---

### 2. `affinity_analysis.py` - Análisis de Afinidades

**Propósito:** Analizar las preferencias de consumo de los usuarios (categorías, marcas, tiendas).

**Análisis realizados:**
- 📊 Afinidad por categoría principal (28 categorías)
- 🏪 Afinidad por tipo de tienda (KA Type)
- 🛍️ Afinidad por tienda específica (11,534 tiendas)
- 🏷️ Afinidad por marca (817 marcas)
- 🎯 Análisis cruzado y especialización vs. diversificación

**Hallazgos Clave:**
- Solo **6 categorías** representan el **80%** de las órdenes
- **brand001** domina con **40.63%** del mercado
- **96.9%** de usuarios compran en **múltiples tiendas** (alta exploración)
- **38.5%** de usuarios son diversificados, **49.1%** moderados, **12.4%** especializados

**Ejecutar:**
```bash
cd scripts
python affinity_analysis.py
```

---

### 3. `univariate_analysis.py` - Análisis Univariado

**Propósito:** Análisis estadístico descriptivo de cada variable individualmente.

**Análisis realizados:**
- 🔢 Variables numéricas: estadísticas descriptivas, distribución, asimetría, curtosis
- 📊 Variables categóricas: frecuencias, diversidad (Shannon), concentración
- 📅 Variables temporales: distribución mensual y por día de semana
- 🔬 Tests de normalidad (Shapiro-Wilk / Anderson-Darling)

**Hallazgos Clave:**
- **Alta variabilidad** en todas las variables numéricas (CV > 50%)
- Distribuciones **asimétricas positivas** (cola derecha)
- Media de **14.9 días** para llegar a 4ta orden
- Recencia tiene **alta diversidad** (Shannon 0.85)
- Más actividad en **fines de semana** (35-36%)

**Ejecutar:**
```bash
cd scripts
python univariate_analysis.py
```

---

### 4. `multivariate_analysis.py` - Análisis Multivariado

**Propósito:** Explorar relaciones entre variables y probar hipótesis.

**Análisis realizados:**
- 🔗 Correlaciones (Pearson y Spearman)
- 📈 Relaciones categóricas-numéricas (ANOVA, Kruskal-Wallis)
- 🎲 Asociaciones categóricas (Chi-cuadrado, Cramér's V)
- 🚀 Patrones de crecimiento
- 🎯 Impacto de recencia y segmento R

**Hallazgos Clave:**
- **Correlación negativa**: efo_to_four vs delta_orders = **-0.201**
  - Usuarios que llegan MÁS RÁPIDO a su 4ta orden **CRECEN MÁS**
- **Impacto de Recencia es CRÍTICO**:
  - Activos (≤7d): **8.97 órdenes** promedio
  - Perdidos (>90d): **1.29 órdenes** (¡7x diferencia!)
- **r_segment002** es el mejor segmento en todas las métricas
- **city005 y city006** lideran en crecimiento

**Ejecutar:**
```bash
cd scripts
python multivariate_analysis.py
```

---

### 5. `visualizations.py` - Generación de Visualizaciones

**Propósito:** Crear visualizaciones profesionales para comunicar hallazgos.

**Visualizaciones generadas:**
- 📊 Distribuciones de variables numéricas (histogramas, boxplots, Q-Q plots)
- 📈 Distribuciones de variables categóricas (barplots, pie charts)
- 🔥 Recencia vs Crecimiento (múltiples perspectivas)
- ⚡ Velocidad de adopción vs Crecimiento (scatter, hexbin, tendencias)
- 🏆 Desempeño por segmento R
- 📅 Análisis temporal (series de tiempo, día de semana)
- 🌡️ Mapa de calor de correlaciones

**Salida:**
- **11 imágenes PNG** de alta resolución (300 DPI)
- Ubicación: `../visualizations/`
- Total: ~4.3 MB

**Ejecutar:**
```bash
cd scripts
python visualizations.py
```

---

## Resumen Ejecutivo de Hallazgos

### 🎯 Insights Principales

#### 1. Calidad de Datos
- ✅ **Excelente calidad**: 100/100
- ✅ Sin valores faltantes ni duplicados
- ✅ Todas las reglas de negocio validadas
- ⚠️ Outliers presentes pero válidos (usuarios power users)

#### 2. Comportamiento de Usuarios
- **96.9%** compran en **múltiples tiendas** (alta exploración)
- Promedio de **3.67 categorías** por usuario
- Promedio de **5.36 tiendas** visitadas
- **38.5%** de usuarios son **diversificados** en sus preferencias

#### 3. Factores de Crecimiento
- **Velocidad de adopción** es clave:
  - Usuarios que llegan rápido a 4ta orden → **Mayor crecimiento**
  - Correlación: -0.201 (negativa)

- **Recencia es crítica**:
  - Activos (≤7d): **8.97 órdenes**
  - Perdidos (>90d): **1.29 órdenes**
  - **Diferencia de 7x** entre extremos

#### 4. Segmentación
- **r_segment002**: Mejor desempeño en crecimiento (7.12 órdenes)
- **city005 y city006**: Ciudades con mayor crecimiento
- **32.7%** bajo crecimiento, **46.9%** medio, **20.3%** alto

#### 5. Concentración de Mercado
- **6 categorías** = 80% de órdenes
- **brand001** = 40.63% del mercado
- **20 tiendas** = 80% de órdenes (de 11,534 totales)

---

## Recomendaciones para el Notebook Final

### Técnicas a Incluir (Requisito del Proyecto)

✅ **Análisis Univariados:**
- Estadísticas descriptivas completas
- Distribuciones (gráficas)
- Tests de normalidad (no gráfico)

✅ **Análisis Multivariados:**
- Correlaciones (gráfico: heatmap)
- ANOVA / Kruskal-Wallis (no gráfico)
- Chi-cuadrado (no gráfico)
- Análisis de segmentación (gráfico)

✅ **Análisis Gráficos:**
- Histogramas, boxplots, scatter plots
- Hexbin plots (densidad)
- Series temporales
- Barplots de segmentación

✅ **Análisis No Gráficos:**
- Tests estadísticos (normalidad, diferencias de grupos)
- Índices de diversidad (Shannon)
- Coeficientes de asociación (Cramér's V)

---

## Próximos Pasos

1. ✅ Revisar outputs de cada script
2. ✅ Validar visualizaciones generadas
3. 🔲 Crear notebook Jupyter consolidado
4. 🔲 Seleccionar insights más relevantes para el reporte
5. 🔲 Documentar conclusiones e insights clave

---

## Dependencias

```bash
pip install pandas numpy scipy matplotlib seaborn
```

---

## Notas Técnicas

- Todos los scripts usan el mismo dataset: `../dataset_protegido (1).csv`
- Los scripts son independientes y pueden ejecutarse en cualquier orden
- Las visualizaciones se guardan automáticamente en `../visualizations/`
- Los análisis usan tanto métodos paramétricos como no paramétricos
- Se incluyen interpretaciones de todos los tests estadísticos

---

## Contacto

**Integrantes:**
- Juan David Valencia – 201728857
- Juan Esteban Cuellar – 202014258

**Curso:** MINE-4101: Ciencia de Datos Aplicada
**Semestre:** 2025-20
