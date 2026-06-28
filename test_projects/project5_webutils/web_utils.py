import json
import re

class api_response_handler_thing:
    def __init__(self):
        self.d = []
        self.c = {}

    def handle_response(self, resp, t):
        if resp == None:
            return {"status": "error", "msg": "No response"}
        if t == "json":
            try:
                d = json.loads(resp)
                self.d.append(d)
                return {"status": "ok", "data": d}
            except:
                return {"status": "error", "msg": "Invalid JSON"}
        elif t == "text":
            self.d.append(resp)
            return {"status": "ok", "data": resp}
        else:
            return {"status": "error", "msg": f"Unknown type: {t}"}

    def get_history(self):
        return self.d

    def clear(self):
        self.d = []
        self.c = {}

    def cache_response(self, k, v):
        self.c[k] = v

    def get_cached(self, k):
        if k in self.c:
            return self.c[k]
        return None


def parse_url(u):
    if u == None:
        return None
    r = {}
    if "://" in u:
        parts = u.split("://")
        r["protocol"] = parts[0]
        rest = parts[1]
    else:
        r["protocol"] = "http"
        rest = u
    if "/" in rest:
        parts = rest.split("/", 1)
        r["host"] = parts[0]
        r["path"] = "/" + parts[1]
    else:
        r["host"] = rest
        r["path"] = "/"
    if "?" in r["path"]:
        parts = r["path"].split("?", 1)
        r["path"] = parts[0]
        r["query"] = parts[1]
    else:
        r["query"] = ""
    return r

def parse_link(u):
    if u == None:
        return None
    r = {}
    if "://" in u:
        parts = u.split("://")
        r["protocol"] = parts[0]
        rest = parts[1]
    else:
        r["protocol"] = "http"
        rest = u
    if "/" in rest:
        parts = rest.split("/", 1)
        r["host"] = parts[0]
        r["path"] = "/" + parts[1]
    else:
        r["host"] = rest
        r["path"] = "/"
    if "?" in r["path"]:
        parts = r["path"].split("?", 1)
        r["path"] = parts[0]
        r["query"] = parts[1]
    else:
        r["query"] = ""
    return r

def build_query_string(d):
    if not d:
        return ""
    parts = []
    for k, v in d.items():
        parts.append(f"{k}={v}")
    return "&".join(parts)

def validate_response(r, schema):
    if not isinstance(r, dict):
        return False, "Response not a dict"
    for k in schema:
        if k not in r:
            return False, f"Missing key: {k}"
        expected_type = schema[k]
        if not isinstance(r[k], expected_type):
            return False, f"Wrong type for {k}: expected {expected_type.__name__}"
    return True, "Valid"

def rate_limiter(requests, max_per_min, window):
    allowed = []
    denied = []
    counts = {}
    for req in requests:
        t = req.get("timestamp", 0)
        bucket = t // window
        if bucket not in counts:
            counts[bucket] = 0
        counts[bucket] += 1
        if counts[bucket] <= max_per_min:
            allowed.append(req)
        else:
            denied.append(req)
    return {"allowed": allowed, "denied": denied, "total": len(requests), "denied_count": len(denied)}

def retry_request(func, max_retries, delay):
    import time
    for i in range(max_retries):
        try:
            r = func()
            return {"success": True, "result": r, "attempts": i + 1}
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(delay)
            else:
                return {"success": False, "error": str(e), "attempts": max_retries}

def sanitize_input(s):
    if s == None:
        return ""
    s = s.strip()
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'[<>"\']', '', s)
    return s

def sanitize_string(s):
    if s == None:
        return ""
    s = s.strip()
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'[<>"\']', '', s)
    return s
