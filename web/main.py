import os
import sys
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from config import *
import json


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
            realpath = os.path.join('.', path[1], QUESTIONS[path[1]][1] + path[2]+'.in')
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
        self._send_error()

    def do_POST(self):
        path = self.path.strip('/').split('/')
        if len(path) < 1:
            self._send_error()
            return
        if path[0] == 'out':
            if SECRET != None and self.headers.get('Authorization', '') != SECRET:
                self._send_error()
                return
            if len(path) != 3:
                self._send_error()
                return
            realpath = os.path.join('.', path[1], QUESTIONS[path[1]][1] + path[2]+'.out')
            if not os.path.exists(realpath):
                self._send_error()
                return
            content = ''
            with open(realpath, 'r') as f:
                content = f.read()
            out = self.rfile.read(int(self.headers.get('Content-Length'))).decode()
            if out is None:
                self._send('False')
                return
            if out.strip() == content.strip():
                self._send('True')
            else:
                self._send('False')
            return
        self._send_error()


def main():
    server = HTTPServer((HOST, PORT), WebHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
