"""
Visualization Script
====================
Generación de visualizaciones exploratorias del dataset.

Este script crea gráficas para:
1. Distribuciones de variables numéricas
2. Distribuciones de variables categóricas
3. Relaciones bivariadas
4. Análisis de segmentación
5. Análisis temporal

Autor: Proyecto Final - Ciencia de Datos Aplicada
Fecha: 2025-10-19
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import ast
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class VisualizationGenerator:
    """Clase para generación de visualizaciones"""

    def __init__(self, filepath):
        """
        Inicializa el generador de visualizaciones

        Parameters:
        -----------
        filepath : str
            Ruta al archivo CSV del dataset
        """
        print("="*80)
        print("GENERACIÓN DE VISUALIZACIONES EXPLORATORIAS")
        print("="*80)
        print(f"\n[INFO] Cargando dataset desde: {filepath}")
        self.df = pd.read_csv(filepath)

        # Convertir fechas
        self.df['first_order_date'] = pd.to_datetime(self.df['first_order_date'])
        self.df['fourth_order_date'] = pd.to_datetime(self.df['fourth_order_date'])

        print(f"[OK] Dataset cargado: {self.df.shape[0]:,} filas x {self.df.shape[1]} columnas\n")

        # Crear directorio de salida
        import os
        self.output_dir = "../visualizations"
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"[OK] Directorio de visualizaciones: {self.output_dir}\n")

    def plot_numeric_distributions(self):
        """Visualiza distribuciones de variables numéricas"""
        print("\n" + "="*80)
        print("1. DISTRIBUCIONES DE VARIABLES NUMÉRICAS")
        print("="*80)

        numeric_vars = {
            'total_orders': 'Total de Órdenes',
            'delta_orders': 'Delta de Órdenes (Crecimiento)',
            'efo_to_four': 'Días entre 1ra y 4ta Orden (EFO-to-Four)'
        }

        for var, title in numeric_vars.items():
            print(f"\n📊 Generando gráficas para {var}...")

            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle(f'Análisis de Distribución: {title}', fontsize=16, fontweight='bold')

            # 1. Histograma
            axes[0, 0].hist(self.df[var], bins=50, edgecolor='black', alpha=0.7)
            axes[0, 0].set_title(f'Histograma de {title}')
            axes[0, 0].set_xlabel(var)
            axes[0, 0].set_ylabel('Frecuencia')
            axes[0, 0].axvline(self.df[var].mean(), color='red', linestyle='--',
                              label=f'Media: {self.df[var].mean():.2f}')
            axes[0, 0].axvline(self.df[var].median(), color='green', linestyle='--',
                              label=f'Mediana: {self.df[var].median():.2f}')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)

            # 2. Boxplot
            axes[0, 1].boxplot(self.df[var], vert=True)
            axes[0, 1].set_title(f'Boxplot de {title}')
            axes[0, 1].set_ylabel(var)
            axes[0, 1].grid(True, alpha=0.3)

            # 3. Violinplot
            axes[1, 0].violinplot([self.df[var]], vert=True, showmeans=True, showmedians=True)
            axes[1, 0].set_title(f'Violin Plot de {title}')
            axes[1, 0].set_ylabel(var)
            axes[1, 0].grid(True, alpha=0.3)

            # 4. Q-Q plot
            from scipy import stats
            stats.probplot(self.df[var], dist="norm", plot=axes[1, 1])
            axes[1, 1].set_title(f'Q-Q Plot de {title}')
            axes[1, 1].grid(True, alpha=0.3)

            plt.tight_layout()
            filename = f"{self.output_dir}/01_dist_{var}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"  ✓ Guardado: {filename}")
            plt.close()

    def plot_categorical_distributions(self):
        """Visualiza distribuciones de variables categóricas"""
        print("\n" + "="*80)
        print("2. DISTRIBUCIONES DE VARIABLES CATEGÓRICAS")
        print("="*80)

        categorical_vars = {
            'categoria_recencia': 'Categoría de Recencia',
            'city_token': 'Ciudad',
            'r_segment': 'Segmento R'
        }

        for var, title in categorical_vars.items():
            print(f"\n📊 Generando gráficas para {var}...")

            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            fig.suptitle(f'Distribución de {title}', fontsize=16, fontweight='bold')

            # Contar frecuencias
            freq = self.df[var].value_counts()

            # 1. Barplot
            freq.plot(kind='bar', ax=axes[0], edgecolor='black', alpha=0.7)
            axes[0].set_title(f'Frecuencia Absoluta de {title}')
            axes[0].set_xlabel(var)
            axes[0].set_ylabel('Cantidad de Usuarios')
            axes[0].tick_params(axis='x', rotation=45)
            axes[0].grid(True, alpha=0.3, axis='y')

            # Agregar etiquetas de valores
            for i, v in enumerate(freq.values):
                axes[0].text(i, v + 100, f'{v:,}', ha='center', va='bottom', fontsize=9)

            # 2. Pie chart
            colors = plt.cm.Set3(range(len(freq)))
            axes[1].pie(freq.values, labels=freq.index, autopct='%1.1f%%',
                       startangle=90, colors=colors)
            axes[1].set_title(f'Proporción de {title}')

            plt.tight_layout()
            filename = f"{self.output_dir}/02_dist_{var}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"  ✓ Guardado: {filename}")
            plt.close()

    def plot_recency_vs_growth(self):
        """Visualiza la relación entre recencia y crecimiento"""
        print("\n" + "="*80)
        print("3. RELACIÓN RECENCIA VS CRECIMIENTO")
        print("="*80)

        # Ordenar categorías de recencia
        recency_order = ['Activo (≤7d)', 'Semi-Activo (8–14d)', 'Tibio (15–30d)',
                        'Frío (31–90d)', 'Perdido (>90d)']

        self.df['categoria_recencia'] = pd.Categorical(
            self.df['categoria_recencia'],
            categories=recency_order,
            ordered=True
        )

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Impacto de la Recencia en las Métricas Clave', fontsize=16, fontweight='bold')

        # 1. Boxplot delta_orders por recencia
        self.df.boxplot(column='delta_orders', by='categoria_recencia', ax=axes[0, 0])
        axes[0, 0].set_title('Delta de Órdenes por Categoría de Recencia')
        axes[0, 0].set_xlabel('Categoría de Recencia')
        axes[0, 0].set_ylabel('Delta de Órdenes')
        axes[0, 0].tick_params(axis='x', rotation=45)
        plt.sca(axes[0, 0])
        plt.xticks(rotation=45, ha='right')

        # 2. Barplot promedio de delta_orders
        grouped = self.df.groupby('categoria_recencia')['delta_orders'].mean().sort_values(ascending=False)
        grouped.plot(kind='bar', ax=axes[0, 1], edgecolor='black', alpha=0.7, color='skyblue')
        axes[0, 1].set_title('Promedio de Crecimiento (Delta) por Recencia')
        axes[0, 1].set_xlabel('Categoría de Recencia')
        axes[0, 1].set_ylabel('Delta Promedio de Órdenes')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3, axis='y')

        # Agregar valores
        for i, v in enumerate(grouped.values):
            axes[0, 1].text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

        # 3. Boxplot total_orders por recencia
        self.df.boxplot(column='total_orders', by='categoria_recencia', ax=axes[1, 0])
        axes[1, 0].set_title('Total de Órdenes por Categoría de Recencia')
        axes[1, 0].set_xlabel('Categoría de Recencia')
        axes[1, 0].set_ylabel('Total de Órdenes')
        axes[1, 0].tick_params(axis='x', rotation=45)
        plt.sca(axes[1, 0])
        plt.xticks(rotation=45, ha='right')

        # 4. Distribución de recencia
        freq = self.df['categoria_recencia'].value_counts()[recency_order]
        freq.plot(kind='bar', ax=axes[1, 1], edgecolor='black', alpha=0.7, color='coral')
        axes[1, 1].set_title('Distribución de Usuarios por Recencia')
        axes[1, 1].set_xlabel('Categoría de Recencia')
        axes[1, 1].set_ylabel('Cantidad de Usuarios')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3, axis='y')

        # Agregar porcentajes
        for i, v in enumerate(freq.values):
            pct = (v / len(self.df) * 100)
            axes[1, 1].text(i, v + 100, f'{v:,}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        filename = f"{self.output_dir}/03_recency_vs_growth.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: {filename}")
        plt.close()

    def plot_efo_vs_growth(self):
        """Visualiza la relación entre velocidad de adopción y crecimiento"""
        print("\n" + "="*80)
        print("4. RELACIÓN VELOCIDAD DE ADOPCIÓN VS CRECIMIENTO")
        print("="*80)

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Velocidad de Adopción (EFO-to-Four) vs Crecimiento', fontsize=16, fontweight='bold')

        # 1. Scatter plot
        axes[0, 0].scatter(self.df['efo_to_four'], self.df['delta_orders'], alpha=0.3, s=20)
        axes[0, 0].set_title('Scatter Plot: EFO-to-Four vs Delta de Órdenes')
        axes[0, 0].set_xlabel('Días entre 1ra y 4ta Orden (EFO-to-Four)')
        axes[0, 0].set_ylabel('Delta de Órdenes')
        axes[0, 0].grid(True, alpha=0.3)

        # Agregar línea de tendencia
        z = np.polyfit(self.df['efo_to_four'], self.df['delta_orders'], 1)
        p = np.poly1d(z)
        axes[0, 0].plot(self.df['efo_to_four'].sort_values(), p(self.df['efo_to_four'].sort_values()),
                       "r--", alpha=0.8, linewidth=2, label=f'Tendencia: y={z[0]:.3f}x+{z[1]:.2f}')
        axes[0, 0].legend()

        # Agregar correlación
        corr = self.df[['efo_to_four', 'delta_orders']].corr().iloc[0, 1]
        axes[0, 0].text(0.05, 0.95, f'Correlación: {corr:.3f}',
                       transform=axes[0, 0].transAxes, fontsize=12,
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # 2. Hexbin plot (densidad)
        hexbin = axes[0, 1].hexbin(self.df['efo_to_four'], self.df['delta_orders'],
                                   gridsize=30, cmap='YlOrRd', mincnt=1)
        axes[0, 1].set_title('Densidad: EFO-to-Four vs Delta de Órdenes')
        axes[0, 1].set_xlabel('Días entre 1ra y 4ta Orden (EFO-to-Four)')
        axes[0, 1].set_ylabel('Delta de Órdenes')
        plt.colorbar(hexbin, ax=axes[0, 1], label='Cantidad de usuarios')

        # 3. Segmentar por velocidad y ver crecimiento
        self.df['efo_segment'] = pd.cut(
            self.df['efo_to_four'],
            bins=[0, 7, 14, 21, 31],
            labels=['Muy Rápido (0-7d)', 'Rápido (8-14d)', 'Moderado (15-21d)', 'Lento (>21d)']
        )

        grouped = self.df.groupby('efo_segment')['delta_orders'].mean().sort_values(ascending=False)
        grouped.plot(kind='bar', ax=axes[1, 0], edgecolor='black', alpha=0.7, color='lightgreen')
        axes[1, 0].set_title('Crecimiento Promedio por Velocidad de Adopción')
        axes[1, 0].set_xlabel('Segmento de Velocidad (EFO-to-Four)')
        axes[1, 0].set_ylabel('Delta Promedio de Órdenes')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3, axis='y')

        for i, v in enumerate(grouped.values):
            axes[1, 0].text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

        # 4. Boxplot
        self.df.boxplot(column='delta_orders', by='efo_segment', ax=axes[1, 1])
        axes[1, 1].set_title('Distribución de Crecimiento por Velocidad')
        axes[1, 1].set_xlabel('Segmento de Velocidad (EFO-to-Four)')
        axes[1, 1].set_ylabel('Delta de Órdenes')
        axes[1, 1].tick_params(axis='x', rotation=45)
        plt.sca(axes[1, 1])
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        filename = f"{self.output_dir}/04_efo_vs_growth.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: {filename}")
        plt.close()

    def plot_segment_performance(self):
        """Visualiza el desempeño por segmento R"""
        print("\n" + "="*80)
        print("5. DESEMPEÑO POR SEGMENTO R")
        print("="*80)

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análisis de Desempeño por Segmento R', fontsize=16, fontweight='bold')

        # 1. Delta promedio por segmento
        grouped = self.df.groupby('r_segment')['delta_orders'].mean().sort_values(ascending=False)
        grouped.plot(kind='bar', ax=axes[0, 0], edgecolor='black', alpha=0.7, color='steelblue')
        axes[0, 0].set_title('Crecimiento Promedio por Segmento R')
        axes[0, 0].set_xlabel('Segmento R')
        axes[0, 0].set_ylabel('Delta Promedio de Órdenes')
        axes[0, 0].tick_params(axis='x', rotation=0)
        axes[0, 0].grid(True, alpha=0.3, axis='y')

        for i, v in enumerate(grouped.values):
            axes[0, 0].text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

        # 2. Total orders promedio por segmento
        grouped_total = self.df.groupby('r_segment')['total_orders'].mean().sort_values(ascending=False)
        grouped_total.plot(kind='bar', ax=axes[0, 1], edgecolor='black', alpha=0.7, color='salmon')
        axes[0, 1].set_title('Total de Órdenes Promedio por Segmento R')
        axes[0, 1].set_xlabel('Segmento R')
        axes[0, 1].set_ylabel('Total Promedio de Órdenes')
        axes[0, 1].tick_params(axis='x', rotation=0)
        axes[0, 1].grid(True, alpha=0.3, axis='y')

        for i, v in enumerate(grouped_total.values):
            axes[0, 1].text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

        # 3. EFO-to-Four promedio por segmento
        grouped_efo = self.df.groupby('r_segment')['efo_to_four'].mean().sort_values()
        grouped_efo.plot(kind='bar', ax=axes[1, 0], edgecolor='black', alpha=0.7, color='mediumseagreen')
        axes[1, 0].set_title('Velocidad de Adopción Promedio por Segmento R')
        axes[1, 0].set_xlabel('Segmento R')
        axes[1, 0].set_ylabel('Días Promedio (EFO-to-Four)')
        axes[1, 0].tick_params(axis='x', rotation=0)
        axes[1, 0].grid(True, alpha=0.3, axis='y')

        for i, v in enumerate(grouped_efo.values):
            axes[1, 0].text(i, v + 0.2, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

        # 4. Distribución de usuarios por segmento
        freq = self.df['r_segment'].value_counts().sort_index()
        freq.plot(kind='bar', ax=axes[1, 1], edgecolor='black', alpha=0.7, color='orchid')
        axes[1, 1].set_title('Distribución de Usuarios por Segmento R')
        axes[1, 1].set_xlabel('Segmento R')
        axes[1, 1].set_ylabel('Cantidad de Usuarios')
        axes[1, 1].tick_params(axis='x', rotation=0)
        axes[1, 1].grid(True, alpha=0.3, axis='y')

        for i, v in enumerate(freq.values):
            pct = (v / len(self.df) * 100)
            axes[1, 1].text(i, v + 100, f'{v:,}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        filename = f"{self.output_dir}/05_segment_performance.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: {filename}")
        plt.close()

    def plot_temporal_analysis(self):
        """Análisis temporal de órdenes"""
        print("\n" + "="*80)
        print("6. ANÁLISIS TEMPORAL")
        print("="*80)

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análisis Temporal de Órdenes', fontsize=16, fontweight='bold')

        # 1. Serie temporal de primera orden
        first_order_monthly = self.df['first_order_date'].dt.to_period('M').value_counts().sort_index()
        first_order_monthly.plot(kind='line', ax=axes[0, 0], marker='o', linewidth=2, markersize=8)
        axes[0, 0].set_title('Evolución de Primeras Órdenes por Mes')
        axes[0, 0].set_xlabel('Mes')
        axes[0, 0].set_ylabel('Cantidad de Usuarios')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].tick_params(axis='x', rotation=45)

        # 2. Serie temporal de cuarta orden
        fourth_order_monthly = self.df['fourth_order_date'].dt.to_period('M').value_counts().sort_index()
        fourth_order_monthly.plot(kind='line', ax=axes[0, 1], marker='s', linewidth=2, markersize=8, color='orange')
        axes[0, 1].set_title('Evolución de Cuartas Órdenes por Mes')
        axes[0, 1].set_xlabel('Mes')
        axes[0, 1].set_ylabel('Cantidad de Usuarios')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].tick_params(axis='x', rotation=45)

        # 3. Distribución por día de la semana - Primera orden
        dow_map = {0: 'Lun', 1: 'Mar', 2: 'Mié', 3: 'Jue', 4: 'Vie', 5: 'Sáb', 6: 'Dom'}
        first_dow = self.df['first_order_date'].dt.dayofweek.map(dow_map).value_counts()
        dow_order = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        first_dow = first_dow.reindex(dow_order)

        first_dow.plot(kind='bar', ax=axes[1, 0], edgecolor='black', alpha=0.7, color='lightcoral')
        axes[1, 0].set_title('Primeras Órdenes por Día de la Semana')
        axes[1, 0].set_xlabel('Día de la Semana')
        axes[1, 0].set_ylabel('Cantidad de Usuarios')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3, axis='y')

        # 4. Distribución por día de la semana - Cuarta orden
        fourth_dow = self.df['fourth_order_date'].dt.dayofweek.map(dow_map).value_counts()
        fourth_dow = fourth_dow.reindex(dow_order)

        fourth_dow.plot(kind='bar', ax=axes[1, 1], edgecolor='black', alpha=0.7, color='lightskyblue')
        axes[1, 1].set_title('Cuartas Órdenes por Día de la Semana')
        axes[1, 1].set_xlabel('Día de la Semana')
        axes[1, 1].set_ylabel('Cantidad de Usuarios')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        filename = f"{self.output_dir}/06_temporal_analysis.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: {filename}")
        plt.close()

    def plot_correlation_heatmap(self):
        """Mapa de calor de correlaciones"""
        print("\n" + "="*80)
        print("7. MAPA DE CALOR DE CORRELACIONES")
        print("="*80)

        numeric_cols = ['total_orders', 'total_orders_tmenos1', 'delta_orders', 'efo_to_four']

        # Calcular matriz de correlación
        corr_matrix = self.df[numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(10, 8))

        # Crear heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   fmt='.3f', ax=ax)

        ax.set_title('Matriz de Correlación de Variables Numéricas', fontsize=16, fontweight='bold', pad=20)

        plt.tight_layout()
        filename = f"{self.output_dir}/07_correlation_heatmap.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: {filename}")
        plt.close()

    def run_all_visualizations(self):
        """Genera todas las visualizaciones"""
        print("\n")
        print("🚀 Iniciando generación de visualizaciones...\n")

        self.plot_numeric_distributions()
        self.plot_categorical_distributions()
        self.plot_recency_vs_growth()
        self.plot_efo_vs_growth()
        self.plot_segment_performance()
        self.plot_temporal_analysis()
        self.plot_correlation_heatmap()

        print("\n" + "="*80)
        print("✅ Todas las visualizaciones generadas exitosamente")
        print("="*80)
        print(f"\n📁 Ubicación: {self.output_dir}/")
        print("\n💡 Las visualizaciones están listas para ser incluidas en el notebook final")


if __name__ == "__main__":
    # Ruta al dataset
    DATASET_PATH = "../dataset_protegido (1).csv"

    # Crear instancia del generador
    visualizer = VisualizationGenerator(DATASET_PATH)

    # Generar todas las visualizaciones
    visualizer.run_all_visualizations()

    print("\n💡 Próximos pasos:")
    print("   1. Revisar las visualizaciones generadas")
    print("   2. Seleccionar las más relevantes para el reporte final")
    print("   3. Integrar en el notebook de análisis exploratorio")
