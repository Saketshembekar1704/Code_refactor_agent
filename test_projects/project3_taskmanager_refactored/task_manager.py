import re
import json
from datetime import datetime

class TaskManager:
    """TaskManager class."""

    def __init__(self):
        """__init__ function.

Args: self."""
        self.d = []
        self.c = 0

    def add_task(self, t, p, dl):
        """add_task function.

Args: self, t, p, dl."""
        self.c += 1
        task = {'id': self.c, 'title': t, 'priority': p, 'deadline': dl, 'status': 'pending', 'created': str(datetime.now())}
        self.d.append(task)
        return task

    def remove_task(self, id):
        """remove_task function.

Args: self, id."""
        for i, t in enumerate(self.d):
            if t['id'] == id:
                self.d.pop(i)
                return True
        return False

    def update_status(self, id, s):
        """update_status function.

Args: self, id, s."""
        for t in self.d:
            if t['id'] == id:
                t['status'] = s
                return True
        return False

    def get_by_priority(self, p):
        """get_by_priority function.

Args: self, p."""
        result = []
        for t in self.d:
            if t['priority'] == p:
                result.append(t)
        return result

    def get_by_status(self, s):
        """get_by_status function.

Args: self, s."""
        result = []
        for t in self.d:
            if t['status'] == s:
                result.append(t)
        return result

    def get_overdue(self):
        """get_overdue function.

Args: self."""
        result = []
        now = datetime.now()
        for t in self.d:
            if t['deadline']:
                try:
                    dl = datetime.strptime(t['deadline'], '%Y-%m-%d')
                    if dl < now and t['status'] != 'completed':
                        result.append(t)
                except:
                    pass
        return result

    def count_by_status(self):
        """count_by_status function.

Args: self."""
        result = {}
        for t in self.d:
            s = t['status']
            if s in result:
                result[s] += 1
            else:
                result[s] = 1
        return result

    def to_json(self):
        """to_json function.

Args: self."""
        return json.dumps(self.d)

    def search(self, q):
        """search function.

Args: self, q."""
        result = []
        for t in self.d:
            if q.lower() in t['title'].lower():
                result.append(t)
        return result

def validate_task_input(t, p, dl):
    """validate_task_input function.

Args: t, p, dl."""
    if t == None or t == '':
        return (False, 'Title required')
    if p not in ['low', 'medium', 'high', 'critical']:
        return (False, 'Invalid priority')
    if dl:
        try:
            datetime.strptime(dl, '%Y-%m-%d')
        except:
            return (False, 'Invalid date format')
    return (True, 'Valid')

def format_task(t, fmt):
    """format_task function.

Args: t, fmt."""
    if fmt == 'json':
        return json.dumps(t)
    elif fmt == 'text':
        result = ''
        for k, v in t.items():
            result += f'{k}: {v}\n'
        return result
    elif fmt == 'csv':
        return ','.join((str(v) for v in t.values()))
    else:
        return str(t)

def sort_tasks(data, key, rev):
    """sort_tasks function.

Args: data, key, rev."""
    if key == 'priority':
        p_map = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        return sorted(data, key=lambda value1: p_map.get(value1.get('priority', 'low'), 0), reverse=rev)
    elif key == 'deadline':
        return sorted(data, key=lambda value1: value1.get('deadline', '9999-99-99'), reverse=rev)
    elif key == 'status':
        return sorted(data, key=lambda value1: value1.get('status', ''), reverse=rev)
    else:
        return data

def generate_report(data):
    """generate_report function.

Args: data."""
    result = {'total': len(data), 'pending': 0, 'in_progress': 0, 'completed': 0, 'overdue': 0}
    now = datetime.now()
    for t in data:
        s = t.get('status', 'pending')
        if s == 'pending':
            result['pending'] += 1
        elif s == 'in_progress':
            result['in_progress'] += 1
        elif s == 'completed':
            result['completed'] += 1
        dl = t.get('deadline')
        if dl:
            try:
                deadline = datetime.strptime(dl, '%Y-%m-%d')
                if deadline < now and s != 'completed':
                    result['overdue'] += 1
            except:
                pass
    return result
