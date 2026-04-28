import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Échantillons Villages – Burkina Faso",
    page_icon="🗺️",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Remove default padding */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 1400px;
}

/* Header */
.app-header {
    background: linear-gradient(135deg, #0D3B2E 0%, #1A6B4A 50%, #0D3B2E 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #2D9B6F30;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, #EF7C1A22 0%, transparent 70%);
    pointer-events: none;
}
.app-header h1 {
    font-size: 2rem;
    font-weight: 800;
    color: #F5F0E8;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.app-header p {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #A8D5B5;
    margin: 0;
    letter-spacing: 0.5px;
}
.flag-line {
    display: flex;
    gap: 4px;
    margin-bottom: 0.8rem;
}
.flag-r { width: 36px; height: 6px; background: #EF2B2D; border-radius: 3px; }
.flag-g { width: 36px; height: 6px; background: #009A3C; border-radius: 3px; }
.flag-y { width: 36px; height: 6px; background: #FCB421; border-radius: 3px; }

/* Stat cards */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.stat-card {
    flex: 1;
    background: #0D2818;
    border: 1px solid #1A6B4A40;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    text-align: center;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: #2D9B6F; }
.stat-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #EF7C1A;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #7DB892;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* Selector */
.stSelectbox > div > div {
    background: #0D2818 !important;
    border: 1.5px solid #2D9B6F !important;
    border-radius: 10px !important;
    color: #F5F0E8 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}

/* Legend card */
.legend-card {
    background: #0D2818;
    border: 1px solid #1A6B4A40;
    border-radius: 12px;
    padding: 1.2rem;
    margin-top: 1rem;
}
.legend-title {
    font-size: 0.75rem;
    font-weight: 700;
    color: #A8D5B5;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.8rem;
    font-family: 'Space Mono', monospace;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 5px;
    font-size: 0.78rem;
    color: #D4E8D8;
}
.dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
    border: 2px solid rgba(255,255,255,0.3);
}

/* Table */
.dataframe-container {
    background: #0D2818;
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid #1A6B4A40;
    margin-top: 1rem;
}
.section-title {
    font-size: 0.72rem;
    font-weight: 700;
    color: #A8D5B5;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 0.6rem;
    font-family: 'Space Mono', monospace;
}

/* Dark theme for DataFrame */
[data-testid="stDataFrame"] {
    background: #0D2818 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #080F0C !important;
    border-right: 1px solid #1A6B4A30 !important;
}

/* Background */
.stApp {
    background: #060E09;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0D2818; }
::-webkit-scrollbar-thumb { background: #2D9B6F; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    xl = pd.ExcelFile("ECHANTILLONS_GPS.xlsx")
    data = {}
    for sheet in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet)
        data[sheet] = df
    return data

data = load_data()

# Color palette per sample
COLORS = {
    "ECHANTILLON1": "#EF7C1A",   # orange
    "ECHANTILLON2": "#3AB4F2",   # cyan
    "ECHANTILLON3": "#E84393",   # fuchsia
    "ECHANTILLON4": "#A8E063",   # lime
    "ECHANTILLON5": "#F5C518",   # gold
}

REGION_COLORS = {
    "Boucle du Mouhoun": "#F4A460",
    "Centre-Ouest": "#87CEEB",
    "Centre-Sud": "#90EE90",
    "Hauts-Bassins": "#DDA0DD",
}

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="flag-line">
        <div class="flag-r"></div>
        <div class="flag-g"></div>
        <div class="flag-y"></div>
    </div>
    <h1>🗺️ Cartographie des Échantillons</h1>
    <p>BURKINA FASO — VISUALISATION GÉOGRAPHIQUE DES VILLAGES ÉCHANTILLONNÉS</p>
</div>
""", unsafe_allow_html=True)

# ── Controls ───────────────────────────────────────────────────────────────────
col_sel, col_info = st.columns([1, 3])

with col_sel:
    st.markdown('<div class="section-title">Sélectionner un échantillon</div>', unsafe_allow_html=True)
    selected = st.selectbox(
        "", options=list(data.keys()), index=0, label_visibility="collapsed"
    )

df = data[selected]
color = COLORS[selected]

# ── Stats row ──────────────────────────────────────────────────────────────────
n_villages = len(df)
n_regions = df["Region"].nunique()
n_provinces = df["Province"].nunique()
n_communes = df["Commune"].nunique()
total_benef = int(df["Benef"].sum())

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-value">{n_villages}</div>
        <div class="stat-label">Villages</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{n_regions}</div>
        <div class="stat-label">Régions</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{n_provinces}</div>
        <div class="stat-label">Provinces</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{n_communes}</div>
        <div class="stat-label">Communes</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{total_benef:,}</div>
        <div class="stat-label">Bénéficiaires</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Map + Sidebar info ─────────────────────────────────────────────────────────
col_map, col_side = st.columns([3, 1])

with col_map:
    # Build Folium map centered on Burkina Faso
    m = folium.Map(
        location=[12.3, -1.7],
        zoom_start=7,
        tiles=None,
    )

    # Dark tile layer
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
        name="Dark",
        max_zoom=19,
    ).add_to(m)

    # Group markers by region for clustering
    region_groups = {}
    for region in df["Region"].unique():
        fg = folium.FeatureGroup(name=region)
        region_groups[region] = fg
        m.add_child(fg)

    # Add markers
    for _, row in df.iterrows():
        if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
            region = row["Region"]
            dot_color = REGION_COLORS.get(region, color)

            popup_html = f"""
            <div style="font-family: 'Segoe UI', sans-serif; min-width: 200px;">
                <div style="background: #1A6B4A; color: white; padding: 8px 12px;
                            border-radius: 6px 6px 0 0; font-weight: 700; font-size: 14px;">
                    📍 {row['Village']}
                </div>
                <div style="background: #f8f9fa; padding: 10px 12px; border-radius: 0 0 6px 6px;">
                    <table style="width:100%; font-size: 12px; border-collapse: collapse;">
                        <tr><td style="color:#666; padding: 2px 0;">Commune</td>
                            <td style="font-weight:600; padding: 2px 0;">{row['Commune']}</td></tr>
                        <tr><td style="color:#666; padding: 2px 0;">Province</td>
                            <td style="font-weight:600; padding: 2px 0;">{row['Province']}</td></tr>
                        <tr><td style="color:#666; padding: 2px 0;">Région</td>
                            <td style="font-weight:600; padding: 2px 0;">{row['Region']}</td></tr>
                        <tr><td colspan="2" style="border-top: 1px solid #ddd; padding-top: 6px; margin-top: 6px;"></td></tr>
                        <tr><td style="color:#666; padding: 2px 0;">Bénéficiaires</td>
                            <td style="font-weight:700; color: #EF7C1A; padding: 2px 0;">{int(row['Benef'])}</td></tr>
                        <tr><td style="color:#666; padding: 2px 0;">Poids (w)</td>
                            <td style="font-weight:600; padding: 2px 0;">{row['w']:.4f}</td></tr>
                        <tr><td style="color:#666; padding: 2px 0;">Prob. inclusion</td>
                            <td style="font-weight:600; padding: 2px 0;">{row['incl_prob']:.4f}</td></tr>
                        <tr><td style="color:#666; padding: 2px 0;">GPS</td>
                            <td style="font-weight:600; font-size: 11px; padding: 2px 0;">
                                {row['Latitude']:.4f}°N, {row['Longitude']:.4f}°E</td></tr>
                    </table>
                </div>
            </div>
            """

            folium.CircleMarker(
                location=[row["Latitude"], row["Longitude"]],
                radius=7,
                color="white",
                weight=1.5,
                fill=True,
                fill_color=dot_color,
                fill_opacity=0.85,
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=f"<b>{row['Village']}</b><br>{row['Commune']} · {int(row['Benef'])} bénéf.",
            ).add_to(region_groups[region])

    folium.LayerControl(collapsed=False).add_to(m)

    st_folium(m, width=None, height=560, returned_objects=[])

with col_side:
    # Légende régions
    region_legend_items = "".join([
        f'<div class="legend-item"><div class="dot" style="background:{c};"></div>{r}</div>'
        for r, c in REGION_COLORS.items() if r in df["Region"].values
    ])
    st.markdown(f"""
    <div class="legend-card">
        <div class="legend-title">Régions</div>
        {region_legend_items}
    </div>
    """, unsafe_allow_html=True)

    # Top 5 communes by beneficiaries
    st.markdown('<br>', unsafe_allow_html=True)
    top_communes = (
        df.groupby("Commune")["Benef"].sum()
        .sort_values(ascending=False)
        .head(5)
    )
    top_html = "".join([
        f'<div style="display:flex; justify-content:space-between; padding:5px 0; '
        f'border-bottom:1px solid #1A6B4A30; font-size:0.78rem;">'
        f'<span style="color:#D4E8D8;">{c}</span>'
        f'<span style="color:{color}; font-weight:700; font-family: Space Mono, monospace;">'
        f'{int(v):,}</span></div>'
        for c, v in top_communes.items()
    ])
    st.markdown(f"""
    <div class="legend-card">
        <div class="legend-title">Top 5 Communes · Bénéf.</div>
        {top_html}
    </div>
    """, unsafe_allow_html=True)

    # Distribution par région
    st.markdown('<br>', unsafe_allow_html=True)
    region_dist = df.groupby("Region").size()
    dist_html = "".join([
        f'<div style="display:flex; justify-content:space-between; padding:5px 0; '
        f'border-bottom:1px solid #1A6B4A30; font-size:0.78rem;">'
        f'<span style="color:#D4E8D8;">{r.replace("Boucle du Mouhoun","Boucle/Mouhoun")}</span>'
        f'<span style="color:{REGION_COLORS.get(r, color)}; font-weight:700; font-family: Space Mono, monospace;">'
        f'{int(v)} villages</span></div>'
        for r, v in region_dist.items()
    ])
    st.markdown(f"""
    <div class="legend-card">
        <div class="legend-title">Villages par Région</div>
        {dist_html}
    </div>
    """, unsafe_allow_html=True)

# ── Data table ──────────────────────────────────────────────────────────────────
with st.expander("📋 Tableau des données — " + selected, expanded=False):
    display_df = df[["Region","Province","Commune","Village","Latitude","Longitude","Benef","incl_prob","w"]].copy()
    display_df.columns = ["Région","Province","Commune","Village","Latitude","Longitude","Bénéficiaires","Prob. Inclusion","Poids (w)"]
    st.dataframe(
        display_df.style
            .format({"Latitude": "{:.4f}", "Longitude": "{:.4f}",
                     "Prob. Inclusion": "{:.4f}", "Poids (w)": "{:.4f}",
                     "Bénéficiaires": "{:,}"}),
        use_container_width=True,
        height=320,
    )

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 1.5rem 0 0.5rem; 
     font-family: 'Space Mono', monospace; font-size: 0.65rem; 
     color: #3A6B4A; letter-spacing: 1px;">
    BURKINA FASO · CARTOGRAPHIE DES ÉCHANTILLONS DE VILLAGES · WGS84
</div>
""", unsafe_allow_html=True)
