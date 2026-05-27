import streamlit as st
from read_pandas import read_csv, make_plot   # EKG-Teil aus der alten Übung
from data_processing import (
    load_activity_data,
    compute_stats,
    compute_zones,
    compute_time_per_zone,
    compute_avg_power_per_zone
)
from plotting import create_interactive_plot


# ---------------- Tabs definieren ----------------
tab1, tab2 = st.tabs(["EKG-Data", "Power-Data"])


# ---------------- TAB 1: EKG-Daten (alte Übung) ----------------
with tab1:
    st.header("EKG-Data")

    df_ekg = read_csv()
    fig_ekg = make_plot(df_ekg)

    st.plotly_chart(fig_ekg, use_container_width=True)



# ---------------- TAB 2: Power-Daten (neue Aufgabe) ----------------
with tab2:
    st.header("Auswertung Leistungstest (Power-Data)")

    # 1) Daten laden
    df = load_activity_data()
    st.write("Vorschau der Daten:", df.head())

    # 2) Maximale Herzfrequenz als Eingabe
    max_hr = st.number_input(
        "Maximale Herzfrequenz eingeben:",
        min_value=100,
        max_value=220,
        value=190
    )

    # 3) Zonen berechnen
    df = compute_zones(df, max_hr)

    # 4) Kennzahlen berechnen
    mean_power, max_power = compute_stats(df)

    st.subheader("Leistungskennzahlen")
    st.metric("Mittelwert der Leistung", f"{mean_power:.1f} W")
    st.metric("Maximalwert der Leistung", f"{max_power:.1f} W")

    # 5) Interaktiver Plot
    st.subheader("Interaktiver Plot: Leistung & Herzfrequenz")
    fig = create_interactive_plot(df)
    st.plotly_chart(fig, width='stretch')

    # 6) Zeit pro Zone
    st.subheader("Zeit in den Herzfrequenz-Zonen")
    time_per_zone = compute_time_per_zone(df)
    st.write(time_per_zone)

    # 7) Durchschnittliche Leistung pro Zone
    st.subheader("Durchschnittliche Leistung pro Zone")
    avg_power_per_zone = compute_avg_power_per_zone(df)
    st.write(avg_power_per_zone)


