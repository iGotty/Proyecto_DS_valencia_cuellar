"""
Univariate Analysis Script
===========================
Análisis univariado exhaustivo de todas las variables del dataset.

Este script realiza análisis estadístico descriptivo y exploratorio de:
- Variables numéricas (total_orders, delta_orders, efo_to_four)
- Variables categóricas (country_code, categoria_recencia, city_token, r_segment)
- Variables temporales (first_order_date, fourth_order_date)

Autor: Proyecto Final - Ciencia de Datos Aplicada
Fecha: 2025-10-19
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class UnivariateAnalyzer:
    """Clase para análisis univariado de variables"""

    def __init__(self, filepath):
        """
        Inicializa el analizador univariado

        Parameters:
        -----------
        filepath : str
            Ruta al archivo CSV del dataset
        """
        print("="*80)
        print("ANÁLISIS UNIVARIADO DE VARIABLES")
        print("="*80)
        print(f"\n[INFO] Cargando dataset desde: {filepath}")
        self.df = pd.read_csv(filepath)

        # Convertir fechas
        self.df['first_order_date'] = pd.to_datetime(self.df['first_order_date'])
        self.df['fourth_order_date'] = pd.to_datetime(self.df['fourth_order_date'])

        print(f"[OK] Dataset cargado: {self.df.shape[0]:,} filas x {self.df.shape[1]} columnas\n")

    def analyze_numeric_variable(self, column_name, description=""):
        """
        Análisis completo de una variable numérica

        Parameters:
        -----------
        column_name : str
            Nombre de la columna a analizar
        description : str
            Descripción de la variable
        """
        print("\n" + "-"*80)
        print(f"📊 Variable: {column_name}")
        if description:
            print(f"   Descripción: {description}")
        print("-"*80)

        data = self.df[column_name]

        # Estadísticas descriptivas básicas
        print("\n🔢 Estadísticas Descriptivas:")
        print(f"   Observaciones: {len(data):,}")
        print(f"   Media: {data.mean():.2f}")
        print(f"   Mediana: {data.median():.2f}")
        print(f"   Moda: {data.mode().values[0] if len(data.mode()) > 0 else 'N/A'}")
        print(f"   Desviación estándar: {data.std():.2f}")
        print(f"   Varianza: {data.var():.2f}")
        print(f"   Mínimo: {data.min()}")
        print(f"   Máximo: {data.max()}")
        print(f"   Rango: {data.max() - data.min()}")

        # Cuartiles
        print(f"\n📈 Cuartiles:")
        print(f"   Q1 (25%): {data.quantile(0.25):.2f}")
        print(f"   Q2 (50% - Mediana): {data.quantile(0.50):.2f}")
        print(f"   Q3 (75%): {data.quantile(0.75):.2f}")
        print(f"   IQR (Q3-Q1): {data.quantile(0.75) - data.quantile(0.25):.2f}")

        # Percentiles adicionales
        print(f"\n🎯 Percentiles Clave:")
        for p in [5, 10, 25, 50, 75, 90, 95, 99]:
            print(f"   P{p}: {data.quantile(p/100):.2f}")

        # Asimetría y curtosis
        print(f"\n📐 Forma de la Distribución:")
        skewness = data.skew()
        kurtosis = data.kurtosis()
        print(f"   Asimetría (Skewness): {skewness:.3f}")
        if skewness > 1:
            print(f"      → Distribución muy sesgada a la derecha")
        elif skewness > 0.5:
            print(f"      → Distribución moderadamente sesgada a la derecha")
        elif skewness < -1:
            print(f"      → Distribución muy sesgada a la izquierda")
        elif skewness < -0.5:
            print(f"      → Distribución moderadamente sesgada a la izquierda")
        else:
            print(f"      → Distribución aproximadamente simétrica")

        print(f"   Curtosis (Kurtosis): {kurtosis:.3f}")
        if kurtosis > 3:
            print(f"      → Distribución leptocúrtica (colas pesadas)")
        elif kurtosis < -1:
            print(f"      → Distribución platicúrtica (colas ligeras)")
        else:
            print(f"      → Distribución mesocúrtica (normal)")

        # Test de normalidad
        print(f"\n🔬 Test de Normalidad (Shapiro-Wilk):")
        if len(data) <= 5000:
            stat, p_value = stats.shapiro(data)
            print(f"   Estadístico: {stat:.4f}")
            print(f"   P-valor: {p_value:.4e}")
            if p_value > 0.05:
                print(f"   ✓ No se rechaza H0: La distribución podría ser normal")
            else:
                print(f"   ✗ Se rechaza H0: La distribución NO es normal")
        else:
            print(f"   ⚠️  Muestra muy grande para Shapiro-Wilk. Usando Anderson-Darling...")
            result = stats.anderson(data)
            print(f"   Estadístico: {result.statistic:.4f}")
            print(f"   Valor crítico (5%): {result.critical_values[2]:.4f}")
            if result.statistic < result.critical_values[2]:
                print(f"   ✓ La distribución podría ser normal")
            else:
                print(f"   ✗ La distribución NO es normal")

        # Distribución de frecuencias
        print(f"\n📊 Distribución de Frecuencias (Top 15):")
        freq_dist = data.value_counts().head(15)
        for value, count in freq_dist.items():
            pct = (count / len(data) * 100)
            print(f"   {value}: {count:,} ({pct:.1f}%)")

        # Coeficiente de variación
        cv = (data.std() / data.mean() * 100) if data.mean() != 0 else 0
        print(f"\n📉 Coeficiente de Variación: {cv:.2f}%")
        if cv < 15:
            print(f"   → Baja variabilidad")
        elif cv < 30:
            print(f"   → Variabilidad moderada")
        else:
            print(f"   → Alta variabilidad")

        return {
            'mean': data.mean(),
            'median': data.median(),
            'std': data.std(),
            'skewness': skewness,
            'kurtosis': kurtosis,
            'cv': cv
        }

    def analyze_categorical_variable(self, column_name, description="", top_n=20):
        """
        Análisis completo de una variable categórica

        Parameters:
        -----------
        column_name : str
            Nombre de la columna a analizar
        description : str
            Descripción de la variable
        top_n : int
            Número de categorías a mostrar
        """
        print("\n" + "-"*80)
        print(f"📊 Variable: {column_name}")
        if description:
            print(f"   Descripción: {description}")
        print("-"*80)

        data = self.df[column_name]

        # Estadísticas básicas
        print("\n🔢 Estadísticas Descriptivas:")
        print(f"   Observaciones: {len(data):,}")
        print(f"   Valores únicos: {data.nunique()}")
        print(f"   Moda: {data.mode().values[0] if len(data.mode()) > 0 else 'N/A'}")

        # Distribución de frecuencias
        print(f"\n📊 Distribución de Frecuencias:")
        freq_dist = data.value_counts()

        # Mostrar todas las categorías si son pocas, sino solo top N
        if data.nunique() <= top_n:
            for value, count in freq_dist.items():
                pct = (count / len(data) * 100)
                print(f"   {value}: {count:,} ({pct:.2f}%)")
        else:
            print(f"\n   Top {top_n} categorías más frecuentes:")
            for value, count in freq_dist.head(top_n).items():
                pct = (count / len(data) * 100)
                print(f"   {value}: {count:,} ({pct:.2f}%)")

            # Categorías menos frecuentes
            print(f"\n   Bottom 10 categorías menos frecuentes:")
            for value, count in freq_dist.tail(10).items():
                pct = (count / len(data) * 100)
                print(f"   {value}: {count:,} ({pct:.2f}%)")

        # Concentración
        print(f"\n🎯 Análisis de Concentración:")
        cumsum = (freq_dist / len(data) * 100).cumsum()
        categories_80 = (cumsum <= 80).sum()
        categories_90 = (cumsum <= 90).sum()
        print(f"   Categorías que representan 80% de datos: {categories_80}")
        print(f"   Categorías que representan 90% de datos: {categories_90}")

        # Índice de diversidad (Shannon)
        proportions = freq_dist / len(data)
        shannon_index = -sum(proportions * np.log(proportions))
        max_shannon = np.log(data.nunique())
        shannon_evenness = shannon_index / max_shannon if max_shannon > 0 else 0

        print(f"\n📈 Índice de Diversidad de Shannon:")
        print(f"   Índice: {shannon_index:.3f}")
        print(f"   Índice máximo posible: {max_shannon:.3f}")
        print(f"   Equitabilidad (evenness): {shannon_evenness:.3f}")
        if shannon_evenness > 0.8:
            print(f"   → Alta diversidad: las categorías están bien distribuidas")
        elif shannon_evenness > 0.5:
            print(f"   → Diversidad moderada")
        else:
            print(f"   → Baja diversidad: hay categorías muy dominantes")

        return {
            'unique_values': data.nunique(),
            'mode': data.mode().values[0] if len(data.mode()) > 0 else None,
            'freq_dist': freq_dist,
            'shannon_index': shannon_index,
            'shannon_evenness': shannon_evenness
        }

    def analyze_temporal_variable(self, column_name, description=""):
        """
        Análisis de variables temporales/fechas

        Parameters:
        -----------
        column_name : str
            Nombre de la columna a analizar
        description : str
            Descripción de la variable
        """
        print("\n" + "-"*80)
        print(f"📊 Variable: {column_name}")
        if description:
            print(f"   Descripción: {description}")
        print("-"*80)

        data = pd.to_datetime(self.df[column_name])

        # Estadísticas básicas
        print("\n📅 Estadísticas Descriptivas:")
        print(f"   Observaciones: {len(data):,}")
        print(f"   Fecha mínima: {data.min().strftime('%Y-%m-%d')}")
        print(f"   Fecha máxima: {data.max().strftime('%Y-%m-%d')}")
        print(f"   Rango: {(data.max() - data.min()).days} días")

        # Distribución por mes
        print(f"\n📊 Distribución por Mes:")
        monthly_dist = data.dt.to_period('M').value_counts().sort_index()
        for month, count in monthly_dist.items():
            pct = (count / len(data) * 100)
            print(f"   {month}: {count:,} ({pct:.1f}%)")

        # Distribución por día de la semana
        print(f"\n📊 Distribución por Día de la Semana:")
        dow_map = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
                   4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
        dow_dist = data.dt.dayofweek.map(dow_map).value_counts()
        dow_order = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        for day in dow_order:
            if day in dow_dist.index:
                count = dow_dist[day]
                pct = (count / len(data) * 100)
                print(f"   {day}: {count:,} ({pct:.1f}%)")

        return {
            'min_date': data.min(),
            'max_date': data.max(),
            'range_days': (data.max() - data.min()).days,
            'monthly_dist': monthly_dist
        }

    def run_full_analysis(self):
        """Ejecuta el análisis univariado completo"""
        print("\n")
        print("🚀 Iniciando análisis univariado completo...\n")

        results = {}

        # Análisis de variables numéricas
        print("\n" + "="*80)
        print("ANÁLISIS DE VARIABLES NUMÉRICAS")
        print("="*80)

        results['total_orders'] = self.analyze_numeric_variable(
            'total_orders',
            'Total de órdenes completadas por el usuario'
        )

        results['total_orders_tmenos1'] = self.analyze_numeric_variable(
            'total_orders_tmenos1',
            'Total de órdenes en el periodo anterior (T-1)'
        )

        results['delta_orders'] = self.analyze_numeric_variable(
            'delta_orders',
            'Incremento de órdenes entre periodos (delta)'
        )

        results['efo_to_four'] = self.analyze_numeric_variable(
            'efo_to_four',
            'Días entre la primera y cuarta orden (velocidad de adopción)'
        )

        # Análisis de variables categóricas
        print("\n" + "="*80)
        print("ANÁLISIS DE VARIABLES CATEGÓRICAS")
        print("="*80)

        results['country_code'] = self.analyze_categorical_variable(
            'country_code',
            'Código del país del usuario'
        )

        results['categoria_recencia'] = self.analyze_categorical_variable(
            'categoria_recencia',
            'Categoría de recencia del usuario (última actividad)'
        )

        results['city_token'] = self.analyze_categorical_variable(
            'city_token',
            'Ciudad del usuario (tokenizada)'
        )

        results['r_segment'] = self.analyze_categorical_variable(
            'r_segment',
            'Segmento R del usuario (de otra línea de negocio)'
        )

        # Análisis de variables temporales
        print("\n" + "="*80)
        print("ANÁLISIS DE VARIABLES TEMPORALES")
        print("="*80)

        results['first_order_date'] = self.analyze_temporal_variable(
            'first_order_date',
            'Fecha de la primera orden del usuario'
        )

        results['fourth_order_date'] = self.analyze_temporal_variable(
            'fourth_order_date',
            'Fecha de la cuarta orden del usuario'
        )

        # Resumen ejecutivo
        self.generate_executive_summary(results)

        print("\n" + "="*80)
        print("✅ Análisis univariado completado")
        print("="*80)

        return results

    def generate_executive_summary(self, results):
        """Genera un resumen ejecutivo del análisis univariado"""
        print("\n" + "="*80)
        print("RESUMEN EJECUTIVO - ANÁLISIS UNIVARIADO")
        print("="*80)

        print(f"""
📊 Variables Numéricas - Hallazgos Principales:

   1. Total de Órdenes:
      - Media: {results['total_orders']['mean']:.1f} órdenes
      - Mediana: {results['total_orders']['median']:.0f} órdenes
      - CV: {results['total_orders']['cv']:.1f}% ({'alta' if results['total_orders']['cv'] > 30 else 'moderada' if results['total_orders']['cv'] > 15 else 'baja'} variabilidad)
      - Asimetría: {'Positiva (cola derecha)' if results['total_orders']['skewness'] > 0 else 'Negativa (cola izquierda)'}

   2. Delta de Órdenes:
      - Media: {results['delta_orders']['mean']:.1f} órdenes
      - Mediana: {results['delta_orders']['median']:.0f} órdenes
      - CV: {results['delta_orders']['cv']:.1f}% ({'alta' if results['delta_orders']['cv'] > 30 else 'moderada' if results['delta_orders']['cv'] > 15 else 'baja'} variabilidad)

   3. EFO-to-Four (Velocidad de Adopción):
      - Media: {results['efo_to_four']['mean']:.1f} días
      - Mediana: {results['efo_to_four']['median']:.0f} días
      - CV: {results['efo_to_four']['cv']:.1f}% ({'alta' if results['efo_to_four']['cv'] > 30 else 'moderada' if results['efo_to_four']['cv'] > 15 else 'baja'} variabilidad)

📊 Variables Categóricas - Hallazgos Principales:

   1. Categoría de Recencia:
      - Valores únicos: {results['categoria_recencia']['unique_values']}
      - Categoría más común: {results['categoria_recencia']['mode']}
      - Diversidad Shannon: {results['categoria_recencia']['shannon_evenness']:.2f} ({'alta' if results['categoria_recencia']['shannon_evenness'] > 0.8 else 'moderada' if results['categoria_recencia']['shannon_evenness'] > 0.5 else 'baja'})

   2. Ciudad:
      - Valores únicos: {results['city_token']['unique_values']}
      - Ciudad más común: {results['city_token']['mode']}
      - Diversidad Shannon: {results['city_token']['shannon_evenness']:.2f}

   3. Segmento R:
      - Valores únicos: {results['r_segment']['unique_values']}
      - Segmento más común: {results['r_segment']['mode']}
      - Diversidad Shannon: {results['r_segment']['shannon_evenness']:.2f}

📅 Variables Temporales - Hallazgos Principales:

   1. Rango de fechas de primera orden: {results['first_order_date']['range_days']} días
   2. Rango de fechas de cuarta orden: {results['fourth_order_date']['range_days']} días
""")


if __name__ == "__main__":
    # Ruta al dataset
    DATASET_PATH = "../dataset_protegido (1).csv"

    # Crear instancia del analizador
    analyzer = UnivariateAnalyzer(DATASET_PATH)

    # Ejecutar análisis completo
    results = analyzer.run_full_analysis()

    print("\n💡 Próximos pasos recomendados:")
    print("   1. Revisar distribuciones no normales para transformaciones")
    print("   2. Investigar variables con alta variabilidad")
    print("   3. Proceder con análisis multivariado y correlaciones")
