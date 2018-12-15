import http.server
import socketserver
import requests
import cgi
import io
import os
import json
import subprocess
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer, CGIHTTPRequestHandler
from urllib import parse


class MyHandler(http.server.CGIHTTPRequestHandler):

    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        print(parsed_path.path)
        filename = self.path[1:]
        if os.path.isfile(filename):
            message_parts = [
                'CLIENT VALUES:',
                'client_address={} ({})'.format(
                    self.client_address,
                    self.address_string()),
                'command={}'.format(self.command),
                'path={}'.format(self.path),
                'real path={}'.format(parsed_path.path),
                'query={}'.format(parsed_path.query),
                'request_version={}'.format(self.request_version),
                '',
                'SERVER VALUES:',
                'server_version={}'.format(self.server_version),
                'sys_version={}'.format(self.sys_version),
                'protocol_version={}'.format(self.protocol_version),
                '',
                'HEADERS RECEIVED:',
            ]
            for name, value in sorted(self.headers.items()):
                message_parts.append('{}={}'.format(name, value.rstrip()))
            message_parts.append('')
            message = '\r\n'.join(message_parts)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

            # Printing the requested file
            f = open(filename, 'r')
            self.wfile.write((f.read()).encode('utf-8'))

            # Network measurements
            cmnd = str(subprocess.getstatusoutput('ss -it'))
            measurements = {'meas': cmnd}
            url = "http://localhost:8900"
            resp = requests.post(url, measurements)
            print(resp.text)

        else:
            self.send_response(404)
            self.end_headers()
            message = "HTTP 404:File Not Found!!"
            self.wfile.write(message.encode('utf-8'))

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        # Begin the response
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()

        out = io.TextIOWrapper(
            self.wfile,
            encoding='utf-8',
            line_buffering=False,
            write_through=True,
        )

        out.write('Client: {}\n'.format(self.client_address))
        out.write('User-agent: {}\n'.format(
            self.headers['user-agent']))
        out.write('Path: {}\n'.format(self.path))
        out.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                out.write(
                    '\tUploaded {} as {!r} ({} bytes)\n'.format(
                        field, field_item.filename, file_len)
                )
            else:
                # Regular form value
                out.write('\t{}={}\n'.format(
                    field, form[field].value))

        # Disconnect our encoding wrapper from the underlying
        # buffer so that deleting the wrapper doesn't close
        # the socket, which is still being used by the server.
        out.detach()

         # Network measurements
        cmnd = str(subprocess.getstatusoutput('ss -it'))
        measurements = {'meas': cmnd}
        url = "http://localhost:8900"
        resp = requests.post(url, measurements)
        print(resp.text)

        # Printing the requested file
        filename = self.path[1:]
        f = open(filename, 'r')
        self.wfile.write((f.read()).encode('utf-8'))



def Main():
    try:
        PORT = 8888
        httpd = socketserver.TCPServer(("", PORT), MyHandler)
        print("Server serving at port", PORT)
        httpd.serve_forever()

    except KeyboardInterrupt:
        print(" ^C pressed, Stopping the server...")
        httpd.socket.close()
        


if __name__ == '__main__':
    Main()
