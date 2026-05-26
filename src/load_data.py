import numpy as np
from sort import bubble_sort
import matplotlib.pyplot as plt
import os

def load_data(file_path):

    # Specify the file path
    #file_path = 'activity.csv'

    # Use numpy.genfromtxt to read the CSV data from the file into a NumPy array
    data_array = np.genfromtxt(file_path, delimiter=',', dtype=None, names=True)

    # Transpose the array to have each column in a separate NumPy array
    column_names = data_array.dtype.names
    column_arrays = {column: data_array[column] for column in column_names}

    # Print each column
    #for column, array in column_arrays.items():
    #    print(f"{column}: {array}")

    return column_arrays



if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'data', 'activity.csv')
    data = load_data(data_path)
    power_W = data['PowerOriginal']
    print(power_W)
    sorted_power_W = bubble_sort(power_W)
    print(sorted_power_W[::-1])
  