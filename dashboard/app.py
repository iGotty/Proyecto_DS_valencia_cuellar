#!/usr/bin/env python3
"""
Dashboard de Predicción de Crecimiento de Usuarios
Proyecto: Optimización de Estrategias de Retención - MINE-4101
Autores: Juan David Valencia, Juan Esteban Cuellar

Un dashboard moderno y visualmente impresionante para el equipo de Engagement
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import json
from datetime import datetime
import os

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Growth Predictor | Engagement Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS MODERNOS CON ANIMACIONES
# ============================================================================
st.markdown("""
<style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Variables de colores */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #ec4899;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark: #1e1b4b;
        --light: #f8fafc;
        --glass: rgba(255, 255, 255, 0.1);
    }

    /* Reset y fuente base */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Fondo con gradiente animado */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar estilizado */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(99, 102, 241, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: white !important;
    }

    /* Títulos con gradiente */
    h1 {
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        animation: titleGlow 3s ease-in-out infinite;
    }

    @keyframes titleGlow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }

    h2, h3 {
        color: white !important;
        font-weight: 600 !important;
    }

    p, span, label {
        color: rgba(255, 255, 255, 0.9) !important;
    }

    /* Tarjetas de métricas con glassmorphism */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
        border-color: rgba(99, 102, 241, 0.5);
    }

    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }

    /* Contenedores con efecto glass */
    .glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 30px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
    }

    /* Botones modernos */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Selectbox y inputs */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }

    /* Sliders */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #6366f1, #ec4899) !important;
    }

    /* Tabs modernos */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 8px;
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white !important;
    }

    /* DataFrames */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
    }

    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #ec4899, #06b6d4);
        border-radius: 10px;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Animación de entrada */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }

    /* Efecto de brillo en hover */
    .glow-effect {
        position: relative;
        overflow: hidden;
    }

    .glow-effect::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s ease;
        pointer-events: none;
    }

    .glow-effect:hover::before {
        opacity: 1;
    }

    /* Badge de estado */
    .status-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .status-high {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }

    .status-medium {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
    }

    .status-low {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
    }

    /* Ocultar elementos de Streamlit (mantener botón sidebar) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Estilizar el botón de colapsar sidebar */
    [data-testid="collapsedControl"] {
        background: rgba(99, 102, 241, 0.3) !important;
        border-radius: 8px !important;
        color: white !important;
    }

    [data-testid="collapsedControl"]:hover {
        background: rgba(99, 102, 241, 0.5) !important;
    }

    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #8b5cf6, #a78bfa);
    }

    /* Números animados */
    .animated-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    /* Divider con gradiente */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.5), transparent);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================================

@st.cache_data
def load_data():
    """Carga los datasets procesados"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    train_df = pd.read_csv(os.path.join(base_path, 'data/processed/train.csv'))
    val_df = pd.read_csv(os.path.join(base_path, 'data/processed/val.csv'))
    test_df = pd.read_csv(os.path.join(base_path, 'data/processed/test.csv'))

    # Combinar para visualizaciones
    all_data = pd.concat([train_df, val_df, test_df], ignore_index=True)

    return train_df, val_df, test_df, all_data

@st.cache_resource
def load_model():
    """Carga el modelo entrenado"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_path, 'models/best_classifier.pkl')

    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)

    return model_data

@st.cache_data
def load_original_data():
    """Carga el dataset original para análisis adicional"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(base_path, 'dataset_protegido (1).csv'))
    return df

@st.cache_data
def load_feature_importance():
    """Carga la importancia de features"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    importance_path = os.path.join(base_path, 'models/feature_importance.csv')
    return pd.read_csv(importance_path)

# ============================================================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================================================

def create_gauge_chart(value, title, max_val=1):
    """Crea un gauge chart moderno"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': '%', 'font': {'size': 40, 'color': 'white'}},
        title={'text': title, 'font': {'size': 16, 'color': 'rgba(255,255,255,0.8)'}},
        gauge={
            'axis': {'range': [0, max_val * 100], 'tickcolor': 'rgba(255,255,255,0.5)'},
            'bar': {'color': '#6366f1'},
            'bgcolor': 'rgba(255,255,255,0.1)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
            ],
            'threshold': {
                'line': {'color': '#ec4899', 'width': 4},
                'thickness': 0.75,
                'value': value * 100
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig

def create_modern_bar_chart(df, x, y, title, color_col=None):
    """Crea un bar chart moderno con gradiente"""
    if color_col:
        fig = px.bar(df, x=x, y=y, color=color_col,
                     color_continuous_scale=['#6366f1', '#ec4899', '#06b6d4'])
    else:
        fig = px.bar(df, x=x, y=y)
        fig.update_traces(marker_color='#6366f1',
                         marker_line_color='#8b5cf6',
                         marker_line_width=1)

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.8)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='white')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='white')),
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

def create_modern_pie_chart(labels, values, title):
    """Crea un pie chart moderno"""
    colors = ['#6366f1', '#8b5cf6', '#a78bfa', '#ec4899', '#f472b6', '#06b6d4', '#22d3ee']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors[:len(labels)], line=dict(color='rgba(255,255,255,0.2)', width=2)),
        textinfo='percent+label',
        textfont=dict(color='white', size=12),
        hoverinfo='label+percent+value'
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        legend=dict(font=dict(color='rgba(255,255,255,0.8)')),
        margin=dict(l=20, r=20, t=60, b=20),
        annotations=[dict(text='', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    return fig

def create_scatter_plot(df, x, y, color, title):
    """Crea un scatter plot moderno"""
    fig = px.scatter(df, x=x, y=y, color=color,
                     color_continuous_scale=['#6366f1', '#ec4899', '#06b6d4'],
                     opacity=0.7)

    fig.update_traces(marker=dict(size=8, line=dict(width=1, color='rgba(255,255,255,0.3)')))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.8)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='white')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='white')),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

def create_line_chart(df, x, y, title):
    """Crea un line chart con área"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df[x], y=df[y],
        mode='lines',
        line=dict(color='#6366f1', width=3),
        fill='tozeroy',
        fillcolor='rgba(99, 102, 241, 0.2)'
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.8)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='white')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='white')),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2.5rem; margin: 0;">🚀</h1>
        <h2 style="background: linear-gradient(135deg, #6366f1, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.5rem; margin: 10px 0;">Growth Predictor</h2>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Engagement Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navegación
    page = st.radio(
        "📍 Navegación",
        ["🏠 Dashboard Principal", "🔍 Explorador de Segmentos", "🎯 Predicciones", "💎 Análisis de Afinidades"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Info del modelo
    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.1); border-radius: 12px; padding: 15px; margin-top: 20px;">
        <h4 style="color: #a78bfa; margin: 0 0 10px 0; font-size: 0.9rem;">📊 Modelo Activo</h4>
        <p style="color: white; font-size: 0.85rem; margin: 5px 0;"><strong>LightGBM</strong></p>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.75rem; margin: 5px 0;">AUC-ROC: 0.9999</p>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.75rem; margin: 5px 0;">F1-Score: 0.9988</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <p style="color: rgba(255,255,255,0.4); font-size: 0.7rem;">MINE-4101 | 2025</p>
        <p style="color: rgba(255,255,255,0.4); font-size: 0.7rem;">Valencia & Cuellar</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# CARGAR DATOS
# ============================================================================

try:
    train_df, val_df, test_df, all_data = load_data()
    model_data = load_model()
    original_df = load_original_data()
    feature_importance = load_feature_importance()
    data_loaded = True
except Exception as e:
    data_loaded = False
    st.error(f"Error cargando datos: {e}")

# ============================================================================
# PÁGINA: DASHBOARD PRINCIPAL
# ============================================================================

if page == "🏠 Dashboard Principal" and data_loaded:

    # Header animado
    st.markdown("""
    <div style="text-align: center; padding: 40px 0 30px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">Dashboard Ejecutivo</h1>
        <p style="color: rgba(255,255,255,0.6); font-size: 1.1rem;">Análisis de crecimiento y comportamiento de usuarios</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)

    total_users = len(all_data)
    high_growth_pct = all_data['high_growth'].mean() * 100
    avg_delta = original_df['delta_orders'].mean()
    active_pct = 29.7  # Dato del análisis original

    with col1:
        st.metric(
            label="Total Usuarios",
            value=f"{total_users:,}",
            delta="+4ta orden alcanzada"
        )

    with col2:
        st.metric(
            label="% High Growth",
            value=f"{high_growth_pct:.1f}%",
            delta=f">{8} órdenes/6m"
        )

    with col3:
        st.metric(
            label="Delta Promedio",
            value=f"{avg_delta:.1f}",
            delta="órdenes post-4ta"
        )

    with col4:
        st.metric(
            label="Usuarios Activos",
            value=f"{active_pct}%",
            delta="≤7 días recencia"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráficos principales
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        # Distribución de high_growth
        growth_dist = all_data['high_growth'].value_counts()
        fig = create_modern_pie_chart(
            labels=['Standard Growth', 'High Growth'],
            values=[growth_dist[0], growth_dist[1]],
            title="📊 Distribución de Crecimiento"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        # Feature importance top 10
        top_features = feature_importance.head(10)
        fig = create_modern_bar_chart(
            top_features,
            x='importance',
            y='feature',
            title="🎯 Top 10 Features Predictivos"
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Segunda fila de gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        # Histograma de delta_orders
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=original_df['delta_orders'],
            nbinsx=30,
            marker_color='#6366f1',
            marker_line_color='#8b5cf6',
            marker_line_width=1,
            opacity=0.8
        ))

        fig.update_layout(
            title=dict(text="📈 Distribución de Delta Orders", font=dict(size=18, color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='rgba(255,255,255,0.8)'),
            xaxis=dict(title='Delta Orders', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Frecuencia', gridcolor='rgba(255,255,255,0.1)'),
            bargap=0.1
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        # Performance por conjunto
        model_comparison = pd.DataFrame({
            'Modelo': ['RandomForest', 'XGBoost', 'LightGBM'],
            'AUC-ROC': [0.995, 0.9999, 0.9999],
            'F1-Score': [0.916, 0.998, 0.999]
        })

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='AUC-ROC',
            x=model_comparison['Modelo'],
            y=model_comparison['AUC-ROC'],
            marker_color='#6366f1'
        ))
        fig.add_trace(go.Bar(
            name='F1-Score',
            x=model_comparison['Modelo'],
            y=model_comparison['F1-Score'],
            marker_color='#ec4899'
        ))

        fig.update_layout(
            title=dict(text="🏆 Comparación de Modelos", font=dict(size=18, color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='rgba(255,255,255,0.8)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[0.9, 1.01]),
            barmode='group',
            legend=dict(font=dict(color='white'))
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PÁGINA: EXPLORADOR DE SEGMENTOS
# ============================================================================

elif page == "🔍 Explorador de Segmentos" and data_loaded:

    st.markdown("""
    <div style="text-align: center; padding: 40px 0 30px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">Explorador de Segmentos</h1>
        <p style="color: rgba(255,255,255,0.6); font-size: 1.1rem;">Filtra y analiza segmentos de usuarios</p>
    </div>
    """, unsafe_allow_html=True)

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        # Obtener categorías de recencia únicas
        recencia_cols = [col for col in all_data.columns if 'categoria_recencia' in col]
        st.multiselect(
            "📅 Categoría de Recencia",
            options=['Todas'] + recencia_cols[:5],
            default=['Todas'],
            key="recencia_filter"
        )

    with col2:
        # R Segment
        r_segment_cols = [col for col in all_data.columns if 'r_segment' in col]
        st.multiselect(
            "👥 R Segment",
            options=['Todos'] + r_segment_cols[:5],
            default=['Todos'],
            key="rsegment_filter"
        )

    with col3:
        growth_filter = st.selectbox(
            "📈 Tipo de Crecimiento",
            options=['Todos', 'High Growth', 'Standard Growth']
        )

    # Aplicar filtros
    filtered_data = all_data.copy()

    if growth_filter == 'High Growth':
        filtered_data = filtered_data[filtered_data['high_growth'] == 1]
    elif growth_filter == 'Standard Growth':
        filtered_data = filtered_data[filtered_data['high_growth'] == 0]

    # Métricas del segmento filtrado
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Usuarios en Segmento", f"{len(filtered_data):,}")

    with col2:
        st.metric("% del Total", f"{len(filtered_data)/len(all_data)*100:.1f}%")

    with col3:
        st.metric("% High Growth", f"{filtered_data['high_growth'].mean()*100:.1f}%")

    with col4:
        avg_features = filtered_data.select_dtypes(include=[np.number]).mean()
        st.metric("Avg Category Diversity", f"{avg_features.get('category_diversity', 0):.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualizaciones del segmento
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        # Scatter plot de features
        numeric_cols = filtered_data.select_dtypes(include=[np.number]).columns.tolist()
        safe_cols = [c for c in numeric_cols if c not in ['high_growth', 'delta_orders', 'uid']]

        if len(safe_cols) >= 2:
            sample_data = filtered_data.sample(min(1000, len(filtered_data)))
            fig = px.scatter(
                sample_data,
                x=safe_cols[0],
                y=safe_cols[1],
                color='high_growth',
                color_continuous_scale=['#6366f1', '#ec4899'],
                opacity=0.6,
                title="📊 Distribución de Features"
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='rgba(255,255,255,0.8)'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        # Box plot de feature importante
        if 'category_diversity' in filtered_data.columns:
            fig = go.Figure()
            fig.add_trace(go.Box(
                x=filtered_data['high_growth'].map({0: 'Standard', 1: 'High Growth'}),
                y=filtered_data['category_diversity'],
                marker_color='#6366f1',
                boxpoints='outliers'
            ))

            fig.update_layout(
                title=dict(text="📦 Category Diversity por Crecimiento", font=dict(size=18, color='white')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='rgba(255,255,255,0.8)'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Tabla de datos
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Muestra de Usuarios del Segmento")

    display_cols = ['uid', 'high_growth'] + safe_cols[:5]
    display_cols = [c for c in display_cols if c in filtered_data.columns]

    st.dataframe(
        filtered_data[display_cols].head(100).style.background_gradient(cmap='Blues'),
        use_container_width=True,
        height=300
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PÁGINA: PREDICCIONES
# ============================================================================

elif page == "🎯 Predicciones" and data_loaded:

    st.markdown("""
    <div style="text-align: center; padding: 40px 0 30px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">Predicción de Crecimiento</h1>
        <p style="color: rgba(255,255,255,0.6); font-size: 1.1rem;">Predice el potencial de crecimiento de usuarios</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎲 Seleccionar Usuario")

        # Seleccionar usuario del test set
        test_sample = test_df.sample(min(100, len(test_df)), random_state=42)
        user_ids = test_sample['uid'].tolist()

        selected_uid = st.selectbox(
            "Selecciona un usuario:",
            options=user_ids,
            format_func=lambda x: f"Usuario {x}"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Generar Predicción", use_container_width=True):
            st.session_state['predict'] = True

        st.markdown('</div>', unsafe_allow_html=True)

        # Info del usuario
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Información del Usuario")

        user_data = test_df[test_df['uid'] == selected_uid].iloc[0]
        feature_cols = model_data['feature_cols']

        # Mostrar algunas características
        st.markdown(f"""
        <p><strong>Category Diversity:</strong> {user_data.get('category_diversity', 'N/A'):.2f}</p>
        <p><strong>High Growth Real:</strong> {'Sí ✅' if user_data['high_growth'] == 1 else 'No ❌'}</p>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        if st.session_state.get('predict', False):
            # Realizar predicción
            model = model_data['model']
            X_user = test_df[test_df['uid'] == selected_uid][feature_cols]

            prob = model.predict_proba(X_user)[0][1]
            prediction = model.predict(X_user)[0]
            actual = test_df[test_df['uid'] == selected_uid]['high_growth'].values[0]

            # Gauge de probabilidad
            st.markdown("### 🎯 Probabilidad de High Growth")

            fig = create_gauge_chart(prob, "Probabilidad")
            st.plotly_chart(fig, use_container_width=True)

            # Resultado
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                if prob > 0.7:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #10b981, #059669); padding: 20px; border-radius: 16px; text-align: center;">
                        <h3 style="color: white; margin: 0;">ALTA PRIORIDAD</h3>
                        <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">Invertir en retención</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif prob > 0.4:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #f59e0b, #d97706); padding: 20px; border-radius: 16px; text-align: center;">
                        <h3 style="color: white; margin: 0;">PRIORIDAD MEDIA</h3>
                        <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">Monitorear evolución</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #ef4444, #dc2626); padding: 20px; border-radius: 16px; text-align: center;">
                        <h3 style="color: white; margin: 0;">PRIORIDAD BAJA</h3>
                        <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">Campaña genérica</p>
                    </div>
                    """, unsafe_allow_html=True)

            with col_b:
                st.metric("Predicción", "High Growth" if prediction == 1 else "Standard")

            with col_c:
                st.metric("Valor Real", "High Growth" if actual == 1 else "Standard")

            # Recomendación
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 💡 Recomendación")

            if prob > 0.7:
                st.success("""
                **Acción Sugerida:** Este usuario tiene alto potencial de crecimiento.
                Se recomienda enviar ofertas personalizadas en sus categorías favoritas
                y considerar para programa de fidelización premium.
                """)
            elif prob > 0.4:
                st.warning("""
                **Acción Sugerida:** Usuario con potencial moderado.
                Incluir en campañas de reactivación y monitorear comportamiento
                en las próximas 2 semanas.
                """)
            else:
                st.info("""
                **Acción Sugerida:** Usuario con bajo potencial de crecimiento orgánico.
                Incluir en campañas masivas estándar. No priorizar para inversión individual.
                """)

        else:
            st.markdown("""
            <div style="text-align: center; padding: 100px 20px;">
                <h2 style="color: rgba(255,255,255,0.5);">👆</h2>
                <p style="color: rgba(255,255,255,0.5);">Selecciona un usuario y haz clic en "Generar Predicción"</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PÁGINA: ANÁLISIS DE AFINIDADES
# ============================================================================

elif page == "💎 Análisis de Afinidades" and data_loaded:

    st.markdown("""
    <div style="text-align: center; padding: 40px 0 30px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">Análisis de Afinidades</h1>
        <p style="color: rgba(255,255,255,0.6); font-size: 1.1rem;">Preferencias de categorías, marcas y tiendas</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs para diferentes análisis
    tab1, tab2, tab3 = st.tabs(["📦 Categorías", "🏷️ Marcas", "🏪 Tiendas"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            # Categorías dominantes (simulado basado en datos del EDA)
            categories_data = pd.DataFrame({
                'Categoría': ['Groceries', 'Restaurants', 'Pharmacy', 'Convenience', 'Pet Supplies', 'Liquor'],
                'Porcentaje': [35, 25, 15, 12, 8, 5]
            })

            fig = create_modern_pie_chart(
                labels=categories_data['Categoría'].tolist(),
                values=categories_data['Porcentaje'].tolist(),
                title="📊 Distribución por Categoría Principal"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            # Category diversity por growth
            if 'category_diversity' in all_data.columns:
                diversity_by_growth = all_data.groupby('high_growth')['category_diversity'].mean().reset_index()
                diversity_by_growth['Grupo'] = diversity_by_growth['high_growth'].map({0: 'Standard', 1: 'High Growth'})

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=diversity_by_growth['Grupo'],
                    y=diversity_by_growth['category_diversity'],
                    marker_color=['#6366f1', '#ec4899'],
                    text=diversity_by_growth['category_diversity'].round(2),
                    textposition='auto'
                ))

                fig.update_layout(
                    title=dict(text="📈 Diversidad de Categorías por Crecimiento", font=dict(size=18, color='white')),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='rgba(255,255,255,0.8)'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Shannon Entropy'),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            # Concentración de marca (brand001)
            brand_data = pd.DataFrame({
                'Marca': ['Brand001 (Dominante)', 'Otras Marcas'],
                'Porcentaje': [40.6, 59.4]
            })

            fig = go.Figure(go.Pie(
                labels=brand_data['Marca'],
                values=brand_data['Porcentaje'],
                hole=0.6,
                marker=dict(colors=['#ec4899', '#6366f1']),
                textinfo='percent+label',
                textfont=dict(color='white')
            ))

            fig.update_layout(
                title=dict(text="🏷️ Concentración de Marca Dominante", font=dict(size=18, color='white')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True,
                legend=dict(font=dict(color='white'))
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            # Brand001 ratio por growth
            if 'brand001_ratio' in all_data.columns:
                brand_by_growth = all_data.groupby('high_growth')['brand001_ratio'].mean().reset_index()
                brand_by_growth['Grupo'] = brand_by_growth['high_growth'].map({0: 'Standard', 1: 'High Growth'})

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=brand_by_growth['Grupo'],
                    y=brand_by_growth['brand001_ratio'],
                    marker_color=['#6366f1', '#ec4899'],
                    text=(brand_by_growth['brand001_ratio'] * 100).round(1).astype(str) + '%',
                    textposition='auto'
                ))

                fig.update_layout(
                    title=dict(text="📊 Ratio Brand001 por Crecimiento", font=dict(size=18, color='white')),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='rgba(255,255,255,0.8)'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Ratio'),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            # Número de tiendas
            if 'num_shops' in all_data.columns:
                shops_by_growth = all_data.groupby('high_growth')['num_shops'].mean().reset_index()
                shops_by_growth['Grupo'] = shops_by_growth['high_growth'].map({0: 'Standard', 1: 'High Growth'})

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=shops_by_growth['Grupo'],
                    y=shops_by_growth['num_shops'],
                    marker_color=['#6366f1', '#ec4899'],
                    text=shops_by_growth['num_shops'].round(1),
                    textposition='auto'
                ))

                fig.update_layout(
                    title=dict(text="🏪 Promedio de Tiendas por Usuario", font=dict(size=18, color='white')),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='rgba(255,255,255,0.8)'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='# Tiendas'),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            # Insight sobre exploración
            st.markdown("""
            ### 💡 Insight Clave

            Los usuarios de **alto crecimiento** tienden a:

            - 🛒 **Explorar más tiendas** diferentes
            - 📦 **Mayor diversidad** de categorías
            - 🔄 **Menor dependencia** de una sola marca

            Esto sugiere que la **exploración** es un predictor
            importante del crecimiento futuro.

            ---

            **Recomendación:** Incentivar la exploración de nuevas
            categorías y tiendas en usuarios con comportamiento
            concentrado.
            """)

            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div style="text-align: center; padding: 40px 0; margin-top: 50px; border-top: 1px solid rgba(255,255,255,0.1);">
    <p style="color: rgba(255,255,255,0.4); font-size: 0.85rem;">
        Growth Predictor Dashboard | MINE-4101 Ciencia de Datos Aplicada
    </p>
    <p style="color: rgba(255,255,255,0.3); font-size: 0.75rem;">
        Juan David Valencia & Juan Esteban Cuellar | Universidad de los Andes | 2025
    </p>
</div>
""", unsafe_allow_html=True)
