import os
import matplotlib.pyplot as plt
from load_data import load_data
from sort import bubble_sort 

# Daten laden und Power-Werte extrahieren
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '..', 'data', 'activity.csv')
data = load_data(data_path)
power_values = list(data["PowerOriginal"])

# Sortieren 
sorted_power_values = bubble_sort(power_values)
sorted_power_values_desc = sorted_power_values[::-1]  # Umkehren, dass ses absteigend sortiert 

# X-Achse: 0 bis len 
x_values = list(range(len(sorted_power_values_desc)))

# Plot
plt.figure(figsize=(10, 6))
plt.plot(x_values, sorted_power_values_desc, label="Power (sortiert)", color='blue', linestyle='solid', linewidth=1.5, markersize=4)
plt.xlabel("Zeit (s)")
plt.ylabel("Kraft (W)")
plt.grid(True, alpha=0.3)
plt.title('Leistungskurve')
plt.legend(loc="upper right")
plt.tight_layout()
plt.fill_between(x_values, sorted_power_values_desc, color='blue', alpha=0.1)  # Füllt den Bereich unter der Kurve
plt.show()