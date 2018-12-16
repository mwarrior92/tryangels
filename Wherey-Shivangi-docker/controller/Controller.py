import requests
import json
import http.server
import cgi
import io
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer, CGIHTTPRequestHandler

# To get the user input to be sent to HTTP client
def controller_to_client():
    targetserver = input("Target Server: ")
    reqtpe = input("Request type (GET/POST): ")
    filename = input("File to be downloaded: ")
    filesize = input("File Size: ")
    if reqtpe == "GET":
        data = {'server': targetserver,
                'requesttype': reqtpe,
                'filename': filename,
                'size': filesize}
    elif reqtpe =="POST":
        print("Enter the data for POST req")
        pdata1 = input("Enter data1: ")
        pdata2 = input("Enter data2: ")
        postdata = {'kpdata1': pdata1, 'kpdata2': pdata2}
        data = {'server': targetserver,
                'requesttype': reqtpe,
                'filename': filename,
                'size': filesize,
                'postdata': postdata}
    else:
        print ("Invalid request type")
        exit(0)

    #Creating the POST request to be sent to HTTP client with the parameters
    url = "http://localhost:8890"
    resp = requests.post(url, data)
    print(resp.text)


class Networkmeasurement(http.server.CGIHTTPRequestHandler):

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

        #Printing the network measurements sent by the HTTP server
        nwmeas = form['meas'].value
        connections = nwmeas.split("ESTAB")
        for i in range (0,len(connections)):
            if "127.0.0.1:8888" in connections[i]:
                connections[i] = connections[i].replace("\n","")
                print (connections[i])

        # Disconnect our encoding wrapper from the underlying
        # buffer so that deleting the wrapper doesn't close
        # the socket, which is still being used by the server.
        out.detach()


def Main():
    controller_to_client()

    try:
        PORT = 8900
        httpd = http.server.HTTPServer(("", PORT), Networkmeasurement)
        print("Receiving from HTTP server at port", PORT)
        httpd.serve_forever()

    except KeyboardInterrupt:
        print(" ^C pressed, Stopping the server...")
        httpd.socket.close()


if __name__ == '__main__':
    Main()