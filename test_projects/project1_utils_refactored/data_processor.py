import os
import json
import csv
import re

def calc(value1, value2, value1):
    """calc function.

Args: value1, value2, value1."""
    if value1 == True:
        result = value1 + value2
    else:
        result = value1 - value2
    return result

class UserManager:
    """UserManager class."""

    def __init__(self):
        """__init__ function.

Args: self."""
        self.d = []
        self.u = []

    def process_data(self, data):
        """process_data function.

Args: self, data."""
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(item.strip().lower())
            elif isinstance(item, int):
                result.append(item * 2)
        return result

    def add(self, user):
        """add function.

Args: self, user."""
        self.u.append(user)
        return True

    def remove(self, user):
        """remove function.

Args: self, user."""
        if user in self.u:
            self.u.remove(user)
            return True
        return False

    def get_all(self):
        """get_all function.

Args: self."""
        return self.u

    def count(self):
        """count function.

Args: self."""
        return len(self.u)

def validate_email(value1):
    """validate_email function.

Args: value1."""
    if value1 == None:
        return False
    if '@' in value1:
        if '.' in value1:
            return True
        else:
            return False
    else:
        return False

def read_data(p):
    """read_data function.

Args: p."""
    f = open(p, 'r')
    data = f.read()
    f.close()
    return data

def parse_csv_data(p):
    """parse_csv_data function.

Args: p."""
    result = []
    f = open(p, 'r')
    reader = csv.reader(f)
    for row in reader:
        result.append(row)
    f.close()
    return result

def transform_records(data, t, f):
    """transform_records function.

Args: data, t, f."""
    result = []
    for item in data:
        if t == 'upper':
            if isinstance(item, str):
                result.append(item.upper())
            elif isinstance(item, list):
                temp = []
                for sub in item:
                    if isinstance(sub, str):
                        temp.append(sub.upper())
                    else:
                        temp.append(sub)
                result.append(temp)
            else:
                result.append(item)
        elif t == 'lower':
            if isinstance(item, str):
                result.append(item.lower())
            elif isinstance(item, list):
                temp = []
                for sub in item:
                    if isinstance(sub, str):
                        temp.append(sub.lower())
                    else:
                        temp.append(sub)
                result.append(temp)
            else:
                result.append(item)
        elif t == 'strip':
            if isinstance(item, str):
                result.append(item.strip())
            else:
                result.append(item)
        else:
            result.append(item)
    if f == True:
        result = [value1 for value1 in result if value1]
    return result

def compute_stats(data):
    """compute_stats function.

Args: data."""
    if len(data) == 0:
        return {}
    s = sum(data)
    avg = s / len(data)
    mn = min(data)
    mx = max(data)
    rng = mx - mn
    var = sum(((value1 - avg) ** 2 for value1 in data)) / len(data)
    return {'sum': s, 'avg': avg, 'min': mn, 'max': mx, 'range': rng, 'variance': var}

def format_output(data, fmt):
    """format_output function.

Args: data, fmt."""
    if fmt == 'json':
        return json.dumps(data)
    elif fmt == 'csv':
        result = ''
        for k, v in data.items():
            result += f'{k},{v}\n'
        return result
    elif fmt == 'text':
        result = ''
        for k, v in data.items():
            result += f'{k}: {v}\n'
        return result
    else:
        return str(data)
