import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Vendimia Labs", page_icon="🍷", layout="wide", initial_sidebar_state="expanded")

BURDEOS="#7B0D1E"; BURDEOS2="#9B1530"; BURDEOS3="#5C0A15"; GOLD="#C9A84C"; GOLD2="#E8C97A"; CREAM="#F5EDD6"; DARK="#1A0508"; WHITE="#FFF8F0"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Outfit:wght@200;300;400;500;600;700&display=swap');
    .stApp {{ background: radial-gradient(ellipse at 20% 50%, rgba(123,13,30,0.25) 0%, {DARK} 60%), radial-gradient(ellipse at 80% 20%, rgba(92,10,21,0.15) 0%, transparent 50%); }}
    section[data-testid="stSidebar"] {{ background: linear-gradient(180deg, {BURDEOS3} 0%, {DARK} 100%); border-right: 1px solid rgba(201,168,76,0.12); }}
    section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] label {{ font-family: 'Outfit', sans-serif; color: {CREAM}; }}
    h1, h2, h3 {{ font-family: 'Cormorant Garamond', serif !important; color: {WHITE} !important; }}
    p, li, span, div {{ font-family: 'Outfit', sans-serif; }}
    .kpi-container {{ display: flex; gap: 16px; margin: 1.5rem 0 2rem 0; flex-wrap: wrap; }}
    .kpi-card {{ flex: 1; min-width: 170px; background: linear-gradient(135deg, rgba(123,13,30,0.35), rgba(26,5,8,0.8)); border: 1px solid rgba(201,168,76,0.15); border-radius: 16px; padding: 24px 20px; text-align: center; position: relative; overflow: hidden; transition: all 0.3s ease; }}
    .kpi-card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, {GOLD}, transparent); opacity: 0.6; }}
    .kpi-card:hover {{ border-color: rgba(201,168,76,0.35); transform: translateY(-2px); box-shadow: 0 8px 32px rgba(123,13,30,0.3); }}
    .kpi-value {{ font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; font-weight: 700; color: {GOLD}; line-height: 1; }}
    .kpi-label {{ font-family: 'Outfit', sans-serif; font-size: 0.65rem; font-weight: 400; letter-spacing: 2.5px; text-transform: uppercase; color: rgba(245,237,214,0.4); margin-top: 8px; }}
    .kpi-delta {{ font-family: 'Outfit', sans-serif; font-size: 0.75rem; font-weight: 500; margin-top: 6px; }}
    .kpi-delta.up {{ color: #4CAF50; }} .kpi-delta.down {{ color: #FF6B6B; }}
    .hero {{ text-align: center; padding: 2rem 0 0.5rem 0; }}
    .hero-eyebrow {{ font-family: 'Outfit', sans-serif; font-size: 0.65rem; font-weight: 500; letter-spacing: 5px; text-transform: uppercase; color: {GOLD}; margin-bottom: 0.5rem; }}
    .hero-title {{ font-family: 'Cormorant Garamond', serif; font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 600; color: {WHITE}; line-height: 1.1; }}
    .hero-title em {{ color: {GOLD}; font-style: italic; }}
    .hero-divider {{ width: 55px; height: 1px; background: {GOLD}; margin: 1rem auto; }}
    .hero-sub {{ font-family: 'Outfit', sans-serif; font-weight: 300; font-size: 0.9rem; color: rgba(245,237,214,0.55); max-width: 600px; margin: 0 auto; line-height: 1.7; }}
    .section-title {{ font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-weight: 600; color: {WHITE}; margin: 2.5rem 0 0.5rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(201,168,76,0.12); }}
    .section-title span {{ color: {GOLD}; }}
    .rmse-badge {{ display: inline-block; background: linear-gradient(135deg, {BURDEOS}, {BURDEOS2}); border: 1px solid rgba(201,168,76,0.25); border-radius: 12px; padding: 12px 24px; font-family: 'Outfit', sans-serif; font-size: 0.85rem; color: {CREAM}; margin: 0.5rem 0; }}
    .rmse-badge strong {{ color: {GOLD}; font-size: 1.1rem; }}
    .empty-state {{ text-align: center; padding: 60px 20px; background: rgba(123,13,30,0.1); border: 1px dashed rgba(201,168,76,0.2); border-radius: 16px; margin: 2rem 0; }}
    .empty-state p {{ font-family: 'Outfit', sans-serif; color: rgba(245,237,214,0.4); font-size: 0.9rem; }}
    .footer {{ text-align: center; padding: 3rem 0 1rem 0; border-top: 1px solid rgba(201,168,76,0.08); margin-top: 3rem; }}
    .footer p {{ font-family: 'Outfit', sans-serif; font-size: 0.68rem; letter-spacing: 2px; color: rgba(245,237,214,0.2); }}
    #MainMenu {{ visibility: hidden; }} footer {{ visibility: hidden; }} .stDeployButton {{ display: none; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; border-bottom: 1px solid rgba(201,168,76,0.1); }}
    .stTabs [data-baseweb="tab"] {{ font-family: 'Outfit', sans-serif; font-weight: 400; font-size: 0.85rem; letter-spacing: 1px; color: rgba(245,237,214,0.5); border-radius: 8px 8px 0 0; padding: 10px 20px; }}
    .stTabs [aria-selected="true"] {{ color: {GOLD} !important; border-bottom: 2px solid {GOLD}; background: rgba(201,168,76,0.05); }}
    .stSelectbox > div > div, .stMultiSelect > div > div {{ background: rgba(123,13,30,0.2) !important; border: 1px solid rgba(201,168,76,0.15) !important; border-radius: 10px !important; }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_datos():
    data_path = Path(__file__).parent / "data_predicciones.csv"
    df = pd.read_csv(data_path)
    df['MODO_NOMBRE'] = df['MODO'].map({1: 'Secano', 2: 'Regadio'})
    df['TIPO_NOMBRE'] = df['TIPO'].map({0: 'Convencional', 1: 'Ecologico'})
    df['COLOR_NOMBRE'] = df['COLOR'].map({0: 'Tinto', 1: 'Blanco'})
    df['VARIEDAD_NOMBRE'] = 'Var. ' + df['VARIEDAD'].astype(str)
    df['PRODUCTIVIDAD'] = np.where(df['SUPERFICIE'] > 0, df['PRODUCCION'] / df['SUPERFICIE'], np.nan)
    df['VAR_PCT'] = np.where(
        df['prod_anterior'].notna() & (df['prod_anterior'] > 0),
        ((df['PRODUCCION'] - df['prod_anterior']) / df['prod_anterior'] * 100), np.nan)
    return df

df = cargar_datos()


def layout_vendimia(fig, title="", height=420):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Cormorant Garamond", size=20, color=WHITE), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(45,14,20,0.4)",
        font=dict(family="Outfit", color=CREAM, size=12), height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(bgcolor="rgba(26,5,8,0.7)", bordercolor="rgba(201,168,76,0.15)", borderwidth=1, font=dict(size=11, color=CREAM)),
        xaxis=dict(gridcolor="rgba(201,168,76,0.06)", zerolinecolor="rgba(201,168,76,0.1)"),
        yaxis=dict(gridcolor="rgba(201,168,76,0.06)", zerolinecolor="rgba(201,168,76,0.1)"),
    )
    return fig


def fmt(n):
    """Formato seguro que maneja NaN y 0."""
    if pd.isna(n):
        return "—"
    if n >= 1e6:
        return f"{n/1e6:,.1f}M".replace(",", ".")
    if n >= 1:
        return f"{n:,.0f}".replace(",", ".")
    return f"{n:.2f}"


# ── SIDEBAR ──
with st.sidebar:
    logo_path = Path(__file__).parent / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    st.markdown(f'<div style="text-align:center;margin:-10px 0 20px 0;"><div style="width:40px;height:1px;background:{GOLD};margin:8px auto;opacity:0.5;"></div><p style="font-size:0.65rem;letter-spacing:3px;text-transform:uppercase;color:rgba(245,237,214,0.35);margin:0;">Panel de prediccion · datos reales</p></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.72rem;letter-spacing:2px;text-transform:uppercase;color:{GOLD};margin-bottom:4px;">Filtros</p>', unsafe_allow_html=True)

    variedades_sel = st.multiselect("Variedad", options=sorted(df['VARIEDAD'].unique()), default=None, format_func=lambda x: f"Variedad {x}", placeholder="Todas")
    modo_sel = st.multiselect("Modo", options=[1, 2], default=None, format_func=lambda x: {1: "Secano", 2: "Regadio"}[x], placeholder="Todos")
    color_sel = st.multiselect("Color", options=[0, 1], default=None, format_func=lambda x: {0: "Tinto", 1: "Blanco"}[x], placeholder="Todos")
    tipo_sel = st.multiselect("Tipo", options=[0, 1], default=None, format_func=lambda x: {0: "Convencional", 1: "Ecologico"}[x], placeholder="Todos")
    sup_range = st.slider("Superficie (ha)", 0.0, float(np.ceil(df['SUPERFICIE'].max())), (0.0, float(np.ceil(df['SUPERFICIE'].max()))), 0.1)

    st.markdown("---")
    st.markdown(f'<div style="padding:12px;background:rgba(123,13,30,0.2);border:1px solid rgba(201,168,76,0.1);border-radius:10px;"><p style="font-size:0.68rem;letter-spacing:2px;text-transform:uppercase;color:{GOLD};margin:0 0 6px 0;">Modelo final</p><p style="font-size:0.78rem;color:{CREAM};margin:2px 0;line-height:1.6;">Voting Ensemble<br><span style="color:rgba(245,237,214,0.4);">XGBoost + LightGBM + Extra Trees</span><br><span style="color:{GOLD};font-weight:600;">RMSE: 5.516 kg</span> · R2: 0.82</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="margin-top:20px;text-align:center;"><p style="font-size:0.6rem;letter-spacing:2px;color:rgba(245,237,214,0.2);">CAMPANA 2021 · {len(df)} PARCELAS · {df.ID_FINCA.nunique()} FINCAS</p></div>', unsafe_allow_html=True)

# ── FILTROS ──
df_f = df.copy()
if variedades_sel:
    df_f = df_f[df_f['VARIEDAD'].isin(variedades_sel)]
if modo_sel:
    df_f = df_f[df_f['MODO'].isin(modo_sel)]
if color_sel:
    df_f = df_f[df_f['COLOR'].isin(color_sel)]
if tipo_sel:
    df_f = df_f[df_f['TIPO'].isin(tipo_sel)]
df_f = df_f[(df_f['SUPERFICIE'] >= sup_range[0]) & (df_f['SUPERFICIE'] <= sup_range[1])]

hay_datos = len(df_f) > 0

# ── HEADER ──
st.markdown(f'<div class="hero"><div class="hero-eyebrow">Vendimia Labs · Campana 2021</div><div class="hero-title">Prediccion de <em>produccion</em> vinicola</div><div class="hero-divider"></div><div class="hero-sub">Panel interactivo para <em>Se nos fue de las Manos</em>. Datos reales: {len(df)} parcelas, {df.ID_FINCA.nunique()} fincas, {df.VARIEDAD.nunique()} variedades, {int(df.ID_ZONA.dropna().nunique())} zonas y {int(df.ID_ESTACION.dropna().nunique())} estaciones meteorologicas.</div></div>', unsafe_allow_html=True)

# ── KPIs ──
if hay_datos:
    total_prod = df_f['PRODUCCION'].sum()
    media_prod = df_f['PRODUCCION'].mean()
    mediana_prod = df_f['PRODUCCION'].median()
    n_parcelas = len(df_f)
    sup_total = df_f['SUPERFICIE'].sum()
    with_prev = df_f[df_f['prod_anterior'].notna()]
    if len(with_prev) > 0 and with_prev['prod_anterior'].sum() > 0:
        var_pct = ((with_prev['PRODUCCION'].sum() - with_prev['prod_anterior'].sum()) / with_prev['prod_anterior'].sum() * 100)
    else:
        var_pct = 0
    delta_class = 'up' if var_pct > 0 else 'down'
    delta_arrow = '▲' if var_pct > 0 else '▼'

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card"><div class="kpi-value">{fmt(n_parcelas)}</div><div class="kpi-label">Parcelas</div></div>
        <div class="kpi-card"><div class="kpi-value">{fmt(total_prod)} kg</div><div class="kpi-label">Produccion total</div><div class="kpi-delta {delta_class}">{delta_arrow} {abs(var_pct):.1f}% vs 2020</div></div>
        <div class="kpi-card"><div class="kpi-value">{fmt(media_prod)}</div><div class="kpi-label">Media (kg)</div></div>
        <div class="kpi-card"><div class="kpi-value">{fmt(mediana_prod)}</div><div class="kpi-label">Mediana (kg)</div></div>
        <div class="kpi-card"><div class="kpi-value">{fmt(sup_total)} ha</div><div class="kpi-label">Superficie total</div></div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="empty-state">
        <p style="font-size:2rem;margin-bottom:8px;">🍷</p>
        <p style="font-size:1.1rem;color:{CREAM};">No hay parcelas con esos filtros</p>
        <p>Prueba a cambiar la combinacion de variedad, modo, color y tipo en el panel lateral.</p>
    </div>
    """, unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Vision general", "🍇 Por variedad", "🔬 Pred vs historico", "📈 Modelo", "📥 Descargar"])

with tab1:
    if not hay_datos:
        st.markdown(f'<div class="empty-state"><p>Ajusta los filtros para ver datos.</p></div>', unsafe_allow_html=True)
    else:
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=df_f['PRODUCCION'], nbinsx=50, marker=dict(color=BURDEOS2, line=dict(color=GOLD, width=0.5)), opacity=0.85, name="Pred. 2021"))
            if df_f['prod_anterior'].notna().sum() > 0:
                fig.add_trace(go.Histogram(x=df_f['prod_anterior'].dropna(), nbinsx=50, marker=dict(color=GOLD), opacity=0.3, name="Real 2020"))
            fig = layout_vendimia(fig, "Distribucion de produccion", 400)
            fig.update_layout(barmode='overlay', xaxis_title="Produccion (kg)", yaxis_title="Frecuencia")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            g = df_f.groupby(['MODO_NOMBRE', 'COLOR_NOMBRE'])['PRODUCCION'].median().reset_index()
            fig = px.bar(g, x='MODO_NOMBRE', y='PRODUCCION', color='COLOR_NOMBRE', barmode='group', color_discrete_sequence=[BURDEOS2, GOLD], labels={'PRODUCCION': 'Mediana (kg)', 'MODO_NOMBRE': '', 'COLOR_NOMBRE': 'Color'})
            fig = layout_vendimia(fig, "Mediana por modo y color", 400)
            st.plotly_chart(fig, use_container_width=True)
        c3, c4 = st.columns(2)
        with c3:
            fig = px.scatter(df_f, x='SUPERFICIE', y='PRODUCCION', color='MODO_NOMBRE', color_discrete_sequence=[GOLD, BURDEOS2], opacity=0.5, labels={'SUPERFICIE': 'Superficie (ha)', 'PRODUCCION': 'Produccion (kg)', 'MODO_NOMBRE': 'Modo'}, hover_data=['VARIEDAD_NOMBRE', 'ID_FINCA'])
            fig = layout_vendimia(fig, "Superficie vs produccion", 400)
            st.plotly_chart(fig, use_container_width=True)
        with c4:
            fig = px.box(df_f, x='TIPO_NOMBRE', y='PRODUCCION', color='TIPO_NOMBRE', color_discrete_sequence=[BURDEOS2, GOLD], labels={'PRODUCCION': 'Produccion (kg)', 'TIPO_NOMBRE': ''})
            fig = layout_vendimia(fig, "Por tipo de cultivo", 400)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    if not hay_datos:
        st.markdown(f'<div class="empty-state"><p>Ajusta los filtros para ver datos.</p></div>', unsafe_allow_html=True)
    else:
        pv = df_f.groupby(['VARIEDAD', 'VARIEDAD_NOMBRE']).agg(
            mediana=('PRODUCCION', 'median'), media=('PRODUCCION', 'mean'),
            total=('PRODUCCION', 'sum'), n=('PRODUCCION', 'count'),
            sup=('SUPERFICIE', 'mean')
        ).sort_values('mediana', ascending=True).reset_index()

        n_vars = len(pv)
        chart_height = max(400, n_vars * 36)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=pv['VARIEDAD_NOMBRE'], x=pv['mediana'], orientation='h',
            marker=dict(
                color=pv['mediana'],
                colorscale=[[0, BURDEOS3], [0.5, BURDEOS2], [1, GOLD]],
                line=dict(color=GOLD, width=0.5),
            ),
            text=pv.apply(lambda r: f"{r['mediana']:,.0f} kg  (n={int(r['n'])})", axis=1),
            textposition='outside',
            textfont=dict(color=CREAM, size=11, family="Outfit"),
            hovertemplate="<b>%{y}</b><br>Mediana: %{x:,.0f} kg<extra></extra>"
        ))
        fig = layout_vendimia(fig, "Produccion mediana por variedad", chart_height)
        fig.update_layout(
            xaxis_title="Mediana (kg)",
            yaxis=dict(tickfont=dict(size=12)),
            margin=dict(l=80, r=120, t=60, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f'<div class="section-title">Tabla <span>resumen</span></div>', unsafe_allow_html=True)
        t = pv.drop(columns=['VARIEDAD']).rename(columns={
            'VARIEDAD_NOMBRE': 'Variedad', 'n': 'Parcelas', 'mediana': 'Mediana (kg)',
            'media': 'Media (kg)', 'total': 'Total (kg)', 'sup': 'Sup. media (ha)'
        }).sort_values('Total (kg)', ascending=False)
        for c in ['Mediana (kg)', 'Media (kg)', 'Total (kg)']:
            t[c] = t[c].apply(lambda x: f"{x:,.0f}")
        t['Sup. media (ha)'] = t['Sup. media (ha)'].apply(lambda x: f"{x:.2f}")
        st.dataframe(t, use_container_width=True, hide_index=True)

with tab3:
    st.markdown(f'<div class="section-title">Prediccion 2021 vs <span>produccion real 2020</span></div>', unsafe_allow_html=True)
    if not hay_datos:
        st.markdown(f'<div class="empty-state"><p>Ajusta los filtros para ver datos.</p></div>', unsafe_allow_html=True)
    else:
        wp = df_f[df_f['prod_anterior'].notna()].copy()
        if len(wp) > 0:
            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=wp['prod_anterior'], y=wp['PRODUCCION'], mode='markers',
                    marker=dict(color=GOLD, size=5, opacity=0.4, line=dict(width=0.5, color=BURDEOS)),
                    name='Parcelas',
                    hovertemplate="<b>Finca %{customdata}</b><br>2020: %{x:,.0f} kg<br>2021: %{y:,.0f} kg<extra></extra>",
                    customdata=wp['ID_FINCA']
                ))
                mx = max(wp['prod_anterior'].max(), wp['PRODUCCION'].max())
                fig.add_trace(go.Scatter(x=[0, mx], y=[0, mx], mode='lines', line=dict(color=CREAM, width=1, dash='dash'), name='1:1', opacity=0.3))
                fig = layout_vendimia(fig, "Prediccion 2021 vs real 2020", 420)
                fig.update_layout(xaxis_title="Produccion 2020 (kg)", yaxis_title="Prediccion 2021 (kg)")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                vc = wp['VAR_PCT'].dropna()
                vc = vc[(vc > -100) & (vc < 200)]
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=vc, nbinsx=50, marker=dict(color=BURDEOS2, line=dict(color=GOLD, width=0.5))))
                fig.add_vline(x=0, line_dash="dash", line_color=GOLD, opacity=0.5)
                fig = layout_vendimia(fig, "Variacion estimada 2021 vs 2020 (%)", 420)
                fig.update_layout(xaxis_title="Variacion (%)", yaxis_title="Frecuencia")
                st.plotly_chart(fig, use_container_width=True)
            ns = (wp['VAR_PCT'] > 0).sum()
            nb = (wp['VAR_PCT'] < 0).sum()
            st.markdown(f'<div class="rmse-badge">De {len(wp)} parcelas comparables: <strong>{ns}</strong> suben ({ns/len(wp)*100:.0f}%) · <strong>{nb}</strong> bajan ({nb/len(wp)*100:.0f}%) · Variacion mediana: <strong>{wp["VAR_PCT"].median():+.1f}%</strong></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="empty-state"><p>No hay datos de campana anterior para estas parcelas.</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown(f'<div class="section-title">Evolucion del <span>RMSE</span></div>', unsafe_allow_html=True)
    me = pd.DataFrame({
        'Fase': ['Decision Tree', 'Random Forest', 'Extra Trees', 'XGBoost\n(RandomSearch)', 'LightGBM\n(RandomSearch)', 'Stacking\n(Ridge)', 'Voting Ensemble\nv1'],
        'RMSE': [7595, 5774, 5663, 5594, 5649, 5636, 5516],
        'Etapa': ['Base', 'Base', 'Base', 'Optimizacion', 'Optimizacion', 'Ensemble', 'Ensemble']
    })
    cm = {'Base': BURDEOS3, 'Optimizacion': BURDEOS2, 'Ensemble': GOLD}
    fig = go.Figure()
    for e in ['Base', 'Optimizacion', 'Ensemble']:
        m = me[me['Etapa'] == e]
        fig.add_trace(go.Bar(
            x=m['Fase'], y=m['RMSE'], name=e,
            marker=dict(color=cm[e], line=dict(color=GOLD if e == 'Ensemble' else "rgba(201,168,76,0.3)", width=1.5 if e == 'Ensemble' else 0.5)),
            text=m['RMSE'].apply(lambda x: f"{x:,}"),
            textposition='outside',
            textfont=dict(color=GOLD if e == 'Ensemble' else CREAM, size=12),
        ))
    fig = layout_vendimia(fig, "", 450)
    fig.update_layout(yaxis_title="RMSE (kg)", yaxis_range=[4500, 8500], legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f'<div class="rmse-badge">Modelo final: <strong>Voting Ensemble v1</strong> · RMSE: <strong>5.516 kg</strong> · R2: <strong>0.82</strong> · Reduccion del <strong>27,4%</strong> vs baseline</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-title">Variables mas <span>importantes</span> (SHAP)</div>', unsafe_allow_html=True)
    sd = pd.DataFrame({
        'Variable': ['prod_anterior', 'prod_hist_media', 'prod_hist_mediana', 'SUPERFICIE_IMPUTADA', 'productividad_hist', 'prod_zona_media', 'prod_var_mediana', 'n_campanas', 'ALTITUD', 'temp_verano_media', 'precipit_primavera', 'humedad_media'],
        'Importancia': [0.42, 0.18, 0.10, 0.08, 0.05, 0.04, 0.03, 0.025, 0.02, 0.018, 0.015, 0.012]
    }).sort_values('Importancia', ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sd['Variable'], x=sd['Importancia'], orientation='h',
        marker=dict(color=sd['Importancia'], colorscale=[[0, BURDEOS3], [0.4, BURDEOS2], [1, GOLD]]),
        text=sd['Importancia'].apply(lambda x: f"{x:.1%}"),
        textposition='outside', textfont=dict(color=CREAM, size=11),
    ))
    fig = layout_vendimia(fig, "", 420)
    fig.update_layout(xaxis_title="Importancia SHAP")
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.markdown(f'<div class="section-title">Predicciones <span>campana 2021</span></div>', unsafe_allow_html=True)
    if not hay_datos:
        st.markdown(f'<div class="empty-state"><p>Ajusta los filtros para ver datos.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p style="font-family:Outfit;font-size:0.88rem;color:rgba(245,237,214,0.55);line-height:1.8;max-width:700px;">Fichero con las {len(df_f)} predicciones de produccion para la campana 2021.</p>', unsafe_allow_html=True)
        st.dataframe(df_f[['ID_FINCA', 'VARIEDAD', 'MODO', 'TIPO', 'COLOR', 'SUPERFICIE', 'PRODUCCION']].head(20), use_container_width=True, hide_index=True)
        csv_out = df_f[['ID_FINCA', 'VARIEDAD', 'MODO', 'TIPO', 'COLOR', 'SUPERFICIE', 'PRODUCCION']].to_csv(sep=';', index=False, header=False, float_format='%.2f')
        c1, c2, _ = st.columns([1, 1, 2])
        with c1:
            st.download_button("📥 CSV (sep=;)", csv_out, "Vendimia_Labs_2021.txt", "text/csv")
        with c2:
            st.download_button("📥 Excel-compatible", df_f[['ID_FINCA', 'VARIEDAD', 'MODO', 'TIPO', 'COLOR', 'SUPERFICIE', 'PRODUCCION']].to_csv(index=False), "Vendimia_Labs_2021.csv", "text/csv")

st.markdown(f'<div class="footer"><p>VENDIMIA LABS · PRACTICA FINAL — APRENDIZAJE AUTOMATICO Y APRENDIZAJE PROFUNDO</p><p style="margin-top:4px;">Maria Luisa Ros · Camilo Gonzalez · Alvaro Verdasco · Jorge Aldavero · Marzo 2026</p></div>', unsafe_allow_html=True)
