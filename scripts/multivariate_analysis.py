"""
Multivariate Analysis Script
=============================
Análisis multivariado para explorar relaciones entre variables.

Este script analiza:
1. Correlaciones entre variables numéricas
2. Relaciones entre variables categóricas y numéricas
3. Análisis de segmentación
4. Pruebas de hipótesis
5. Análisis de asociación

Autor: Proyecto Final - Ciencia de Datos Aplicada
Fecha: 2025-10-19
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, f_oneway, kruskal
import warnings
warnings.filterwarnings('ignore')


class MultivariateAnalyzer:
    """Clase para análisis multivariado de variables"""

    def __init__(self, filepath):
        """
        Inicializa el analizador multivariado

        Parameters:
        -----------
        filepath : str
            Ruta al archivo CSV del dataset
        """
        print("="*80)
        print("ANÁLISIS MULTIVARIADO")
        print("="*80)
        print(f"\n[INFO] Cargando dataset desde: {filepath}")
        self.df = pd.read_csv(filepath)

        # Convertir fechas
        self.df['first_order_date'] = pd.to_datetime(self.df['first_order_date'])
        self.df['fourth_order_date'] = pd.to_datetime(self.df['fourth_order_date'])

        print(f"[OK] Dataset cargado: {self.df.shape[0]:,} filas x {self.df.shape[1]} columnas\n")

    def analyze_numeric_correlations(self):
        """Análisis de correlaciones entre variables numéricas"""
        print("\n" + "="*80)
        print("1. CORRELACIONES ENTRE VARIABLES NUMÉRICAS")
        print("="*80)

        numeric_cols = ['total_orders', 'total_orders_tmenos1', 'delta_orders', 'efo_to_four']

        # Matriz de correlación de Pearson
        print("\n📊 Matriz de Correlación de Pearson:")
        corr_pearson = self.df[numeric_cols].corr(method='pearson')
        print(corr_pearson.round(3).to_string())

        # Matriz de correlación de Spearman (no paramétrica)
        print("\n📊 Matriz de Correlación de Spearman:")
        corr_spearman = self.df[numeric_cols].corr(method='spearman')
        print(corr_spearman.round(3).to_string())

        # Análisis de correlaciones significativas
        print("\n🔍 Correlaciones Significativas (|r| > 0.3):")
        for i in range(len(numeric_cols)):
            for j in range(i+1, len(numeric_cols)):
                var1, var2 = numeric_cols[i], numeric_cols[j]
                r_pearson = corr_pearson.loc[var1, var2]
                r_spearman = corr_spearman.loc[var1, var2]

                if abs(r_pearson) > 0.3 or abs(r_spearman) > 0.3:
                    print(f"\n   {var1} vs {var2}:")
                    print(f"      Pearson: {r_pearson:.3f} ({'Positiva' if r_pearson > 0 else 'Negativa'})")
                    print(f"      Spearman: {r_spearman:.3f} ({'Positiva' if r_spearman > 0 else 'Negativa'})")

                    # Interpretación
                    r = abs(r_pearson)
                    if r > 0.7:
                        strength = "muy fuerte"
                    elif r > 0.5:
                        strength = "fuerte"
                    elif r > 0.3:
                        strength = "moderada"
                    else:
                        strength = "débil"
                    print(f"      Interpretación: Correlación {strength}")

        return {'pearson': corr_pearson, 'spearman': corr_spearman}

    def analyze_categorical_numeric_relationship(self, cat_var, num_var, description=""):
        """
        Analiza la relación entre una variable categórica y una numérica

        Parameters:
        -----------
        cat_var : str
            Variable categórica
        num_var : str
            Variable numérica
        description : str
            Descripción del análisis
        """
        print("\n" + "-"*80)
        print(f"📊 {cat_var} vs {num_var}")
        if description:
            print(f"   {description}")
        print("-"*80)

        # Estadísticas descriptivas por grupo
        print("\n📈 Estadísticas Descriptivas por Grupo:")
        grouped = self.df.groupby(cat_var)[num_var].agg(['count', 'mean', 'median', 'std', 'min', 'max'])
        print(grouped.round(2).to_string())

        # Test de normalidad por grupo (si hay pocos grupos)
        groups = [group[num_var].values for name, group in self.df.groupby(cat_var)]

        # Test ANOVA (paramétrico) o Kruskal-Wallis (no paramétrico)
        print(f"\n🔬 Test de Diferencias entre Grupos:")

        # ANOVA
        f_stat, p_value_anova = f_oneway(*groups)
        print(f"\n   ANOVA (paramétrico):")
        print(f"      F-estadístico: {f_stat:.4f}")
        print(f"      P-valor: {p_value_anova:.4e}")
        if p_value_anova < 0.05:
            print(f"      ✓ Hay diferencias significativas entre grupos (p < 0.05)")
        else:
            print(f"      ✗ No hay diferencias significativas entre grupos (p >= 0.05)")

        # Kruskal-Wallis (alternativa no paramétrica)
        h_stat, p_value_kruskal = kruskal(*groups)
        print(f"\n   Kruskal-Wallis (no paramétrico):")
        print(f"      H-estadístico: {h_stat:.4f}")
        print(f"      P-valor: {p_value_kruskal:.4e}")
        if p_value_kruskal < 0.05:
            print(f"      ✓ Hay diferencias significativas entre grupos (p < 0.05)")
        else:
            print(f"      ✗ No hay diferencias significativas entre grupos (p >= 0.05)")

        # Tamaño del efecto (eta cuadrado)
        grand_mean = self.df[num_var].mean()
        ss_between = sum([len(group) * (group[num_var].mean() - grand_mean)**2
                          for name, group in self.df.groupby(cat_var)])
        ss_total = sum((self.df[num_var] - grand_mean)**2)
        eta_squared = ss_between / ss_total

        print(f"\n   Tamaño del Efecto (η²):")
        print(f"      η² = {eta_squared:.4f}")
        if eta_squared < 0.01:
            effect_size = "muy pequeño"
        elif eta_squared < 0.06:
            effect_size = "pequeño"
        elif eta_squared < 0.14:
            effect_size = "mediano"
        else:
            effect_size = "grande"
        print(f"      Interpretación: Efecto {effect_size}")

        return {
            'grouped_stats': grouped,
            'anova': {'f_stat': f_stat, 'p_value': p_value_anova},
            'kruskal': {'h_stat': h_stat, 'p_value': p_value_kruskal},
            'eta_squared': eta_squared
        }

    def analyze_categorical_associations(self):
        """Analiza asociaciones entre variables categóricas"""
        print("\n" + "="*80)
        print("3. ASOCIACIONES ENTRE VARIABLES CATEGÓRICAS")
        print("="*80)

        cat_vars = ['categoria_recencia', 'city_token', 'r_segment']

        results = {}

        for i in range(len(cat_vars)):
            for j in range(i+1, len(cat_vars)):
                var1, var2 = cat_vars[i], cat_vars[j]

                print(f"\n📊 {var1} vs {var2}")
                print("-"*80)

                # Tabla de contingencia
                contingency_table = pd.crosstab(self.df[var1], self.df[var2])

                # Test Chi-cuadrado
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)

                print(f"\n🔬 Test Chi-Cuadrado de Independencia:")
                print(f"   Chi² estadístico: {chi2:.4f}")
                print(f"   Grados de libertad: {dof}")
                print(f"   P-valor: {p_value:.4e}")

                if p_value < 0.05:
                    print(f"   ✓ Las variables están asociadas (p < 0.05)")
                else:
                    print(f"   ✗ Las variables son independientes (p >= 0.05)")

                # Coeficiente de Cramér's V (tamaño del efecto)
                n = contingency_table.sum().sum()
                min_dim = min(contingency_table.shape[0] - 1, contingency_table.shape[1] - 1)
                cramers_v = np.sqrt(chi2 / (n * min_dim))

                print(f"\n   Cramér's V (tamaño del efecto):")
                print(f"   V = {cramers_v:.4f}")
                if cramers_v < 0.1:
                    strength = "muy débil"
                elif cramers_v < 0.3:
                    strength = "débil"
                elif cramers_v < 0.5:
                    strength = "moderada"
                else:
                    strength = "fuerte"
                print(f"   Interpretación: Asociación {strength}")

                # Mostrar tabla de contingencia (solo si no es muy grande)
                if contingency_table.shape[0] <= 10 and contingency_table.shape[1] <= 10:
                    print(f"\n   Tabla de Contingencia:")
                    print(contingency_table.to_string())

                results[f"{var1}_vs_{var2}"] = {
                    'chi2': chi2,
                    'p_value': p_value,
                    'cramers_v': cramers_v,
                    'contingency_table': contingency_table
                }

        return results

    def analyze_growth_patterns(self):
        """Análisis de patrones de crecimiento (delta_orders)"""
        print("\n" + "="*80)
        print("4. ANÁLISIS DE PATRONES DE CRECIMIENTO")
        print("="*80)

        # Segmentar usuarios por crecimiento
        print("\n📊 Segmentación por Nivel de Crecimiento:")

        self.df['growth_segment'] = pd.cut(
            self.df['delta_orders'],
            bins=[0, 4, 8, 15, float('inf')],
            labels=['Bajo (1-4)', 'Medio (5-8)', 'Alto (9-15)', 'Muy Alto (>15)']
        )

        growth_dist = self.df['growth_segment'].value_counts().sort_index()
        print("\n   Distribución:")
        for segment, count in growth_dist.items():
            pct = (count / len(self.df) * 100)
            print(f"     {segment}: {count:,} ({pct:.1f}%)")

        # Relación entre velocidad (efo_to_four) y crecimiento
        print("\n\n📈 Relación entre Velocidad de Adopción (EFO-to-Four) y Crecimiento:")
        grouped = self.df.groupby('growth_segment')['efo_to_four'].agg(['mean', 'median', 'std'])
        print(grouped.round(2).to_string())

        # Test de correlación
        corr = self.df[['efo_to_four', 'delta_orders']].corr().iloc[0, 1]
        print(f"\n   Correlación efo_to_four vs delta_orders: {corr:.3f}")
        if abs(corr) > 0.3:
            direction = "negativa" if corr < 0 else "positiva"
            print(f"   💡 Insight: Hay una correlación {direction} {'fuerte' if abs(corr) > 0.5 else 'moderada'}")
            if corr < 0:
                print(f"      → Usuarios que llegan rápido a su 4ta orden tienden a tener MAYOR crecimiento")
            else:
                print(f"      → Usuarios que tardan más en su 4ta orden tienden a tener MAYOR crecimiento")

        return growth_dist

    def analyze_recency_impact(self):
        """Analiza el impacto de la recencia en el crecimiento"""
        print("\n" + "="*80)
        print("5. IMPACTO DE LA RECENCIA EN EL CRECIMIENTO")
        print("="*80)

        # Ordenar categorías de recencia
        recency_order = ['Activo (≤7d)', 'Semi-Activo (8–14d)', 'Tibio (15–30d)',
                        'Frío (31–90d)', 'Perdido (>90d)']

        self.df['categoria_recencia'] = pd.Categorical(
            self.df['categoria_recencia'],
            categories=recency_order,
            ordered=True
        )

        print("\n📊 Delta de Órdenes por Categoría de Recencia:")
        grouped = self.df.groupby('categoria_recencia')['delta_orders'].agg([
            'count', 'mean', 'median', 'std'
        ])
        print(grouped.round(2).to_string())

        print("\n💡 Insights:")
        max_growth = grouped['mean'].idxmax()
        min_growth = grouped['mean'].idxmin()
        print(f"   - Mayor crecimiento promedio: {max_growth} ({grouped.loc[max_growth, 'mean']:.2f} órdenes)")
        print(f"   - Menor crecimiento promedio: {min_growth} ({grouped.loc[min_growth, 'mean']:.2f} órdenes)")

        return grouped

    def analyze_segment_performance(self):
        """Analiza el desempeño por segmento R"""
        print("\n" + "="*80)
        print("6. DESEMPEÑO POR SEGMENTO R")
        print("="*80)

        print("\n📊 Métricas Clave por Segmento R:")

        # Agrupar por segmento R
        segment_analysis = self.df.groupby('r_segment').agg({
            'uid': 'count',
            'total_orders': ['mean', 'median', 'std'],
            'delta_orders': ['mean', 'median', 'std'],
            'efo_to_four': ['mean', 'median', 'std']
        }).round(2)

        segment_analysis.columns = ['_'.join(col).strip() for col in segment_analysis.columns.values]
        print(segment_analysis.to_string())

        # Identificar el mejor segmento
        print("\n💡 Insights:")
        best_growth = self.df.groupby('r_segment')['delta_orders'].mean().idxmax()
        best_retention = self.df.groupby('r_segment')['total_orders'].mean().idxmax()
        fastest = self.df.groupby('r_segment')['efo_to_four'].mean().idxmin()

        print(f"   - Segmento con mayor crecimiento (delta): {best_growth}")
        print(f"   - Segmento con más órdenes totales: {best_retention}")
        print(f"   - Segmento con adopción más rápida: {fastest}")

        return segment_analysis

    def analyze_city_performance(self):
        """Analiza el desempeño por ciudad"""
        print("\n" + "="*80)
        print("7. DESEMPEÑO POR CIUDAD")
        print("="*80)

        print("\n📊 Métricas Clave por Ciudad:")

        # Agrupar por ciudad
        city_analysis = self.df.groupby('city_token').agg({
            'uid': 'count',
            'total_orders': ['mean', 'median'],
            'delta_orders': ['mean', 'median'],
            'efo_to_four': ['mean', 'median']
        }).round(2)

        city_analysis.columns = ['_'.join(col).strip() for col in city_analysis.columns.values]
        city_analysis = city_analysis.sort_values('delta_orders_mean', ascending=False)
        print(city_analysis.to_string())

        print("\n💡 Insights:")
        best_city = city_analysis['delta_orders_mean'].idxmax()
        print(f"   - Ciudad con mayor crecimiento promedio: {best_city}")
        print(f"   - Delta promedio: {city_analysis.loc[best_city, 'delta_orders_mean']:.2f} órdenes")

        return city_analysis

    def generate_executive_summary(self):
        """Genera resumen ejecutivo del análisis multivariado"""
        print("\n" + "="*80)
        print("RESUMEN EJECUTIVO - ANÁLISIS MULTIVARIADO")
        print("="*80)

        # Calcular algunas métricas clave
        corr_efo_delta = self.df[['efo_to_four', 'delta_orders']].corr().iloc[0, 1]

        print(f"""
🎯 Hallazgos Principales:

   1. Correlación Velocidad-Crecimiento:
      - Correlación efo_to_four vs delta_orders: {corr_efo_delta:.3f}
      - {'Los usuarios que llegan más rápido a su 4ta orden tienden a crecer MÁS' if corr_efo_delta < 0 else 'Los usuarios que tardan más tienden a crecer MÁS'}

   2. Segmentación por Crecimiento:
      - {(self.df['delta_orders'] <= 4).sum():,} usuarios con bajo crecimiento (1-4 órdenes)
      - {((self.df['delta_orders'] > 4) & (self.df['delta_orders'] <= 8)).sum():,} usuarios con crecimiento medio (5-8 órdenes)
      - {(self.df['delta_orders'] > 8).sum():,} usuarios con alto crecimiento (>8 órdenes)

   3. Mejores Segmentos:
      - Segmento R con mayor crecimiento: {self.df.groupby('r_segment')['delta_orders'].mean().idxmax()}
      - Ciudad con mayor crecimiento: {self.df.groupby('city_token')['delta_orders'].mean().idxmax()}

💡 Recomendaciones Estratégicas:
   1. Enfocar recursos en usuarios con alta velocidad de adopción (bajo efo_to_four)
   2. Personalizar estrategias por segmento R y ciudad
   3. Investigar qué diferencia a los usuarios de alto crecimiento
""")

    def run_full_analysis(self):
        """Ejecuta el análisis multivariado completo"""
        print("\n")
        print("🚀 Iniciando análisis multivariado completo...\n")

        # Ejecutar análisis
        corr_results = self.analyze_numeric_correlations()

        print("\n" + "="*80)
        print("2. RELACIONES CATEGÓRICAS-NUMÉRICAS")
        print("="*80)

        # Recencia vs variables numéricas
        rec_orders = self.analyze_categorical_numeric_relationship(
            'categoria_recencia', 'total_orders',
            'Impacto de la recencia en el total de órdenes'
        )

        rec_delta = self.analyze_categorical_numeric_relationship(
            'categoria_recencia', 'delta_orders',
            'Impacto de la recencia en el crecimiento (delta)'
        )

        # Segmento R vs variables numéricas
        seg_delta = self.analyze_categorical_numeric_relationship(
            'r_segment', 'delta_orders',
            'Impacto del segmento R en el crecimiento'
        )

        seg_efo = self.analyze_categorical_numeric_relationship(
            'r_segment', 'efo_to_four',
            'Impacto del segmento R en la velocidad de adopción'
        )

        # Asociaciones categóricas
        assoc_results = self.analyze_categorical_associations()

        # Análisis específicos
        growth_dist = self.analyze_growth_patterns()
        recency_impact = self.analyze_recency_impact()
        segment_perf = self.analyze_segment_performance()
        city_perf = self.analyze_city_performance()

        # Resumen ejecutivo
        self.generate_executive_summary()

        print("\n" + "="*80)
        print("✅ Análisis multivariado completado")
        print("="*80)

        return {
            'correlations': corr_results,
            'categorical_associations': assoc_results,
            'growth_distribution': growth_dist,
            'recency_impact': recency_impact,
            'segment_performance': segment_perf,
            'city_performance': city_perf
        }


if __name__ == "__main__":
    # Ruta al dataset
    DATASET_PATH = "../dataset_protegido (1).csv"

    # Crear instancia del analizador
    analyzer = MultivariateAnalyzer(DATASET_PATH)

    # Ejecutar análisis completo
    results = analyzer.run_full_analysis()

    print("\n💡 Próximos pasos recomendados:")
    print("   1. Crear visualizaciones para comunicar estos hallazgos")
    print("   2. Realizar análisis de clustering basado en comportamiento")
    print("   3. Construir modelos predictivos de crecimiento")
