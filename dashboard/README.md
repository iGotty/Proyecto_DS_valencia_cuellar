

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
