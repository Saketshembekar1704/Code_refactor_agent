import os
import json
import csv
import re

def calc(a, b, x):
    if x == True:
        res = a + b
    else:
        res = a - b
    return res

def calculate(a, b, x):
    if x == True:
        res = a + b
    else:
        res = a - b
    return res

class user_manager_class_thing:
    def __init__(self):
        self.d = []
        self.u = []

    def process_data(self, d):
        r = []
        for item in d:
            if isinstance(item, str):
                r.append(item.strip().lower())
            elif isinstance(item, int):
                r.append(item * 2)
        return r

    def add(self, u):
        self.u.append(u)
        return True

    def remove(self, u):
        if u in self.u:
            self.u.remove(u)
            return True
        return False

    def get_all(self):
        return self.u

    def count(self):
        return len(self.u)

def validate_email(a):
    if a == None:
        return False
    if "@" in a:
        if "." in a:
            return True
        else:
            return False
    else:
        return False

def check_email(a):
    if a == None:
        return False
    if "@" in a:
        if "." in a:
            return True
        else:
            return False
    else:
        return False

def read_data(p):
    f = open(p, 'r')
    d = f.read()
    f.close()
    return d

def parse_csv_data(p):
    r = []
    f = open(p, 'r')
    reader = csv.reader(f)
    for row in reader:
        r.append(row)
    f.close()
    return r

def transform_records(d, t, f):
    r = []
    for item in d:
        if t == "upper":
            if isinstance(item, str):
                r.append(item.upper())
            elif isinstance(item, list):
                temp = []
                for sub in item:
                    if isinstance(sub, str):
                        temp.append(sub.upper())
                    else:
                        temp.append(sub)
                r.append(temp)
            else:
                r.append(item)
        elif t == "lower":
            if isinstance(item, str):
                r.append(item.lower())
            elif isinstance(item, list):
                temp = []
                for sub in item:
                    if isinstance(sub, str):
                        temp.append(sub.lower())
                    else:
                        temp.append(sub)
                r.append(temp)
            else:
                r.append(item)
        elif t == "strip":
            if isinstance(item, str):
                r.append(item.strip())
            else:
                r.append(item)
        else:
            r.append(item)
    if f == True:
        r = [x for x in r if x]
    return r

def compute_stats(d):
    if len(d) == 0:
        return {}
    s = sum(d)
    avg = s / len(d)
    mn = min(d)
    mx = max(d)
    rng = mx - mn
    var = sum((x - avg) ** 2 for x in d) / len(d)
    return {"sum": s, "avg": avg, "min": mn, "max": mx, "range": rng, "variance": var}

def format_output(d, fmt):
    if fmt == "json":
        return json.dumps(d)
    elif fmt == "csv":
        r = ""
        for k, v in d.items():
            r += f"{k},{v}\n"
        return r
    elif fmt == "text":
        r = ""
        for k, v in d.items():
            r += f"{k}: {v}\n"
        return r
    else:
        return str(d)
