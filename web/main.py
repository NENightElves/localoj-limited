import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from config import *
import json

result = {}
rlock = threading.Lock()
tokens = {}
if os.path.exists('result.json'):
    with open('result.json', 'r') as f:
        result = json.loads(f.read())
if os.path.exists('tokens.txt'):
    with open('tokens.txt', 'r') as f:
        for _ in f:
            t = _.strip().split()
            tokens[t[0]] = ' '.join(t[1:])
template = ''
with open('dashboard.html', 'r') as f:
    template = f.read()


class WebHandler(BaseHTTPRequestHandler):

    def _send_error(self):
        self.send_error(404)

    def _send(self, content):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def do_GET(self):
        path = self.path.strip('/').split('/')
        if len(path) < 1:
            self._send_error()
            return
        if path[0] == 'in':
            if SECRET != None and self.headers.get('Authorization', '') != SECRET:
                self._send_error()
                return
            if len(path) != 3:
                self._send_error()
                return
            realpath = os.path.join('.', path[1], QUESTIONS_PREFIX[path[1]] + path[2]+'.in')
            if not os.path.exists(realpath):
                self._send_error()
                return
            content = ''
            with open(realpath, 'r') as f:
                content = f.read()
            self._send(content)
            return
        elif path[0] == 'qsize':
            if SECRET != None and self.headers.get('Authorization', '') != SECRET:
                self._send_error()
                return
            if len(path) != 1:
                self._send_error()
                return
            content = json.dumps(QUESTIONS)
            self._send(content)
            return
        elif path[0] == "dashboard":
            t = None
            with rlock:
                with open('result.json', 'r') as f:
                    t = json.loads(f.read())
            q = []
            for _ in QUESTIONS:
                q.append(_[0])
            for k, v in t.items():
                s = 0
                for _ in q:
                    s += sum(v[_])
                    v['sum'] = s
                    v['num'] = v['t'] + v['f']
            sq = json.dumps(q)
            sp = json.dumps(sorted(list(t.values()), key=lambda x: (-x['sum'], x['num'])))
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(template.replace('{{ Q }}', sq).replace('{{ P }}', sp).encode())
            return
        self._send_error()

    def do_POST(self):
        path = self.path.strip('/').split('/')
        if len(path) < 1:
            self._send_error()
            return
        if path[0] == 'out':
            token = self.headers.get('Token', '')
            if len(tokens) > 0 and token not in tokens:
                self._send_error()
                return
            if SECRET != None and self.headers.get('Authorization', '') != SECRET:
                self._send_error()
                return
            if len(path) != 3:
                self._send_error()
                return
            realpath = os.path.join('.', path[1], QUESTIONS_PREFIX[path[1]] + path[2]+'.out')
            if not os.path.exists(realpath):
                self._send_error()
                return
            content = ''
            with open(realpath, 'r') as f:
                content = f.read()
            out = self.rfile.read(int(self.headers.get('Content-Length'))).decode()
            if token != '':
                if token not in result:
                    result[token] = {'info': tokens[token], 't': 0, 'f': 0}
                    for k, v in QUESTIONS:
                        result[token][k] = [0 for i in range(v)]
            if out is None:
                if token != '':
                    result[token][path[1]][int(path[2])-1] = 0
                    result[token]['f'] += 1
                self._send('False')
                return
            if out.strip() == content.strip():
                if token != '':
                    result[token][path[1]][int(path[2])-1] = 1
                    result[token]['t'] += 1
                self._send('True')
            else:
                if token != '':
                    result[token][path[1]][int(path[2])-1] = 0
                    result[token]['f'] += 1
                self._send('False')
            if token != '':
                with rlock:
                    with open('result.json', 'w') as f:
                        f.write(json.dumps(result))
            return
        self._send_error()


def main():
    server = HTTPServer((HOST, PORT), WebHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
