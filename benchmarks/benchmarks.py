import time
import json
import random

def fib_recursive(n):
    """
    Calculate the nth Fibonacci number using a recursive approach.

    Parameters:
        n (int): The position in the Fibonacci sequence (must be a non-negative integer).

    Returns:
        int: The nth Fibonacci number.

    Raises:
        RecursionError: If the maximum recursion depth is exceeded for large n.
        TypeError: If n is not an integer.
        ValueError: If n is negative.

    Example:
        >>> fib_recursive(5)
        5
    """
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)

def manual_sort(lst):
    """
    Sorts a list in ascending order using the bubble sort algorithm.
    Args:
        lst (list): The list of elements to be sorted. Elements must be comparable.
    Returns:
        list: The sorted list in ascending order.
    Example:
        >>> manual_sort([3, 1, 2])
        [1, 2, 3]
    """
    n = len(lst)

    for i in range(n):

        for j in range(0, n-i-1):

            if lst[j] > lst[j+1]:

                lst[j], lst[j+1] = lst[j+1], lst[j]

    return lst

def sum_large_list(lst):
    """
    Calculates the sum of all elements in a given list.
    Args:
        lst (list of numbers): The list of numbers to sum.
    Returns:
        int or float: The total sum of all elements in the list.
    """

    total = 0

    for num in lst:

        total += num

    return total

def matrix_multiplication(size):
    """
    Performs matrix multiplication of two randomly generated square matrices of the given size.
    Args:
        size (int): The number of rows and columns for the square matrices.
    Returns:
        list[list[int]]: The resulting matrix after multiplying two randomly generated matrices.
    """


    A = [[random.random() for _ in range(size)] for _ in range(size)]
    B = [[random.random() for _ in range(size)] for _ in range(size)]
    result = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):

        for j in range(size):

            for k in range(size):

                result[i][j] += int(A[i][k] * B[k][j])

    return result

def string_concat(n):
    """
    Concatenates the string representations of integers from 0 to n-1.
    Args:
        n (int): The number of integers to concatenate.
    Returns:
        str: A single string containing the concatenated string representations of integers from 0 to n-1.
    """

    s = ""

    for i in range(n):

        s += str(i)

    return s

def benchmark():
    """
    Runs a series of benchmark tests on various algorithms and prints the results as a JSON object.
    The benchmarks include:
        - Recursive Fibonacci calculation for different input sizes.
        - Manual sorting of lists with varying lengths.
        - Summing elements of large lists.
        - Multiplication of square matrices of different sizes.
        - String concatenation for different string lengths.
    Each benchmark records the input size and the time taken to execute the corresponding function.
    Returns:
        None. Prints the benchmark results as a formatted JSON string.
    """

    results = dict()

    # Fibonacci
    fib_inputs = [10, 15, 20, 30, 35]

    results['fibonacci'] = []

    for n in fib_inputs:

        start = time.time()
        fib_recursive(n)
        end = time.time()
        results['fibonacci'].append({'input': n, 'time': end - start})

    # Manual sort
    sort_sizes = [10, 100, 1000, 10000, 50000]
    results['manual_sort'] = []

    for size in sort_sizes:

        lst = [random.randint(0, 10000) for _ in range(size)]
        start = time.time()
        manual_sort(lst)
        end = time.time()
        results['manual_sort'].append({'input': size, 'time': end - start})

    # Sum large list
    sum_sizes = [10**2, 10**3, 10**4, 10**5, (10**5)*2]
    results['sum_large_list'] = []

    for size in sum_sizes:

        lst = [random.randint(0, 100) for _ in range(size)]
        start = time.time()
        sum_large_list(lst)
        end = time.time()
        results['sum_large_list'].append({'input': size, 'time': end - start})

    # Matrix multiplication
    matrix_sizes = [10, 20, 25, 30, 35]
    results['matrix_multiplication'] = []

    for size in matrix_sizes:

        start = time.time()
        matrix_multiplication(size)
        end = time.time()
        results['matrix_multiplication'].append({'input': size, 'time': end - start})

    # String concatenation
    concat_sizes = [1000, 5000, 10000, 30000, 40000]
    results['string_concat'] = []

    for size in concat_sizes:

        start = time.time()
        string_concat(size)
        end = time.time()
        results['string_concat'].append({'input': size, 'time': end - start})
    
    print(json.dumps(results, indent=4))

if __name__ == "__main__":

    benchmark()
