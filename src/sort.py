def bubble_sort(activity):
    # Work on a copy so the original list isn't modified
    arr = list(activity)
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # Wenn in diesem Durchlauf nichts getauscht wurde, ist die Liste sortiert
        if not swapped:
            break

    return arr

