def bubble_sort(activity):
    n = len(activity)

    for i in range(n):
        swapped = False
        for j in range (0, n - i - 1):
            if activity[j] > activity[j+1]:
                activity[j], activity[j+1] = activity[j+1], activity[j]
                swapped = True
            if not swapped:
                break
    return activity

