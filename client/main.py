import os
from urllib.request import Request, urlopen
from config import *
import subprocess
import json

SECRET = ''
if not URL.endswith('/'):
    URL = URL+'/'
SECRET = input()


def get(p1=None, p2=None):
    if p1 is None and p2 is None:
        url = URL+'qsize'
    elif p1 is not None and p2 is not None:
        url = URL+'testcases'+'/'+p1+'/'+p2
    else:
        return None
    r = Request(url, headers={'Authorization': SECRET}, method='GET')
    content = ''
    with urlopen(r) as f:
        content = f.read().decode('utf-8')
    return content


def get_q():
    return json.loads(get())


def get_in(p1, p2, prefix=''):
    return get(p1, prefix+str(p2)+'.in')


def get_out(p1, p2, prefix=''):
    return get(p1, prefix+str(p2)+'.out')


def run(q, q_in):
    cmd = get_cmd(q)
    if cmd is None:
        return None
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    o = None
    try:
        o, _ = proc.communicate(input=q_in, timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
    if proc.returncode != 0:
        return None
    return o


def check(q, q_in, q_out):
    r = run(q, q_in)
    if r is None:
        return False
    if r.strip() == q_out.strip():
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
            q_in = get_in(k, str(_), prefix)
            q_out = get_out(k, str(_), prefix)
            r = check(k, q_in, q_out)
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
