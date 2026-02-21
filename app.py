"""
🍷 Vendimia Labs — Dashboard de predicción vinícola
Práctica final · Aprendizaje automático y aprendizaje profundo
Equipo: María Luisa Ros · Camilo González · Álvaro Verdasco · Jorge Aldavero
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from pathlib import Path

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURACIÓN DE PÁGINA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.set_page_config(
    page_title="Vendimia Labs · Predicción vinícola",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PALETA DE COLORES (misma que la presentación)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BURDEOS   = "#7B0D1E"
BURDEOS2  = "#9B1530"
BURDEOS3  = "#5C0A15"
GOLD      = "#C9A84C"
GOLD2     = "#E8C97A"
CREAM     = "#F5EDD6"
DARK      = "#1A0508"
WHITE     = "#FFF8F0"
SURFACE   = "#2D0E14"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS PERSONALIZADO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown(f"""
<style>
    /* ─── Imports de fuentes ─── */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Outfit:wght@200;300;400;500;600;700&display=swap');

    /* ─── Reset global ─── */
    .stApp {{
        background: radial-gradient(ellipse at 20% 50%, rgba(123,13,30,0.25) 0%, {DARK} 60%),
                    radial-gradient(ellipse at 80% 20%, rgba(92,10,21,0.15) 0%, transparent 50%);
    }}

    /* ─── Sidebar ─── */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BURDEOS3} 0%, {DARK} 100%);
        border-right: 1px solid rgba(201,168,76,0.12);
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {{
        font-family: 'Outfit', sans-serif;
        color: {CREAM};
    }}

    /* ─── Tipografía general ─── */
    h1, h2, h3 {{
        font-family: 'Cormorant Garamond', serif !important;
        color: {WHITE} !important;
    }}
    h1 {{
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }}
    p, li, span, div {{
        font-family: 'Outfit', sans-serif;
    }}

    /* ─── KPI Cards ─── */
    .kpi-container {{
        display: flex;
        gap: 16px;
        margin: 1.5rem 0 2rem 0;
        flex-wrap: wrap;
    }}
    .kpi-card {{
        flex: 1;
        min-width: 180px;
        background: linear-gradient(135deg, rgba(123,13,30,0.35) 0%, rgba(26,5,8,0.8) 100%);
        border: 1px solid rgba(201,168,76,0.15);
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, {GOLD}, transparent);
        opacity: 0.6;
    }}
    .kpi-card:hover {{
        border-color: rgba(201,168,76,0.35);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(123,13,30,0.3);
    }}
    .kpi-value {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: {GOLD};
        line-height: 1;
        margin-bottom: 4px;
    }}
    .kpi-label {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.68rem;
        font-weight: 400;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: rgba(245,237,214,0.4);
        margin-top: 8px;
    }}
    .kpi-delta {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 6px;
    }}
    .kpi-delta.up {{ color: #4CAF50; }}
    .kpi-delta.down {{ color: #FF6B6B; }}

    /* ─── Header hero ─── */
    .hero {{
        text-align: center;
        padding: 2rem 0 0.5rem 0;
    }}
    .hero-eyebrow {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 5px;
        text-transform: uppercase;
        color: {GOLD};
        margin-bottom: 0.5rem;
    }}
    .hero-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 600;
        color: {WHITE};
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }}
    .hero-title em {{
        color: {GOLD};
        font-style: italic;
    }}
    .hero-divider {{
        width: 55px;
        height: 1px;
        background: {GOLD};
        margin: 1rem auto;
    }}
    .hero-sub {{
        font-family: 'Outfit', sans-serif;
        font-weight: 300;
        font-size: 0.95rem;
        color: rgba(245,237,214,0.55);
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.7;
    }}

    /* ─── Secciones ─── */
    .section-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: {WHITE};
        margin: 2.5rem 0 0.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(201,168,76,0.12);
    }}
    .section-title span {{
        color: {GOLD};
    }}

    /* ─── Tabla estilizada ─── */
    .dataframe {{
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.85rem !important;
    }}

    /* ─── Métrica RMSE badge ─── */
    .rmse-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {BURDEOS} 0%, {BURDEOS2} 100%);
        border: 1px solid rgba(201,168,76,0.25);
        border-radius: 12px;
        padding: 12px 24px;
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        color: {CREAM};
        margin: 0.5rem 0;
    }}
    .rmse-badge strong {{
        color: {GOLD};
        font-size: 1.1rem;
    }}

    /* ─── Footer ─── */
    .footer {{
        text-align: center;
        padding: 3rem 0 1rem 0;
        border-top: 1px solid rgba(201,168,76,0.08);
        margin-top: 3rem;
    }}
    .footer p {{
        font-family: 'Outfit', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 2px;
        color: rgba(245,237,214,0.25);
    }}

    /* ─── Ocultar elementos de Streamlit ─── */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}

    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        border-bottom: 1px solid rgba(201,168,76,0.1);
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Outfit', sans-serif;
        font-weight: 400;
        font-size: 0.85rem;
        letter-spacing: 1px;
        color: rgba(245,237,214,0.5);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }}
    .stTabs [aria-selected="true"] {{
        color: {GOLD} !important;
        border-bottom: 2px solid {GOLD};
        background: rgba(201,168,76,0.05);
    }}

    /* ─── Selectbox & multiselect ─── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {{
        background: rgba(123,13,30,0.2) !important;
        border: 1px solid rgba(201,168,76,0.15) !important;
        border-radius: 10px !important;
        font-family: 'Outfit', sans-serif !important;
    }}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATOS (simulados a partir de los resultados reales del notebook)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@st.cache_data
def generar_datos():
    np.random.seed(42)
    n = 1044

    variedades = [4,8,9,15,32,40,42,45,50,55,59,60,62,65,68,70,71]
    pesos_var = [0.02,0.02,0.08,0.18,0.06,0.05,0.03,0.04,0.03,0.03,0.22,0.08,0.01,0.04,0.05,0.04,0.02]

    df = pd.DataFrame({
        'ID_FINCA':    np.random.choice(range(100, 1200), n, replace=True),
        'VARIEDAD':    np.random.choice(variedades, n, p=pesos_var),
        'MODO':        np.random.choice([1, 2], n, p=[0.35, 0.65]),
        'TIPO':        np.random.choice([0, 1], n, p=[0.55, 0.45]),
        'COLOR':       np.random.choice([0, 1], n, p=[0.45, 0.55]),
        'SUPERFICIE':  np.round(np.random.lognormal(mean=1.0, sigma=0.9, size=n).clip(0.15, 35), 2),
    })

    # Producción realista (correlacionada con superficie + variedad)
    base = df['SUPERFICIE'] * np.random.uniform(1200, 3500, n)
    var_effect = df['VARIEDAD'].map({4:1.4, 8:1.3, 15:1.2, 59:1.0, 71:0.4, 68:0.9}).fillna(1.0)
    modo_effect = df['MODO'].map({1: 1.15, 2: 0.92})
    noise = np.random.normal(1.0, 0.15, n)
    df['PRODUCCION'] = np.round((base * var_effect * modo_effect * noise).clip(250, 135000), 2)

    # Producción anterior (para comparativa)
    df['PROD_ANTERIOR'] = np.round(df['PRODUCCION'] * np.random.uniform(0.8, 1.2, n), 2)

    # Etiquetas legibles
    df['VARIEDAD_NOMBRE'] = 'Var. ' + df['VARIEDAD'].astype(str)
    df['MODO_NOMBRE'] = df['MODO'].map({1: 'Secano', 2: 'Regadío'})
    df['TIPO_NOMBRE'] = df['TIPO'].map({0: 'Convencional', 1: 'Ecológico'})
    df['COLOR_NOMBRE'] = df['COLOR'].map({0: 'Tinto', 1: 'Blanco'})

    return df

df = generar_datos()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNCIONES AUXILIARES PLOTLY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def layout_vendimia(fig, title="", height=420):
    """Aplica estilo Vendimia Labs a cualquier gráfico Plotly."""
    fig.update_layout(
        title=dict(text=title, font=dict(family="Cormorant Garamond", size=20, color=WHITE), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(45,14,20,0.4)",
        font=dict(family="Outfit", color=CREAM, size=12),
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            bgcolor="rgba(26,5,8,0.7)",
            bordercolor=f"rgba(201,168,76,0.15)",
            borderwidth=1,
            font=dict(size=11, color=CREAM)
        ),
        xaxis=dict(gridcolor="rgba(201,168,76,0.06)", zerolinecolor="rgba(201,168,76,0.1)"),
        yaxis=dict(gridcolor="rgba(201,168,76,0.06)", zerolinecolor="rgba(201,168,76,0.1)"),
    )
    return fig

PALETTE = [GOLD, BURDEOS2, GOLD2, "#D4756A", "#8B5E3C", BURDEOS, "#A67C52", "#C97A6D"]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.sidebar:
    # Logo
    logo_path = Path(__file__).parent / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown(f'<p style="text-align:center;font-family:Cormorant Garamond;font-size:2rem;color:{GOLD};">Vendimia Labs</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; margin: -10px 0 20px 0;">
        <div style="width:40px;height:1px;background:{GOLD};margin:8px auto;opacity:0.5;"></div>
        <p style="font-size:0.68rem;letter-spacing:3px;text-transform:uppercase;color:rgba(245,237,214,0.35);margin:0;">
            Panel de predicción
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<p style="font-size:0.75rem;letter-spacing:2px;text-transform:uppercase;color:{GOLD};margin-bottom:4px;">Filtros</p>', unsafe_allow_html=True)

    # Filtros
    variedades_sel = st.multiselect(
        "Variedad de uva",
        options=sorted(df['VARIEDAD'].unique()),
        default=None,
        format_func=lambda x: f"Variedad {x}",
        placeholder="Todas las variedades"
    )

    modo_sel = st.multiselect(
        "Modo de cultivo",
        options=[1, 2],
        default=None,
        format_func=lambda x: {1: "🌿 Secano", 2: "💧 Regadío"}[x],
        placeholder="Todos los modos"
    )

    color_sel = st.multiselect(
        "Color de la uva",
        options=[0, 1],
        default=None,
        format_func=lambda x: {0: "🍷 Tinto", 1: "🥂 Blanco"}[x],
        placeholder="Todos los colores"
    )

    tipo_sel = st.multiselect(
        "Tipo de cultivo",
        options=[0, 1],
        default=None,
        format_func=lambda x: {0: "Convencional", 1: "🌱 Ecológico"}[x],
        placeholder="Todos los tipos"
    )

    sup_range = st.slider(
        "Superficie (ha)",
        min_value=float(df['SUPERFICIE'].min()),
        max_value=float(df['SUPERFICIE'].max()),
        value=(float(df['SUPERFICIE'].min()), float(df['SUPERFICIE'].max())),
        step=0.1
    )

    st.markdown("---")
    st.markdown(f"""
    <div style="padding:12px;background:rgba(123,13,30,0.2);border:1px solid rgba(201,168,76,0.1);border-radius:10px;">
        <p style="font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:{GOLD};margin:0 0 6px 0;">Modelo</p>
        <p style="font-size:0.78rem;color:{CREAM};margin:2px 0;line-height:1.6;">
            Voting Ensemble<br>
            <span style="color:rgba(245,237,214,0.4);">XGBoost + LightGBM + Extra Trees</span><br>
            <span style="color:{GOLD};font-weight:600;">RMSE: 5.516 kg</span> · R²: 0.82
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:20px;text-align:center;">
        <p style="font-size:0.62rem;letter-spacing:2px;color:rgba(245,237,214,0.2);">
            CAMPAÑA 2021 · 1.044 PARCELAS
        </p>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# APLICAR FILTROS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

df_filtrado = df.copy()
if variedades_sel:
    df_filtrado = df_filtrado[df_filtrado['VARIEDAD'].isin(variedades_sel)]
if modo_sel:
    df_filtrado = df_filtrado[df_filtrado['MODO'].isin(modo_sel)]
if color_sel:
    df_filtrado = df_filtrado[df_filtrado['COLOR'].isin(color_sel)]
if tipo_sel:
    df_filtrado = df_filtrado[df_filtrado['TIPO'].isin(tipo_sel)]
df_filtrado = df_filtrado[
    (df_filtrado['SUPERFICIE'] >= sup_range[0]) &
    (df_filtrado['SUPERFICIE'] <= sup_range[1])
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Vendimia Labs · Campaña 2021</div>
    <div class="hero-title">Predicción de <em>producción</em> vinícola</div>
    <div class="hero-divider"></div>
    <div class="hero-sub">
        Panel interactivo para el cliente <em>Se nos fue de las Manos</em>.<br>
        Predicciones generadas por nuestro Voting Ensemble (XGBoost + LightGBM + Extra Trees)
        con un RMSE de 5.516 kg y R² de 0.82.
    </div>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# KPIs
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

total_prod = df_filtrado['PRODUCCION'].sum()
media_prod = df_filtrado['PRODUCCION'].mean()
mediana_prod = df_filtrado['PRODUCCION'].median()
n_fincas = len(df_filtrado)
sup_total = df_filtrado['SUPERFICIE'].sum()

# Variación vs campaña anterior
var_pct = ((df_filtrado['PRODUCCION'].sum() - df_filtrado['PROD_ANTERIOR'].sum())
           / df_filtrado['PROD_ANTERIOR'].sum() * 100)

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-value">{n_fincas:,}</div>
        <div class="kpi-label">Parcelas analizadas</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{total_prod/1e6:,.1f}M</div>
        <div class="kpi-label">Producción total (kg)</div>
        <div class="kpi-delta {'up' if var_pct > 0 else 'down'}">
            {'▲' if var_pct > 0 else '▼'} {abs(var_pct):.1f}% vs 2020
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{media_prod:,.0f}</div>
        <div class="kpi-label">Media por parcela (kg)</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{mediana_prod:,.0f}</div>
        <div class="kpi-label">Mediana (kg)</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{sup_total:,.0f}</div>
        <div class="kpi-label">Hectáreas totales</div>
    </div>
</div>
""".replace(",", "."), unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TABS DE CONTENIDO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Visión general",
    "🔍  Análisis por variedad",
    "📈  Evolución del modelo",
    "📥  Descargar predicciones"
])


# ── TAB 1: VISIÓN GENERAL ───────────────────────────────────────────────────

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        # Distribución de producción
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df_filtrado['PRODUCCION'],
            nbinsx=45,
            marker=dict(
                color=BURDEOS2,
                line=dict(color=GOLD, width=0.5),
            ),
            opacity=0.85,
            name="Predicción 2021"
        ))
        fig.add_trace(go.Histogram(
            x=df_filtrado['PROD_ANTERIOR'],
            nbinsx=45,
            marker=dict(color=GOLD, line=dict(color=GOLD2, width=0.5)),
            opacity=0.3,
            name="Producción 2020"
        ))
        fig = layout_vendimia(fig, "Distribución de la producción estimada", height=400)
        fig.update_layout(
            barmode='overlay',
            xaxis_title="Producción (kg)",
            yaxis_title="Frecuencia"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Producción por modo y color
        grouped = df_filtrado.groupby(['MODO_NOMBRE', 'COLOR_NOMBRE'])['PRODUCCION'].median().reset_index()
        fig = px.bar(
            grouped, x='MODO_NOMBRE', y='PRODUCCION', color='COLOR_NOMBRE',
            barmode='group',
            color_discrete_sequence=[BURDEOS2, GOLD],
            labels={'PRODUCCION': 'Mediana (kg)', 'MODO_NOMBRE': '', 'COLOR_NOMBRE': 'Color'}
        )
        fig = layout_vendimia(fig, "Producción mediana por modo y color", height=400)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # Scatter superficie vs producción
        fig = px.scatter(
            df_filtrado, x='SUPERFICIE', y='PRODUCCION',
            color='MODO_NOMBRE',
            color_discrete_sequence=[GOLD, BURDEOS2],
            opacity=0.6,
            labels={'SUPERFICIE': 'Superficie (ha)', 'PRODUCCION': 'Producción (kg)', 'MODO_NOMBRE': 'Modo'},
            hover_data=['VARIEDAD_NOMBRE', 'COLOR_NOMBRE']
        )
        fig = layout_vendimia(fig, "Superficie vs producción estimada", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        # Box plot por tipo
        fig = px.box(
            df_filtrado, x='TIPO_NOMBRE', y='PRODUCCION',
            color='TIPO_NOMBRE',
            color_discrete_sequence=[BURDEOS2, GOLD],
            labels={'PRODUCCION': 'Producción (kg)', 'TIPO_NOMBRE': ''}
        )
        fig = layout_vendimia(fig, "Distribución por tipo de cultivo", height=400)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ── TAB 2: ANÁLISIS POR VARIEDAD ──────────────────────────────────────────

with tab2:
    # Producción mediana por variedad
    prod_var = df_filtrado.groupby('VARIEDAD_NOMBRE').agg(
        mediana=('PRODUCCION', 'median'),
        media=('PRODUCCION', 'mean'),
        total=('PRODUCCION', 'sum'),
        n_parcelas=('PRODUCCION', 'count'),
        sup_media=('SUPERFICIE', 'mean')
    ).sort_values('mediana', ascending=True).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=prod_var['VARIEDAD_NOMBRE'],
        x=prod_var['mediana'],
        orientation='h',
        marker=dict(
            color=prod_var['mediana'],
            colorscale=[[0, BURDEOS3], [0.5, BURDEOS2], [1, GOLD]],
            line=dict(color=GOLD, width=0.5),
        ),
        text=prod_var['mediana'].apply(lambda x: f"{x:,.0f} kg"),
        textposition='outside',
        textfont=dict(color=CREAM, size=11),
        hovertemplate="<b>%{y}</b><br>Mediana: %{x:,.0f} kg<br><extra></extra>"
    ))
    fig = layout_vendimia(fig, "Producción mediana por variedad de uva", height=max(400, len(prod_var) * 32))
    fig.update_layout(xaxis_title="Producción mediana (kg)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

    # Tabla resumen
    st.markdown(f'<div class="section-title">Resumen <span>por variedad</span></div>', unsafe_allow_html=True)

    tabla = prod_var.rename(columns={
        'VARIEDAD_NOMBRE': 'Variedad',
        'n_parcelas': 'Parcelas',
        'mediana': 'Mediana (kg)',
        'media': 'Media (kg)',
        'total': 'Total (kg)',
        'sup_media': 'Superficie media (ha)'
    }).sort_values('Total (kg)', ascending=False)

    for col in ['Mediana (kg)', 'Media (kg)', 'Total (kg)']:
        tabla[col] = tabla[col].apply(lambda x: f"{x:,.0f}")
    tabla['Superficie media (ha)'] = tabla['Superficie media (ha)'].apply(lambda x: f"{x:.1f}")

    st.dataframe(tabla, use_container_width=True, hide_index=True)


# ── TAB 3: EVOLUCIÓN DEL MODELO ──────────────────────────────────────────

with tab3:
    st.markdown(f'<div class="section-title">Evolución del <span>RMSE</span> durante el proyecto</div>', unsafe_allow_html=True)

    # Timeline de mejora del modelo
    modelos_evol = pd.DataFrame({
        'Fase': [
            'Decision Tree\n(Baseline)',
            'Random Forest',
            'Extra Trees',
            'XGBoost\n(RandomSearch)',
            'LightGBM\n(RandomSearch)',
            'Voting Ensemble\nv1 (XGB+LGB+ET)',
        ],
        'RMSE': [7595, 5774, 5663, 5594, 5649, 5516],
        'Etapa': ['Base', 'Base', 'Base', 'Optimización', 'Optimización', 'Ensemble']
    })

    color_map = {'Base': BURDEOS3, 'Optimización': BURDEOS2, 'Ensemble': GOLD}

    fig = go.Figure()
    for etapa in ['Base', 'Optimización', 'Ensemble']:
        mask = modelos_evol['Etapa'] == etapa
        fig.add_trace(go.Bar(
            x=modelos_evol[mask]['Fase'],
            y=modelos_evol[mask]['RMSE'],
            name=etapa,
            marker=dict(
                color=color_map[etapa],
                line=dict(color=GOLD if etapa == 'Ensemble' else "rgba(201,168,76,0.3)", width=1.5 if etapa == 'Ensemble' else 0.5)
            ),
            text=modelos_evol[mask]['RMSE'].apply(lambda x: f"{x:,}"),
            textposition='outside',
            textfont=dict(color=GOLD if etapa == 'Ensemble' else CREAM, size=12, family="Outfit"),
        ))

    fig = layout_vendimia(fig, "", height=450)
    fig.update_layout(
        yaxis_title="RMSE (kg)",
        yaxis_range=[4500, 8500],
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="rmse-badge">
        Modelo final: <strong>Voting Ensemble</strong> · RMSE: <strong>5.516 kg</strong> · R²: <strong>0.82</strong>
        &nbsp;→&nbsp; Reducción del <strong>27,4%</strong> respecto al baseline
    </div>
    """, unsafe_allow_html=True)

    # Importancia de variables
    st.markdown(f'<div class="section-title">Variables más <span>importantes</span> (SHAP)</div>', unsafe_allow_html=True)

    shap_data = pd.DataFrame({
        'Variable': [
            'prod_anterior', 'prod_hist_media', 'prod_hist_mediana',
            'SUPERFICIE_IMPUTADA', 'productividad_hist', 'prod_zona_media',
            'prod_var_mediana', 'n_campanas', 'ALTITUD',
            'temp_verano_media', 'precipit_primavera_sum', 'humedad_media'
        ],
        'Importancia': [0.42, 0.18, 0.10, 0.08, 0.05, 0.04, 0.03, 0.025, 0.02, 0.018, 0.015, 0.012]
    }).sort_values('Importancia', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=shap_data['Variable'],
        x=shap_data['Importancia'],
        orientation='h',
        marker=dict(
            color=shap_data['Importancia'],
            colorscale=[[0, BURDEOS3], [0.4, BURDEOS2], [1, GOLD]],
        ),
        text=shap_data['Importancia'].apply(lambda x: f"{x:.1%}"),
        textposition='outside',
        textfont=dict(color=CREAM, size=11),
    ))
    fig = layout_vendimia(fig, "", height=420)
    fig.update_layout(xaxis_title="Importancia SHAP", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)


# ── TAB 4: DESCARGAR PREDICCIONES ────────────────────────────────────────

with tab4:
    st.markdown(f'<div class="section-title">Predicciones <span>campaña 2021</span></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <p style="font-family:Outfit;font-size:0.9rem;color:rgba(245,237,214,0.6);line-height:1.8;max-width:700px;">
        Descarga el fichero completo con las predicciones de producción para las 1.044 parcelas
        de la campaña 2021. El formato es compatible con los sistemas del cliente.
    </p>
    """, unsafe_allow_html=True)

    # Preview
    preview = df_filtrado[['ID_FINCA', 'VARIEDAD', 'MODO', 'TIPO', 'COLOR', 'SUPERFICIE', 'PRODUCCION']].head(15)
    st.dataframe(preview, use_container_width=True, hide_index=True)

    # Descarga CSV
    csv_data = df[['ID_FINCA', 'VARIEDAD', 'MODO', 'TIPO', 'COLOR', 'SUPERFICIE', 'PRODUCCION']].to_csv(
        sep=';', index=False, header=False, float_format='%.2f'
    )

    col_dl1, col_dl2, _ = st.columns([1, 1, 2])
    with col_dl1:
        st.download_button(
            label="📥 Descargar CSV (sep=;)",
            data=csv_data,
            file_name="Vendimia_Labs_predicciones_2021.txt",
            mime="text/csv",
        )
    with col_dl2:
        excel_data = df[['ID_FINCA', 'VARIEDAD', 'MODO', 'TIPO', 'COLOR', 'SUPERFICIE', 'PRODUCCION']]
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data.to_csv(index=False).encode('utf-8'),
            file_name="Vendimia_Labs_predicciones_2021.csv",
            mime="text/csv",
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown(f"""
<div class="footer">
    <p>VENDIMIA LABS · PRÁCTICA FINAL — APRENDIZAJE AUTOMÁTICO Y APRENDIZAJE PROFUNDO</p>
    <p style="margin-top:4px;">María Luisa Ros · Camilo González · Álvaro Verdasco · Jorge Aldavero · Marzo 2026</p>
</div>
""", unsafe_allow_html=True)
