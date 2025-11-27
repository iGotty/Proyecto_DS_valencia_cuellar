#!/usr/bin/env python3
"""
Script para ejecutar el pipeline de preparación de datos
Genera train/val/test datasets procesados
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
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from scipy.stats import chi2_contingency
import os

# Configuración
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
np.random.seed(42)  # Reproducibilidad

print("✅ Imports completados")
print(f"📅 Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================================
# 1. CARGA DE DATOS
# ============================================================================
DATASET_PATH = 'dataset_protegido (1).csv'

print(f"\n📂 Cargando dataset desde: {DATASET_PATH}")
df = pd.read_csv(DATASET_PATH)

print(f"✅ Dataset cargado: {df.shape[0]:,} filas × {df.shape[1]} columnas")

# ============================================================================
# 2. FEATURE ENGINEERING
# ============================================================================

# 2.1 Parsear columnas diccionario
dict_columns = ['main_category_counts', 'ka_type_counts', 'shop_name_counts', 'brand_name_counts']

print("\n🔧 Parseando columnas de diccionarios...")
for col in dict_columns:
    if col in df.columns:
        try:
            df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            print(f"  ✓ {col} parseado correctamente")
        except Exception as e:
            print(f"  ✗ Error parseando {col}: {str(e)}")

# 2.2 Derivar features de afinidades

# Función para calcular índice de Shannon (diversidad)
def shannon_entropy(counts_dict):
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

# Función para obtener categoría dominante
def get_dominant_category(counts_dict):
    if not isinstance(counts_dict, dict) or len(counts_dict) == 0:
        return 'unknown'

    return max(counts_dict, key=counts_dict.get)

print("\n🔧 Derivando features de afinidades...")

df['dominant_category'] = df['main_category_counts'].apply(get_dominant_category)
df['category_diversity'] = df['main_category_counts'].apply(shannon_entropy)
df['num_categories'] = df['main_category_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
df['num_shops'] = df['shop_name_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
df['num_brands'] = df['brand_name_counts'].apply(lambda x: len(x) if isinstance(x, dict) else 0)

def get_brand001_ratio(brand_dict, total_orders):
    if not isinstance(brand_dict, dict) or total_orders == 0:
        return 0.0
    return brand_dict.get('brand001', 0) / total_orders

df['brand001_ratio'] = df.apply(lambda row: get_brand001_ratio(row['brand_name_counts'], row['total_orders']), axis=1)

print("✅ Features de afinidades creados")

# 2.3 Features temporales
print("\n🔧 Derivando features temporales...")

df['first_order_date'] = pd.to_datetime(df['first_order_date'])
df['fourth_order_date'] = pd.to_datetime(df['fourth_order_date'])

df['is_weekend_first_order'] = df['first_order_date'].dt.dayofweek.isin([5, 6]).astype(int)
df['first_order_month'] = df['first_order_date'].dt.month

reference_date = df['first_order_date'].max()
df['days_since_first_order'] = (reference_date - df['first_order_date']).dt.days

print("✅ Features temporales creados")

# 2.4 Transformaciones numéricas
print("\n🔧 Aplicando transformaciones numéricas...")

df['log_total_orders'] = np.log1p(df['total_orders'])
df['log_efo_to_four'] = np.log1p(df['efo_to_four'])
df['orders_per_day'] = df['total_orders'] / (df['days_since_first_order'] + 1)

print("✅ Transformaciones numéricas aplicadas")

# 2.5 Crear variable objetivo
print("\n🎯 Creando variable objetivo...")

THRESHOLD_HIGH_GROWTH = 8
df['high_growth'] = (df['delta_orders'] > THRESHOLD_HIGH_GROWTH).astype(int)

print(f"✅ high_growth creado (threshold: {THRESHOLD_HIGH_GROWTH} órdenes)")
print(f"   Distribución: {df['high_growth'].value_counts(normalize=True).to_dict()}")

# ============================================================================
# 3. SELECCIÓN DE FEATURES
# ============================================================================

print("\n🔧 Seleccionando features para modelado...")

# Features NUMÉRICOS
numeric_features = [
    'total_orders_tmenos1',
    'efo_to_four',
    'log_efo_to_four',
    'category_diversity',
    'num_categories',
    'num_shops',
    'num_brands',
    'brand001_ratio',
    'days_since_first_order',
    'orders_per_day',
    'first_order_month',
]

# Features CATEGÓRICOS
categorical_features = [
    'categoria_recencia',
    'city_token',
    'r_segment',
    'dominant_category',
    'is_weekend_first_order',
]

all_features = numeric_features + categorical_features

print(f"📊 Features Numéricos: {len(numeric_features)}")
print(f"📊 Features Categóricos: {len(categorical_features)}")
print(f"✅ Total de features: {len(all_features)}")

# Verificar missings
missing_in_features = df[all_features].isnull().sum()
if missing_in_features.sum() > 0:
    print(f"\n⚠️ ADVERTENCIA: Hay valores faltantes:")
    print(missing_in_features[missing_in_features > 0])
else:
    print(f"✅ No hay valores faltantes")

# ============================================================================
# 4. ENCODING Y SCALING
# ============================================================================

# 4.1 One-Hot Encoding
print("\n🔧 Aplicando One-Hot Encoding...")

encoder = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
encoded_features = encoder.fit_transform(df[categorical_features])
encoded_feature_names = encoder.get_feature_names_out(categorical_features)

df_encoded = pd.DataFrame(encoded_features, columns=encoded_feature_names, index=df.index)

print(f"✅ Encoding completado: {len(encoded_feature_names)} features")

# 4.2 Scaling
print("\n🔧 Aplicando StandardScaler...")

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[numeric_features])

df_scaled = pd.DataFrame(scaled_features, columns=numeric_features, index=df.index)

print(f"✅ Scaling completado")
print(f"   Verificación - Media de primeros 3 features: {df_scaled[numeric_features[:3]].mean().values}")
print(f"   Verificación - Std de primeros 3 features: {df_scaled[numeric_features[:3]].std().values}")

# 4.3 Combinar
print("\n🔧 Combinando features...")

df_processed = pd.concat([df_scaled, df_encoded], axis=1)
df_processed['high_growth'] = df['high_growth'].values
df_processed['delta_orders'] = df['delta_orders'].values
df_processed['uid'] = df['uid'].values

print(f"✅ Dataset procesado: {df_processed.shape}")

# ============================================================================
# 5. SPLITTING
# ============================================================================

print("\n🔧 Realizando split estratificado...")

X = df_processed.drop(['high_growth', 'delta_orders', 'uid'], axis=1)
y_classification = df_processed['high_growth']
y_regression = df_processed['delta_orders']
uids = df_processed['uid']

# Primer split: Train (60%) vs Temp (40%)
X_train, X_temp, y_class_train, y_class_temp, y_reg_train, y_reg_temp, uid_train, uid_temp = train_test_split(
    X, y_classification, y_regression, uids,
    test_size=0.4,
    stratify=y_classification,
    random_state=42
)

# Segundo split: Val (20%) vs Test (20%)
X_val, X_test, y_class_val, y_class_test, y_reg_val, y_reg_test, uid_val, uid_test = train_test_split(
    X_temp, y_class_temp, y_reg_temp, uid_temp,
    test_size=0.5,
    stratify=y_class_temp,
    random_state=42
)

print(f"✅ Split completado:")
print(f"   - Train: {X_train.shape[0]:,} usuarios ({X_train.shape[0]/len(df)*100:.1f}%)")
print(f"   - Validation: {X_val.shape[0]:,} usuarios ({X_val.shape[0]/len(df)*100:.1f}%)")
print(f"   - Test: {X_test.shape[0]:,} usuarios ({X_test.shape[0]/len(df)*100:.1f}%)")

# Crear DataFrames finales
train_df = X_train.copy()
train_df['high_growth'] = y_class_train.values
train_df['delta_orders'] = y_reg_train.values
train_df['uid'] = uid_train.values

val_df = X_val.copy()
val_df['high_growth'] = y_class_val.values
val_df['delta_orders'] = y_reg_val.values
val_df['uid'] = uid_val.values

test_df = X_test.copy()
test_df['high_growth'] = y_class_test.values
test_df['delta_orders'] = y_reg_test.values
test_df['uid'] = uid_test.values

# ============================================================================
# 6. VERIFICACIÓN DE DISTRIBUCIONES
# ============================================================================

print("\n🔍 Verificando preservación de distribuciones...")

print(f"\n📊 Distribución de high_growth:")
print(f"   - Original: {y_classification.mean()*100:.2f}%")
print(f"   - Train: {y_class_train.mean()*100:.2f}%")
print(f"   - Validation: {y_class_val.mean()*100:.2f}%")
print(f"   - Test: {y_class_test.mean()*100:.2f}%")

print(f"\n📊 Estadísticas de delta_orders:")
stats_comparison = pd.DataFrame({
    'Original': y_regression.describe(),
    'Train': y_reg_train.describe(),
    'Validation': y_reg_val.describe(),
    'Test': y_reg_test.describe()
})
print(stats_comparison)

print(f"\n✅ Distribuciones preservadas correctamente")

# ============================================================================
# 7. GUARDAR DATASETS
# ============================================================================

print("\n💾 Guardando datasets procesados...")

# Crear directorios
output_dir = 'data/processed'
os.makedirs(output_dir, exist_ok=True)

# Guardar CSVs
train_path = os.path.join(output_dir, 'train.csv')
val_path = os.path.join(output_dir, 'val.csv')
test_path = os.path.join(output_dir, 'test.csv')

train_df.to_csv(train_path, index=False)
print(f"  ✓ Train guardado: {train_path} ({train_df.shape[0]:,} × {train_df.shape[1]})")

val_df.to_csv(val_path, index=False)
print(f"  ✓ Validation guardado: {val_path} ({val_df.shape[0]:,} × {val_df.shape[1]})")

test_df.to_csv(test_path, index=False)
print(f"  ✓ Test guardado: {test_path} ({test_df.shape[0]:,} × {test_df.shape[1]})")

print(f"\n✅ Datasets guardados en: {output_dir}")

# Guardar pipeline
models_dir = 'models'
os.makedirs(models_dir, exist_ok=True)

pipeline_dict = {
    'scaler': scaler,
    'encoder': encoder,
    'numeric_features': numeric_features,
    'categorical_features': categorical_features,
    'encoded_feature_names': list(encoded_feature_names)
}

pipeline_path = os.path.join(models_dir, 'feature_engineering_pipeline.pkl')
with open(pipeline_path, 'wb') as f:
    pickle.dump(pipeline_dict, f)

print(f"✅ Pipeline guardado: {pipeline_path}")

# ============================================================================
# 8. RESUMEN FINAL
# ============================================================================

print("\n" + "="*80)
print("RESUMEN FINAL - PREPARACIÓN DE DATOS")
print("="*80)

print(f"\n📊 DATASET ORIGINAL:")
print(f"   - Tamaño: {df.shape[0]:,} usuarios × {df.shape[1]} variables")

print(f"\n🔧 FEATURE ENGINEERING:")
print(f"   - Features de afinidades: 6")
print(f"   - Features temporales: 3")
print(f"   - Transformaciones numéricas: 3")

print(f"\n📊 FEATURES FINALES:")
print(f"   - Features numéricos: {len(numeric_features)}")
print(f"   - Features categóricos: {len(categorical_features)}")
print(f"   - Features after encoding: {len(encoded_feature_names)}")
print(f"   - TOTAL: {X_train.shape[1]}")

print(f"\n🎯 VARIABLES OBJETIVO:")
print(f"   - high_growth: {y_classification.sum():,} usuarios ({y_classification.mean()*100:.1f}%)")
print(f"   - delta_orders: media {y_regression.mean():.2f}")

print(f"\n📂 DATASETS GENERADOS:")
print(f"   - Train: {train_df.shape[0]:,} usuarios")
print(f"   - Validation: {val_df.shape[0]:,} usuarios")
print(f"   - Test: {test_df.shape[0]:,} usuarios")

print(f"\n✅ PREPARACIÓN COMPLETADA EXITOSAMENTE")
print("="*80)
