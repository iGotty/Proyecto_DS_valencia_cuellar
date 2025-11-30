#!/usr/bin/env python3
"""
Script de entrenamiento de modelos de clasificación - Versión Mejorada
=======================================================================

Entrena Random Forest y XGBoost para clasificación de usuarios high-growth.

Métricas de evaluación (en orden de prioridad):
1. AUC-ROC (principal): Capacidad de ordenar usuarios correctamente
2. Precision@20%: Precisión al targetear el top 20% de usuarios
3. F1-Score: Balance entre precisión y recall

Cambios respecto a versión anterior:
- Solo Random Forest y XGBoost (sin LightGBM)
- Métricas alineadas con caso de uso de negocio
- Comentarios en español con narrativa de negocio
- Resumen ejecutivo con recomendaciones

Autor: Proyecto Final - MINE-4101
Fecha: Noviembre 2025
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
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score, recall_score, accuracy_score,
    classification_report, confusion_matrix, roc_curve, precision_recall_curve,
    average_precision_score
)
import xgboost as xgb

# Visualización
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# CONSTANTES DE NEGOCIO
# =============================================================================

# Umbral para definir "alto crecimiento" (documentado en ENTREGA_FINAL.md)
HIGH_GROWTH_THRESHOLD = 8

# Porcentaje para Precision@k (top 20% de usuarios a targetear)
TOP_K_PERCENT = 0.20

# Semilla para reproducibilidad
RANDOM_SEED = 42

print("="*80)
print("ENTRENAMIENTO DE MODELOS DE CLASIFICACIÓN - VERSIÓN MEJORADA")
print("="*80)
print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n📌 CONFIGURACIÓN:")
print(f"   - HIGH_GROWTH_THRESHOLD = {HIGH_GROWTH_THRESHOLD}")
print(f"   - TOP_K_PERCENT = {TOP_K_PERCENT*100:.0f}%")
print(f"   - Modelos: Random Forest, XGBoost")
print("="*80)

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
print(f"\n⚖️ Scale pos weight (para desbalance): {scale_pos_weight:.2f}")

# ============================================================================
# 2. FUNCIONES DE EVALUACIÓN
# ============================================================================

def precision_at_k(y_true, y_proba, k=TOP_K_PERCENT):
    """
    Calcula Precision@k: Si seleccionamos el top k% de usuarios según
    la probabilidad predicha, ¿qué porcentaje son realmente high-growth?

    Esta métrica es clave para el negocio porque responde:
    "Si el equipo de Engagement contacta al top 20% de usuarios recomendados,
    ¿qué tasa de acierto tendrá?"
    """
    n_top = int(len(y_true) * k)
    top_indices = np.argsort(y_proba)[-n_top:]
    return y_true.iloc[top_indices].mean() if hasattr(y_true, 'iloc') else y_true[top_indices].mean()


def evaluate_model(model, X, y, name="Model"):
    """
    Evalúa un modelo y retorna todas las métricas relevantes.

    Métricas calculadas:
    - AUC-ROC: Capacidad de ordenamiento (métrica principal)
    - F1-Score: Balance precisión-recall
    - Precision@20%: Precisión en top usuarios (caso de uso de negocio)
    """
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]

    metrics = {
        'auc_roc': roc_auc_score(y, y_proba),
        'f1': f1_score(y, y_pred),
        'precision': precision_score(y, y_pred),
        'recall': recall_score(y, y_pred),
        'accuracy': accuracy_score(y, y_pred),
        'avg_precision': average_precision_score(y, y_proba),
        'precision_at_20': precision_at_k(y, y_proba, k=TOP_K_PERCENT)
    }

    return metrics, y_pred, y_proba


def print_metrics_table(metrics, title="Métricas"):
    """Imprime una tabla formateada de métricas."""
    print(f"\n📊 {title}")
    print("="*50)
    print(f"{'Métrica':<20} {'Valor':>15}")
    print("-"*50)
    print(f"{'AUC-ROC (principal)':<20} {metrics['auc_roc']:>15.4f}")
    print(f"{'Precision@20%':<20} {metrics['precision_at_20']:>15.4f}")
    print(f"{'F1-Score':<20} {metrics['f1']:>15.4f}")
    print(f"{'Precision':<20} {metrics['precision']:>15.4f}")
    print(f"{'Recall':<20} {metrics['recall']:>15.4f}")
    print(f"{'Accuracy':<20} {metrics['accuracy']:>15.4f}")
    print("="*50)


# ============================================================================
# 3. ENTRENAR MODELOS CON GRIDSEARCH
# ============================================================================

models = {}
results = {}

# --------------------------------------------------------------------------
# 3.1 RANDOM FOREST
# --------------------------------------------------------------------------
print("\n" + "="*80)
print("2. RANDOM FOREST CLASSIFIER")
print("="*80)

# Grid de hiperparámetros (moderado para balance exploración/tiempo)
param_grid_rf = {
    'n_estimators': [100, 200],
    'max_depth': [10, 15, 20],
    'min_samples_split': [10, 20],
    'min_samples_leaf': [5, 10],
}

print("\n📋 Grid de hiperparámetros:")
for param, values in param_grid_rf.items():
    print(f"   - {param}: {values}")

total_combinations = np.prod([len(v) for v in param_grid_rf.values()])
print(f"\n🔢 Combinaciones a probar: {total_combinations}")

# Modelo base con class_weight='balanced' para manejar desbalance
rf_base = RandomForestClassifier(
    max_features='sqrt',
    class_weight='balanced',
    random_state=RANDOM_SEED,
    n_jobs=-1
)

# GridSearchCV optimizando AUC-ROC
rf_grid = GridSearchCV(
    rf_base,
    param_grid=param_grid_rf,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

print("\n⏳ Entrenando Random Forest con GridSearchCV...")
start_time = datetime.now()
rf_grid.fit(X_train, y_train)
rf_time = (datetime.now() - start_time).total_seconds()

print(f"\n✅ Random Forest entrenado en {rf_time:.1f} segundos")
print(f"\n🏆 Mejores hiperparámetros:")
for param, value in rf_grid.best_params_.items():
    print(f"   - {param}: {value}")
print(f"\n📊 Mejor AUC-ROC (5-fold CV): {rf_grid.best_score_:.4f}")

best_rf = rf_grid.best_estimator_

# Evaluar
rf_metrics_train, _, _ = evaluate_model(best_rf, X_train, y_train, "RF")
rf_metrics_val, _, _ = evaluate_model(best_rf, X_val, y_val, "RF")
rf_metrics_test, rf_pred, rf_proba = evaluate_model(best_rf, X_test, y_test, "RF")

print_metrics_table(rf_metrics_val, "Random Forest - Validation")

# Comparar train vs val para detectar overfitting
stability_rf = abs(rf_metrics_train['auc_roc'] - rf_metrics_val['auc_roc'])
print(f"\n🔎 Estabilidad (Δ train-val AUC): {stability_rf:.4f} {'✅' if stability_rf < 0.05 else '⚠️'}")

models['RandomForest'] = best_rf
results['RandomForest'] = {
    'val': rf_metrics_val,
    'test': rf_metrics_test,
    'train_time': rf_time,
    'params': rf_grid.best_params_,
    'stability': stability_rf
}

# --------------------------------------------------------------------------
# 3.2 XGBOOST
# --------------------------------------------------------------------------
print("\n" + "="*80)
print("3. XGBOOST CLASSIFIER")
print("="*80)

# Grid de hiperparámetros
param_grid_xgb = {
    'n_estimators': [100, 200],
    'max_depth': [4, 6, 8],
    'learning_rate': [0.05, 0.1],
    'subsample': [0.8, 0.9],
}

print("\n📋 Grid de hiperparámetros:")
for param, values in param_grid_xgb.items():
    print(f"   - {param}: {values}")

total_combinations_xgb = np.prod([len(v) for v in param_grid_xgb.values()])
print(f"\n🔢 Combinaciones a probar: {total_combinations_xgb}")

# Modelo base con scale_pos_weight para desbalance
xgb_base = xgb.XGBClassifier(
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    random_state=RANDOM_SEED,
    n_jobs=-1,
    eval_metric='auc',
    use_label_encoder=False
)

# GridSearchCV
xgb_grid = GridSearchCV(
    xgb_base,
    param_grid=param_grid_xgb,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

print("\n⏳ Entrenando XGBoost con GridSearchCV...")
start_time = datetime.now()
xgb_grid.fit(X_train, y_train)
xgb_time = (datetime.now() - start_time).total_seconds()

print(f"\n✅ XGBoost entrenado en {xgb_time:.1f} segundos")
print(f"\n🏆 Mejores hiperparámetros:")
for param, value in xgb_grid.best_params_.items():
    print(f"   - {param}: {value}")
print(f"\n📊 Mejor AUC-ROC (5-fold CV): {xgb_grid.best_score_:.4f}")

best_xgb = xgb_grid.best_estimator_

# Evaluar
xgb_metrics_train, _, _ = evaluate_model(best_xgb, X_train, y_train, "XGB")
xgb_metrics_val, _, _ = evaluate_model(best_xgb, X_val, y_val, "XGB")
xgb_metrics_test, xgb_pred, xgb_proba = evaluate_model(best_xgb, X_test, y_test, "XGB")

print_metrics_table(xgb_metrics_val, "XGBoost - Validation")

# Estabilidad
stability_xgb = abs(xgb_metrics_train['auc_roc'] - xgb_metrics_val['auc_roc'])
print(f"\n🔎 Estabilidad (Δ train-val AUC): {stability_xgb:.4f} {'✅' if stability_xgb < 0.05 else '⚠️'}")

models['XGBoost'] = best_xgb
results['XGBoost'] = {
    'val': xgb_metrics_val,
    'test': xgb_metrics_test,
    'train_time': xgb_time,
    'params': xgb_grid.best_params_,
    'stability': stability_xgb
}

# ============================================================================
# 4. COMPARACIÓN Y SELECCIÓN DEL MEJOR MODELO
# ============================================================================
print("\n" + "="*80)
print("4. COMPARACIÓN DE MODELOS")
print("="*80)

comparison_df = pd.DataFrame({
    'Modelo': ['RandomForest', 'XGBoost'],
    'AUC-ROC (Val)': [results['RandomForest']['val']['auc_roc'],
                      results['XGBoost']['val']['auc_roc']],
    'AUC-ROC (Test)': [results['RandomForest']['test']['auc_roc'],
                       results['XGBoost']['test']['auc_roc']],
    'F1 (Test)': [results['RandomForest']['test']['f1'],
                  results['XGBoost']['test']['f1']],
    'Precision@20% (Test)': [results['RandomForest']['test']['precision_at_20'],
                              results['XGBoost']['test']['precision_at_20']],
    'Estabilidad (Δ)': [results['RandomForest']['stability'],
                        results['XGBoost']['stability']],
    'Tiempo (s)': [results['RandomForest']['train_time'],
                   results['XGBoost']['train_time']]
})

print("\n📊 TABLA COMPARATIVA:")
print(comparison_df.to_string(index=False))

# Seleccionar mejor modelo por AUC-ROC en validación
best_model_name = max(results.keys(), key=lambda x: results[x]['val']['auc_roc'])
best_model = models[best_model_name]
best_metrics = results[best_model_name]

print(f"\n🏆 MODELO GANADOR: {best_model_name}")
print(f"\n📝 JUSTIFICACIÓN:")
print(f"   - Mejor AUC-ROC en validation: {best_metrics['val']['auc_roc']:.4f}")
print(f"   - Precision@20%: {best_metrics['val']['precision_at_20']:.4f}")
print(f"     → Si contactamos al top 20% de usuarios, ~{best_metrics['val']['precision_at_20']*100:.0f}% serán high-growth")
print(f"   - Estabilidad: Δ train-val = {best_metrics['stability']:.4f}")

# ============================================================================
# 5. EVALUACIÓN FINAL EN TEST SET
# ============================================================================
print("\n" + "="*80)
print("5. EVALUACIÓN FINAL EN TEST SET")
print("="*80)
print("⚠️ IMPORTANTE: Esta evaluación se realiza UNA SOLA VEZ en datos nunca vistos.\n")

y_test_pred = best_model.predict(X_test)
y_test_proba = best_model.predict_proba(X_test)[:, 1]

test_metrics = best_metrics['test']

print(f"{'Métrica':<20} {'Valor':>10} {'Objetivo':>12} {'Status':>8}")
print("-"*55)
print(f"{'AUC-ROC (principal)':<20} {test_metrics['auc_roc']:>10.4f} {'>0.70':>12} {'✅' if test_metrics['auc_roc'] > 0.70 else '⚠️':>8}")
print(f"{'Precision@20%':<20} {test_metrics['precision_at_20']:>10.4f} {'>0.50':>12} {'✅' if test_metrics['precision_at_20'] > 0.50 else '⚠️':>8}")
print(f"{'F1-Score':<20} {test_metrics['f1']:>10.4f} {'>0.50':>12} {'✅' if test_metrics['f1'] > 0.50 else '⚠️':>8}")
print(f"{'Precision':<20} {test_metrics['precision']:>10.4f} {'-':>12} {'-':>8}")
print(f"{'Recall':<20} {test_metrics['recall']:>10.4f} {'-':>12} {'-':>8}")
print(f"{'Accuracy':<20} {test_metrics['accuracy']:>10.4f} {'-':>12} {'-':>8}")

# Matriz de confusión
cm = confusion_matrix(y_test, y_test_pred)
print(f"\n📊 Matriz de Confusión (Test):")
print(f"              Pred: 0    Pred: 1")
print(f"   Real: 0    {cm[0,0]:>6}     {cm[0,1]:>6}")
print(f"   Real: 1    {cm[1,0]:>6}     {cm[1,1]:>6}")

# ============================================================================
# 6. FEATURE IMPORTANCE
# ============================================================================
print("\n" + "="*80)
print("6. FEATURE IMPORTANCE")
print("="*80)

importance_df = None
if hasattr(best_model, 'feature_importances_'):
    importance_df = pd.DataFrame({
        'feature': feature_cols,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n📊 TOP 15 FEATURES MÁS IMPORTANTES:")
    print(f"\n{'Rank':<6} {'Feature':<40} {'Importance':>12}")
    print("-"*60)
    for i, (_, row) in enumerate(importance_df.head(15).iterrows(), 1):
        print(f"{i:<6} {row['feature']:<40} {row['importance']:>12.4f}")

# ============================================================================
# 7. VISUALIZACIONES
# ============================================================================
print("\n" + "="*80)
print("7. GENERANDO VISUALIZACIONES")
print("="*80)

# Crear directorios
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

# ROC Curve - Ambos modelos
ax1 = axes[0]
for name, model in models.items():
    y_proba_temp = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_proba_temp)
    auc = roc_auc_score(y_test, y_proba_temp)
    ax1.plot(fpr, tpr, label=f'{name} (AUC={auc:.3f})', linewidth=2)

ax1.plot([0, 1], [0, 1], 'k--', label='Random (AUC=0.50)', linewidth=1)
ax1.set_xlabel('False Positive Rate')
ax1.set_ylabel('True Positive Rate')
ax1.set_title('Curvas ROC - Comparación de Modelos')
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)

# PR Curve - Ambos modelos
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
plt.savefig('documento/figuras/roc_pr_curves_best_model.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Guardado: documento/figuras/roc_pr_curves_best_model.png")

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
    plt.savefig('documento/figuras/feature_importance_best_model.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Guardado: documento/figuras/feature_importance_best_model.png")

# 7.4 Comparación de Modelos
print("📊 Generando comparación de modelos...")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(2)
width = 0.25

modelo_names = ['RandomForest', 'XGBoost']
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
ax.axhline(y=0.70, color='red', linestyle='--', alpha=0.5, label='Objetivo AUC')
ax.axhline(y=0.50, color='orange', linestyle='--', alpha=0.5, label='Objetivo F1/P@20')
ax.grid(True, alpha=0.3, axis='y')

# Anotaciones
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        ax.annotate(f'{bar.get_height():.3f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('documento/figuras/model_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Guardado: documento/figuras/model_comparison.png")

# ============================================================================
# 8. GUARDAR MODELO Y RESULTADOS
# ============================================================================
print("\n" + "="*80)
print("8. GUARDANDO MODELO Y RESULTADOS")
print("="*80)

# Guardar mejor modelo
model_path = 'models/best_classifier.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(best_model, f)
print(f"✅ Modelo guardado: {model_path}")

# Guardar reporte JSON
report = {
    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'mejor_modelo': best_model_name,
    'high_growth_threshold': HIGH_GROWTH_THRESHOLD,
    'top_k_percent': TOP_K_PERCENT,
    'mejores_params': best_metrics['params'],
    'metricas_validacion': {k: float(v) for k, v in best_metrics['val'].items()},
    'metricas_test': {k: float(v) for k, v in best_metrics['test'].items()},
    'comparacion': {
        name: {
            'val': {k: float(v) for k, v in res['val'].items()},
            'test': {k: float(v) for k, v in res['test'].items()},
            'train_time': res['train_time'],
            'params': res['params'],
            'stability': float(res['stability'])
        }
        for name, res in results.items()
    },
    'objetivos_cumplidos': {
        'auc_roc_070': bool(test_metrics['auc_roc'] > 0.70),
        'f1_050': bool(test_metrics['f1'] > 0.50),
        'precision_at_20_050': bool(test_metrics['precision_at_20'] > 0.50)
    },
    'dataset_sizes': {
        'train': len(X_train),
        'validation': len(X_val),
        'test': len(X_test)
    },
    'feature_count': len(feature_cols),
    'top_10_features': importance_df.head(10)['feature'].tolist() if importance_df is not None else []
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
# 9. RESUMEN EJECUTIVO
# ============================================================================
print("\n" + "="*80)
print("RESUMEN EJECUTIVO - MODELO DE CLASIFICACIÓN")
print("="*80)

print(f"""
🎯 OBJETIVO:
   Identificar usuarios con alto potencial de crecimiento (high_growth)
   para optimizar la asignación del presupuesto de Engagement.

📊 DEFINICIÓN DE HIGH-GROWTH:
   Usuario con delta_orders > {HIGH_GROWTH_THRESHOLD} (aproximadamente top 20%)
   Son usuarios que realizaron más de 8 órdenes adicionales después de su 4ta orden.

🤖 MODELO SELECCIONADO: {best_model_name}
   Se compararon Random Forest y XGBoost, seleccionando {best_model_name}
   por mejor desempeño en AUC-ROC y estabilidad.

📈 MÉTRICAS EN TEST SET (datos nunca vistos):
   - AUC-ROC: {test_metrics['auc_roc']:.4f}
     → El modelo ordena correctamente a los usuarios el {test_metrics['auc_roc']*100:.0f}% de las veces

   - Precision@20%: {test_metrics['precision_at_20']:.4f}
     → Si contactamos al top 20% de usuarios, {test_metrics['precision_at_20']*100:.0f}% serán high-growth

   - F1-Score: {test_metrics['f1']:.4f}
     → Balance entre identificar high-growth sin generar falsos positivos

⭐ TOP 5 VARIABLES MÁS IMPORTANTES:""")

if importance_df is not None:
    for i, (_, row) in enumerate(importance_df.head(5).iterrows(), 1):
        print(f"   {i}. {row['feature']} ({row['importance']:.4f})")

print(f"""
💼 IMPLICACIONES DE NEGOCIO:

   1. PRIORIZACIÓN DE RECURSOS:
      - El modelo identifica el top 20% de usuarios con mayor potencial
      - Precision@20% de {test_metrics['precision_at_20']:.1%} = lift de {test_metrics['precision_at_20']/0.20:.1f}x sobre aleatorio

   2. PERFIL DEL USUARIO HIGH-GROWTH:
      - Adopción RÁPIDA: Llegaron a su 4ta orden en pocos días
      - Alta ACTIVIDAD: Están en categorías "Activo" o "Semi-Activo"
      - EXPLORADORES: Compran en múltiples categorías y tiendas

   3. RECOMENDACIONES DE ACCIÓN:
      - ALTA PRIORIDAD (top 20%): Cupón 20% en categoría dominante
      - MEDIA PRIORIDAD (next 30%): Email de reactivación + cupón 10%
      - BAJA PRIORIDAD (bottom 50%): Comunicación genérica de bajo costo

📁 ARCHIVOS GENERADOS:
   - models/best_classifier.pkl
   - models/classification_report.json
   - models/feature_importance.csv
   - models/model_comparison.csv
   - documento/figuras/confusion_matrix.png
   - documento/figuras/roc_pr_curves_best_model.png
   - documento/figuras/feature_importance_best_model.png
   - documento/figuras/model_comparison.png
""")

print("="*80)
print("✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
print("="*80)
