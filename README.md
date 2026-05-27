# Sport Analytics App

Eine Streamlit-App zur Auswertung von EKG-Daten und Leistungstests.

![Screenshot der App](./screenshot.png)

## Was die App kann

- EKG-Rohdaten als interaktiven Plot anzeigen
- Leistungsdaten aus `activity.csv` laden und auswerten
- Mittlere und maximale Leistung berechnen
- Herzfrequenz und Leistung gemeinsam plotten
- Aktivitaet in 5 Herzfrequenz-Zonen einteilen (basierend auf eingegebener HFmax)
- Zeit und durchschnittliche Leistung pro Zone anzeigen

## Projektstruktur

```
Pandas_Abgabe/
├── main.py               # Streamlit-App (Einstiegspunkt)
├── data_processing.py    # Daten laden, Zonen und Kennzahlen berechnen
├── plotting.py           # Interaktiver Plot mit Plotly
├── read_pandas.py        # EKG-Daten laden und plotten
├── data/
│   ├── activity.csv        # Leistungsdaten
│   └── ekg_data/           # EKG-Rohdaten
├── requirements.txt      # Abhaengigkeiten
└── pyproject.toml        # PDM-Projektkonfiguration
```

## App starten

### Mit PDM

1. PDM installieren (falls noch nicht vorhanden):

```bash
pip install pdm
```

2. Abhaengigkeiten installieren:

```bash
pdm install
```

3. App starten:

```bash
pdm run streamlit run main.py
```

### Ohne PDM (alternativ)

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Autoren

Antonio Mrkonja, Lenn Oswald, Noah Reinermann
