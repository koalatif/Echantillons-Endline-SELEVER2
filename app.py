import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Evaluation Endline de SELEVER2 de Tanager - Burkina Faso: Visualisation des 5 échantillons Villages tirés",
    page_icon="🗺️",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 1400px;
}

/* ── Header ── */
.app-header {
    background: #FFFDF7;
    border-radius: 20px;
    padding: 1.8rem 2.5rem;
    margin-bottom: 1.5rem;
    border: 1.5px solid #E8E0D0;
    display: flex;
    align-items: center;
    gap: 2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.header-flag {
    display: flex;
    flex-direction: column;
    gap: 3px;
}
.flag-r { width: 8px; height: 28px; background: #EF2B2D; border-radius: 4px; }
.flag-g { width: 8px; height: 28px; background: #009A3C; border-radius: 4px; }
.flag-y { width: 8px; height: 28px; background: #FCB421; border-radius: 4px; }
.header-text h1 {
    font-size: 1.75rem;
    font-weight: 800;
    color: #1A2E1A;
    margin: 0 0 0.2rem 0;
    letter-spacing: -0.5px;
}
.header-text p {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #7A8C7A;
    margin: 0;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.header-badge {
    margin-left: auto;
    background: #F0F7EE;
    border: 1.5px solid #B8D9B0;
    border-radius: 50px;
    padding: 0.5rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    color: #2E7D32;
    letter-spacing: 0.5px;
}

/* ── Stat cards ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: #FFFFFF;
    border: 1.5px solid #EBE5D8;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    text-align: center;
    transition: all 0.2s ease;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.stat-card:hover {
    border-color: #A8C5A0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    transform: translateY(-1px);
}
.stat-icon {
    font-size: 1.2rem;
    margin-bottom: 0.4rem;
}
.stat-value {
    font-size: 1.7rem;
    font-weight: 800;
    color: #1A2E1A;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #9A9080;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.stat-accent { color: #2E7D32; }

/* ── Selectbox ── */
.stSelectbox label { color: #4A5A4A !important; font-weight: 600 !important; font-size: 0.85rem !important; }
.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #C8DEC4 !important;
    border-radius: 12px !important;
    color: #1A2E1A !important;
}
.stSelectbox > div > div:hover { border-color: #4A9A54 !important; }

/* ── Side panels ── */
.info-card {
    background: #FFFFFF;
    border: 1.5px solid #EBE5D8;
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.info-card-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    color: #7A8C7A;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 0.85rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #F0EAE0;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 6px;
    font-size: 0.8rem;
    color: #3A4A3A;
    font-weight: 500;
}
.dot {
    width: 11px; height: 11px;
    border-radius: 50%;
    flex-shrink: 0;
    border: 2px solid rgba(255,255,255,0.8);
    box-shadow: 0 0 0 1px rgba(0,0,0,0.1);
}
.rank-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #F5F0E8;
    font-size: 0.78rem;
}
.rank-row:last-child { border-bottom: none; }
.rank-name { color: #3A4A3A; font-weight: 500; }
.rank-val {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 0.75rem;
}

/* ── Expander / Table ── */
.streamlit-expanderHeader {
    background: #FAFAF7 !important;
    border: 1.5px solid #EBE5D8 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    color: #3A4A3A !important;
}
.streamlit-expanderContent {
    border: 1.5px solid #EBE5D8 !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    background: #FAFAF7 !important;
}

/* ── App background ── */
.stApp { background: #F7F4EE; }
[data-testid="stSidebar"] { background: #F0EDE5 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F0EAE0; border-radius: 4px; }
::-webkit-scrollbar-thumb { background: #B8C8B0; border-radius: 4px; }

/* ── Section label ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    font-weight: 500;
    color: #7A8C7A;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 0.5rem;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #B0A898;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    xl = pd.ExcelFile("ECHANTILLONS_GPS.xlsx")
    return {sheet: pd.read_excel(xl, sheet_name=sheet) for sheet in xl.sheet_names}

data = load_data()

SAMPLE_COLORS = {
    "ECHANTILLON1": "#E85D26",
    "ECHANTILLON2": "#2196A8",
    "ECHANTILLON3": "#C2185B",
    "ECHANTILLON4": "#558B2F",
    "ECHANTILLON5": "#F9A825",
}

REGION_COLORS = {
    "Boucle du Mouhoun": "#E85D26",
    "Centre-Ouest":      "#2196A8",
    "Centre-Sud":        "#558B2F",
    "Hauts-Bassins":     "#7B3FA0",
}

REGION_BG = {
    "Boucle du Mouhoun": "#FEF0EB",
    "Centre-Ouest":      "#EBF5F7",
    "Centre-Sud":        "#EEF5E8",
    "Hauts-Bassins":     "#F3EBF8",
}

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="header-flag">
        <div class="flag-r"></div>
        <div class="flag-g"></div>
        <div class="flag-y"></div>
    </div>
    <div class="header-text">
        <h1>🗺️ EVALUATION FINALE DU PROJET SELEVER2 DE TANAGER</h1>
        <p>Burkina Faso — Visualisation géographique des villages échantillonnés</p>
    </div>
    <div class="header-badge">WGS 84 </div>
</div>
""", unsafe_allow_html=True)

# ── Sample selector ────────────────────────────────────────────────────────────
col_sel, col_spacer = st.columns([1, 3])
with col_sel:
    st.markdown('<div class="section-label">Sélectionner un échantillon</div>', unsafe_allow_html=True)
    selected = st.selectbox("", options=list(data.keys()), index=0, label_visibility="collapsed")

df = data[selected]
color = SAMPLE_COLORS[selected]

# ── Stats ──────────────────────────────────────────────────────────────────────
n_villages  = len(df)
n_regions   = df["Region"].nunique()
n_provinces = df["Province"].nunique()
n_communes  = df["Commune"].nunique()
total_benef = int(df["Benef"].sum())

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-icon">🏘️</div>
        <div class="stat-value stat-accent">{n_villages}</div>
        <div class="stat-label">Villages</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">🌍</div>
        <div class="stat-value">{n_regions}</div>
        <div class="stat-label">Régions</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">🗂️</div>
        <div class="stat-value">{n_provinces}</div>
        <div class="stat-label">Provinces</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">🏛️</div>
        <div class="stat-value">{n_communes}</div>
        <div class="stat-label">Communes</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-value stat-accent">{total_benef:,}</div>
        <div class="stat-label">Bénéficiaires</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Map + Side info ────────────────────────────────────────────────────────────
col_map, col_side = st.columns([3, 1])

with col_map:
    m = folium.Map(
        location=[12.3, -1.7],
        zoom_start=7,
        tiles=None,
    )

    # Light tile layer
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
        name="Light",
        max_zoom=19,
    ).add_to(m)

    region_groups = {}
    for region in df["Region"].unique():
        fg = folium.FeatureGroup(name=region)
        region_groups[region] = fg
        m.add_child(fg)

    for _, row in df.iterrows():
        if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
            region    = row["Region"]
            dot_color = REGION_COLORS.get(region, color)
            bg_color  = REGION_BG.get(region, "#F5F5F5")

            popup_html = f"""
            <div style="font-family: 'Segoe UI', sans-serif; min-width: 210px; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.12);">
                <div style="background: {dot_color}; color: white; padding: 9px 13px;
                            font-weight: 700; font-size: 14px; letter-spacing: 0.2px;">
                    📍 {row['Village']}
                </div>
                <div style="background: #FAFAFA; padding: 10px 13px;">
                    <div style="background: {bg_color}; border-radius: 6px; padding: 6px 10px; margin-bottom: 8px;
                                font-size: 11px; color: {dot_color}; font-weight: 600;">
                        {row['Commune']} · {row['Province']} · {row['Region']}
                    </div>
                    <table style="width:100%; font-size: 12px; border-collapse: collapse;">
                        <tr>
                            <td style="color:#888; padding: 3px 0;">Bénéficiaires</td>
                            <td style="font-weight:700; color:{dot_color}; text-align:right; padding: 3px 0;">{int(row['Benef'])}</td>
                        </tr>
                        <tr>
                            <td style="color:#888; padding: 3px 0;">Poids (w)</td>
                            <td style="font-weight:600; text-align:right; padding: 3px 0;">{row['w']:.4f}</td>
                        </tr>
                        <tr>
                            <td style="color:#888; padding: 3px 0;">Prob. inclusion</td>
                            <td style="font-weight:600; text-align:right; padding: 3px 0;">{row['incl_prob']:.4f}</td>
                        </tr>
                        <tr>
                            <td style="color:#888; padding: 3px 0; border-top:1px solid #EEE; padding-top:6px;">GPS</td>
                            <td style="font-size:10px; font-family:monospace; text-align:right; padding: 3px 0; border-top:1px solid #EEE; padding-top:6px;">
                                {row['Latitude']:.6f}, {row['Longitude']:.6f}
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
            """

            folium.CircleMarker(
                location=[row["Latitude"], row["Longitude"]],
                radius=7,
                color="white",
                weight=2,
                fill=True,
                fill_color=dot_color,
                fill_opacity=0.88,
                popup=folium.Popup(popup_html, max_width=270),
                tooltip=f"<b style='font-family:sans-serif'>{row['Village']}</b><br>"
                        f"<span style='color:#666;font-size:12px'>{row['Commune']} · {int(row['Benef'])} bénéf.</span>",
            ).add_to(region_groups[region])

    folium.LayerControl(collapsed=False).add_to(m)
    st_folium(m, width=None, height=560, returned_objects=[])

with col_side:
    # Légende régions
    region_items = "".join([
        f'<div class="legend-item">'
        f'<div class="dot" style="background:{REGION_COLORS.get(r, color)};"></div>'
        f'{r}</div>'
        for r in df["Region"].unique()
    ])
    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">🌍 Régions représentées</div>
        {region_items}
    </div>
    """, unsafe_allow_html=True)

    # Top 5 communes
    top5 = df.groupby("Commune")["Benef"].sum().sort_values(ascending=False).head(5)
    top_rows = "".join([
        f'<div class="rank-row">'
        f'<span class="rank-name">{c}</span>'
        f'<span class="rank-val" style="color:{color};">{int(v):,}</span>'
        f'</div>'
        for c, v in top5.items()
    ])
    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">👥 Top 5 communes · bénéf.</div>
        {top_rows}
    </div>
    """, unsafe_allow_html=True)

    # Villages par région
    reg_dist = df.groupby("Region").size()
    reg_rows = "".join([
        f'<div class="rank-row">'
        f'<span class="rank-name">{r.replace("Boucle du Mouhoun","Boucle/Mouhoun")}</span>'
        f'<span class="rank-val" style="color:{REGION_COLORS.get(r, color)};">{v} vill.</span>'
        f'</div>'
        for r, v in reg_dist.items()
    ])
    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">📊 Villages par région</div>
        {reg_rows}
    </div>
    """, unsafe_allow_html=True)

    # Stat poids moyen
    w_mean = df["w"].mean()
    w_min  = df["w"].min()
    w_max  = df["w"].max()
    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">⚖️ Poids d'échantillonnage</div>
        <div class="rank-row"><span class="rank-name">Moyen</span>
            <span class="rank-val" style="color:{color};">{w_mean:.2f}</span></div>
        <div class="rank-row"><span class="rank-name">Min</span>
            <span class="rank-val">{w_min:.2f}</span></div>
        <div class="rank-row"><span class="rank-name">Max</span>
            <span class="rank-val">{w_max:.2f}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ── Data table ──────────────────────────────────────────────────────────────────
with st.expander(f"📋  Tableau des données — {selected}", expanded=False):
    display_df = df[["Region","Province","Commune","Village","Latitude","Longitude","Benef","incl_prob","w"]].copy()
    display_df.columns = ["Région","Province","Commune","Village","Latitude","Longitude","Bénéficiaires","Prob. Inclusion","Poids (w)"]
    st.dataframe(
        display_df.style.format({
            "Latitude":       "{:.6f}",
            "Longitude":      "{:.6f}",
            "Prob. Inclusion":"{:.4f}",
            "Poids (w)":      "{:.4f}",
            "Bénéficiaires":  "{:,}",
        }),
        use_container_width=True,
        height=320,
    )

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    Burkina Faso · Cartographie des Échantillons de Villages · WGS84 · GeoNames
</div>
""", unsafe_allow_html=True)
