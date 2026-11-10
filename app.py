"""Plataforma de Agricultura Inteligente Macollo.

Aplicacion Streamlit que expone la ingenieria de datos del proyecto, un
dashboard interactivo por fecha y el cuaderno de analisis (Cuaderno1_macollo).
"""

from __future__ import annotations

import base64
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html as st_html

BASE_DIR = Path(__file__).resolve().parent
RAW_CSV = BASE_DIR / "Data_Mocollo1.csv"
CLEAN_CSV = BASE_DIR / "Data_Mocollo1_Limpio.csv"
TRANSFORMED_CSV = BASE_DIR / "Data_Mocollo1_Transformado.csv"
NOTEBOOK_PATH = BASE_DIR / "Cuaderno1_macollo.ipynb"
CACHE_DIR = BASE_DIR / ".cache"
EXECUTED_HTML = CACHE_DIR / "cuaderno_ejecutado.html"
EXECUTED_IPYNB = CACHE_DIR / "cuaderno_ejecutado.ipynb"

NUMERIC_COLS = ["T_Ext_C", "T_Int_C", "Humedad_Pct", "T_Planta_C", "pH", "Altura_cm"]
CATEGORICAL_COLS = ["Responsable", "Fila", "Planta", "ID_Planta"]
METRIC_LABELS = {
    "T_Ext_C": "Temperatura exterior (C)",
    "T_Int_C": "Temperatura interior (C)",
    "Humedad_Pct": "Humedad relativa",
    "T_Planta_C": "Temperatura de planta (C)",
    "pH": "pH",
    "Altura_cm": "Altura (cm)",
}
PLOT_CONFIG = {"displayModeBar": False}

st.set_page_config(
    page_title="Macollo | Ingenieria de Datos",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    :root {
        --mc-green: #2E8B57;
        --mc-lime: #8BC34A;
        --mc-teal: #2E86AB;
        --mc-ink: #17262e;
        --mc-muted: #5c6b73;
        --mc-bg: #f3f7f5;
        --mc-card: #ffffff;
        --mc-border: #e2ebe6;
    }
    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(139, 195, 74, 0.12), transparent 38%),
            radial-gradient(circle at 100% 0%, rgba(46, 134, 171, 0.10), transparent 35%),
            var(--mc-bg);
    }
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--mc-border);
    }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 600;
    }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }
    h1, h2, h3, h4 {
        color: var(--mc-ink);
        letter-spacing: -0.02em;
    }
    .mc-hero {
        position: relative;
        overflow: hidden;
        border-radius: 26px;
        padding: 46px 48px;
        color: #ffffff;
        background:
            radial-gradient(circle at 88% 18%, rgba(139, 195, 74, 0.55), transparent 45%),
            linear-gradient(120deg, #0f3d2e 0%, #1c6b4c 52%, #2E86AB 100%);
        box-shadow: 0 24px 60px rgba(15, 61, 46, 0.25);
    }
    .mc-hero .mc-kicker {
        display: inline-block;
        font-size: 0.78rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        padding: 7px 14px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.25);
        margin-bottom: 20px;
    }
    .mc-hero h1 {
        color: #ffffff;
        font-size: 2.55rem;
        line-height: 1.12;
        margin: 0 0 16px 0;
        font-weight: 800;
    }
    .mc-hero p {
        color: rgba(255, 255, 255, 0.86);
        font-size: 1.05rem;
        max-width: 680px;
        margin-bottom: 26px;
    }
    .mc-hero .mc-hero-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .mc-hero .mc-hero-tags span {
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.22);
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 14px;
        margin: 8px 0 22px 0;
    }
    .kpi {
        background: var(--mc-card);
        border: 1px solid var(--mc-border);
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 10px 26px rgba(23, 38, 46, 0.05);
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: var(--mc-muted);
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: var(--mc-ink);
        line-height: 1.1;
    }
    .kpi-value.green { color: var(--mc-green); }
    .kpi-value.teal { color: var(--mc-teal); }
    .kpi-value.lime { color: #5d8f1f; }
    .kpi-sub {
        font-size: 0.78rem;
        color: var(--mc-muted);
        margin-top: 6px;
    }
    .step-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-top: 4px;
    }
    .step-card {
        background: var(--mc-card);
        border: 1px solid var(--mc-border);
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 10px 26px rgba(23, 38, 46, 0.05);
        height: 100%;
    }
    .step-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 10px;
        font-weight: 800;
        color: #ffffff;
        background: linear-gradient(135deg, var(--mc-green), var(--mc-teal));
        margin-bottom: 12px;
    }
    .step-card h4 {
        margin: 0 0 8px 0;
        font-size: 1.02rem;
    }
    .step-card p {
        margin: 0;
        color: var(--mc-muted);
        font-size: 0.9rem;
        line-height: 1.55;
    }
    .tag {
        display: inline-block;
        padding: 5px 11px;
        margin: 0 6px 6px 0;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
        color: #1c4b39;
        background: #e9f5ee;
        border: 1px solid #cfe8da;
    }
    .panel {
        background: var(--mc-card);
        border: 1px solid var(--mc-border);
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 10px 26px rgba(23, 38, 46, 0.05);
    }
    .panel h4 { margin-top: 0; }
    .muted { color: var(--mc-muted); }
    .pipeline {
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
        gap: 10px;
        margin: 6px 0 4px 0;
    }
    .pipeline .node {
        flex: 1 1 140px;
        background: #f7fbf8;
        border: 1px dashed #b9dcc8;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        font-size: 0.86rem;
        font-weight: 600;
        color: #1c4b39;
    }
    .pipeline .arrow {
        align-self: center;
        color: var(--mc-green);
        font-weight: 800;
        font-size: 1.1rem;
    }
    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
    }
    .tool-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 9px 14px;
        border-radius: 12px;
        background: #ffffff;
        border: 1px solid var(--mc-border);
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--mc-ink);
        box-shadow: 0 4px 12px rgba(23, 38, 46, 0.04);
    }
    .tool-badge .dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--mc-green);
    }
    .callout {
        border-left: 5px solid var(--mc-teal);
        background: #eef6fa;
        border-radius: 0 14px 14px 0;
        padding: 16px 20px;
        color: #274b5c;
        font-size: 0.92rem;
    }
    .footer-note {
        text-align: center;
        color: var(--mc-muted);
        font-size: 0.8rem;
        margin-top: 34px;
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid var(--mc-border);
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow: 0 8px 20px rgba(23, 38, 46, 0.04);
    }
    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid var(--mc-border);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 8px 16px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------
def convertir_a_numero(valor: object) -> float:
    """Convierte valores con coma decimal europea a float (logica del cuaderno)."""
    if pd.isna(valor):
        return np.nan
    try:
        if isinstance(valor, str):
            valor = valor.replace(",", ".")
            num = float(valor)
            if num > 10000:
                return np.nan
            return num
        return float(valor)
    except (TypeError, ValueError):
        return np.nan


@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, int]:
    raw = pd.read_csv(RAW_CSV, sep=";", encoding="utf-8-sig")
    clean = raw.copy()

    for col in NUMERIC_COLS:
        clean[col] = clean[col].apply(convertir_a_numero)

    clean["Fecha"] = pd.to_datetime(clean["Fecha"], format="%d/%m/%Y", errors="coerce")
    clean = clean.dropna(subset=["Fecha"]).reset_index(drop=True)

    # Correccion documentada: la humedad viene como proporcion (0-1) salvo
    # algunos lotes registrados como porcentaje (ej. 67 en lugar de 0.67).
    humidity_fixed = int((clean["Humedad_Pct"] > 1).sum())
    clean.loc[clean["Humedad_Pct"] > 1, "Humedad_Pct"] = (
        clean.loc[clean["Humedad_Pct"] > 1, "Humedad_Pct"] / 100.0
    )

    encoded = pd.get_dummies(
        clean, columns=CATEGORICAL_COLS, prefix=CATEGORICAL_COLS, drop_first=False
    )
    return raw, clean, encoded, humidity_fixed


def format_date(value: date) -> str:
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ]
    return f"{value.day} de {months[value.month - 1]} de {value.year}"


def fmt_number(value: float, suffix: str = "", decimals: int = 1) -> str:
    if pd.isna(value):
        return "Sin dato"
    return f"{value:.{decimals}f}{suffix}"


def kpi_grid(items: list[tuple[str, str, str, str]]) -> None:
    cards = "".join(
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value {tone}">{value}</div>'
        f'<div class="kpi-sub">{sub}</div></div>'
        for label, value, sub, tone in items
    )
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)


def quality_summary(clean: pd.DataFrame) -> dict:
    nulls = clean[NUMERIC_COLS].isna().sum()
    outliers = {}
    for col in NUMERIC_COLS:
        series = clean[col].dropna()
        if series.empty:
            outliers[col] = 0
            continue
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        outliers[col] = int(((series < q1 - 1.5 * iqr) | (series > q3 + 1.5 * iqr)).sum())
    return {
        "nulos_total": int(nulls.sum()),
        "nulos": nulls.to_dict(),
        "outliers": outliers,
        "duplicados": int(clean.duplicated().sum()),
        "completitud": float(100 * (1 - nulls.sum() / (len(clean) * len(NUMERIC_COLS)))),
    }


# ---------------------------------------------------------------------------
# Paginas
# ---------------------------------------------------------------------------
def page_inicio(clean: pd.DataFrame, encoded: pd.DataFrame, humidity_fixed: int) -> None:
    dates = clean["Fecha"].dt.date
    st.markdown(
        f"""
        <div class="mc-hero">
            <span class="mc-kicker">Ingenieria de datos aplicada</span>
            <h1>Agricultura inteligente Macollo</h1>
            <p>Del dato crudo del invernadero a decisiones agronomicas: un pipeline
            reproducible de ingesta, limpieza, analisis exploratorio, transformacion
            y visualizacion interactiva de 540 mediciones de cultivo.</p>
            <div class="mc-hero-tags">
                <span>ETL reproducible</span>
                <span>Analisis exploratorio</span>
                <span>One Hot Encoding</span>
                <span>Dashboard interactivo</span>
                <span>Cuaderno ejecutable</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi_grid(
        [
            ("Registros", f"{len(clean):,}".replace(",", "."), "Mediciones procesadas", "green"),
            ("Fechas", str(dates.nunique()), f"{dates.min():%d/%m/%Y} - {dates.max():%d/%m/%Y}", "teal"),
            ("Variables", str(len(clean.columns)), "Columnas del dataset limpio", ""),
            ("Codificadas", str(encoded.shape[1]), "Columnas tras One Hot Encoding", "lime"),
            ("Responsables", str(clean["Responsable"].nunique()), "Equipo de medicion", ""),
            ("Tratamientos", str(clean["Fila"].nunique()), f"{clean['Planta'].nunique()} plantas por fila", ""),
        ]
    )

    st.markdown("## Como esta construida la ingenieria de datos")
    step_html = """
    <div class="step-grid">
        <div class="step-card">
            <div class="step-num">1</div>
            <h4>Extraccion</h4>
            <p>Lectura del CSV original separado por punto y coma, con codificacion
            UTF-8 y validacion de dimensiones (540 filas x 11 columnas).</p>
        </div>
        <div class="step-card">
            <div class="step-num">2</div>
            <h4>Limpieza</h4>
            <p>Conversion de decimales europeos, normalizacion de fechas, tratamiento
            de nulos y correccion de escala en la humedad relativa.</p>
        </div>
        <div class="step-card">
            <div class="step-num">3</div>
            <h4>Analisis exploratorio</h4>
            <p>Distribuciones, boxplots, densidad, series temporales y matriz de
            correlacion para entender el comportamiento del invernadero.</p>
        </div>
        <div class="step-card">
            <div class="step-num">4</div>
            <h4>Transformacion</h4>
            <p>One Hot Encoding sobre responsable, fila, planta e ID de planta para
            dejar el dataset listo para modelos de machine learning.</p>
        </div>
        <div class="step-card">
            <div class="step-num">5</div>
            <h4>Carga y publicacion</h4>
            <p>Persistencia de datasets limpio y transformado, y generacion del
            reporte ejecutivo y del dashboard interactivo.</p>
        </div>
        <div class="step-card">
            <div class="step-num">6</div>
            <h4>Despliegue</h4>
            <p>Aplicacion Streamlit servida en local y lista para Streamlit Cloud,
            con el cuaderno integrado y ejecutable desde la interfaz.</p>
        </div>
    </div>
    """
    st.markdown(step_html, unsafe_allow_html=True)

    st.markdown("## Pipeline de datos")
    st.markdown(
        """
        <div class="pipeline">
            <div class="node">CSV original<br><span class="muted">Data_Mocollo1</span></div>
            <div class="arrow">&#8594;</div>
            <div class="node">Limpieza ETL<br><span class="muted">tipos y nulos</span></div>
            <div class="arrow">&#8594;</div>
            <div class="node">EDA<br><span class="muted">patrones</span></div>
            <div class="arrow">&#8594;</div>
            <div class="node">Transformacion<br><span class="muted">One Hot Encoding</span></div>
            <div class="arrow">&#8594;</div>
            <div class="node">Streamlit<br><span class="muted">dashboard</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Stack tecnologico")
    tools = [
        ("Python 3.11", "green"),
        ("pandas", "teal"),
        ("NumPy", "lime"),
        ("scikit-learn", "green"),
        ("Matplotlib", "teal"),
        ("Seaborn", "lime"),
        ("Plotly", "green"),
        ("Streamlit", "teal"),
        ("Jupyter", "lime"),
        ("Bootstrap", "green"),
    ]
    badges = "".join(
        f'<span class="tool-badge"><span class="dot" style="background:var(--mc-{color});"></span>{name}</span>'
        for name, color in tools
    )
    st.markdown(f'<div class="badge-row">{badges}</div>', unsafe_allow_html=True)

    st.markdown("## Calidad del dato")
    quality = quality_summary(clean)
    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.markdown(
            f"""
            <div class="panel">
                <h4>Hallazgos del proceso de limpieza</h4>
                <p class="muted">El dataset original mezcla formatos numericos y
                registra temperaturas en algunos dias sin lectura. El pipeline
                conserva la trazabilidad y documenta cada decision.</p>
                <ul>
                    <li><strong>{quality['nulos_total']} valores nulos</strong> en variables
                    numericas, conservados como ausencia de lectura (sin imputacion artificial).</li>
                    <li><strong>{quality['duplicados']} filas duplicadas</strong> en el dataset limpio.</li>
                    <li><strong>{humidity_fixed} registros de humedad</strong> normalizados de
                    porcentaje a proporcion (0-1).</li>
                    <li><strong>Completitud global: {quality['completitud']:.1f}%</strong> sobre
                    las seis variables numericas.</li>
                    <li><strong>Outliers detectados por IQR</strong> en variables numericas,
                    marcados para revision agronomica sin eliminarlos.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="panel">
                <h4>Reglas de transformacion</h4>
                <ul>
                    <li>Fecha <code>dd/mm/aaaa</code> a tipo datetime.</li>
                    <li>Coma decimal europea a punto decimal.</li>
                    <li>Humedad relativa normalizada a rango 0-1.</li>
                    <li>Categoricas a variables binarias con One Hot Encoding.</li>
                    <li>Sin eliminacion de outliers: se senalan, no se borran.</li>
                    <li>Salida en CSV limpio y CSV transformado.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("## Navegacion")
    st.markdown(
        """
        <div class="callout">
        Usa el menu lateral para explorar el <strong>Dashboard</strong> por fecha,
        revisar la seccion de <strong>Ingenieria de datos</strong>, abrir el
        <strong>Cuaderno</strong> (con opcion de ejecutarlo) o inspeccionar los
        <strong>Datos</strong> originales y transformados.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="footer-note">Proyecto academico - Equipo de Data Science, '
        'Agricultura Inteligente Macollo, 2026.</div>',
        unsafe_allow_html=True,
    )


def page_dashboard(clean: pd.DataFrame) -> None:
    st.markdown("## Dashboard interactivo por fecha")
    st.caption("Explora las mediciones del invernadero y compara tratamientos y plantas.")

    available_dates = sorted(clean["Fecha"].dt.date.unique())
    default_date = date(2026, 9, 22)
    default_index = available_dates.index(default_date) if default_date in available_dates else len(available_dates) - 1

    filters = st.columns([1.1, 1, 1, 1])
    selected_date = filters[0].selectbox(
        "Fecha de consulta",
        available_dates,
        index=default_index,
        format_func=format_date,
    )
    day_df = clean[clean["Fecha"].dt.date == selected_date]

    responsables = filters[1].multiselect(
        "Responsable",
        sorted(day_df["Responsable"].unique().tolist()),
        default=sorted(day_df["Responsable"].unique().tolist()),
    )
    treatments = filters[2].multiselect(
        "Fila / tratamiento",
        sorted(day_df["Fila"].unique().tolist()),
        default=sorted(day_df["Fila"].unique().tolist()),
    )
    plants = filters[3].multiselect(
        "Planta",
        sorted(day_df["Planta"].unique().tolist()),
        default=sorted(day_df["Planta"].unique().tolist()),
    )

    filtered = day_df[
        day_df["Responsable"].isin(responsables)
        & day_df["Fila"].isin(treatments)
        & day_df["Planta"].isin(plants)
    ]

    st.markdown(
        f'<p class="muted">Reporte del <strong>{format_date(selected_date)}</strong> - '
        f'{len(filtered)} mediciones seleccionadas de {len(day_df)} registradas.</p>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.warning("No hay mediciones con los filtros seleccionados.")
        return

    kpi_grid(
        [
            ("Responsable(s)", ", ".join(responsables) if responsables else "N/A", "Equipo del dia", "green"),
            ("Mediciones", str(len(filtered)), "Plantas evaluadas", ""),
            ("T exterior", fmt_number(filtered["T_Ext_C"].mean(), " C"), "Promedio del dia", "teal"),
            ("T interior", fmt_number(filtered["T_Int_C"].mean(), " C"), "Promedio del dia", "teal"),
            ("Humedad", fmt_number(filtered["Humedad_Pct"].mean() * 100, " %"), "Humedad relativa media", "lime"),
            ("Altura", fmt_number(filtered["Altura_cm"].mean(), " cm"), "Crecimiento medio", "green"),
        ]
    )

    left, right = st.columns([1.55, 1])

    with left:
        pivot = filtered.pivot_table(
            values="Altura_cm", index="Fila", columns="Planta", aggfunc="mean"
        )
        fig = px.imshow(
            pivot,
            text_auto=".0f",
            aspect="auto",
            color_continuous_scale="YlGnBu",
            labels={"x": "Planta", "y": "Fila / tratamiento", "color": "Altura (cm)"},
            title="Mapa de calor de altura por fila y planta",
        )
        fig.update_layout(height=360, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    with right:
        altura_fila = (
            filtered.groupby("Fila", as_index=False)["Altura_cm"].mean().sort_values("Fila")
        )
        fig = px.bar(
            altura_fila,
            x="Fila",
            y="Altura_cm",
            color="Fila",
            text_auto=".0f",
            title="Altura promedio por tratamiento",
            labels={"Fila": "Tratamiento", "Altura_cm": "Altura (cm)"},
        )
        fig.update_layout(
            height=360,
            showlegend=False,
            margin=dict(l=10, r=10, t=50, b=10),
            yaxis_range=[0, max(altura_fila["Altura_cm"].max() * 1.18, 10)],
        )
        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    left, right = st.columns(2)
    with left:
        fig = px.histogram(
            filtered,
            x="Altura_cm",
            nbins=12,
            marginal="box",
            title="Distribucion de alturas",
            labels={"Altura_cm": "Altura (cm)", "count": "Frecuencia"},
            color_discrete_sequence=["#2E8B57"],
        )
        fig.update_layout(height=340, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    with right:
        temps = filtered[["T_Ext_C", "T_Int_C", "T_Planta_C"]].melt(
            var_name="Tipo", value_name="Temperatura"
        )
        temps["Tipo"] = temps["Tipo"].map(
            {
                "T_Ext_C": "Exterior",
                "T_Int_C": "Interior",
                "T_Planta_C": "Planta",
            }
        )
        fig = px.box(
            temps.dropna(subset=["Temperatura"]),
            x="Tipo",
            y="Temperatura",
            color="Tipo",
            points="all",
            title="Comparacion de temperaturas",
            labels={"Tipo": "Tipo", "Temperatura": "Temperatura (C)"},
        )
        fig.update_layout(height=340, showlegend=False, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    st.markdown("### Evolucion temporal del invernadero")
    metric = st.selectbox(
        "Variable a seguir",
        NUMERIC_COLS,
        index=NUMERIC_COLS.index("Altura_cm"),
        format_func=lambda key: METRIC_LABELS[key],
    )
    temporal = (
        clean.assign(Fecha_dia=clean["Fecha"].dt.date)
        .groupby("Fecha_dia", as_index=False)[metric]
        .mean()
        .rename(columns={"Fecha_dia": "Fecha"})
    )
    fig = px.line(
        temporal,
        x="Fecha",
        y=metric,
        markers=True,
        title=f"{METRIC_LABELS[metric]} - promedio por fecha",
        labels={"Fecha": "Fecha", metric: METRIC_LABELS[metric]},
    )
    fig.update_traces(line_color="#2E86AB", marker_color="#2E8B57")
    fig.add_vline(x=selected_date.isoformat(), line_dash="dash", line_color="#8BC34A")
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    st.markdown("### Detalle de mediciones")
    detail_cols = [
        "Fila", "Planta", "ID_Planta", "Responsable", "T_Planta_C",
        "pH", "Altura_cm", "T_Ext_C", "T_Int_C", "Humedad_Pct",
    ]
    detail = filtered[detail_cols].sort_values(["Fila", "Planta"]).reset_index(drop=True)
    detail["Humedad_Pct"] = (detail["Humedad_Pct"] * 100).round(1)
    st.dataframe(
        detail.rename(
            columns={
                "Fila": "Fila",
                "Planta": "Planta",
                "ID_Planta": "ID",
                "Responsable": "Responsable",
                "T_Planta_C": "T planta (C)",
                "pH": "pH",
                "Altura_cm": "Altura (cm)",
                "T_Ext_C": "T ext (C)",
                "T_Int_C": "T int (C)",
                "Humedad_Pct": "Humedad (%)",
            }
        ),
        use_container_width=True,
        hide_index=True,
        height=420,
    )

    csv_bytes = filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Descargar mediciones del dia (CSV)",
        data=csv_bytes,
        file_name=f"macollo_{selected_date.isoformat()}.csv",
        mime="text/csv",
    )


def page_ingenieria(clean: pd.DataFrame, encoded: pd.DataFrame, humidity_fixed: int) -> None:
    st.markdown("## Ingenieria de datos del proyecto")
    st.caption("Documentacion del flujo ETL, las decisiones de calidad y la transformacion final.")

    st.markdown("### 1. Extraccion e inspeccion")
    st.markdown(
        """
        El insumo es `Data_Mocollo1.csv`, un archivo delimitado por punto y coma con
        11 columnas y 540 registros de medicion. Cada registro combina informacion
        ambientacional (temperaturas y humedad) con informacion de la planta
        (tratamiento, planta, pH y altura).
        """
    )

    st.markdown("### 2. Diccionario de datos")
    dictionary = pd.DataFrame(
        [
            ("Fecha", "Texto", "Fecha de medicion en formato dd/mm/aaaa"),
            ("Responsable", "Categorica", "Persona que registra la medicion"),
            ("T_Ext_C", "Numerica", "Temperatura exterior en grados Celsius"),
            ("T_Int_C", "Numerica", "Temperatura interior del invernadero en Celsius"),
            ("Humedad_Pct", "Numerica", "Humedad relativa en proporcion (0-1)"),
            ("Fila", "Categorica", "Tratamiento o fila experimental (T0-T3)"),
            ("Planta", "Categorica", "Identificador de planta dentro de la fila (P1-P5)"),
            ("ID_Planta", "Categorica", "Clave compuesta fila-planta"),
            ("T_Planta_C", "Numerica", "Temperatura de la planta en Celsius"),
            ("pH", "Numerica", "pH del sustrato"),
            ("Altura_cm", "Numerica", "Altura de la planta en centimetros"),
        ],
        columns=["Campo", "Tipo", "Descripcion"],
    )
    st.dataframe(dictionary, use_container_width=True, hide_index=True)

    st.markdown("### 3. Decisiones de limpieza")
    quality = quality_summary(clean)
    null_table = pd.DataFrame(
        {
            "Variable": NUMERIC_COLS,
            "Nulos": [quality["nulos"][col] for col in NUMERIC_COLS],
            "Outliers (IQR)": [quality["outliers"][col] for col in NUMERIC_COLS],
        }
    )
    col1, col2 = st.columns([1.1, 1])
    with col1:
        st.dataframe(null_table, use_container_width=True, hide_index=True)
    with col2:
        st.markdown(
            f"""
            <div class="panel">
                <h4>Resumen de calidad</h4>
                <p><strong>Completitud:</strong> {quality['completitud']:.1f}%</p>
                <p><strong>Valores nulos:</strong> {quality['nulos_total']}</p>
                <p><strong>Duplicados:</strong> {quality['duplicados']}</p>
                <p><strong>Humedad corregida:</strong> {humidity_fixed} registros</p>
                <p class="muted">Los nulos no se imputan: representan mediciones que
                no se tomaron y forzarlas distorsionaria el analisis temporal.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 4. Transformacion One Hot Encoding")
    new_cols = encoded.shape[1] - clean.shape[1]
    st.markdown(
        f"""
        Las variables categoricas (`Responsable`, `Fila`, `Planta`, `ID_Planta`) se
        convierten en columnas binarias. El dataset pasa de **{clean.shape[1]}** a
        **{encoded.shape[1]}** columnas, es decir, se agregan **{new_cols}** variables
        indicadoras listas para algoritmos de machine learning.
        """
    )
    encoded_columns = pd.DataFrame(
        {"Columna generada": [c for c in encoded.columns if c not in clean.columns]}
    )
    st.dataframe(encoded_columns, use_container_width=True, hide_index=True, height=240)

    st.markdown("### 5. Arquitectura de la solucion")
    st.markdown(
        """
        <div class="pipeline">
            <div class="node">CSV crudo</div>
            <div class="arrow">&#8594;</div>
            <div class="node">ETL en pandas</div>
            <div class="arrow">&#8594;</div>
            <div class="node">CSV limpio</div>
            <div class="arrow">&#8594;</div>
            <div class="node">One Hot Encoding</div>
            <div class="arrow">&#8594;</div>
            <div class="node">CSV transformado</div>
            <div class="arrow">&#8594;</div>
            <div class="node">Streamlit</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="callout">
        El cuaderno `Cuaderno1_macollo.ipynb` es la fuente de verdad del analisis.
        La aplicacion reutiliza su logica de limpieza, permite ejecutarlo y publica
        sus resultados en el dashboard. El archivo `dashboard_reporte.html` es el
        reporte ejecutivo exportado para una fecha puntual.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_outputs(cell: dict) -> None:
    for output in cell.get("outputs", []):
        kind = output.get("output_type")
        if kind == "stream":
            st.code("".join(output.get("text", "")), language="text")
        elif kind in ("execute_result", "display_data"):
            data = output.get("data", {})
            if "image/png" in data:
                st.image(base64.b64decode(data["image/png"]))
            elif "text/html" in data:
                st.markdown("".join(data["text/html"]), unsafe_allow_html=True)
            elif "text/plain" in data:
                st.code("".join(data["text/plain"]), language="text")
        elif kind == "error":
            st.error("\n".join(output.get("traceback", [])))


def render_notebook(nb: dict) -> None:
    for index, cell in enumerate(nb.get("cells", []), start=1):
        if cell.get("cell_type") == "markdown":
            st.markdown("".join(cell.get("source", "")))
        elif cell.get("cell_type") == "code":
            with st.container():
                st.code("".join(cell.get("source", "")), language="python")
                _render_outputs(cell)
        elif cell.get("cell_type") == "raw":
            st.text("".join(cell.get("source", "")))


def ensure_kernel() -> str:
    try:
        from jupyter_client.kernelspec import KernelSpecManager

        specs = KernelSpecManager().find_kernel_specs()
        if "macollo" in specs:
            return "macollo"
        from ipykernel.kernelspec import install

        install(user=True, kernel_name="macollo", display_name="Macollo (venv)")
        return "macollo"
    except Exception:
        return "python3"


def execute_notebook() -> Path:
    import nbformat
    from nbconvert import HTMLExporter
    from nbconvert.preprocessors import ExecutePreprocessor

    nb = nbformat.read(NOTEBOOK_PATH, as_version=4)
    preprocessor = ExecutePreprocessor(timeout=900, kernel_name=ensure_kernel())
    preprocessor.preprocess(nb, {"metadata": {"path": str(BASE_DIR)}})

    CACHE_DIR.mkdir(exist_ok=True)
    nbformat.write(nb, str(EXECUTED_IPYNB))

    html, _ = HTMLExporter(template_name="lab").from_notebook_node(nb)
    EXECUTED_HTML.write_text(html, encoding="utf-8")
    return EXECUTED_HTML


def page_cuaderno() -> None:
    st.markdown("## Cuaderno de analisis")
    st.caption(
        "Cuaderno1_macollo.ipynb: ETL, analisis exploratorio, One Hot Encoding y dashboard."
    )

    if not NOTEBOOK_PATH.exists():
        st.error("No se encontro Cuaderno1_macollo.ipynb en la carpeta del proyecto.")
        return

    import nbformat

    raw_bytes = NOTEBOOK_PATH.read_bytes()
    st.download_button(
        "Descargar cuaderno (.ipynb)",
        data=raw_bytes,
        file_name="Cuaderno1_macollo.ipynb",
        mime="application/x-ipynb+json",
    )

    st.markdown("### Ejecutar el cuaderno")
    st.markdown(
        """
        El cuaderno se puede ejecutar desde la aplicacion. Al hacerlo se generan de
        nuevo los datasets limpio y transformado, se producen las graficas y queda un
        reporte HTML con todas las salidas. La ejecucion puede tardar hasta un minuto.
        """
    )
    col1, col2 = st.columns([1, 2])
    with col1:
        run = st.button("Ejecutar y generar reporte", type="primary", use_container_width=True)
    with col2:
        if EXECUTED_HTML.exists():
            st.download_button(
                "Descargar reporte HTML",
                data=EXECUTED_HTML.read_bytes(),
                file_name="Cuaderno1_macollo_reporte.html",
                mime="text/html",
                use_container_width=True,
            )

    if run:
        with st.spinner("Ejecutando el cuaderno..."):
            try:
                execute_notebook()
                st.success("Cuaderno ejecutado correctamente.")
            except Exception as exc:  # pragma: no cover - depende del entorno
                st.error(f"No se pudo ejecutar el cuaderno: {exc}")

    st.markdown("### Vista del cuaderno")
    source_nb = nbformat.read(NOTEBOOK_PATH, as_version=4)
    view = st.radio(
        "Contenido",
        ["Codigo fuente", "Reporte ejecutado"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if view == "Codigo fuente":
        render_notebook(source_nb)
    elif EXECUTED_HTML.exists():
        html = EXECUTED_HTML.read_text(encoding="utf-8")
        st_html(html, height=1000, scrolling=True)
    else:
        st.info("Aun no hay reporte ejecutado. Usa el boton 'Ejecutar y generar reporte'.")


def page_datos(raw: pd.DataFrame, clean: pd.DataFrame, encoded: pd.DataFrame) -> None:
    st.markdown("## Datos del proyecto")
    st.caption("Inspecciona y descarga los tres estados del dataset.")

    tab_raw, tab_clean, tab_encoded = st.tabs(
        ["Original", "Limpio", "Transformado (One Hot Encoding)"]
    )

    with tab_raw:
        st.markdown(
            f"**Data_Mocollo1.csv** - {raw.shape[0]} filas x {raw.shape[1]} columnas. "
            "Formato original con separador `;` y decimales con coma."
        )
        st.dataframe(raw, use_container_width=True, height=420)
        st.download_button(
            "Descargar original",
            data=RAW_CSV.read_bytes(),
            file_name="Data_Mocollo1.csv",
            mime="text/csv",
        )

    with tab_clean:
        st.markdown(
            f"**Data_Mocollo1_Limpio.csv** - {clean.shape[0]} filas x {clean.shape[1]} "
            "columnas. Fechas y variables numericas normalizadas."
        )
        preview = clean.copy()
        preview["Fecha"] = preview["Fecha"].dt.strftime("%Y-%m-%d")
        st.dataframe(preview, use_container_width=True, height=420)
        st.download_button(
            "Descargar limpio",
            data=CLEAN_CSV.read_bytes() if CLEAN_CSV.exists() else clean.to_csv(index=False).encode(),
            file_name="Data_Mocollo1_Limpio.csv",
            mime="text/csv",
        )

    with tab_encoded:
        st.markdown(
            f"**Data_Mocollo1_Transformado.csv** - {encoded.shape[0]} filas x "
            f"{encoded.shape[1]} columnas. Variables categoricas convertidas a binarias."
        )
        st.dataframe(encoded, use_container_width=True, height=420)
        st.download_button(
            "Descargar transformado",
            data=TRANSFORMED_CSV.read_bytes()
            if TRANSFORMED_CSV.exists()
            else encoded.to_csv(index=False).encode(),
            file_name="Data_Mocollo1_Transformado.csv",
            mime="text/csv",
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    if not RAW_CSV.exists():
        st.error(f"No se encontro el dataset: {RAW_CSV.name}")
        st.stop()

    try:
        raw, clean, encoded, humidity_fixed = load_data()
    except Exception as exc:
        st.error(f"Error al cargar los datos: {exc}")
        st.stop()

    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <div style="width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#2E8B57,#2E86AB);display:flex;align-items:center;justify-content:center;color:white;font-weight:800;">M</div>
                <div>
                    <div style="font-weight:800;font-size:1.05rem;color:#17262e;">Macollo</div>
                    <div style="font-size:0.72rem;color:#5c6b73;">Ingenieria de datos</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        page = st.radio(
            "Navegacion",
            [
                "Inicio",
                "Dashboard",
                "Ingenieria de datos",
                "Cuaderno",
                "Datos",
            ],
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown(
            f"""
            <div style="font-size:0.78rem;color:#5c6b73;line-height:1.7;">
                <strong>{len(clean)}</strong> registros<br>
                <strong>{clean['Fecha'].dt.date.nunique()}</strong> fechas<br>
                <strong>{encoded.shape[1]}</strong> columnas codificadas<br>
                <span style="color:#2E8B57;">Datos cargados correctamente</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Streamlit + pandas + scikit-learn")

    if page == "Inicio":
        page_inicio(clean, encoded, humidity_fixed)
    elif page == "Dashboard":
        page_dashboard(clean)
    elif page == "Ingenieria de datos":
        page_ingenieria(clean, encoded, humidity_fixed)
    elif page == "Cuaderno":
        page_cuaderno()
    else:
        page_datos(raw, clean, encoded)


if __name__ == "__main__":
    main()
