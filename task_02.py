def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            upper_bound = arr[mid]
            high = mid - 1
        else:
            return (iterations, arr[mid])

    if low < len(arr):
        upper_bound = arr[low]

    return (iterations, upper_bound)

arr = [1.2, 2.5, 3.8, 4.6, 5.9, 7.3, 8.1]

def run_tests():
    numbers = [-1.0, 2.0, 4.6, 9.5]

    for number in numbers:
        print(f"Result for searching {number} number:")
        result = binary_search(arr, number)
        print(result)

if __name__ == "__main__":
    run_tests()