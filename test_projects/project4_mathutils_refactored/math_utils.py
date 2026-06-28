import math
import json

class CalculatorHelperThing:
    """CalculatorHelperThing class."""

    def __init__(self):
        """__init__ function.

Args: self."""
        self.d = []

    def add(self, value1, value2):
        """add function.

Args: self, value1, value2."""
        result = value1 + value2
        self.d.append({'op': 'add', 'a': value1, 'b': value2, 'r': result})
        return result

    def subtract(self, value1, value2):
        """subtract function.

Args: self, value1, value2."""
        result = value1 - value2
        self.d.append({'op': 'sub', 'a': value1, 'b': value2, 'r': result})
        return result

    def multiply(self, value1, value2):
        """multiply function.

Args: self, value1, value2."""
        result = value1 * value2
        self.d.append({'op': 'mul', 'a': value1, 'b': value2, 'r': result})
        return result

    def divide(self, value1, value2):
        """divide function.

Args: self, value1, value2."""
        if value2 == 0:
            return None
        result = value1 / value2
        self.d.append({'op': 'div', 'a': value1, 'b': value2, 'r': result})
        return result

    def power(self, value1, value2):
        """power function.

Args: self, value1, value2."""
        result = value1 ** value2
        self.d.append({'op': 'pow', 'a': value1, 'b': value2, 'r': result})
        return result

    def sqrt(self, value1):
        """sqrt function.

Args: self, value1."""
        if value1 < 0:
            return None
        result = math.sqrt(value1)
        self.d.append({'op': 'sqrt', 'a': value1, 'r': result})
        return result

    def get_history(self):
        """get_history function.

Args: self."""
        return self.d

    def clear_history(self):
        """clear_history function.

Args: self."""
        self.d = []

def compute_average(data):
    """compute_average function.

Args: data."""
    if len(data) == 0:
        return 0
    s = sum(data)
    return s / len(data)

def compute_median(data):
    """compute_median function.

Args: data."""
    if len(data) == 0:
        return 0
    d_sorted = sorted(data)
    n = len(d_sorted)
    if n % 2 == 0:
        return (d_sorted[n // 2 - 1] + d_sorted[n // 2]) / 2
    else:
        return d_sorted[n // 2]

def compute_std_dev(data):
    """compute_std_dev function.

Args: data."""
    if len(data) == 0:
        return 0
    avg = compute_average(data)
    var = sum(((value1 - avg) ** 2 for value1 in data)) / len(data)
    return math.sqrt(var)

def compute_variance(data):
    """compute_variance function.

Args: data."""
    if len(data) == 0:
        return 0
    avg = compute_average(data)
    return sum(((value1 - avg) ** 2 for value1 in data)) / len(data)

def normalize_data(data, method):
    """normalize_data function.

Args: data, method."""
    if len(data) == 0:
        return []
    if method == 'minmax':
        mn = min(data)
        mx = max(data)
        if mx == mn:
            return [0] * len(data)
        return [(value1 - mn) / (mx - mn) for value1 in data]
    elif method == 'zscore':
        avg = compute_average(data)
        std = compute_std_dev(data)
        if std == 0:
            return [0] * len(data)
        return [(value1 - avg) / std for value1 in data]
    else:
        return data

def is_prime(n):
    """is_prime function.

Args: n."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def fibonacci(n):
    """fibonacci function.

Args: n."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    result = [0, 1]
    for i in range(2, n):
        result.append(result[i - 1] + result[i - 2])
    return result

def factorial(n):
    """factorial function.

Args: n."""
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def matrix_multiply(value1, value2):
    """matrix_multiply function.

Args: value1, value2."""
    if len(value1[0]) != len(value2):
        return None
    result = [[0] * len(value2[0]) for _ in range(len(value1))]
    for i in range(len(value1)):
        for j in range(len(value2[0])):
            for k in range(len(value2)):
                result[i][j] += value1[i][k] * value2[k][j]
    return result

def format_result(data, fmt):
    """format_result function.

Args: data, fmt."""
    if fmt == 'json':
        return json.dumps(data)
    elif fmt == 'text':
        return str(data)
    elif fmt == 'csv':
        if isinstance(data, list):
            return ','.join((str(value1) for value1 in data))
        return str(data)
    else:
        return str(data)
