import time
import json
import random
import os

def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)

def manual_sort(lst):
    # Simple bubble sort
    n = len(lst)
    for i in range(n):
        for j in range(0, n-i-1):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst

def sum_large_list(lst):
    total = 0
    for num in lst:
        total += num
    return total

def matrix_multiplication(size):
    A = [[random.random() for _ in range(size)] for _ in range(size)]
    B = [[random.random() for _ in range(size)] for _ in range(size)]
    result = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += A[i][k] * B[k][j]
    return result

def string_concat(n):
    s = ""
    for i in range(n):
        s += str(i)
    return s

def benchmark():
    results = {}

    # Fibonacci
    fib_inputs = [10, 20, 25]
    results['fibonacci'] = []
    for n in fib_inputs:
        start = time.time()
        fib_recursive(n)
        end = time.time()
        results['fibonacci'].append({'input': n, 'time': end - start})

    # Manual sort
    sort_sizes = [100, 500, 1000]
    results['manual_sort'] = []
    for size in sort_sizes:
        lst = [random.randint(0, 10000) for _ in range(size)]
        start = time.time()
        manual_sort(lst)
        end = time.time()
        results['manual_sort'].append({'input': size, 'time': end - start})

    # Sum large list
    sum_sizes = [10**5, 5*10**5, 10**6]
    results['sum_large_list'] = []
    for size in sum_sizes:
        lst = [random.randint(0, 100) for _ in range(size)]
        start = time.time()
        sum_large_list(lst)
        end = time.time()
        results['sum_large_list'].append({'input': size, 'time': end - start})

    # Matrix multiplication
    matrix_sizes = [10, 20, 30]
    results['matrix_multiplication'] = []
    for size in matrix_sizes:
        start = time.time()
        matrix_multiplication(size)
        end = time.time()
        results['matrix_multiplication'].append({'input': size, 'time': end - start})

    # String concatenation
    concat_sizes = [1000, 5000, 10000]
    results['string_concat'] = []
    for size in concat_sizes:
        start = time.time()
        string_concat(size)
        end = time.time()
        results['string_concat'].append({'input': size, 'time': end - start})

    # Save to JSON
    os.makedirs('benchmarks/results', exist_ok=True)
    
    print(json.dump(results, indent=4))

if __name__ == "__main__":
    benchmark()