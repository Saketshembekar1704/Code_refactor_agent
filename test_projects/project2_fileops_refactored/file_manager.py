import os
import re
import hashlib

class FileHandlerThing:
    """FileHandlerThing class."""

    def __init__(self, p):
        """__init__ function.

Args: self, p."""
        self.p = p
        self.d = {}

    def read(self, f):
        """read function.

Args: self, f."""
        fp = os.path.join(self.p, f)
        h = open(fp, 'r')
        c = h.read()
        h.close()
        return c

    def write(self, f, c):
        """write function.

Args: self, f, c."""
        fp = os.path.join(self.p, f)
        h = open(fp, 'w')
        h.write(c)
        h.close()
        return True

    def delete(self, f):
        """delete function.

Args: self, f."""
        fp = os.path.join(self.p, f)
        if os.path.exists(fp):
            os.remove(fp)
            return True
        return False

    def list_files(self):
        """list_files function.

Args: self."""
        result = []
        for f in os.listdir(self.p):
            if os.path.isfile(os.path.join(self.p, f)):
                result.append(f)
        return result

    def get_size(self, f):
        """get_size function.

Args: self, f."""
        fp = os.path.join(self.p, f)
        if os.path.exists(fp):
            return os.path.getsize(fp)
        return -1

    def search(self, pattern, f):
        """search function.

Args: self, pattern, f."""
        c = self.read(f)
        result = re.findall(pattern, c)
        return result

    def replace(self, old, new, f):
        """replace function.

Args: self, old, new, f."""
        c = self.read(f)
        c = c.replace(old, new)
        self.write(f, c)
        return True

    def count_lines(self, f):
        """count_lines function.

Args: self, f."""
        c = self.read(f)
        return len(c.split('\n'))

    def get_hash(self, f):
        """get_hash function.

Args: self, f."""
        c = self.read(f)
        return hashlib.md5(c.encode()).hexdigest()

def process_path(p):
    """process_path function.

Args: p."""
    if p == None:
        return None
    if os.path.isabs(p):
        return p
    else:
        return os.path.abspath(p)

def count_files(p, ext):
    """count_files function.

Args: p, ext."""
    result = 0
    for root, dirs, files in os.walk(p):
        for f in files:
            if ext:
                if f.endswith(ext):
                    result += 1
            else:
                result += 1
    return result

def batch_rename(p, prefix, ext):
    """batch_rename function.

Args: p, prefix, ext."""
    result = []
    c = 0
    for f in os.listdir(p):
        if f.endswith(ext):
            old = os.path.join(p, f)
            new = os.path.join(p, f'{prefix}_{c}{ext}')
            os.rename(old, new)
            result.append({'old': f, 'new': f'{prefix}_{c}{ext}'})
            c += 1
    return result

def find_duplicates(p):
    """find_duplicates function.

Args: p."""
    data = {}
    result = []
    for root, dirs, files in os.walk(p):
        for f in files:
            fp = os.path.join(root, f)
            try:
                h = open(fp, 'rb')
                content = h.read()
                h.close()
                hash_val = hashlib.md5(content).hexdigest()
                if hash_val in data:
                    result.append({'file1': data[hash_val], 'file2': fp, 'hash': hash_val})
                else:
                    data[hash_val] = fp
            except:
                pass
    return result

class LogWriterThing:
    """LogWriterThing class."""

    def __init__(self, p):
        """__init__ function.

Args: self, p."""
        self.p = p
        self.d = []

    def log(self, msg, lvl):
        """log function.

Args: self, msg, lvl."""
        entry = {'msg': msg, 'lvl': lvl}
        self.d.append(entry)
        h = open(self.p, 'a')
        h.write(f'[{lvl}] {msg}\n')
        h.close()

    def get_logs(self, lvl):
        """get_logs function.

Args: self, lvl."""
        result = []
        for entry in self.d:
            if entry['lvl'] == lvl:
                result.append(entry)
        return result

    def clear(self):
        """clear function.

Args: self."""
        self.d = []
        h = open(self.p, 'w')
        h.write('')
        h.close()

    def count(self, lvl):
        """count function.

Args: self, lvl."""
        c = 0
        for entry in self.d:
            if entry['lvl'] == lvl:
                c += 1
        return c
