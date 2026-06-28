import re
import json
from datetime import datetime

class task_manager_class_thing:
    def __init__(self):
        self.d = []
        self.c = 0

    def add_task(self, t, p, dl):
        self.c += 1
        task = {"id": self.c, "title": t, "priority": p, "deadline": dl, "status": "pending", "created": str(datetime.now())}
        self.d.append(task)
        return task

    def remove_task(self, id):
        for i, t in enumerate(self.d):
            if t["id"] == id:
                self.d.pop(i)
                return True
        return False

    def update_status(self, id, s):
        for t in self.d:
            if t["id"] == id:
                t["status"] = s
                return True
        return False

    def get_by_priority(self, p):
        r = []
        for t in self.d:
            if t["priority"] == p:
                r.append(t)
        return r

    def get_by_status(self, s):
        r = []
        for t in self.d:
            if t["status"] == s:
                r.append(t)
        return r

    def get_overdue(self):
        r = []
        now = datetime.now()
        for t in self.d:
            if t["deadline"]:
                try:
                    dl = datetime.strptime(t["deadline"], "%Y-%m-%d")
                    if dl < now and t["status"] != "completed":
                        r.append(t)
                except:
                    pass
        return r

    def count_by_status(self):
        r = {}
        for t in self.d:
            s = t["status"]
            if s in r:
                r[s] += 1
            else:
                r[s] = 1
        return r

    def to_json(self):
        return json.dumps(self.d)

    def search(self, q):
        r = []
        for t in self.d:
            if q.lower() in t["title"].lower():
                r.append(t)
        return r


def validate_task_input(t, p, dl):
    if t == None or t == "":
        return False, "Title required"
    if p not in ["low", "medium", "high", "critical"]:
        return False, "Invalid priority"
    if dl:
        try:
            datetime.strptime(dl, "%Y-%m-%d")
        except:
            return False, "Invalid date format"
    return True, "Valid"

def check_task_input(t, p, dl):
    if t == None or t == "":
        return False, "Title required"
    if p not in ["low", "medium", "high", "critical"]:
        return False, "Invalid priority"
    if dl:
        try:
            datetime.strptime(dl, "%Y-%m-%d")
        except:
            return False, "Invalid date format"
    return True, "Valid"

def format_task(t, fmt):
    if fmt == "json":
        return json.dumps(t)
    elif fmt == "text":
        r = ""
        for k, v in t.items():
            r += f"{k}: {v}\n"
        return r
    elif fmt == "csv":
        return ",".join(str(v) for v in t.values())
    else:
        return str(t)

def sort_tasks(d, key, rev):
    if key == "priority":
        p_map = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        return sorted(d, key=lambda x: p_map.get(x.get("priority", "low"), 0), reverse=rev)
    elif key == "deadline":
        return sorted(d, key=lambda x: x.get("deadline", "9999-99-99"), reverse=rev)
    elif key == "status":
        return sorted(d, key=lambda x: x.get("status", ""), reverse=rev)
    else:
        return d

def generate_report(d):
    r = {"total": len(d), "pending": 0, "in_progress": 0, "completed": 0, "overdue": 0}
    now = datetime.now()
    for t in d:
        s = t.get("status", "pending")
        if s == "pending":
            r["pending"] += 1
        elif s == "in_progress":
            r["in_progress"] += 1
        elif s == "completed":
            r["completed"] += 1
        dl = t.get("deadline")
        if dl:
            try:
                deadline = datetime.strptime(dl, "%Y-%m-%d")
                if deadline < now and s != "completed":
                    r["overdue"] += 1
            except:
                pass
    return r
