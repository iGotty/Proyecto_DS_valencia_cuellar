"""
Data Quality Analysis Script
=============================
Análisis exhaustivo de la calidad de los datos del dataset de usuarios de Engagement.

Este script evalúa:
1. Valores faltantes (missings)
2. Duplicados
3. Tipos de datos y consistencia
4. Rangos y valores atípicos
5. Integridad referencial

Autor: Proyecto Final - Ciencia de Datos Aplicada
Fecha: 2025-10-19
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')


class DataQualityAnalyzer:
    """Clase para análisis de calidad de datos"""

    def __init__(self, filepath):
        """
        Inicializa el analizador de calidad de datos

        Parameters:
        -----------
        filepath : str
            Ruta al archivo CSV del dataset
        """
        print("="*80)
        print("ANÁLISIS DE CALIDAD DE DATOS")
        print("="*80)
        print(f"\n[INFO] Cargando dataset desde: {filepath}")
        self.df = pd.read_csv(filepath)
        print(f"[OK] Dataset cargado: {self.df.shape[0]:,} filas x {self.df.shape[1]} columnas\n")

    def basic_info(self):
        """Información básica del dataset"""
        print("\n" + "="*80)
        print("1. INFORMACIÓN BÁSICA DEL DATASET")
        print("="*80)

        print(f"\n📊 Dimensiones: {self.df.shape[0]:,} filas x {self.df.shape[1]} columnas")
        print(f"💾 Memoria utilizada: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

        print("\n📋 Tipos de datos:")
        print(self.df.dtypes.value_counts())

        print("\n🔍 Primeras 3 filas del dataset:")
        print(self.df.head(3).to_string())

        return self.df.info()

    def check_missing_values(self):
        """Análisis de valores faltantes"""
        print("\n" + "="*80)
        print("2. ANÁLISIS DE VALORES FALTANTES")
        print("="*80)

        missing_stats = pd.DataFrame({
            'Missing_Count': self.df.isnull().sum(),
            'Missing_Percentage': (self.df.isnull().sum() / len(self.df) * 100).round(2),
            'Non_Null_Count': self.df.notnull().sum(),
            'Data_Type': self.df.dtypes
        }).sort_values('Missing_Count', ascending=False)

        print("\n📉 Resumen de valores faltantes:")
        print(missing_stats)

        total_missing = missing_stats['Missing_Count'].sum()
        if total_missing == 0:
            print("\n✅ ¡Excelente! No se encontraron valores faltantes en el dataset.")
        else:
            print(f"\n⚠️  Se encontraron {total_missing:,} valores faltantes en total.")

        return missing_stats

    def check_duplicates(self):
        """Análisis de duplicados"""
        print("\n" + "="*80)
        print("3. ANÁLISIS DE DUPLICADOS")
        print("="*80)

        # Duplicados completos
        duplicates_all = self.df.duplicated().sum()
        print(f"\n🔍 Filas completamente duplicadas: {duplicates_all}")

        # Duplicados por UID (identificador de usuario)
        if 'uid' in self.df.columns:
            duplicates_uid = self.df['uid'].duplicated().sum()
            print(f"🔍 UIDs duplicados: {duplicates_uid}")

            if duplicates_uid > 0:
                print("\n⚠️  UIDs que aparecen más de una vez:")
                duplicate_uids = self.df[self.df['uid'].duplicated(keep=False)]['uid'].value_counts()
                print(duplicate_uids.head(10))

        if duplicates_all == 0 and duplicates_uid == 0:
            print("\n✅ ¡Excelente! No se encontraron duplicados.")

        return {'duplicates_all': duplicates_all, 'duplicates_uid': duplicates_uid}

    def check_data_types_consistency(self):
        """Verifica consistencia de tipos de datos"""
        print("\n" + "="*80)
        print("4. CONSISTENCIA DE TIPOS DE DATOS")
        print("="*80)

        inconsistencies = []

        # Verificar variables numéricas
        numeric_cols = ['total_orders', 'total_orders_tmenos1', 'delta_orders', 'efo_to_four']
        print("\n🔢 Variables numéricas:")
        for col in numeric_cols:
            if col in self.df.columns:
                print(f"\n  {col}:")
                print(f"    - Tipo: {self.df[col].dtype}")
                print(f"    - Rango: [{self.df[col].min()}, {self.df[col].max()}]")

                # Verificar si hay valores negativos donde no deberían
                if col in ['total_orders', 'total_orders_tmenos1', 'efo_to_four']:
                    negative_count = (self.df[col] < 0).sum()
                    if negative_count > 0:
                        inconsistencies.append(f"{col} tiene {negative_count} valores negativos")
                        print(f"    ⚠️  {negative_count} valores negativos detectados!")

        # Verificar variables categóricas
        categorical_cols = ['country_code', 'categoria_recencia', 'city_token', 'r_segment']
        print("\n\n📊 Variables categóricas:")
        for col in categorical_cols:
            if col in self.df.columns:
                unique_count = self.df[col].nunique()
                print(f"\n  {col}:")
                print(f"    - Valores únicos: {unique_count}")
                print(f"    - Distribución:")
                print(self.df[col].value_counts().head(10).to_string())

        # Verificar fechas
        date_cols = ['first_order_date', 'fourth_order_date']
        print("\n\n📅 Variables de fecha:")
        for col in date_cols:
            if col in self.df.columns:
                print(f"\n  {col}:")
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    print(f"    - Rango: {self.df[col].min()} a {self.df[col].max()}")
                    print(f"    - Tipo: {self.df[col].dtype}")
                except Exception as e:
                    inconsistencies.append(f"{col} no se puede convertir a fecha: {str(e)}")
                    print(f"    ⚠️  Error al convertir a fecha: {str(e)}")

        if inconsistencies:
            print("\n⚠️  Inconsistencias encontradas:")
            for inc in inconsistencies:
                print(f"  - {inc}")
        else:
            print("\n✅ Todos los tipos de datos son consistentes.")

        return inconsistencies

    def check_business_rules(self):
        """Verifica reglas de negocio"""
        print("\n" + "="*80)
        print("5. VALIDACIÓN DE REGLAS DE NEGOCIO")
        print("="*80)

        violations = []

        # Regla 1: total_orders debe ser >= 4 (usuarios que alcanzaron su cuarta orden)
        if 'total_orders' in self.df.columns:
            rule1_violations = (self.df['total_orders'] < 4).sum()
            print(f"\n📋 Regla 1: total_orders >= 4")
            print(f"   Violaciones: {rule1_violations}")
            if rule1_violations > 0:
                violations.append(f"Regla 1: {rule1_violations} usuarios con menos de 4 órdenes")
                print(f"   Distribución de usuarios con < 4 órdenes:")
                print(self.df[self.df['total_orders'] < 4]['total_orders'].value_counts())

        # Regla 2: delta_orders = total_orders - total_orders_tmenos1
        if all(col in self.df.columns for col in ['delta_orders', 'total_orders', 'total_orders_tmenos1']):
            expected_delta = self.df['total_orders'] - self.df['total_orders_tmenos1']
            rule2_violations = (self.df['delta_orders'] != expected_delta).sum()
            print(f"\n📋 Regla 2: delta_orders = total_orders - total_orders_tmenos1")
            print(f"   Violaciones: {rule2_violations}")
            if rule2_violations > 0:
                violations.append(f"Regla 2: {rule2_violations} cálculos de delta incorrectos")

        # Regla 3: fourth_order_date >= first_order_date
        if all(col in self.df.columns for col in ['first_order_date', 'fourth_order_date']):
            self.df['first_order_date'] = pd.to_datetime(self.df['first_order_date'])
            self.df['fourth_order_date'] = pd.to_datetime(self.df['fourth_order_date'])
            rule3_violations = (self.df['fourth_order_date'] < self.df['first_order_date']).sum()
            print(f"\n📋 Regla 3: fourth_order_date >= first_order_date")
            print(f"   Violaciones: {rule3_violations}")
            if rule3_violations > 0:
                violations.append(f"Regla 3: {rule3_violations} fechas inconsistentes")

        # Regla 4: efo_to_four debe ser >= 0
        if 'efo_to_four' in self.df.columns:
            rule4_violations = (self.df['efo_to_four'] < 0).sum()
            print(f"\n📋 Regla 4: efo_to_four >= 0")
            print(f"   Violaciones: {rule4_violations}")
            if rule4_violations > 0:
                violations.append(f"Regla 4: {rule4_violations} valores negativos en efo_to_four")

        if not violations:
            print("\n✅ Todas las reglas de negocio se cumplen correctamente.")
        else:
            print("\n⚠️  Violaciones de reglas de negocio:")
            for v in violations:
                print(f"  - {v}")

        return violations

    def check_outliers(self):
        """Análisis de valores atípicos en variables numéricas"""
        print("\n" + "="*80)
        print("6. ANÁLISIS DE VALORES ATÍPICOS (OUTLIERS)")
        print("="*80)

        numeric_cols = ['total_orders', 'total_orders_tmenos1', 'delta_orders', 'efo_to_four']

        outlier_summary = []

        for col in numeric_cols:
            if col in self.df.columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
                outlier_pct = (outliers / len(self.df) * 100)

                outlier_summary.append({
                    'Variable': col,
                    'Q1': Q1,
                    'Q3': Q3,
                    'IQR': IQR,
                    'Lower_Bound': lower_bound,
                    'Upper_Bound': upper_bound,
                    'Outliers_Count': outliers,
                    'Outliers_Percentage': f"{outlier_pct:.2f}%"
                })

        outlier_df = pd.DataFrame(outlier_summary)
        print("\n📊 Resumen de outliers (método IQR):")
        print(outlier_df.to_string(index=False))

        return outlier_df

    def generate_summary_report(self):
        """Genera reporte resumen de calidad de datos"""
        print("\n" + "="*80)
        print("RESUMEN EJECUTIVO - CALIDAD DE DATOS")
        print("="*80)

        summary = {
            'total_records': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().sum(),
            'duplicates': self.df.duplicated().sum(),
            'memory_mb': self.df.memory_usage(deep=True).sum() / 1024**2
        }

        print(f"""
📊 Dataset Overview:
   - Total de registros: {summary['total_records']:,}
   - Total de columnas: {summary['total_columns']}
   - Valores faltantes: {summary['missing_values']}
   - Duplicados: {summary['duplicates']}
   - Memoria utilizada: {summary['memory_mb']:.2f} MB

🎯 Estado de Calidad de Datos:
""")

        quality_score = 100
        issues = []

        if summary['missing_values'] > 0:
            quality_score -= 20
            issues.append(f"❌ {summary['missing_values']} valores faltantes")
        else:
            issues.append("✅ Sin valores faltantes")

        if summary['duplicates'] > 0:
            quality_score -= 20
            issues.append(f"❌ {summary['duplicates']} duplicados")
        else:
            issues.append("✅ Sin duplicados")

        for issue in issues:
            print(f"   {issue}")

        print(f"\n🏆 Puntuación de Calidad: {quality_score}/100")

        if quality_score == 100:
            print("   ¡Excelente! El dataset tiene una calidad óptima.")
        elif quality_score >= 80:
            print("   Buena calidad. Pocas correcciones necesarias.")
        elif quality_score >= 60:
            print("   Calidad moderada. Se requieren algunas correcciones.")
        else:
            print("   Baja calidad. Se requiere limpieza significativa.")

        return summary

    def run_full_analysis(self):
        """Ejecuta el análisis completo de calidad de datos"""
        print("\n")
        print("🚀 Iniciando análisis completo de calidad de datos...\n")

        # Ejecutar todos los análisis
        self.basic_info()
        missing_stats = self.check_missing_values()
        duplicate_stats = self.check_duplicates()
        inconsistencies = self.check_data_types_consistency()
        violations = self.check_business_rules()
        outliers = self.check_outliers()
        summary = self.generate_summary_report()

        print("\n" + "="*80)
        print("✅ Análisis de calidad de datos completado")
        print("="*80)

        return {
            'missing_stats': missing_stats,
            'duplicate_stats': duplicate_stats,
            'inconsistencies': inconsistencies,
            'violations': violations,
            'outliers': outliers,
            'summary': summary
        }


if __name__ == "__main__":
    # Ruta al dataset
    DATASET_PATH = "../dataset_protegido (1).csv"

    # Crear instancia del analizador
    analyzer = DataQualityAnalyzer(DATASET_PATH)

    # Ejecutar análisis completo
    results = analyzer.run_full_analysis()

    print("\n💡 Próximos pasos recomendados:")
    print("   1. Revisar outliers identificados y determinar si son válidos")
    print("   2. Investigar inconsistencias en reglas de negocio")
    print("   3. Proceder con análisis univariado y multivariado")
