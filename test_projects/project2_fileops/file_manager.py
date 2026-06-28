import os
import re
import hashlib

class file_handler_thing:
    def __init__(self, p):
        self.p = p
        self.d = {}

    def read(self, f):
        fp = os.path.join(self.p, f)
        h = open(fp, 'r')
        c = h.read()
        h.close()
        return c

    def write(self, f, c):
        fp = os.path.join(self.p, f)
        h = open(fp, 'w')
        h.write(c)
        h.close()
        return True

    def delete(self, f):
        fp = os.path.join(self.p, f)
        if os.path.exists(fp):
            os.remove(fp)
            return True
        return False

    def list_files(self):
        r = []
        for f in os.listdir(self.p):
            if os.path.isfile(os.path.join(self.p, f)):
                r.append(f)
        return r

    def get_size(self, f):
        fp = os.path.join(self.p, f)
        if os.path.exists(fp):
            return os.path.getsize(fp)
        return -1

    def search(self, pattern, f):
        c = self.read(f)
        r = re.findall(pattern, c)
        return r

    def replace(self, old, new, f):
        c = self.read(f)
        c = c.replace(old, new)
        self.write(f, c)
        return True

    def count_lines(self, f):
        c = self.read(f)
        return len(c.split('\n'))

    def get_hash(self, f):
        c = self.read(f)
        return hashlib.md5(c.encode()).hexdigest()


def process_path(p):
    if p == None:
        return None
    if os.path.isabs(p):
        return p
    else:
        return os.path.abspath(p)

def process_filepath(p):
    if p == None:
        return None
    if os.path.isabs(p):
        return p
    else:
        return os.path.abspath(p)

def count_files(p, ext):
    r = 0
    for root, dirs, files in os.walk(p):
        for f in files:
            if ext:
                if f.endswith(ext):
                    r += 1
            else:
                r += 1
    return r

def batch_rename(p, prefix, ext):
    r = []
    c = 0
    for f in os.listdir(p):
        if f.endswith(ext):
            old = os.path.join(p, f)
            new = os.path.join(p, f"{prefix}_{c}{ext}")
            os.rename(old, new)
            r.append({"old": f, "new": f"{prefix}_{c}{ext}"})
            c += 1
    return r

def find_duplicates(p):
    d = {}
    r = []
    for root, dirs, files in os.walk(p):
        for f in files:
            fp = os.path.join(root, f)
            try:
                h = open(fp, 'rb')
                content = h.read()
                h.close()
                hash_val = hashlib.md5(content).hexdigest()
                if hash_val in d:
                    r.append({"file1": d[hash_val], "file2": fp, "hash": hash_val})
                else:
                    d[hash_val] = fp
            except:
                pass
    return r

class log_writer_thing:
    def __init__(self, p):
        self.p = p
        self.d = []

    def log(self, msg, lvl):
        entry = {"msg": msg, "lvl": lvl}
        self.d.append(entry)
        h = open(self.p, 'a')
        h.write(f"[{lvl}] {msg}\n")
        h.close()

    def get_logs(self, lvl):
        r = []
        for entry in self.d:
            if entry["lvl"] == lvl:
                r.append(entry)
        return r

    def clear(self):
        self.d = []
        h = open(self.p, 'w')
        h.write('')
        h.close()

    def count(self, lvl):
        c = 0
        for entry in self.d:
            if entry["lvl"] == lvl:
                c += 1
        return c
