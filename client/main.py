import os
from urllib.request import Request, urlopen
from config import *
import subprocess
import json
from getpass import getpass

TOKEN = ''
TOKEN = input()
SECRET = ''
if not URL.endswith('/'):
    URL = URL+'/'
SECRET = getpass()


def get(url, content=None):
    h = {}
    if SECRET is not None and SECRET != '':
        h['Authorization'] = SECRET
    if TOKEN is not None and TOKEN != '':
        h['Token'] = TOKEN
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
        return (1, '')
    q_in = get_in(q, qn)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    o = None
    try:
        o, _ = proc.communicate(input=q_in, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        return (3, '')
    if proc.returncode != 0:
        return (2, '')
    return (0, o)


def check(q, qn):
    r = run(q, qn)
    if r[0] == 1:
        return 'Skip'
    if get_out(q, qn, r[1]).strip().lower() == "true":
        return 'True'
    return 'False'


def checkall():
    q = get_q()
    a = 0
    b = 0
    for k, v in q:
        print(f'\033[0m{k.center(20, '=')}')
        x = 0
        for _ in range(1, v+1):
            r = check(k, str(_))
            if r == 'True':
                x += 1
                print(f'\033[32mtest{_}: True')
            elif r == 'False':
                print(f'\033[31mtest{_}: False')
            else:
                print(f'\033[34mtest{_}: Skip')
        a += x
        b += v
        print(f'\033[33m{(str(x)+'/'+str(v)).center(20, '=')}')
        print('\033[0m')
    print(f'\033[30;47mFinal: {a}/{b}\033[0m')


if __name__ == '__main__':
    checkall()
