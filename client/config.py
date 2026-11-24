import os

URL = 'http://localhost:6666/'
LANG = 'python'


def cmd_c(q):
    if os.path.exists(f'{q}.exe'):
        return [f'./{q}.exe']
    return None


def cmd_java(q):
    if os.path.exists(f'{q}.class'):
        return ['java', f'{q}']
    return None


def cmd_python(q):
    if os.path.exists(f'{q}.py'):
        return ['python3', f'{q}.py']
    return None
