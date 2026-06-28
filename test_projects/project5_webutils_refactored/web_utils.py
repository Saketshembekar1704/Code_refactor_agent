import json
import re

class ApiResponseHandlerThing:
    """ApiResponseHandlerThing class."""

    def __init__(self):
        """__init__ function.

Args: self."""
        self.d = []
        self.c = {}

    def handle_response(self, resp, t):
        """handle_response function.

Args: self, resp, t."""
        if resp == None:
            return {'status': 'error', 'msg': 'No response'}
        if t == 'json':
            try:
                data = json.loads(resp)
                self.d.append(data)
                return {'status': 'ok', 'data': data}
            except:
                return {'status': 'error', 'msg': 'Invalid JSON'}
        elif t == 'text':
            self.d.append(resp)
            return {'status': 'ok', 'data': resp}
        else:
            return {'status': 'error', 'msg': f'Unknown type: {t}'}

    def get_history(self):
        """get_history function.

Args: self."""
        return self.d

    def clear(self):
        """clear function.

Args: self."""
        self.d = []
        self.c = {}

    def cache_response(self, k, v):
        """cache_response function.

Args: self, k, v."""
        self.c[k] = v

    def get_cached(self, k):
        """get_cached function.

Args: self, k."""
        if k in self.c:
            return self.c[k]
        return None

def parse_url(user):
    """parse_url function.

Args: user."""
    if user == None:
        return None
    result = {}
    if '://' in user:
        parts = user.split('://')
        result['protocol'] = parts[0]
        rest = parts[1]
    else:
        result['protocol'] = 'http'
        rest = user
    if '/' in rest:
        parts = rest.split('/', 1)
        result['host'] = parts[0]
        result['path'] = '/' + parts[1]
    else:
        result['host'] = rest
        result['path'] = '/'
    if '?' in result['path']:
        parts = result['path'].split('?', 1)
        result['path'] = parts[0]
        result['query'] = parts[1]
    else:
        result['query'] = ''
    return result

def build_query_string(data):
    """build_query_string function.

Args: data."""
    if not data:
        return ''
    parts = []
    for k, v in data.items():
        parts.append(f'{k}={v}')
    return '&'.join(parts)

def validate_response(result, schema):
    """validate_response function.

Args: result, schema."""
    if not isinstance(result, dict):
        return (False, 'Response not a dict')
    for k in schema:
        if k not in result:
            return (False, f'Missing key: {k}')
        expected_type = schema[k]
        if not isinstance(result[k], expected_type):
            return (False, f'Wrong type for {k}: expected {expected_type.__name__}')
    return (True, 'Valid')

def rate_limiter(requests, max_per_min, window):
    """rate_limiter function.

Args: requests, max_per_min, window."""
    allowed = []
    denied = []
    counts = {}
    for req in requests:
        t = req.get('timestamp', 0)
        bucket = t // window
        if bucket not in counts:
            counts[bucket] = 0
        counts[bucket] += 1
        if counts[bucket] <= max_per_min:
            allowed.append(req)
        else:
            denied.append(req)
    return {'allowed': allowed, 'denied': denied, 'total': len(requests), 'denied_count': len(denied)}

def retry_request(func, max_retries, delay):
    """retry_request function.

Args: func, max_retries, delay."""
    import time
    for i in range(max_retries):
        try:
            result = func()
            return {'success': True, 'result': result, 'attempts': i + 1}
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(delay)
            else:
                return {'success': False, 'error': str(e), 'attempts': max_retries}

def sanitize_input(s):
    """sanitize_input function.

Args: s."""
    if s == None:
        return ''
    s = s.strip()
    s = re.sub('<[^>]+>', '', s)
    s = re.sub('[<>"\\\']', '', s)
    return s
