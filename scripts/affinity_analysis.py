"""
Affinity Analysis Script
=========================
Análisis profundo de las afinidades de consumo de usuarios.

Este script analiza las variables tipo diccionario que contienen:
- main_category_counts: Afinidades por categoría de producto
- ka_type_counts: Afinidades por tipo de tienda (KA)
- shop_name_counts: Afinidades por tienda específica
- brand_name_counts: Afinidades por marca

Autor: Proyecto Final - Ciencia de Datos Aplicada
Fecha: 2025-10-19
"""

import pandas as pd
import numpy as np
import json
import ast
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')


class AffinityAnalyzer:
    """Clase para análisis de afinidades de consumo"""

    def __init__(self, filepath):
        """
        Inicializa el analizador de afinidades

        Parameters:
        -----------
        filepath : str
            Ruta al archivo CSV del dataset
        """
        print("="*80)
        print("ANÁLISIS DE AFINIDADES DE CONSUMO")
        print("="*80)
        print(f"\n[INFO] Cargando dataset desde: {filepath}")
        self.df = pd.read_csv(filepath)
        print(f"[OK] Dataset cargado: {self.df.shape[0]:,} filas x {self.df.shape[1]} columnas\n")

        # Convertir las columnas de diccionarios de string a dict
        self._parse_dict_columns()

    def _parse_dict_columns(self):
        """Convierte las columnas que son strings de diccionarios a diccionarios reales"""
        dict_columns = ['main_category_counts', 'ka_type_counts', 'shop_name_counts', 'brand_name_counts']

        print("[INFO] Parseando columnas de diccionarios...")
        for col in dict_columns:
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
                    print(f"  ✓ {col} parseado correctamente")
                except Exception as e:
                    print(f"  ✗ Error parseando {col}: {str(e)}")

        print("[OK] Parseo completado\n")

    def analyze_category_affinity(self):
        """Análisis de afinidad por categoría principal"""
        print("\n" + "="*80)
        print("1. ANÁLISIS DE AFINIDAD POR CATEGORÍA PRINCIPAL")
        print("="*80)

        # Extraer todas las categorías
        all_categories = Counter()
        total_category_orders = 0

        for idx, row in self.df.iterrows():
            categories = row['main_category_counts']
            if isinstance(categories, dict):
                for cat, count in categories.items():
                    all_categories[cat] += count
                    total_category_orders += count

        print(f"\n📊 Resumen General:")
        print(f"   Total de categorías únicas: {len(all_categories)}")
        print(f"   Total de órdenes por categoría: {total_category_orders:,}")

        # Top 20 categorías más populares
        print(f"\n🔝 Top 20 Categorías Más Populares:")
        top_categories = pd.DataFrame(all_categories.most_common(20), columns=['Categoría', 'Total_Órdenes'])
        top_categories['Porcentaje'] = (top_categories['Total_Órdenes'] / total_category_orders * 100).round(2)
        top_categories['Porcentaje_Acumulado'] = top_categories['Porcentaje'].cumsum().round(2)
        print(top_categories.to_string(index=False))

        # Análisis de diversidad de categorías por usuario
        print(f"\n📈 Diversidad de Categorías por Usuario:")
        category_diversity = self.df['main_category_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
        print(f"   Promedio de categorías por usuario: {category_diversity.mean():.2f}")
        print(f"   Mediana de categorías por usuario: {category_diversity.median():.0f}")
        print(f"   Rango: [{category_diversity.min()}, {category_diversity.max()}]")

        print(f"\n   Distribución de diversidad:")
        diversity_dist = category_diversity.value_counts().sort_index()
        for n_cats, n_users in diversity_dist.head(10).items():
            pct = (n_users / len(self.df) * 100)
            print(f"     {n_cats} categorías: {n_users:,} usuarios ({pct:.1f}%)")

        # Concentración: ¿Cuántas categorías representan el 80% de las órdenes?
        cumsum_80 = top_categories[top_categories['Porcentaje_Acumulado'] <= 80]
        print(f"\n💡 Insight de Concentración:")
        print(f"   {len(cumsum_80)} categorías representan el 80% de todas las órdenes")

        return {
            'all_categories': all_categories,
            'top_categories': top_categories,
            'diversity': category_diversity
        }

    def analyze_ka_type_affinity(self):
        """Análisis de afinidad por tipo de tienda (KA Type)"""
        print("\n" + "="*80)
        print("2. ANÁLISIS DE AFINIDAD POR TIPO DE TIENDA (KA TYPE)")
        print("="*80)

        # Extraer todos los tipos de KA
        all_ka_types = Counter()
        total_ka_orders = 0

        for idx, row in self.df.iterrows():
            ka_types = row['ka_type_counts']
            if isinstance(ka_types, dict):
                for ka, count in ka_types.items():
                    all_ka_types[ka] += count
                    total_ka_orders += count

        print(f"\n📊 Resumen General:")
        print(f"   Total de tipos de KA únicos: {len(all_ka_types)}")
        print(f"   Total de órdenes por tipo de KA: {total_ka_orders:,}")

        # Distribución de tipos de KA
        print(f"\n🏪 Distribución de Tipos de Tienda:")
        ka_df = pd.DataFrame(all_ka_types.most_common(), columns=['Tipo_KA', 'Total_Órdenes'])
        ka_df['Porcentaje'] = (ka_df['Total_Órdenes'] / total_ka_orders * 100).round(2)
        print(ka_df.to_string(index=False))

        # Análisis de diversidad de KA types por usuario
        print(f"\n📈 Diversidad de Tipos de Tienda por Usuario:")
        ka_diversity = self.df['ka_type_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
        print(f"   Promedio de tipos de KA por usuario: {ka_diversity.mean():.2f}")
        print(f"   Mediana de tipos de KA por usuario: {ka_diversity.median():.0f}")

        print(f"\n   Distribución de diversidad:")
        ka_diversity_dist = ka_diversity.value_counts().sort_index()
        for n_types, n_users in ka_diversity_dist.items():
            pct = (n_users / len(self.df) * 100)
            print(f"     {n_types} tipos de KA: {n_users:,} usuarios ({pct:.1f}%)")

        return {
            'all_ka_types': all_ka_types,
            'ka_df': ka_df,
            'diversity': ka_diversity
        }

    def analyze_shop_affinity(self):
        """Análisis de afinidad por tienda específica"""
        print("\n" + "="*80)
        print("3. ANÁLISIS DE AFINIDAD POR TIENDA ESPECÍFICA")
        print("="*80)

        # Extraer todas las tiendas
        all_shops = Counter()
        total_shop_orders = 0

        for idx, row in self.df.iterrows():
            shops = row['shop_name_counts']
            if isinstance(shops, dict):
                for shop, count in shops.items():
                    all_shops[shop] += count
                    total_shop_orders += count

        print(f"\n📊 Resumen General:")
        print(f"   Total de tiendas únicas: {len(all_shops)}")
        print(f"   Total de órdenes por tienda: {total_shop_orders:,}")

        # Top 20 tiendas más populares
        print(f"\n🔝 Top 20 Tiendas Más Populares:")
        top_shops = pd.DataFrame(all_shops.most_common(20), columns=['Tienda', 'Total_Órdenes'])
        top_shops['Porcentaje'] = (top_shops['Total_Órdenes'] / total_shop_orders * 100).round(2)
        top_shops['Porcentaje_Acumulado'] = top_shops['Porcentaje'].cumsum().round(2)
        print(top_shops.to_string(index=False))

        # Análisis de lealtad a tiendas
        print(f"\n🎯 Análisis de Lealtad a Tiendas:")
        shop_diversity = self.df['shop_name_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
        print(f"   Promedio de tiendas visitadas por usuario: {shop_diversity.mean():.2f}")
        print(f"   Mediana de tiendas visitadas por usuario: {shop_diversity.median():.0f}")

        # Usuarios que compran en una sola tienda vs. múltiples
        single_shop_users = (shop_diversity == 1).sum()
        multi_shop_users = (shop_diversity > 1).sum()
        print(f"\n   👤 Usuarios con 1 sola tienda: {single_shop_users:,} ({single_shop_users/len(self.df)*100:.1f}%)")
        print(f"   👥 Usuarios con múltiples tiendas: {multi_shop_users:,} ({multi_shop_users/len(self.df)*100:.1f}%)")

        # Concentración
        cumsum_80 = top_shops[top_shops['Porcentaje_Acumulado'] <= 80]
        print(f"\n💡 Insight de Concentración:")
        print(f"   {len(cumsum_80)} tiendas representan el 80% de todas las órdenes")

        return {
            'all_shops': all_shops,
            'top_shops': top_shops,
            'diversity': shop_diversity
        }

    def analyze_brand_affinity(self):
        """Análisis de afinidad por marca"""
        print("\n" + "="*80)
        print("4. ANÁLISIS DE AFINIDAD POR MARCA")
        print("="*80)

        # Extraer todas las marcas
        all_brands = Counter()
        total_brand_orders = 0

        for idx, row in self.df.iterrows():
            brands = row['brand_name_counts']
            if isinstance(brands, dict):
                for brand, count in brands.items():
                    all_brands[brand] += count
                    total_brand_orders += count

        print(f"\n📊 Resumen General:")
        print(f"   Total de marcas únicas: {len(all_brands)}")
        print(f"   Total de órdenes por marca: {total_brand_orders:,}")

        # Top 20 marcas más populares
        print(f"\n🔝 Top 20 Marcas Más Populares:")
        top_brands = pd.DataFrame(all_brands.most_common(20), columns=['Marca', 'Total_Órdenes'])
        top_brands['Porcentaje'] = (top_brands['Total_Órdenes'] / total_brand_orders * 100).round(2)
        top_brands['Porcentaje_Acumulado'] = top_brands['Porcentaje'].cumsum().round(2)
        print(top_brands.to_string(index=False))

        # Análisis de lealtad a marcas
        print(f"\n🎯 Análisis de Lealtad a Marcas:")
        brand_diversity = self.df['brand_name_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
        print(f"   Promedio de marcas compradas por usuario: {brand_diversity.mean():.2f}")
        print(f"   Mediana de marcas compradas por usuario: {brand_diversity.median():.0f}")

        # Concentración
        cumsum_80 = top_brands[top_brands['Porcentaje_Acumulado'] <= 80]
        print(f"\n💡 Insight de Concentración:")
        print(f"   {len(cumsum_80)} marcas representan el 80% de todas las órdenes")

        return {
            'all_brands': all_brands,
            'top_brands': top_brands,
            'diversity': brand_diversity
        }

    def analyze_cross_affinity(self):
        """Análisis cruzado de afinidades"""
        print("\n" + "="*80)
        print("5. ANÁLISIS CRUZADO DE AFINIDADES")
        print("="*80)

        # Crear una categoría dominante para cada usuario
        print("\n📊 Categoría Dominante por Usuario:")
        self.df['dominant_category'] = self.df['main_category_counts'].apply(
            lambda x: max(x.items(), key=lambda i: i[1])[0] if isinstance(x, dict) and len(x) > 0 else None
        )

        dominant_cat_dist = self.df['dominant_category'].value_counts().head(10)
        print("\n  Top 10 categorías dominantes:")
        for cat, count in dominant_cat_dist.items():
            pct = (count / len(self.df) * 100)
            print(f"    {cat}: {count:,} usuarios ({pct:.1f}%)")

        # Tipo de KA dominante
        print("\n\n🏪 Tipo de Tienda Dominante por Usuario:")
        self.df['dominant_ka_type'] = self.df['ka_type_counts'].apply(
            lambda x: max(x.items(), key=lambda i: i[1])[0] if isinstance(x, dict) and len(x) > 0 else None
        )

        dominant_ka_dist = self.df['dominant_ka_type'].value_counts()
        print("\n  Distribución de tipos de tienda dominantes:")
        for ka, count in dominant_ka_dist.items():
            pct = (count / len(self.df) * 100)
            print(f"    {ka}: {count:,} usuarios ({pct:.1f}%)")

        # Análisis de especialización vs diversificación
        print("\n\n🎯 Índice de Especialización vs. Diversificación:")

        # Calcular índice de concentración (Herfindahl) para categorías
        def herfindahl_index(counts_dict):
            """Calcula el índice de Herfindahl-Hirschman (concentración)"""
            if not isinstance(counts_dict, dict) or len(counts_dict) == 0:
                return 0
            total = sum(counts_dict.values())
            if total == 0:
                return 0
            return sum((count / total) ** 2 for count in counts_dict.values())

        self.df['category_concentration'] = self.df['main_category_counts'].apply(herfindahl_index)

        print(f"   Concentración en categorías (índice Herfindahl):")
        print(f"     Promedio: {self.df['category_concentration'].mean():.3f}")
        print(f"     Mediana: {self.df['category_concentration'].median():.3f}")
        print(f"\n   Interpretación:")
        print(f"     - Cercano a 1.0 = Usuario muy especializado (compra en pocas categorías)")
        print(f"     - Cercano a 0.0 = Usuario muy diversificado (compra en muchas categorías)")

        # Segmentar usuarios por concentración
        self.df['user_type'] = pd.cut(
            self.df['category_concentration'],
            bins=[0, 0.33, 0.66, 1.0],
            labels=['Diversificado', 'Moderado', 'Especializado']
        )

        print(f"\n   Segmentación de usuarios:")
        user_type_dist = self.df['user_type'].value_counts()
        for utype, count in user_type_dist.items():
            pct = (count / len(self.df) * 100)
            print(f"     {utype}: {count:,} usuarios ({pct:.1f}%)")

        return {
            'dominant_cat_dist': dominant_cat_dist,
            'dominant_ka_dist': dominant_ka_dist,
            'user_type_dist': user_type_dist
        }

    def generate_affinity_summary(self):
        """Genera un resumen ejecutivo de afinidades"""
        print("\n" + "="*80)
        print("RESUMEN EJECUTIVO - AFINIDADES DE CONSUMO")
        print("="*80)

        # Calcular métricas clave
        category_diversity = self.df['main_category_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
        shop_diversity = self.df['shop_name_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
        brand_diversity = self.df['brand_name_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
        ka_diversity = self.df['ka_type_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)

        print(f"""
🎯 Diversidad Promedio por Usuario:
   - Categorías: {category_diversity.mean():.2f}
   - Tipos de tienda: {ka_diversity.mean():.2f}
   - Tiendas específicas: {shop_diversity.mean():.2f}
   - Marcas: {brand_diversity.mean():.2f}

💡 Insights Clave:
   1. Los usuarios tienen un comportamiento {'diversificado' if category_diversity.mean() > 3 else 'concentrado'} en categorías
   2. El promedio de tiendas visitadas ({shop_diversity.mean():.1f}) sugiere {'alta exploración' if shop_diversity.mean() > 5 else 'lealtad a pocas tiendas'}
   3. La base de usuarios es {'heterogénea' if len(self.df['dominant_category'].unique()) > 10 else 'homogénea'} en sus preferencias

🎲 Concentración del Mercado:
   - Índice de concentración promedio: {self.df['category_concentration'].mean():.3f}
   - Usuarios especializados: {(self.df['user_type'] == 'Especializado').sum()} ({(self.df['user_type'] == 'Especializado').sum()/len(self.df)*100:.1f}%)
   - Usuarios diversificados: {(self.df['user_type'] == 'Diversificado').sum()} ({(self.df['user_type'] == 'Diversificado').sum()/len(self.df)*100:.1f}%)
""")

    def run_full_analysis(self):
        """Ejecuta el análisis completo de afinidades"""
        print("\n")
        print("🚀 Iniciando análisis completo de afinidades...\n")

        # Ejecutar todos los análisis
        category_results = self.analyze_category_affinity()
        ka_results = self.analyze_ka_type_affinity()
        shop_results = self.analyze_shop_affinity()
        brand_results = self.analyze_brand_affinity()
        cross_results = self.analyze_cross_affinity()
        self.generate_affinity_summary()

        print("\n" + "="*80)
        print("✅ Análisis de afinidades completado")
        print("="*80)

        return {
            'category_results': category_results,
            'ka_results': ka_results,
            'shop_results': shop_results,
            'brand_results': brand_results,
            'cross_results': cross_results,
            'df_enriched': self.df
        }


if __name__ == "__main__":
    # Ruta al dataset
    DATASET_PATH = "../dataset_protegido (1).csv"

    # Crear instancia del analizador
    analyzer = AffinityAnalyzer(DATASET_PATH)

    # Ejecutar análisis completo
    results = analyzer.run_full_analysis()

    print("\n💡 Próximos pasos recomendados:")
    print("   1. Usar las categorías/marcas/tiendas dominantes para segmentación")
    print("   2. Analizar relación entre especialización y crecimiento de órdenes")
    print("   3. Identificar oportunidades de cross-selling basadas en afinidades")
