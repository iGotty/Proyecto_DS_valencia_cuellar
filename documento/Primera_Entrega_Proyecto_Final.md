# Primera Entrega - Proyecto Final

**Curso:** MINE-4101: Ciencia de Datos Aplicada  
**Semestre:** 2025-20  
**Integrantes:**  
- Juan David Valencia – 201728857  
- Juan Esteban Cuellar – 202014258  

---

## 1. Definición de la problemática y entendimiento del negocio

La empresa analizada es una **plataforma de delivery de comida** que busca aumentar la cantidad de órdenes. Dentro del negocio existen dos equipos encargados de los usuarios:

- **Growth:** encargado de acompañar al usuario desde su primera hasta su cuarta orden.  
- **Engagement:** toma el relevo una vez los usuarios alcanzan esa cuarta compra.

El análisis se enfoca en los **usuarios nuevos de Engagement**, es decir, aquellos que completaron su cuarta orden entre el **29 de marzo y el 29 de septiembre** y que no hicieron parte de la segmentación inicial del año. Se consideraron únicamente los usuarios clasificados con `r_segment`, que es una clasificación proveniente de otra línea de negocio, y que históricamente muestra que estos son usuarios con mejor comportamiento y mayor potencial futuro en la vertical de comida.

El problema principal es que el equipo de Engagement **no cuenta con un esquema claro para priorizar recursos y definir qué usuarios recientes tienen mayor probabilidad de seguir creciendo en órdenes.** Esto limita la efectividad de las estrategias de retención e incrementa el costo por adquisición.

El objetivo del proyecto es **caracterizar y segmentar a estos nuevos usuarios** para identificar perfiles de alto potencial, entendiendo su comportamiento en los tres meses posteriores a la cuarta orden. Los resultados permitirán orientar de forma más eficiente las campañas e incentivos.

**KPIs principales:**
- Delta de órdenes entre periodos (Δ órdenes)  
- Tasa de actividad por recencia (≤7d, 8–14d, 15–30d, 31–90d)  
- Retención posterior a la cuarta orden  
- Costo por orden incremental (CPOI)

---

## 2. Ideación del producto de datos

El producto propuesto busca apoyar al equipo de Engagement en la toma de decisiones sobre a quién dirigir incentivos y comunicaciones, **optimizando el uso del presupuesto promocional.**

La idea es construir una herramienta analítica que combine **visualización y modelado** para identificar usuarios dentro del grupo de nuevos usuarios que alcanzaron su cuarta orden.

**Usuarios internos:**
- Equipo de Engagement: para definir estrategias de retención y priorización de campañas.  
- Equipo de Operaciones: para ejecutar envíos segmentados según tipo de usuario.  
- Equipo de Data: para ajustar modelos de propensión y validar resultados.

**Componentes del producto:**
- Dashboard interactivo que muestre métricas clave (órdenes totales, delta de órdenes, recencia, y segmentación por afinidades).  
- Modelo analítico que calcule la probabilidad de que un usuario vuelva a ordenar en los próximos 30–90 días.  
- Recomendador de incentivos, que priorice los usuarios según su potencial y afinidades (categorías, marcas o tipo de tienda).

**Mockup conceptual:**
- Vista principal con KPIs y evolución de cohortes.  
- Segmentación dinámica por frecuencia y velocidad de adopción (*EFO-to-Four*).  
- Panel de afinidades que muestra las categorías más frecuentes por grupo.

---

## 3. Responsible

El proyecto se basa en **datos internos de usuarios transaccionales**, por lo que se deben considerar aspectos de **privacidad, confidencialidad y transparencia**. Todos los identificadores fueron anonimizados y tokenizados, evitando la exposición de información personal o sensible.

Desde el punto de vista ético, el análisis debe garantizar que las recomendaciones **no generen discriminación ni sesgos** hacia grupos de usuarios específicos. También se busca mantener la **transparencia en el uso de los datos**, comunicando que el propósito del proyecto es mejorar la experiencia del usuario y optimizar las estrategias de retención.

En cuanto a aspectos regulatorios, el uso de la información se ajusta a la **Ley 1581 de 2012** y al **Decreto 1377 de 2013** sobre protección de datos personales en Colombia, así como a los principios de tratamiento legítimo, proporcionalidad y finalidad definidos por la **Superintendencia de Industria y Comercio (SIC, 2024)**.  
> Referencia: Superintendencia de Industria y Comercio – [Guía oficial de protección de datos personales](https://habeasdata.todoenuno.net.co/wp-content/uploads/2023/10/SuperIndustria-publico-la-Guia-oficial-de-proteccion-de-datos-personales_compressed.pdf)

---

## 4. Enfoque analítico

El análisis busca entender **qué factores explican el crecimiento en órdenes** de los nuevos usuarios de Engagement durante los tres meses posteriores a su cuarta compra.

**Hipótesis principales:**
1. Los usuarios con menor tiempo entre su primera y cuarta orden (*EFO-to-Four*) tienden a mostrar mayor crecimiento posterior.  
2. La frecuencia de actividad es un buen predictor de retención y volumen de órdenes.  
3. Las afinidades de consumo (categorías, marcas y tipo de tienda) pueden orientar estrategias personalizadas de incentivo.

El dataset contiene un número elevado de variables derivadas de las órdenes históricas, muchas de ellas representadas como variables tipo *one-hot encoder* (por ejemplo, conteos de categorías, marcas y tiendas). Esto genera **alta dimensionalidad**, lo que puede dificultar el modelado y aumentar el riesgo de sobreajuste.

**Estrategia para mitigar esto:**
- Agrupar variables similares (por categoría o tipo de tienda) para reducir el número de columnas.  
- Aplicar técnicas de reducción de dimensionalidad como **PCA** o **selección de características** basada en varianza o importancia del modelo.

**Métricas de evaluación:**
- Variación de órdenes (Δ órdenes)  
- Tasa de reactivación  
- Precisión del modelo (AUC o F1-score)

---

## 5. Recolección de datos

El dataset se construyó a partir de múltiples **tablas internas del sistema**, que almacenan información con diferentes estructuras y frecuencias de actualización. Las principales fuentes fueron tablas de órdenes, usuarios, tiendas y segmentaciones.

Uno de los mayores retos fue **integrar datos de varias tablas con diferentes estilos**. Se identificaron tres tipos de tabla:

- **Tablas incrementales** (como `dwm_finance_order_d_increment`) que agregan información día a día y pueden tener millones de registros.  
- **Tablas de versión diaria** (como `dwm_shop_wide_d_whole` o `dwm_user_order_info_label_d_whole`) que se sobrescriben cada día.  
- **Tablas estáticas o de referencia** (como `dim_city`), usadas para relacionar identificadores con variables descriptivas.

Además, fue necesario unir el `r_segment` proveniente de otra línea del negocio y alinear fechas para evitar duplicidad de registros. Esto implicó manejar múltiples uniones, condiciones de negocio y validaciones de consistencia antes de generar la base final.

El resultado fue un **dataset limpio y consolidado**, con un registro por usuario que resume su comportamiento, afinidades y nivel de actividad, listo para el análisis exploratorio.

---

## 6. Entendimiento de los datos

### 6.1 Calidad de los Datos

Se realizó un análisis exhaustivo de la calidad del dataset obteniendo los siguientes resultados:

**Evaluación de calidad:**
- **Puntuación general: 100/100** ✅
- **Valores faltantes:** 0 (0%)
- **Registros duplicados:** 0 (0%)
- **Registros analizados:** 41,667 usuarios

**Validación de reglas de negocio:**
1. ✅ `total_orders >= 4`: 0 violaciones (todos los usuarios alcanzaron su 4ta orden)
2. ✅ `delta_orders = total_orders - total_orders_tmenos1`: 0 violaciones
3. ✅ `fourth_order_date >= first_order_date`: 0 violaciones
4. ✅ `efo_to_four >= 0`: 0 violaciones

**Detección de outliers (método IQR):**
- `total_orders`: 2,578 outliers (6.19%) - Usuarios con más de 14 órdenes
- `delta_orders`: 2,402 outliers (5.76%) - Crecimiento superior a 14 órdenes
- `efo_to_four`: 0 outliers (0%) - Todos los valores dentro del rango esperado

**Conclusión:** El dataset presenta una **calidad óptima** sin requerir limpieza adicional. Los outliers identificados corresponden a usuarios "power users" con comportamiento válido y relevante para el análisis.

---

### 6.2 Análisis Exploratorio

El análisis exploratorio se realizó utilizando **técnicas univariadas, multivariadas, gráficas y no gráficas** para caracterizar el comportamiento de los usuarios y validar las hipótesis planteadas.

#### 6.2.1 Análisis Univariado

**Variables numéricas:**

| Variable | Media | Mediana | Desv. Std | CV (%) | Asimetría | Kurtosis |
|----------|-------|---------|-----------|--------|-----------|----------|
| total_orders | 7.2 | 6.0 | 4.97 | 68.7 | 3.11 | 17.98 |
| delta_orders | 6.9 | 5.0 | 4.99 | 72.3 | 3.16 | 18.35 |
| efo_to_four | 14.9 | 14.0 | 8.12 | 54.5 | 0.07 | -0.81 |

**Hallazgos clave:**
- **Alta variabilidad:** Todas las variables presentan coeficientes de variación superiores al 50%, indicando gran heterogeneidad en el comportamiento de los usuarios.
- **Distribuciones asimétricas:** `total_orders` y `delta_orders` presentan asimetría positiva fuerte (>3.0), con colas largas hacia la derecha debido a la presencia de usuarios con alto número de órdenes.
- **Distribución de velocidad:** `efo_to_four` presenta una distribución más simétrica (asimetría cercana a 0) con una media de 14.9 días.

**Variables categóricas:**

| Variable | Valores únicos | Categoría más frecuente | Frecuencia | Índice Shannon |
|----------|----------------|------------------------|------------|----------------|
| categoria_recencia | 5 | Frío (31-90d) | 33.7% | 0.85 |
| city_token | 7 | city006 | 39.6% | 0.74 |
| r_segment | 3 | r_segment001 | 38.3% | 0.99 |
| country_code | 1 | CO | 100% | - |

**Hallazgos clave:**
- **Alta diversidad en recencia:** Índice de Shannon de 0.85 indica que las categorías de recencia están bien distribuidas.
- **Segmento R balanceado:** Índice de Shannon de 0.99 (cercano al máximo de 1.10) indica distribución casi uniforme entre los 3 segmentos.
- **Concentración geográfica:** city006 y city001 concentran el 70% de los usuarios.

**Análisis temporal:**

- **Distribución mensual de primera orden:**
  - Mayo 2025: 0.0%
  - Junio 2025: 18.6%
  - Julio 2025: 32.4%
  - Agosto 2025: 33.6%
  - Septiembre 2025: 15.4%

- **Distribución por día de semana:**
  - Fin de semana (Sáb-Dom): **35.8%** de las órdenes
  - Entre semana (Lun-Vie): 64.2%
  - Día con mayor actividad: **Domingo (18.8%)**

**Conclusión:** El pico de adquisición se concentra en julio-agosto (66%), y existe un patrón marcado de mayor actividad en fines de semana, sugiriendo un uso recreativo/familiar de la plataforma.

#### 6.2.2 Análisis Multivariado

**Correlaciones (Pearson):**

|  | total_orders | delta_orders | efo_to_four |
|---|--------------|--------------|-------------|
| total_orders | 1.000 | 0.994 | -0.198 |
| delta_orders | 0.994 | 1.000 | -0.201 |
| efo_to_four | -0.198 | -0.201 | 1.000 |

**Hallazgos clave:**
- **Correlación casi perfecta** entre `total_orders` y `delta_orders` (0.994) - esperado por construcción del dataset.
- **Correlación negativa moderada** entre `efo_to_four` y `delta_orders` (-0.201) - **VALIDACIÓN DE HIPÓTESIS 1**: Usuarios que llegan más rápido a su 4ta orden tienden a tener mayor crecimiento posterior.

**Análisis de la relación Recencia vs Crecimiento:**

| Categoría de Recencia | N usuarios | Delta promedio | Desv. Std | Diferencia vs Perdido |
|----------------------|------------|----------------|-----------|----------------------|
| Activo (≤7d) | 12,369 | **8.97** | 6.86 | **7.0x** |
| Semi-Activo (8-14d) | 6,393 | 7.45 | 4.53 | 5.8x |
| Tibio (15-30d) | 8,603 | 6.51 | 3.48 | 5.0x |
| Frío (31-90d) | 14,064 | 5.02 | 2.58 | 3.9x |
| Perdido (>90d) | 238 | **1.29** | 0.55 | 1.0x |

**Test ANOVA:**
- F-estadístico: 1,087.5
- P-valor: < 0.001
- **Conclusión:** Existen diferencias estadísticamente significativas entre las categorías de recencia.

**Tamaño del efecto (η²):** 0.073 (efecto mediano)

**Hallazgo crítico:** La recencia es el **factor más importante** para predecir el crecimiento. Usuarios activos crecen **7 veces más** que usuarios perdidos. Este es el insight más relevante del análisis y **valida la hipótesis 2**.

**Análisis de Velocidad de Adopción vs Crecimiento:**

| Segmento de Velocidad | EFO-to-Four promedio | Delta promedio | N usuarios |
|----------------------|---------------------|----------------|------------|
| Muy Rápido (0-7d) | ~5 días | 9.5 | - |
| Rápido (8-14d) | ~11 días | 7.2 | - |
| Moderado (15-21d) | ~18 días | 5.8 | - |
| Lento (>21d) | ~25 días | 4.1 | - |

**Hallazgo crítico:** Existe una relación **inversamente proporcional** entre la velocidad de adopción y el crecimiento. Usuarios que llegan más rápido a su 4ta orden tienen **2.3x mayor crecimiento** que los lentos.

**Análisis por Segmento R:**

| Segmento | N usuarios | Delta promedio | Total orders promedio | EFO-to-Four promedio |
|----------|------------|----------------|----------------------|---------------------|
| r_segment002 | 11,094 | **7.12** ✅ | **7.44** ✅ | **14.58** ✅ |
| r_segment001 | 15,968 | 6.97 | 7.30 | 15.16 |
| r_segment003 | 14,605 | 6.53 | 6.90 | 14.98 |

**Test ANOVA:**
- P-valor: < 0.001 (diferencias significativas)
- Tamaño del efecto (η²): 0.002 (efecto pequeño)

**Hallazgo:** `r_segment002` supera consistentemente a los demás segmentos en **todas las métricas clave**, aunque el efecto es pequeño.

**Asociaciones entre variables categóricas (Chi-cuadrado):**

| Pares de variables | Chi² | P-valor | Cramér's V | Interpretación |
|-------------------|------|---------|------------|----------------|
| recencia vs city | 96.5 | <0.001 | 0.024 | Asociación muy débil |
| recencia vs r_segment | 173.9 | <0.001 | 0.046 | Asociación muy débil |
| city vs r_segment | 840.4 | <0.001 | 0.100 | Asociación débil |

**Conclusión:** Aunque existen asociaciones estadísticamente significativas entre las variables categóricas, los tamaños de efecto son débiles, indicando que estas relaciones tienen poca relevancia práctica.

#### 6.2.3 Análisis de Afinidades

**Afinidades por categoría principal:**
- **Total de categorías únicas:** 28
- **Concentración:** Solo **6 categorías** representan el **80%** de todas las órdenes
- **Top 3:** main_category008 (18.2%), main_category007 (17.6%), main_category013 (14.0%)
- **Diversidad promedio por usuario:** 3.67 categorías

**Afinidades por marca:**
- **Total de marcas únicas:** 817
- **Dominio de brand001:** Representa el **40.63%** de todas las órdenes
- **Concentración:** Top 20 marcas representan el **80%** del mercado
- **Diversidad promedio por usuario:** 3.68 marcas

**Afinidades por tienda:**
- **Total de tiendas únicas:** 11,534
- **Concentración:** Solo **20 tiendas** representan el **80%** de las órdenes
- **Lealtad a tiendas:**
  - Solo **3.1%** de usuarios compran en una sola tienda
  - **96.9%** compran en múltiples tiendas
- **Promedio de tiendas visitadas:** 5.36

**Hallazgo crítico:** Los usuarios son **altamente exploradores** en cuanto a tiendas (no muestran lealtad), pero existe **alta concentración** en pocas categorías y marcas. Esto sugiere que las estrategias deben enfocarse en **categorías** más que en tiendas específicas. **Valida la hipótesis 3** sobre afinidades.

**Especialización vs Diversificación:**

Usando el índice de concentración de Herfindahl:
- **Usuarios diversificados:** 38.5% (compran en muchas categorías)
- **Usuarios moderados:** 49.1% (comportamiento mixto)
- **Usuarios especializados:** 12.4% (se concentran en pocas categorías)
- **Índice promedio:** 0.422 (moderadamente diversificado)

**Conclusión:** La mayoría de usuarios (87.6%) son exploradores, lo que abre oportunidades para **cross-selling** y personalización basada en afinidades.

---

### 6.3 Validación de Hipótesis

| Hipótesis | Estado | Evidencia Estadística |
|-----------|--------|---------------------|
| **H1:** Usuarios con menor efo_to_four tienen mayor crecimiento | ✅ **Validada** | Correlación -0.201 (p<0.001), diferencia de 2.3x entre extremos |
| **H2:** La recencia predice el volumen de órdenes | ✅ **Validada** | ANOVA p<0.001, η²=0.073 (efecto mediano), diferencia de 7x |
| **H3:** Las afinidades pueden orientar estrategias personalizadas | ✅ **Validada** | Alta concentración en 6 categorías (80%), diversidad promedio 3.67 |

---

### 6.4 Insights Principales

#### 🔥 Insight #1: Velocidad de Adopción Predice Crecimiento
- **Correlación:** -0.201 entre efo_to_four y delta_orders (p < 0.001)
- Usuarios **muy rápidos** (0-7 días) vs **lentos** (>21 días): **2.3x más crecimiento**
- **Implicación:** Priorizar recursos en usuarios con velocidad de adopción ≤14 días

#### 🔥 Insight #2: Recencia es el Factor MÁS Crítico
- Usuarios **Activos** (≤7d): 8.97 órdenes promedio
- Usuarios **Perdidos** (>90d): 1.29 órdenes promedio
- **Diferencia:** **7x** entre extremos (p < 0.001)
- **Implicación:** Implementar campañas urgentes de reactivación para usuarios "Frío" antes de que pasen a "Perdido"

#### 🏆 Insight #3: r_segment002 es Superior
- Mejor en **crecimiento** (7.12 vs 6.53-6.97)
- Mejor en **órdenes totales** (7.44)
- **Adopción más rápida** (14.58 días)
- **Implicación:** Asignar mayor presupuesto promocional a este segmento por su mejor ROI esperado

#### 🛍️ Insight #4: Alta Exploración, Baja Lealtad
- **96.9%** de usuarios compran en **múltiples tiendas**
- Solo **6 categorías** representan el **80%** de las órdenes
- **brand001** domina con **40.63%** del mercado
- **Implicación:** Enfocar estrategias en categorías clave, no en tiendas específicas. Aprovechar la exploración para cross-selling

#### 📅 Insight #5: Patrón de Fin de Semana
- **35.8%** de actividad en fin de semana (Sáb-Dom)
- Pico de nuevos usuarios en **julio-agosto** (66%)
- **Implicación:** Concentrar campañas promocionales en viernes-domingo

---

### 6.5 Conclusiones sobre la Suficiencia de los Datos

**Evaluación de suficiencia:**

| Criterio | Evaluación | Justificación |
|----------|------------|---------------|
| **Calidad** | ✅ Excelente | 100/100: Sin faltantes ni duplicados, todas las reglas validadas |
| **Cantidad** | ✅ Suficiente | 41,667 usuarios - muestra robusta para modelado |
| **Variabilidad** | ✅ Alta | CV > 50% en todas las métricas, gran diversidad de comportamientos |
| **Completitud** | ✅ Completa | Todas las variables clave presentes (actividad, fechas, afinidades, segmentación) |
| **Representatividad** | ✅ Adecuada | Período de 6 meses, múltiples ciudades, 3 segmentos R |
| **Relevancia** | ✅ Alta | Variables directamente relacionadas con objetivos de negocio |

**Conclusión final:** Los datos son **suficientes y adecuados** para:
1. Construir modelos predictivos de crecimiento (clasificación y regresión)
2. Desarrollar sistema de recomendación basado en afinidades
3. Crear dashboard interactivo con métricas clave
4. Implementar estrategias personalizadas por segmento

El dataset cumple con todos los requisitos para desarrollar el **producto de datos propuesto** (modelo + dashboard + recomendador) y responder a la problemática planteada.

---

## Diccionario de datos

| Variable | Descripción | Tipo | Fuente |
|-----------|--------------|------|---------|
| `uid` | Identificador único del usuario (anonimizado) | Numérico | Transaccional |
| `country_code` | País del usuario | Categórica | Transaccional |
| `city_token` | Ciudad del usuario (tokenizada) | Categórica | `dim_city` |
| `total_orders` | Total de órdenes completadas | Numérica | `dwm_finance_order_d_increment` |
| `total_orders_tmenos1` | Total de órdenes en el corte anterior | Numérica | `dwm_user_order_accumulate_by_bizline_d_whole` |
| `delta_orders` | Diferencia entre órdenes actuales y anteriores | Numérica | Derivada |
| `categoria_recencia` | Nivel de recencia según última orden (≤7d, 8–14d, etc.) | Categórica | Derivada |
| `efo_to_four` | Días entre la primera y cuarta orden | Numérica | `dwm_finance_order_d_increment` |
| `r_segment` | Segmento de valor del usuario (Loyal, Casual, Rare) | Categórica | `ssl_freq_rider_segmentation` |
| `main_category_counts` | Conteo de órdenes por categoría | JSON/dict | `orders_enriched` |
| `ka_type_counts` | Conteo de órdenes por tipo de tienda | JSON/dict | `orders_enriched` |
| `shop_name_counts` | Conteo de órdenes por tienda | JSON/dict | `orders_enriched` |
| `brand_name_counts` | Conteo de órdenes por marca | JSON/dict | `orders_enriched` |

---

## 7. Conclusiones Iniciales

### 7.1 Logros de la Primera Entrega

Se ha completado exitosamente el **entendimiento del negocio y de los datos**, cumpliendo con todos los objetivos establecidos para esta primera fase del proyecto:

✅ **Problemática claramente definida:** Falta de esquema para priorizar recursos en usuarios nuevos de Engagement
✅ **Producto de datos diseñado:** Dashboard + Modelo + Recomendador
✅ **Aspectos éticos y regulatorios considerados:** Cumplimiento con normativa colombiana
✅ **Enfoque analítico establecido:** Hipótesis validadas estadísticamente
✅ **Datos recolectados y validados:** 41,667 usuarios con calidad óptima (100/100)
✅ **Análisis exploratorio exhaustivo:** Técnicas univariadas, multivariadas, gráficas y no gráficas

### 7.2 Insights Clave

Los hallazgos más relevantes que guiarán las fases posteriores del proyecto son:

#### Factores Predictivos de Crecimiento

1. **Recencia (Impacto crítico - 7x):**
   - Es el **factor más importante** para predecir crecimiento
   - Usuarios activos crecen 7 veces más que usuarios perdidos
   - Acción inmediata: Campañas de reactivación para usuarios "Frío"

2. **Velocidad de Adopción (Impacto moderado - 2.3x):**
   - Correlación negativa significativa (-0.201)
   - Usuarios rápidos tienen 2.3x más crecimiento que lentos
   - Acción: Priorizar incentivos a usuarios con efo_to_four ≤14 días

3. **Segmento R (Impacto pequeño pero consistente):**
   - r_segment002 supera en todas las métricas
   - Acción: Mayor inversión en este segmento

#### Patrones de Comportamiento

4. **Alta Exploración:**
   - 96.9% de usuarios compran en múltiples tiendas (no hay lealtad)
   - Oportunidad: Cross-selling basado en categorías, no tiendas

5. **Concentración en Pocas Categorías:**
   - Solo 6 categorías = 80% de órdenes
   - brand001 domina con 40.63% del mercado
   - Oportunidad: Enfocar estrategias en categorías clave

6. **Patrón Temporal:**
   - 35.8% de actividad en fin de semana
   - Oportunidad: Campañas concentradas viernes-domingo

### 7.3 Validación de Hipótesis Iniciales

| Hipótesis | Resultado | Evidencia |
|-----------|-----------|-----------|
| H1: Velocidad de adopción predice crecimiento | ✅ **VALIDADA** | r=-0.201 (p<0.001), diferencia 2.3x |
| H2: Recencia predice volumen de órdenes | ✅ **VALIDADA** | F=1,087 (p<0.001), diferencia 7x |
| H3: Afinidades orientan estrategias | ✅ **VALIDADA** | 6 categorías = 80%, diversidad 3.67 |

**Conclusión:** Las tres hipótesis planteadas fueron **validadas estadísticamente**, lo que confirma la viabilidad del enfoque analítico propuesto.

### 7.4 Suficiencia de los Datos para el Producto Planteado

Los datos recolectados son **suficientes y adecuados** para construir el producto de datos propuesto:

**Dashboard:**
- ✅ Métricas clave disponibles (delta, recencia, segmentación)
- ✅ Variables temporales para evolución de cohortes
- ✅ Afinidades para visualización de patrones

**Modelo Predictivo:**
- ✅ Variable objetivo clara (delta_orders)
- ✅ Features predictivos identificados (efo_to_four, recencia, r_segment)
- ✅ Muestra robusta (41,667 usuarios)
- ✅ Alta variabilidad para capturar patrones

**Recomendador:**
- ✅ Datos de afinidades disponibles (categorías, marcas, tiendas)
- ✅ Segmentación por especialización vs diversificación
- ✅ Patrones claros de concentración identificados

### 7.5 Próximas Acciones

Para la **segunda entrega** del proyecto, las acciones priorizadas son:

#### Preparación de Datos (Prioridad Alta)

1. **Feature Engineering:**
   - Crear variables derivadas de afinidades (categoría dominante, índice de especialización)
   - Transformar variables temporales (días desde última orden, day of week)
   - Generar features de interacción (recencia × velocidad, segmento × ciudad)

2. **Tratamiento de Outliers:**
   - Decidir estrategia para usuarios con >14 órdenes (6.19%)
   - Opciones: mantener, cap, transformación log

3. **Codificación:**
   - One-hot encoding para variables categóricas (recencia, ciudad, segmento)
   - Extracción de features de diccionarios de afinidades

#### Modelado (Prioridad Alta)

4. **Modelo de Clasificación:**
   - **Objetivo:** Predecir usuarios de "alto crecimiento" (>8 órdenes)
   - **Algoritmos:** Random Forest, XGBoost, LightGBM
   - **Features clave:** efo_to_four, categoria_recencia, r_segment, ciudad

5. **Modelo de Regresión:**
   - **Objetivo:** Predecir valor exacto de delta_orders
   - **Algoritmos:** Gradient Boosting, Ridge, ElasticNet
   - **Evaluación:** RMSE, MAE, R²

#### Construcción del Producto (Prioridad Media)

6. **Dashboard Interactivo:**
   - Herramienta: Streamlit o Dash
   - Componentes: KPIs, segmentación dinámica, evolución temporal

7. **Sistema de Recomendación:**
   - Basado en afinidades + predicción de modelo
   - Priorización de usuarios por potencial

#### Evaluación y Retroalimentación (Prioridad Media)

8. **Evaluación Cuantitativa:**
   - Validación cruzada estratificada
   - Comparación de múltiples modelos
   - Análisis de errores

9. **Retroalimentación con Stakeholders:**
   - Presentar hallazgos iniciales
   - Validar métricas y KPIs
   - Ajustar producto según feedback

### 7.6 Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Alta dimensionalidad de afinidades | Media | Alto | Aplicar PCA o selección de características |
| Desbalance en variable objetivo | Alta | Medio | SMOTE o ajuste de pesos en modelo |
| Overfitting por outliers | Media | Medio | Regularización y validación cruzada |
| Cambios en comportamiento temporal | Baja | Alto | Validación en período más reciente |

### 7.7 Métricas de Éxito Propuestas

Para validar el impacto del producto de datos en la **segunda entrega**, se proponen las siguientes métricas:

**Métricas del Modelo:**
- AUC-ROC > 0.75 (clasificación)
- RMSE < 3.5 órdenes (regresión)
- Top 20% de usuarios predichos capturan >40% del crecimiento total

**Métricas de Negocio (Simuladas):**
- Incremento esperado en delta promedio: +16% (6.9 → 8.0 órdenes)
- Reducción de CPOI: -15%
- Mejora en tasa de retención de usuarios "Frío": +20%

### 7.8 Resumen Ejecutivo

Esta primera entrega ha logrado **caracterizar exitosamente** el comportamiento de los 41,667 usuarios nuevos de Engagement, identificando **factores claros y accionables** que predicen el crecimiento:

**Los datos confirman que:**
1. La **recencia es crítica** (diferencia de 7x)
2. La **velocidad de adopción predice** el crecimiento futuro
3. El **r_segment002 es superior** consistentemente
4. Los usuarios son **exploradores**, no leales a tiendas
5. Existe **concentración en pocas categorías** (80% en 6)

**El dataset es suficiente para:**
- Construir modelos predictivos robustos
- Desarrollar sistema de recomendación
- Crear dashboard interactivo
- Implementar estrategias personalizadas

**Próximo paso crítico:**
Proceder con la **preparación de datos y modelado**, priorizando la predicción de usuarios de alto potencial basada en recencia y velocidad de adopción.

---

## Referencias

1. Superintendencia de Industria y Comercio. “**Guía oficial de protección de datos personales**.” Superintendencia de Industria y Comercio – Protección de Datos Personales, 10 oct 2023.  
   [https://habeasdata.todoenuno.net.co/.../Guia-oficial-de-proteccion-de-datos-personales.pdf](https://habeasdata.todoenuno.net.co/wp-content/uploads/2023/10/SuperIndustria-publico-la-Guia-oficial-de-proteccion-de-datos-personales_compressed.pdf)
