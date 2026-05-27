import pandas as pd
import plotly.express as px

def read_csv():
    #Liest Textdatei mit EKG-Daten ein, trennt die Spalten mit Tabulatoren und benennt die Spalten entsprechend
    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep="\t", header=None)
    df.columns = ["Messwerte in mV", "Zeit in ms"]
    return df

def nake_plot(df):# Erstellt ein Liniendiagramm mit Plotly Express, wobei die x-Achse die Zeit in ms und die y-Achse die Messwerte in mV darstellt. Der Titel des Diagramms ist "EKG-Daten".
    fig = px.line(df, x="Zeit in ms", y="Messwerte in mV", title="EKG-Daten")
    return fig

if __name__ == "__main__":# Liest die CSV-Datei ein, gibt die ersten Zeilen des DataFrames aus und erstellt dann ein Liniendiagramm der EKG-Daten.
    df = read_csv()
    print(df.head())
    fig = nake_plot(df)
    fig.show()

