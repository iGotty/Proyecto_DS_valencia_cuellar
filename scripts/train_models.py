#!/usr/bin/env python3
"""
Script de entrenamiento de modelos de clasificación - Versión Optimizada
Entrena Random Forest, XGBoost y LightGBM SIN GridSearchCV para ejecución rápida
Usa validation set para evaluación en lugar de cross-validation
"""

# Backend no interactivo para matplotlib
import matplotlib
matplotlib.use('Agg')

import pandas as pd
import numpy as np
import pickle
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Machine Learning
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score, recall_score, accuracy_score,
    classification_report, confusion_matrix, roc_curve, precision_recall_curve,
    average_precision_score
)
import xgboost as xgb
import lightgbm as lgb

# Visualización
import matplotlib.pyplot as plt
import seaborn as sns

print("="*80)
print("ENTRENAMIENTO DE MODELOS DE CLASIFICACIÓN - VERSIÓN RÁPIDA")
print("="*80)
print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================================
# 1. CARGAR DATOS
# ============================================================================
print("\n" + "="*80)
print("1. CARGANDO DATOS")
print("="*80)

train_df = pd.read_csv('data/processed/train.csv')
val_df = pd.read_csv('data/processed/val.csv')
test_df = pd.read_csv('data/processed/test.csv')

print(f"✅ Train: {train_df.shape[0]:,} × {train_df.shape[1]}")
print(f"✅ Validation: {val_df.shape[0]:,} × {val_df.shape[1]}")
print(f"✅ Test: {test_df.shape[0]:,} × {test_df.shape[1]}")

# Separar features y target
feature_cols = [col for col in train_df.columns if col not in ['high_growth', 'delta_orders', 'uid']]

X_train = train_df[feature_cols]
y_train = train_df['high_growth']

X_val = val_df[feature_cols]
y_val = val_df['high_growth']

X_test = test_df[feature_cols]
y_test = test_df['high_growth']

print(f"\n📊 Features: {len(feature_cols)}")
print(f"📊 Distribución high_growth:")
print(f"   - Train: {y_train.mean()*100:.2f}% positivos")
print(f"   - Val: {y_val.mean()*100:.2f}% positivos")
print(f"   - Test: {y_test.mean()*100:.2f}% positivos")

# Calcular peso para desbalance
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
print(f"\n⚖️ Scale pos weight: {scale_pos_weight:.2f}")

# ============================================================================
# 2. FUNCIÓN DE EVALUACIÓN
# ============================================================================

def evaluate_model(model, X, y, name="Model"):
    """Evalúa un modelo y retorna métricas"""
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]

    metrics = {
        'auc_roc': roc_auc_score(y, y_proba),
        'f1': f1_score(y, y_pred),
        'precision': precision_score(y, y_pred),
        'recall': recall_score(y, y_pred),
        'accuracy': accuracy_score(y, y_pred),
        'avg_precision': average_precision_score(y, y_proba)
    }

    # Precision@20%
    n_top = int(len(y) * 0.2)
    top_indices = np.argsort(y_proba)[-n_top:]
    precision_at_20 = y.iloc[top_indices].mean()
    metrics['precision_at_20'] = precision_at_20

    return metrics, y_pred, y_proba

# ============================================================================
# 3. ENTRENAR MODELOS (SIN GRIDSEARCH - ENTRENAMIENTO DIRECTO)
# ============================================================================

models = {}
results = {}

# --------------------------------------------------------------------------
# 3.1 RANDOM FOREST
# --------------------------------------------------------------------------
print("\n" + "="*80)
print("2. RANDOM FOREST CLASSIFIER")
print("="*80)

print("⏳ Entrenando Random Forest (entrenamiento directo, sin GridSearch)...")
start_time = datetime.now()

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    max_features='sqrt',
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

rf_time = (datetime.now() - start_time).total_seconds()
print(f"✅ Random Forest entrenado en {rf_time:.1f} segundos")

# Evaluar
rf_metrics_val, _, _ = evaluate_model(rf_model, X_val, y_val, "RF")
rf_metrics_test, rf_pred, rf_proba = evaluate_model(rf_model, X_test, y_test, "RF")

print(f"\n📊 Métricas en Validación:")
print(f"   AUC-ROC: {rf_metrics_val['auc_roc']:.4f}")
print(f"   F1-Score: {rf_metrics_val['f1']:.4f}")
print(f"   Precision@20%: {rf_metrics_val['precision_at_20']:.4f}")

print(f"\n📊 Métricas en Test:")
print(f"   AUC-ROC: {rf_metrics_test['auc_roc']:.4f}")
print(f"   F1-Score: {rf_metrics_test['f1']:.4f}")
print(f"   Precision@20%: {rf_metrics_test['precision_at_20']:.4f}")

models['RandomForest'] = rf_model
results['RandomForest'] = {
    'val': rf_metrics_val,
    'test': rf_metrics_test,
    'train_time': rf_time,
    'params': {'n_estimators': 200, 'max_depth': 15, 'min_samples_split': 10, 'min_samples_leaf': 5}
}

# --------------------------------------------------------------------------
# 3.2 XGBOOST
# --------------------------------------------------------------------------
print("\n" + "="*80)
print("3. XGBOOST CLASSIFIER")
print("="*80)

print("⏳ Entrenando XGBoost (entrenamiento directo, sin GridSearch)...")
start_time = datetime.now()

xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    n_jobs=-1,
    eval_metric='auc'
)
xgb_model.fit(X_train, y_train)

xgb_time = (datetime.now() - start_time).total_seconds()
print(f"✅ XGBoost entrenado en {xgb_time:.1f} segundos")

# Evaluar
xgb_metrics_val, _, _ = evaluate_model(xgb_model, X_val, y_val, "XGB")
xgb_metrics_test, xgb_pred, xgb_proba = evaluate_model(xgb_model, X_test, y_test, "XGB")

print(f"\n📊 Métricas en Validación:")
print(f"   AUC-ROC: {xgb_metrics_val['auc_roc']:.4f}")
print(f"   F1-Score: {xgb_metrics_val['f1']:.4f}")
print(f"   Precision@20%: {xgb_metrics_val['precision_at_20']:.4f}")

print(f"\n📊 Métricas en Test:")
print(f"   AUC-ROC: {xgb_metrics_test['auc_roc']:.4f}")
print(f"   F1-Score: {xgb_metrics_test['f1']:.4f}")
print(f"   Precision@20%: {xgb_metrics_test['precision_at_20']:.4f}")

models['XGBoost'] = xgb_model
results['XGBoost'] = {
    'val': xgb_metrics_val,
    'test': xgb_metrics_test,
    'train_time': xgb_time,
    'params': {'n_estimators': 200, 'max_depth': 6, 'learning_rate': 0.1, 'subsample': 0.8}
}

# --------------------------------------------------------------------------
# 3.3 LIGHTGBM
# --------------------------------------------------------------------------
print("\n" + "="*80)
print("4. LIGHTGBM CLASSIFIER")
print("="*80)

print("⏳ Entrenando LightGBM (entrenamiento directo, sin GridSearch)...")
start_time = datetime.now()

lgb_model = lgb.LGBMClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    n_jobs=-1,
    verbose=-1
)
lgb_model.fit(X_train, y_train)

lgb_time = (datetime.now() - start_time).total_seconds()
print(f"✅ LightGBM entrenado en {lgb_time:.1f} segundos")

# Evaluar
lgb_metrics_val, _, _ = evaluate_model(lgb_model, X_val, y_val, "LGB")
lgb_metrics_test, lgb_pred, lgb_proba = evaluate_model(lgb_model, X_test, y_test, "LGB")

print(f"\n📊 Métricas en Validación:")
print(f"   AUC-ROC: {lgb_metrics_val['auc_roc']:.4f}")
print(f"   F1-Score: {lgb_metrics_val['f1']:.4f}")
print(f"   Precision@20%: {lgb_metrics_val['precision_at_20']:.4f}")

print(f"\n📊 Métricas en Test:")
print(f"   AUC-ROC: {lgb_metrics_test['auc_roc']:.4f}")
print(f"   F1-Score: {lgb_metrics_test['f1']:.4f}")
print(f"   Precision@20%: {lgb_metrics_test['precision_at_20']:.4f}")

models['LightGBM'] = lgb_model
results['LightGBM'] = {
    'val': lgb_metrics_val,
    'test': lgb_metrics_test,
    'train_time': lgb_time,
    'params': {'n_estimators': 200, 'max_depth': 8, 'learning_rate': 0.1, 'num_leaves': 31}
}

# ============================================================================
# 4. COMPARACIÓN Y SELECCIÓN DEL MEJOR MODELO
# ============================================================================
print("\n" + "="*80)
print("5. COMPARACIÓN DE MODELOS")
print("="*80)

comparison_df = pd.DataFrame({
    'Modelo': ['RandomForest', 'XGBoost', 'LightGBM'],
    'AUC-ROC (Val)': [results['RandomForest']['val']['auc_roc'],
                      results['XGBoost']['val']['auc_roc'],
                      results['LightGBM']['val']['auc_roc']],
    'AUC-ROC (Test)': [results['RandomForest']['test']['auc_roc'],
                       results['XGBoost']['test']['auc_roc'],
                       results['LightGBM']['test']['auc_roc']],
    'F1 (Test)': [results['RandomForest']['test']['f1'],
                  results['XGBoost']['test']['f1'],
                  results['LightGBM']['test']['f1']],
    'Precision@20% (Test)': [results['RandomForest']['test']['precision_at_20'],
                              results['XGBoost']['test']['precision_at_20'],
                              results['LightGBM']['test']['precision_at_20']],
    'Tiempo (s)': [results['RandomForest']['train_time'],
                   results['XGBoost']['train_time'],
                   results['LightGBM']['train_time']]
})

print("\n📊 Tabla Comparativa:")
print(comparison_df.to_string(index=False))

# Seleccionar mejor modelo por AUC-ROC en validación
best_model_name = max(results.keys(), key=lambda x: results[x]['val']['auc_roc'])
best_model = models[best_model_name]
best_metrics = results[best_model_name]
best_params = results[best_model_name]['params']

print(f"\n🏆 MEJOR MODELO: {best_model_name}")
print(f"   AUC-ROC (Val): {best_metrics['val']['auc_roc']:.4f}")
print(f"   AUC-ROC (Test): {best_metrics['test']['auc_roc']:.4f}")
print(f"   F1-Score (Test): {best_metrics['test']['f1']:.4f}")
print(f"   Precision@20% (Test): {best_metrics['test']['precision_at_20']:.4f}")

# Verificar objetivos
print("\n📋 VERIFICACIÓN DE OBJETIVOS:")
auc_ok = best_metrics['test']['auc_roc'] > 0.75
f1_ok = best_metrics['test']['f1'] > 0.65
prec_ok = best_metrics['test']['precision_at_20'] > 0.80

print(f"   AUC-ROC > 0.75: {'✅' if auc_ok else '⚠️'} ({best_metrics['test']['auc_roc']:.4f})")
print(f"   F1-Score > 0.65: {'✅' if f1_ok else '⚠️'} ({best_metrics['test']['f1']:.4f})")
print(f"   Precision@20% > 0.80: {'✅' if prec_ok else '⚠️'} ({best_metrics['test']['precision_at_20']:.4f})")

# ============================================================================
# 5. FEATURE IMPORTANCE
# ============================================================================
print("\n" + "="*80)
print("6. FEATURE IMPORTANCE")
print("="*80)

# Obtener importancia del mejor modelo
importance_df = None
if hasattr(best_model, 'feature_importances_'):
    importance_df = pd.DataFrame({
        'feature': feature_cols,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n📊 Top 15 Features más importantes:")
    print(importance_df.head(15).to_string(index=False))

# ============================================================================
# 6. EVALUACIÓN FINAL EN TEST SET
# ============================================================================
print("\n" + "="*80)
print("7. EVALUACIÓN FINAL EN TEST SET")
print("="*80)
print("⚠️ Esta evaluación se realiza UNA SOLA VEZ\n")

y_test_pred = best_model.predict(X_test)
y_test_proba = best_model.predict_proba(X_test)[:, 1]

# Métricas finales
test_auc = best_metrics['test']['auc_roc']
test_f1 = best_metrics['test']['f1']
test_precision = best_metrics['test']['precision']
test_recall = best_metrics['test']['recall']
test_accuracy = best_metrics['test']['accuracy']
test_p20 = best_metrics['test']['precision_at_20']

print(f"{'Métrica':<20} {'Valor':>10} {'Objetivo':>12} {'Status':>8}")
print("-"*55)
print(f"{'AUC-ROC':<20} {test_auc:>10.4f} {'>0.75':>12} {'✅' if test_auc > 0.75 else '⚠️':>8}")
print(f"{'F1-Score':<20} {test_f1:>10.4f} {'>0.65':>12} {'✅' if test_f1 > 0.65 else '⚠️':>8}")
print(f"{'Precision@20%':<20} {test_p20:>10.4f} {'>0.80':>12} {'✅' if test_p20 > 0.80 else '⚠️':>8}")
print(f"{'Precision':<20} {test_precision:>10.4f} {'-':>12} {'-':>8}")
print(f"{'Recall':<20} {test_recall:>10.4f} {'-':>12} {'-':>8}")
print(f"{'Accuracy':<20} {test_accuracy:>10.4f} {'-':>12} {'-':>8}")

# Matriz de confusión
cm = confusion_matrix(y_test, y_test_pred)
print(f"\n📊 Matriz de Confusión (Test):")
print(f"              Pred: 0    Pred: 1")
print(f"   Real: 0    {cm[0,0]:>6}     {cm[0,1]:>6}")
print(f"   Real: 1    {cm[1,0]:>6}     {cm[1,1]:>6}")

# ============================================================================
# 7. VISUALIZACIONES
# ============================================================================
print("\n" + "="*80)
print("8. GENERANDO VISUALIZACIONES")
print("="*80)

# Crear directorio
os.makedirs('documento/figuras', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Configuración de estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')

# 7.1 Matriz de Confusión
print("📊 Generando matriz de confusión...")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=['No High-Growth', 'High-Growth'],
            yticklabels=['No High-Growth', 'High-Growth'])
axes[0].set_title(f'Matriz de Confusión - {best_model_name}\n(Counts)', fontsize=12)
axes[0].set_ylabel('Valor Real')
axes[0].set_xlabel('Valor Predicho')

cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
sns.heatmap(cm_norm, annot=True, fmt='.2%', cmap='Blues', ax=axes[1],
            xticklabels=['No High-Growth', 'High-Growth'],
            yticklabels=['No High-Growth', 'High-Growth'])
axes[1].set_title(f'Matriz de Confusión - {best_model_name}\n(Normalized)', fontsize=12)
axes[1].set_ylabel('Valor Real')
axes[1].set_xlabel('Valor Predicho')

plt.tight_layout()
plt.savefig('documento/figuras/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Guardado: documento/figuras/confusion_matrix.png")

# 7.2 Curvas ROC y PR
print("📊 Generando curvas ROC y PR...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ROC Curve - Todos los modelos
ax1 = axes[0]
for name, model in models.items():
    y_proba_temp = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_proba_temp)
    auc = roc_auc_score(y_test, y_proba_temp)
    ax1.plot(fpr, tpr, label=f'{name} (AUC={auc:.3f})', linewidth=2)

ax1.plot([0, 1], [0, 1], 'k--', label='Random', linewidth=1)
ax1.set_xlabel('False Positive Rate')
ax1.set_ylabel('True Positive Rate')
ax1.set_title('Curvas ROC - Comparación de Modelos')
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)

# PR Curve - Todos los modelos
ax2 = axes[1]
for name, model in models.items():
    y_proba_temp = model.predict_proba(X_test)[:, 1]
    precision_c, recall_c, _ = precision_recall_curve(y_test, y_proba_temp)
    ap = average_precision_score(y_test, y_proba_temp)
    ax2.plot(recall_c, precision_c, label=f'{name} (AP={ap:.3f})', linewidth=2)

baseline = y_test.mean()
ax2.axhline(y=baseline, color='k', linestyle='--', label=f'Baseline ({baseline:.3f})', linewidth=1)
ax2.set_xlabel('Recall')
ax2.set_ylabel('Precision')
ax2.set_title('Curvas Precision-Recall')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('documento/figuras/roc_pr_curves.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Guardado: documento/figuras/roc_pr_curves.png")

# 7.3 Feature Importance
if importance_df is not None:
    print("📊 Generando gráfico de importancia de features...")
    fig, ax = plt.subplots(figsize=(10, 8))
    top_n = 20
    top_features = importance_df.head(top_n)
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, top_n))[::-1]
    bars = ax.barh(range(top_n), top_features['importance'].values, color=colors)
    ax.set_yticks(range(top_n))
    ax.set_yticklabels(top_features['feature'].values)
    ax.invert_yaxis()
    ax.set_xlabel('Importancia')
    ax.set_title(f'Top {top_n} Features Más Importantes - {best_model_name}')
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('documento/figuras/feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Guardado: documento/figuras/feature_importance.png")

# 7.4 Comparación de Modelos
print("📊 Generando comparación de modelos...")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(3)
width = 0.25

modelo_names = ['RandomForest', 'XGBoost', 'LightGBM']
auc_vals = [results[m]['test']['auc_roc'] for m in modelo_names]
f1_vals = [results[m]['test']['f1'] for m in modelo_names]
p20_vals = [results[m]['test']['precision_at_20'] for m in modelo_names]

bars1 = ax.bar(x - width, auc_vals, width, label='AUC-ROC', color='steelblue')
bars2 = ax.bar(x, f1_vals, width, label='F1-Score', color='coral')
bars3 = ax.bar(x + width, p20_vals, width, label='Precision@20%', color='seagreen')

ax.set_ylabel('Score')
ax.set_title('Comparación de Métricas por Modelo (Test Set)')
ax.set_xticks(x)
ax.set_xticklabels(modelo_names)
ax.legend()
ax.set_ylim(0, 1)
ax.axhline(y=0.75, color='red', linestyle='--', alpha=0.5)
ax.axhline(y=0.65, color='orange', linestyle='--', alpha=0.5)
ax.axhline(y=0.80, color='green', linestyle='--', alpha=0.5)
ax.grid(True, alpha=0.3, axis='y')

# Anotaciones
for bar in bars1:
    ax.annotate(f'{bar.get_height():.3f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax.annotate(f'{bar.get_height():.3f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                ha='center', va='bottom', fontsize=8)
for bar in bars3:
    ax.annotate(f'{bar.get_height():.3f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('documento/figuras/model_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Guardado: documento/figuras/model_comparison.png")

# ============================================================================
# 8. GUARDAR MODELO Y RESULTADOS
# ============================================================================
print("\n" + "="*80)
print("9. GUARDANDO MODELO Y RESULTADOS")
print("="*80)

# Guardar mejor modelo
model_path = 'models/best_classifier.pkl'
with open(model_path, 'wb') as f:
    pickle.dump({
        'model': best_model,
        'model_name': best_model_name,
        'feature_cols': feature_cols,
        'metrics': best_metrics,
        'params': best_params
    }, f)
print(f"✅ Modelo guardado: {model_path}")

# Guardar reporte JSON
report = {
    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'mejor_modelo': best_model_name,
    'mejores_params': best_params,
    'metricas_validacion': {k: float(v) for k, v in best_metrics['val'].items()},
    'metricas_test': {k: float(v) for k, v in best_metrics['test'].items()},
    'comparacion': {
        name: {
            'val': {k: float(v) for k, v in res['val'].items()},
            'test': {k: float(v) for k, v in res['test'].items()},
            'train_time': res['train_time'],
            'params': res['params']
        }
        for name, res in results.items()
    },
    'objetivos': {
        'auc_roc_075': bool(auc_ok),
        'f1_065': bool(f1_ok),
        'precision_at_20_080': bool(prec_ok)
    },
    'dataset_sizes': {
        'train': len(X_train),
        'validation': len(X_val),
        'test': len(X_test)
    },
    'feature_count': len(feature_cols)
}

report_path = 'models/classification_report.json'
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)
print(f"✅ Reporte guardado: {report_path}")

# Guardar feature importance
if importance_df is not None:
    importance_path = 'models/feature_importance.csv'
    importance_df.to_csv(importance_path, index=False)
    print(f"✅ Feature importance guardado: {importance_path}")

# Guardar comparación
comparison_path = 'models/model_comparison.csv'
comparison_df.to_csv(comparison_path, index=False)
print(f"✅ Comparación guardada: {comparison_path}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMEN FINAL - ENTRENAMIENTO DE MODELOS")
print("="*80)

total_time = sum([results[m]['train_time'] for m in results.keys()])
print(f"\n⏱️ TIEMPO TOTAL DE ENTRENAMIENTO: {total_time:.1f} segundos")

print(f"\n🏆 MEJOR MODELO: {best_model_name}")
print(f"\n📊 MÉTRICAS FINALES (Test Set):")
print(f"   • AUC-ROC: {best_metrics['test']['auc_roc']:.4f} {'✅' if auc_ok else '⚠️'}")
print(f"   • F1-Score: {best_metrics['test']['f1']:.4f} {'✅' if f1_ok else '⚠️'}")
print(f"   • Precision: {best_metrics['test']['precision']:.4f}")
print(f"   • Recall: {best_metrics['test']['recall']:.4f}")
print(f"   • Precision@20%: {best_metrics['test']['precision_at_20']:.4f} {'✅' if prec_ok else '⚠️'}")

print(f"\n📂 ARCHIVOS GENERADOS:")
print(f"   • models/best_classifier.pkl")
print(f"   • models/classification_report.json")
print(f"   • models/feature_importance.csv")
print(f"   • models/model_comparison.csv")
print(f"   • documento/figuras/confusion_matrix.png")
print(f"   • documento/figuras/roc_pr_curves.png")
print(f"   • documento/figuras/feature_importance.png")
print(f"   • documento/figuras/model_comparison.png")

print(f"\n✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
print("="*80)
