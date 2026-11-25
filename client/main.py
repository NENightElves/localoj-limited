import os
from urllib.request import Request, urlopen
from config import *
import subprocess
import json
from getpass import getpass

SECRET = ''
if not URL.endswith('/'):
    URL = URL+'/'
SECRET = getpass()


def get(url, content=None):
    h = {}
    if SECRET is not None and SECRET != '':
        h['Authorization'] = SECRET
    r = None
    if content is None:
        r = Request(url, headers=h, method='GET')
    else:
        r = Request(url, content.encode(), headers=h, method='POST')
    result = None
    with urlopen(r) as f:
        result = f.read().decode('utf-8')
    return result


def get_q():
    return json.loads(get(URL + 'qsize'))


def get_in(p1, p2):
    return get(URL + 'in/' + p1 + '/' + p2)


def get_out(p1, p2, out):
    return get(URL + 'out/' + p1 + '/' + p2, out)


def run(q, qn):
    cmd = get_cmd(q)
    if cmd is None:
        return None
    q_in = get_in(q, qn)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    o = None
    try:
        o, _ = proc.communicate(input=q_in, timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        return None
    if proc.returncode != 0:
        return None
    return o


def check(q, qn):
    r = run(q, qn)
    if r is None:
        return False
    if get_out(q, qn, r).strip().lower() == "true":
        return True
    return False


def checkall():
    q = get_q()
    a = 0
    b = 0
    for k, (v, prefix) in q.items():
        print(f'\033[0m{k.center(20, '=')}')
        x = 0
        for _ in range(1, v+1):
            r = check(k, str(_))
            if r:
                x += 1
                print(f'\033[32mtest{_}: True')
            else:
                print(f'\033[31mtest{_}: False')
        a += x
        b += v
        print(f'\033[34m{(str(x)+'/'+str(v)).center(20, '=')}')
        print('\033[0m')
    print(f'\033[30;47mFinal: {a}/{b}\033[0m')


if __name__ == '__main__':
    checkall()
