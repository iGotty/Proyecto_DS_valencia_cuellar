#!/usr/bin/env python3
"""
Script para ejecutar el pipeline de preparación de datos - Versión Mejorada
============================================================================

Cambios respecto a versión anterior:
- Features NORMALIZADOS en lugar de conteos crudos (evita correlación con volumen)
- Índices de diversidad Shannon para categorías Y tiendas
- Features binarios de negocio (is_multi_category, is_multi_shop)
- Selección de 10-15 features "estrella" interpretables
- Umbral HIGH_GROWTH_THRESHOLD documentado como constante

Genera train/val/test datasets procesados listos para modelado.

Autor: Proyecto Final - MINE-4101
Fecha: Noviembre 2025
"""

# Imports
import pandas as pd
import numpy as np
import ast
import pickle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

# =============================================================================
# CONSTANTES DE NEGOCIO (DOCUMENTADAS)
# =============================================================================

# UMBRAL DE ALTO CRECIMIENTO
# Un usuario se considera "high_growth" si delta_orders > HIGH_GROWTH_THRESHOLD
# El valor 8 corresponde aproximadamente al percentil 80 de la distribución,
# es decir, el top ~20% de usuarios con mayor crecimiento.
HIGH_GROWTH_THRESHOLD = 8

# UMBRALES PARA FEATURES DE NEGOCIO
# is_multi_category = 1 si el usuario compra en >= MULTI_CATEGORY_THRESHOLD categorías
MULTI_CATEGORY_THRESHOLD = 3

# is_multi_shop = 1 si el usuario compra en >= MULTI_SHOP_THRESHOLD tiendas
MULTI_SHOP_THRESHOLD = 5

# SPLIT DE DATOS
TRAIN_SIZE = 0.60
VAL_SIZE = 0.20
TEST_SIZE = 0.20
RANDOM_SEED = 42

# Configuración
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
np.random.seed(RANDOM_SEED)

print("="*80)
print("PIPELINE DE PREPARACIÓN DE DATOS - VERSIÓN MEJORADA")
print("="*80)
print(f"📅 Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n📌 CONSTANTES DE NEGOCIO:")
print(f"   - HIGH_GROWTH_THRESHOLD = {HIGH_GROWTH_THRESHOLD} (top ~20% usuarios)")
print(f"   - MULTI_CATEGORY_THRESHOLD = {MULTI_CATEGORY_THRESHOLD}")
print(f"   - MULTI_SHOP_THRESHOLD = {MULTI_SHOP_THRESHOLD}")
print("="*80)

# ============================================================================
# 1. CARGA DE DATOS
# ============================================================================
DATASET_PATH = 'dataset_protegido (1).csv'

print(f"\n📂 Cargando dataset desde: {DATASET_PATH}")
df = pd.read_csv(DATASET_PATH)
print(f"✅ Dataset cargado: {df.shape[0]:,} filas × {df.shape[1]} columnas")

# ============================================================================
# 2. FUNCIONES AUXILIARES
# ============================================================================

def shannon_entropy(counts_dict):
    """
    Calcula el índice de Shannon (entropía) de un diccionario de conteos.

    La entropía de Shannon mide la "diversidad" o "dispersión" de las compras:
    - Entropía = 0: Usuario compra solo en 1 categoría/tienda
    - Entropía alta: Usuario distribuye compras uniformemente

    Interpretación de negocio:
    - Alta diversidad → Usuario explorador → Oportunidad de cross-sell
    - Baja diversidad → Usuario enfocado → Oportunidad de fidelización
    """
    if not isinstance(counts_dict, dict) or len(counts_dict) == 0:
        return 0.0

    total = sum(counts_dict.values())
    if total == 0:
        return 0.0

    entropy = 0
    for count in counts_dict.values():
        if count > 0:
            p = count / total
            entropy -= p * np.log(p)

    return entropy


def get_dominant_item(counts_dict):
    """Retorna el item con mayor número de órdenes."""
    if not isinstance(counts_dict, dict) or len(counts_dict) == 0:
        return 'unknown'
    return max(counts_dict, key=counts_dict.get)


def get_dominant_ratio(counts_dict):
    """Calcula el ratio de concentración en el item dominante."""
    if not isinstance(counts_dict, dict) or len(counts_dict) == 0:
        return 0.0

    total = sum(counts_dict.values())
    if total == 0:
        return 0.0

    max_count = max(counts_dict.values())
    return max_count / total


def get_brand001_ratio(brand_dict, total_orders):
    """Calcula el ratio de órdenes de brand001 (marca líder del mercado)."""
    if not isinstance(brand_dict, dict) or total_orders == 0:
        return 0.0
    return brand_dict.get('brand001', 0) / total_orders


# ============================================================================
# 3. FEATURE ENGINEERING
# ============================================================================

# 3.1 Parsear columnas diccionario
dict_columns = ['main_category_counts', 'ka_type_counts', 'shop_name_counts', 'brand_name_counts']

print("\n🔧 Parseando columnas de diccionarios...")
for col in dict_columns:
    if col in df.columns:
        try:
            df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            print(f"  ✓ {col} parseado correctamente")
        except Exception as e:
            print(f"  ✗ Error parseando {col}: {str(e)}")

# -----------------------------------------------------------------------------
# 3.2 CONTEOS BASE (solo para cálculos intermedios, NO para modelo final)
# -----------------------------------------------------------------------------
print("\n🔧 Calculando conteos base (uso interno)...")
df['_num_categories'] = df['main_category_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
df['_num_shops'] = df['shop_name_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
df['_num_brands'] = df['brand_name_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)

# -----------------------------------------------------------------------------
# 3.3 FEATURES NORMALIZADOS POR ORDEN (reemplazan conteos crudos)
# Capturan "intensidad de exploración" independiente del volumen de órdenes
# -----------------------------------------------------------------------------
print("\n🔧 Creando features NORMALIZADOS (reemplazan conteos crudos)...")

# Categorías por orden: ¿Cuántas categorías distintas usa en promedio por orden?
df['categories_per_order'] = df['_num_categories'] / df['total_orders']
print(f"  ✓ categories_per_order: exploración de categorías normalizada")

# Tiendas por orden: ¿Cuántas tiendas distintas visita en promedio por orden?
df['shops_per_order'] = df['_num_shops'] / df['total_orders']
print(f"  ✓ shops_per_order: diversidad de tiendas normalizada")

# -----------------------------------------------------------------------------
# 3.4 ÍNDICES DE DIVERSIDAD (Shannon)
# -----------------------------------------------------------------------------
print("\n🔧 Calculando índices de diversidad Shannon...")

df['category_diversity'] = df['main_category_counts'].apply(shannon_entropy)
print(f"  ✓ category_diversity: índice Shannon para categorías")

df['shop_diversity'] = df['shop_name_counts'].apply(shannon_entropy)
print(f"  ✓ shop_diversity: índice Shannon para tiendas")

# -----------------------------------------------------------------------------
# 3.5 RATIOS DE CONCENTRACIÓN
# -----------------------------------------------------------------------------
print("\n🔧 Calculando ratios de concentración...")

df['dominant_category_ratio'] = df['main_category_counts'].apply(get_dominant_ratio)
print(f"  ✓ dominant_category_ratio: concentración en categoría favorita")

df['brand001_ratio'] = df.apply(
    lambda row: get_brand001_ratio(row['brand_name_counts'], row['total_orders']),
    axis=1
)
print(f"  ✓ brand001_ratio: afinidad con marca líder")

# -----------------------------------------------------------------------------
# 3.6 FEATURES BINARIOS DE NEGOCIO
# -----------------------------------------------------------------------------
print("\n🔧 Creando features binarios de negocio...")

df['is_multi_category'] = (df['_num_categories'] >= MULTI_CATEGORY_THRESHOLD).astype(int)
pct_multi_cat = df['is_multi_category'].mean() * 100
print(f"  ✓ is_multi_category: 1 si usa >={MULTI_CATEGORY_THRESHOLD} categorías ({pct_multi_cat:.1f}% de usuarios)")

df['is_multi_shop'] = (df['_num_shops'] >= MULTI_SHOP_THRESHOLD).astype(int)
pct_multi_shop = df['is_multi_shop'].mean() * 100
print(f"  ✓ is_multi_shop: 1 si usa >={MULTI_SHOP_THRESHOLD} tiendas ({pct_multi_shop:.1f}% de usuarios)")

# -----------------------------------------------------------------------------
# 3.7 FEATURES TEMPORALES
# -----------------------------------------------------------------------------
print("\n🔧 Derivando features temporales...")

df['first_order_date'] = pd.to_datetime(df['first_order_date'])
df['fourth_order_date'] = pd.to_datetime(df['fourth_order_date'])

# Fecha de referencia para calcular recencia
REFERENCE_DATE = df['first_order_date'].max()
df['days_since_first_order'] = (REFERENCE_DATE - df['first_order_date']).dt.days
print(f"  ✓ days_since_first_order: antigüedad del usuario")
print(f"  ✓ efo_to_four: velocidad de adopción (ya existe en dataset)")

# -----------------------------------------------------------------------------
# 3.8 FEATURES DE AFINIDAD
# -----------------------------------------------------------------------------
print("\n🔧 Creando features de afinidad...")

df['dominant_category'] = df['main_category_counts'].apply(get_dominant_item)
print(f"  ✓ dominant_category: categoría preferida del usuario")

df['dominant_ka_type'] = df['ka_type_counts'].apply(get_dominant_item)
print(f"  ✓ dominant_ka_type: tipo de tienda preferido")

print("\n✅ Feature Engineering completado")

# ============================================================================
# 4. CREAR VARIABLE OBJETIVO
# ============================================================================

print("\n🎯 Creando variable objetivo...")
df['high_growth'] = (df['delta_orders'] > HIGH_GROWTH_THRESHOLD).astype(int)

# Calcular percentil real del umbral
percentil_real = (df['delta_orders'] <= HIGH_GROWTH_THRESHOLD).mean() * 100

print(f"  📌 Umbral HIGH_GROWTH_THRESHOLD = {HIGH_GROWTH_THRESHOLD}")
print(f"  📌 El umbral {HIGH_GROWTH_THRESHOLD} corresponde al percentil {percentil_real:.1f}%")
print(f"  📌 Distribución: {df['high_growth'].value_counts(normalize=True).to_dict()}")

# ============================================================================
# 5. SELECCIÓN DE FEATURES "ESTRELLA" (10-15 interpretables)
# ============================================================================

print("\n⭐ SELECCIÓN DE FEATURES ESTRELLA")
print("="*60)

# Features NUMÉRICOS (9 features)
numeric_features = [
    # VELOCIDAD (predictor #1 según EDA)
    'efo_to_four',              # Días hasta 4ta orden (CLAVE)

    # ANTIGÜEDAD
    'days_since_first_order',   # Antigüedad del usuario

    # DIVERSIDAD (normalizados - NO conteos crudos)
    'categories_per_order',     # Categorías por orden
    'shops_per_order',          # Tiendas por orden
    'category_diversity',       # Índice Shannon categorías
    'shop_diversity',           # Índice Shannon tiendas

    # CONCENTRACIÓN Y LEALTAD
    'dominant_category_ratio',  # % órdenes en categoría favorita
    'brand001_ratio',           # Afinidad con marca líder
]

# Features BINARIOS (2 features)
binary_features = [
    'is_multi_category',        # ¿Compra en 3+ categorías?
    'is_multi_shop',            # ¿Compra en 5+ tiendas?
]

# Features CATEGÓRICOS (4 features)
categorical_features = [
    'categoria_recencia',       # CLAVE: 7x impacto
    'r_segment',                # Segmentación negocio
    'city_token',               # Diferencias geográficas
    'dominant_category',        # Preferencia para personalización
]

all_features = numeric_features + binary_features + categorical_features

print(f"  - Numéricos: {len(numeric_features)}")
print(f"  - Binarios: {len(binary_features)}")
print(f"  - Categóricos: {len(categorical_features)}")
print(f"  - TOTAL pre-encoding: {len(all_features)}")

# Verificar missings
missing_in_features = df[all_features].isnull().sum()
if missing_in_features.sum() > 0:
    print(f"\n⚠️ ADVERTENCIA: Hay valores faltantes:")
    print(missing_in_features[missing_in_features > 0])
else:
    print(f"\n✅ No hay valores faltantes en features seleccionados")

# ============================================================================
# 6. ENCODING Y SCALING
# ============================================================================

# 6.1 One-Hot Encoding
print("\n🔧 Aplicando One-Hot Encoding...")

df_model = df[all_features + ['high_growth', 'delta_orders', 'uid']].copy()
df_encoded = pd.get_dummies(df_model, columns=categorical_features, drop_first=True, dtype=int)

encoded_cols = [col for col in df_encoded.columns if col not in df_model.columns]
print(f"  ✓ Encoding completado: {len(categorical_features)} categóricas → {len(encoded_cols)} dummies")

# 6.2 Scaling
print("\n🔧 Aplicando StandardScaler a variables numéricas...")

scaler = StandardScaler()
cols_to_scale = numeric_features.copy()
df_encoded[cols_to_scale] = scaler.fit_transform(df_encoded[cols_to_scale])

print(f"  ✓ Scaling completado")

# ============================================================================
# 7. SPLITTING
# ============================================================================

print("\n🔧 Realizando split estratificado...")

# Separar features y targets
feature_cols = [col for col in df_encoded.columns if col not in ['uid', 'high_growth', 'delta_orders']]
X = df_encoded[feature_cols]
y = df_encoded['high_growth']
y_regression = df_encoded['delta_orders']
uids = df_encoded['uid']

# Primer split: Train (60%) vs Temp (40%)
X_train, X_temp, y_train, y_temp, y_reg_train, y_reg_temp, uid_train, uid_temp = train_test_split(
    X, y, y_regression, uids,
    test_size=(VAL_SIZE + TEST_SIZE),
    stratify=y,
    random_state=RANDOM_SEED
)

# Segundo split: Val (50% de temp = 20%) vs Test (50% de temp = 20%)
X_val, X_test, y_val, y_test, y_reg_val, y_reg_test, uid_val, uid_test = train_test_split(
    X_temp, y_temp, y_reg_temp, uid_temp,
    test_size=0.5,
    stratify=y_temp,
    random_state=RANDOM_SEED
)

print(f"✅ Split completado:")
print(f"   - Train: {X_train.shape[0]:,} usuarios ({X_train.shape[0]/len(df)*100:.1f}%)")
print(f"   - Validation: {X_val.shape[0]:,} usuarios ({X_val.shape[0]/len(df)*100:.1f}%)")
print(f"   - Test: {X_test.shape[0]:,} usuarios ({X_test.shape[0]/len(df)*100:.1f}%)")

# Verificar preservación de distribuciones
print(f"\n📊 Verificación de estratificación (% high_growth):")
print(f"   - Original: {y.mean()*100:.2f}%")
print(f"   - Train: {y_train.mean()*100:.2f}%")
print(f"   - Validation: {y_val.mean()*100:.2f}%")
print(f"   - Test: {y_test.mean()*100:.2f}%")

# Crear DataFrames finales
train_df = X_train.copy()
train_df['high_growth'] = y_train.values
train_df['delta_orders'] = y_reg_train.values
train_df['uid'] = uid_train.values

val_df = X_val.copy()
val_df['high_growth'] = y_val.values
val_df['delta_orders'] = y_reg_val.values
val_df['uid'] = uid_val.values

test_df = X_test.copy()
test_df['high_growth'] = y_test.values
test_df['delta_orders'] = y_reg_test.values
test_df['uid'] = uid_test.values

# ============================================================================
# 8. GUARDAR DATASETS
# ============================================================================

print("\n💾 Guardando datasets procesados...")

# Crear directorios
output_dir = 'data/processed'
models_dir = 'models'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(models_dir, exist_ok=True)

# Guardar CSVs
train_df.to_csv(f'{output_dir}/train.csv', index=False)
print(f"  ✓ Train guardado: {output_dir}/train.csv")

val_df.to_csv(f'{output_dir}/val.csv', index=False)
print(f"  ✓ Validation guardado: {output_dir}/val.csv")

test_df.to_csv(f'{output_dir}/test.csv', index=False)
print(f"  ✓ Test guardado: {output_dir}/test.csv")

# Guardar pipeline
pipeline_dict = {
    'scaler': scaler,
    'numeric_features': numeric_features,
    'binary_features': binary_features,
    'categorical_features': categorical_features,
    'feature_cols': feature_cols,
    'high_growth_threshold': HIGH_GROWTH_THRESHOLD,
    'multi_category_threshold': MULTI_CATEGORY_THRESHOLD,
    'multi_shop_threshold': MULTI_SHOP_THRESHOLD,
}

with open(f'{models_dir}/feature_engineering_pipeline.pkl', 'wb') as f:
    pickle.dump(pipeline_dict, f)
print(f"  ✓ Pipeline guardado: {models_dir}/feature_engineering_pipeline.pkl")

# ============================================================================
# 9. RESUMEN FINAL
# ============================================================================

print("\n" + "="*80)
print("RESUMEN FINAL - PREPARACIÓN DE DATOS (VERSIÓN MEJORADA)")
print("="*80)

print(f"\n📊 DATASET ORIGINAL:")
print(f"   - Tamaño: {df.shape[0]:,} usuarios × {df.shape[1]} variables")

print(f"\n🎯 VARIABLE OBJETIVO:")
print(f"   - high_growth = 1 si delta_orders > {HIGH_GROWTH_THRESHOLD}")
print(f"   - Umbral corresponde al percentil {percentil_real:.1f}%")
print(f"   - {df['high_growth'].sum():,} usuarios high-growth ({df['high_growth'].mean()*100:.1f}%)")

print(f"\n⭐ FEATURES ESTRELLA (mejoras vs versión anterior):")
print(f"   ❌ ELIMINADOS: num_categories, num_shops, num_brands (conteos crudos)")
print(f"   ✅ NUEVOS: categories_per_order, shops_per_order (normalizados)")
print(f"   ✅ NUEVOS: shop_diversity, is_multi_category, is_multi_shop")

print(f"\n📊 FEATURES FINALES:")
print(f"   - Pre-encoding: {len(all_features)} features interpretables")
print(f"   - Post-encoding: {len(feature_cols)} features totales")

print(f"\n📂 DATASETS GENERADOS:")
print(f"   - Train: {train_df.shape[0]:,} usuarios ({TRAIN_SIZE*100:.0f}%)")
print(f"   - Validation: {val_df.shape[0]:,} usuarios ({VAL_SIZE*100:.0f}%)")
print(f"   - Test: {test_df.shape[0]:,} usuarios ({TEST_SIZE*100:.0f}%)")

print(f"\n✅ PREPARACIÓN COMPLETADA EXITOSAMENTE")
print("="*80)
