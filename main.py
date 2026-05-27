import streamlit as st
from read_pandas import read_csv, make_plot
from data_processing import (
    load_activity_data,
    compute_stats,
    compute_zones,
    compute_time_per_zone,
    compute_avg_power_per_zone,
)
from plotting import create_interactive_plot

# ------------------------------------------------------------------ #
#  Globales Styling                                                    #
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="Sport Analytics",
    page_icon="🏋️",
    layout="wide",
)

st.markdown("""
<style>
/* Hintergrund */
[data-testid="stAppViewContainer"] { background: #f7f6f2; }
[data-testid="stHeader"] { background: transparent; }

/* Metriken */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e0deda;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: #edeae5;
    border-radius: 8px 8px 0 0;
    padding: 0.5rem 1.25rem;
    font-weight: 600;
    color: #7a7974;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #01696f !important;
    border-bottom: 3px solid #01696f;
}

/* Divider */
hr { border: none; border-top: 1px solid #dcd9d5; margin: 1.5rem 0; }

/* DataFrames */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------ #
#  App-Titel                                                           #
# ------------------------------------------------------------------ #
st.markdown("## 🏋️ Sport Analytics")
st.caption("EKG-Auswertung & Leistungstest-Analyse")
st.divider()

# ------------------------------------------------------------------ #
#  Tabs                                                                #
# ------------------------------------------------------------------ #
tab1, tab2 = st.tabs(["\U0001fac0  EKG-Daten", "\u26a1  Leistungstest"])


# ============================  TAB 1  ============================== #
with tab1:
    st.markdown("### EKG-Rohdaten")
    st.caption("Ruhemessung – erste 2000 Messpunkte")

    df_ekg = read_csv()
    fig_ekg = make_plot(df_ekg)
    st.plotly_chart(fig_ekg, use_container_width=True)


# ============================  TAB 2  ============================== #
with tab2:
    st.markdown("### Leistungstest-Auswertung")

    # ---- Sidebar-ähnliche Eingabe oben ---- #
    with st.container():
        col_input, col_spacer = st.columns([1, 3])
        with col_input:
            max_hr = st.number_input(
                "💓 Maximale Herzfrequenz (HFmax)",
                min_value=100,
                max_value=220,
                value=190,
                help="Deine persönliche maximale Herzfrequenz in Schlägen pro Minute.",
            )

    st.divider()

    # ---- Daten laden & Zonen berechnen ---- #
    df = load_activity_data()
    df = compute_zones(df, max_hr)
    mean_power, max_power = compute_stats(df)

    # ---- KPI-Kacheln ---- #
    st.markdown("#### 📊 Leistungskennzahlen")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Mittlere Leistung", f"{mean_power:.1f} W", help="Durchschnittswatt über die gesamte Aktivität")
    kpi2.metric("Maximale Leistung", f"{max_power:.1f} W", help="Höchster gemessener Wattwert")
    kpi3.metric("HFmax (eingegeben)", f"{max_hr} bpm")

    st.divider()

    # ---- Interaktiver Plot ---- #
    st.markdown("#### 📈 Leistung & Herzfrequenz über Zeit")
    st.caption("Die Herzfrequenz-Linie ist nach HF-Zone eingefärbt. Zoomen und Hovern möglich.")
    fig = create_interactive_plot(df, max_hr=max_hr)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---- Zonen-Tabellen nebeneinander ---- #
    st.markdown("#### 🔥 Herzfrequenz-Zonen")

    col_time, col_power = st.columns(2)

    with col_time:
        st.markdown("**⏱️ Zeit pro Zone**")
        time_per_zone = compute_time_per_zone(df)
        st.dataframe(
            time_per_zone.rename("Messpunkte").reset_index().rename(columns={"index": "Zone"}),
            use_container_width=True,
            hide_index=True,
        )

    with col_power:
        st.markdown("**⚡ Durchschnittliche Leistung pro Zone**")
        avg_power = compute_avg_power_per_zone(df)
        st.dataframe(
            avg_power.round(1).rename("Leistung (W)").reset_index().rename(columns={"index": "Zone"}),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # ---- Daten-Vorschau ausklappbar ---- #
    with st.expander("🔍 Rohdaten-Vorschau"):
        st.dataframe(df.head(20), use_container_width=True)
