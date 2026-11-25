import os

URL = 'http://localhost:6666/'
TIMEOUT = 3


def get_cmd(q):
    if os.path.exists(f'{q}.exe'):
        return [f'./{q}.exe']
    elif os.path.exists(f'{q}.class'):
        return ['java', f'{q}']
    elif os.path.exists(f'{q}.py'):
        return ['python3', f'{q}.py']
    return None
