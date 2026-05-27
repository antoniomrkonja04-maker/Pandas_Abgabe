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

st.set_page_config(
    page_title="Sport Analytics",
    layout="wide",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f7f6f2; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e0deda;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
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
</style>
""", unsafe_allow_html=True)

st.markdown("## Sport Analytics")
st.caption("EKG-Auswertung und Leistungstest-Analyse")
st.divider()

tab1, tab2 = st.tabs(["EKG-Daten", "Leistungstest"])


with tab1:
    st.markdown("### EKG-Rohdaten")
    st.caption("Ruhemessung - erste 2000 Messpunkte")

    df_ekg = read_csv()
    fig_ekg = make_plot(df_ekg)
    st.plotly_chart(fig_ekg, use_container_width=True)


with tab2:
    st.markdown("### Leistungstest-Auswertung")

    col_input, col_spacer = st.columns([1, 3])
    with col_input:
        max_hr = st.number_input(
            "Maximale Herzfrequenz (HFmax)",
            min_value=100,
            max_value=220,
            value=190,
            help="Deine persönliche maximale Herzfrequenz in Schlägen pro Minute.",
        )

    st.divider()

    df = load_activity_data()
    df = compute_zones(df, max_hr)
    mean_power, max_power = compute_stats(df)

    st.markdown("#### Leistungskennzahlen")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Mittlere Leistung", f"{mean_power:.1f} W")
    kpi2.metric("Maximale Leistung", f"{max_power:.1f} W")
    kpi3.metric("HFmax (eingegeben)", f"{max_hr} bpm")

    st.divider()

    st.markdown("#### Leistung und Herzfrequenz über Zeit")
    st.caption("Die Herzfrequenz-Linie ist nach HF-Zone eingefärbt. Zoomen und Hovern möglich.")
    fig = create_interactive_plot(df, max_hr=max_hr)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("#### Herzfrequenz-Zonen")
    col_time, col_power = st.columns(2)

    with col_time:
        st.markdown("**Zeit pro Zone**")
        time_per_zone = compute_time_per_zone(df)
        st.dataframe(
            time_per_zone.rename("Messpunkte").reset_index().rename(columns={"index": "Zone"}),
            use_container_width=True,
            hide_index=True,
        )

    with col_power:
        st.markdown("**Durchschnittliche Leistung pro Zone**")
        avg_power = compute_avg_power_per_zone(df)
        st.dataframe(
            avg_power.round(1).rename("Leistung (W)").reset_index().rename(columns={"index": "Zone"}),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    with st.expander("Rohdaten-Vorschau"):
        st.dataframe(df.head(20), use_container_width=True)
