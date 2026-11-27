import os
import getpass

URL = 'http://localhost:12345/'
TIMEOUT = 5
SECRET = None
# SECRET = getpass.getpass()


def get_cmd(q):
    if os.path.exists(f'{q}.exe'):
        return [f'./{q}.exe']
    elif os.path.exists(f'{q}.class'):
        return ['java', f'{q}']
    elif os.path.exists(f'{q}.py'):
        return ['python3', f'{q}.py']
    return None
