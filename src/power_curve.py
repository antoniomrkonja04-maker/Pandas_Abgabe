import pandas as pd
import matplotlib.pyplot as plt
from sort import bubble_sort


def load_activity_data():
    df = pd.read_csv('data/activity.csv')
    return df


def print_power_stats(df: pd.DataFrame) -> None:
    if 'PowerOriginal' not in df.columns:
        print('Spalte PowerOriginal nicht gefunden.')
        return
    mean_power = df['PowerOriginal'].mean()
    max_power = df['PowerOriginal'].max()
    print(f'Mittelwert der Leistung: {mean_power:.1f} W')
    print(f'Maximale Leistung: {int(max_power)} W')


def plot_power(df: pd.DataFrame) -> None:
    if 'PowerOriginal' not in df.columns:
        return

    if 'Duration' in df.columns:
        x = df['Duration'].cumsum()
        x_label = 'Zeit (s)'
    else:
        x = df.index
        x_label = 'Messpunkt'

    # Plot der Leistung über die Zeit
    plt.figure(figsize=(10, 4))
    plt.plot(x, df['PowerOriginal'], label='Leistung', color='blue')
    plt.xlabel(x_label)
    plt.ylabel('Leistung (W)')
    plt.title('Leistung über Zeit')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Erzeuge die Leistungskurve (absteigend sortierte Leistung)
    power_values = df['PowerOriginal'].dropna().tolist()
    if len(power_values) > 0:
        sorted_values = bubble_sort(power_values)
        sorted_desc = sorted_values[::-1]
        x2 = list(range(len(sorted_desc)))
        plt.figure(figsize=(10, 4))
        plt.plot(x2, sorted_desc, label='Leistung (sortiert absteigend)', color='green')
        plt.xlabel('Rang')
        plt.ylabel('Leistung (W)')
        plt.title('Leistungskurve (Power Curve)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


def main() -> None:
    try:
        df = load_activity_data()
    except FileNotFoundError:
        print('Datei data/activity.csv nicht gefunden.')
        return

    print_power_stats(df)
    plot_power(df)


if __name__ == '__main__':
    main()
