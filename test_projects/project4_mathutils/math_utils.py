import math
import json

class calculator_helper_thing:
    def __init__(self):
        self.d = []

    def add(self, a, b):
        r = a + b
        self.d.append({"op": "add", "a": a, "b": b, "r": r})
        return r

    def subtract(self, a, b):
        r = a - b
        self.d.append({"op": "sub", "a": a, "b": b, "r": r})
        return r

    def multiply(self, a, b):
        r = a * b
        self.d.append({"op": "mul", "a": a, "b": b, "r": r})
        return r

    def divide(self, a, b):
        if b == 0:
            return None
        r = a / b
        self.d.append({"op": "div", "a": a, "b": b, "r": r})
        return r

    def power(self, a, b):
        r = a ** b
        self.d.append({"op": "pow", "a": a, "b": b, "r": r})
        return r

    def sqrt(self, a):
        if a < 0:
            return None
        r = math.sqrt(a)
        self.d.append({"op": "sqrt", "a": a, "r": r})
        return r

    def get_history(self):
        return self.d

    def clear_history(self):
        self.d = []

def compute_average(d):
    if len(d) == 0:
        return 0
    s = sum(d)
    return s / len(d)

def compute_mean(d):
    if len(d) == 0:
        return 0
    s = sum(d)
    return s / len(d)

def compute_median(d):
    if len(d) == 0:
        return 0
    d_sorted = sorted(d)
    n = len(d_sorted)
    if n % 2 == 0:
        return (d_sorted[n//2 - 1] + d_sorted[n//2]) / 2
    else:
        return d_sorted[n//2]

def compute_std_dev(d):
    if len(d) == 0:
        return 0
    avg = compute_average(d)
    var = sum((x - avg) ** 2 for x in d) / len(d)
    return math.sqrt(var)

def compute_variance(d):
    if len(d) == 0:
        return 0
    avg = compute_average(d)
    return sum((x - avg) ** 2 for x in d) / len(d)

def normalize_data(d, method):
    if len(d) == 0:
        return []
    if method == "minmax":
        mn = min(d)
        mx = max(d)
        if mx == mn:
            return [0] * len(d)
        return [(x - mn) / (mx - mn) for x in d]
    elif method == "zscore":
        avg = compute_average(d)
        std = compute_std_dev(d)
        if std == 0:
            return [0] * len(d)
        return [(x - avg) / std for x in d]
    else:
        return d

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def check_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def fibonacci(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]
    r = [0, 1]
    for i in range(2, n):
        r.append(r[i-1] + r[i-2])
    return r

def factorial(n):
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r

def matrix_multiply(a, b):
    if len(a[0]) != len(b):
        return None
    r = [[0] * len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                r[i][j] += a[i][k] * b[k][j]
    return r

def format_result(d, fmt):
    if fmt == "json":
        return json.dumps(d)
    elif fmt == "text":
        return str(d)
    elif fmt == "csv":
        if isinstance(d, list):
            return ",".join(str(x) for x in d)
        return str(d)
    else:
        return str(d)
