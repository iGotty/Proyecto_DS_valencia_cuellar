# Growth Predictor Dashboard

Un dashboard moderno y visualmente impresionante para el equipo de Engagement, desarrollado con Streamlit.

## Características

- **Dashboard Ejecutivo**: KPIs principales, distribución de crecimiento, comparación de modelos
- **Explorador de Segmentos**: Filtros interactivos por recencia, segmento y tipo de crecimiento
- **Predicciones en Tiempo Real**: Predicción de probabilidad de high-growth para usuarios individuales
- **Análisis de Afinidades**: Preferencias de categorías, marcas y tiendas

## Diseño

- Interfaz moderna con glassmorphism y gradientes animados
- Colores: Indigo (#6366f1), Rosa (#ec4899), Cyan (#06b6d4)
- Tipografía: Inter (Google Fonts)
- Gráficos interactivos con Plotly
- Responsive design

## Instalación

```bash
# Desde el directorio raíz del proyecto
cd dashboard

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
# Desde el directorio del dashboard
streamlit run app.py

# O desde la raíz del proyecto
streamlit run dashboard/app.py
```

El dashboard se abrirá en `http://localhost:8501`

## Estructura de Archivos

```
dashboard/
├── app.py              # Aplicación principal de Streamlit
├── requirements.txt    # Dependencias de Python
└── README.md          # Este archivo
```

## Dependencias de Datos

El dashboard requiere los siguientes archivos (generados por los scripts de preparación y entrenamiento):

```
data/processed/
├── train.csv
├── val.csv
└── test.csv

models/
├── best_classifier.pkl
├── feature_importance.csv
└── classification_report.json

dataset_protegido (1).csv  # Dataset original
```

## Páginas del Dashboard

### 1. Dashboard Principal
- 4 KPIs principales (Total Usuarios, % High Growth, Delta Promedio, Usuarios Activos)
- Distribución de crecimiento (pie chart)
- Top 10 features predictivos
- Histograma de delta_orders
- Comparación de modelos

### 2. Explorador de Segmentos
- Filtros por recencia, R segment y tipo de crecimiento
- Métricas dinámicas del segmento seleccionado
- Visualizaciones interactivas
- Tabla de datos filtrados

### 3. Predicciones
- Selector de usuario del test set
- Gauge de probabilidad de high-growth
- Clasificación de prioridad (Alta/Media/Baja)
- Recomendaciones de acción personalizadas

### 4. Análisis de Afinidades
- Distribución por categoría principal
- Concentración de marca dominante (Brand001)
- Diversidad de categorías por tipo de crecimiento
- Insights y recomendaciones

## Tecnologías

- **Streamlit** - Framework de dashboard
- **Plotly** - Visualizaciones interactivas
- **Pandas** - Manipulación de datos
- **Scikit-learn, XGBoost, LightGBM** - Modelos ML

## Autores

- Juan David Valencia
- Juan Esteban Cuellar

## Curso

MINE-4101 - Ciencia de Datos Aplicada
Universidad de los Andes
2025
