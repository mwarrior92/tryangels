import http.client
import http.server
import cgi
import io
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, CGIHTTPRequestHandler
import requests
import json

servername = None
requesttype = None
filename = None
filesize = None
postdata = {}


class ControllerHandler(CGIHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        # Getting parameters from request sent by the Controller
        global servername, filename, requesttype, filesize, postdata
        servername = form['server'].value
        requesttype = form['requesttype'].value
        filename = form['filename'].value
        filesize = form['size'].value
        if str(requesttype) == "POST":
            postdata = {'k1': form['kpdata1'].value,
                        'k2': form['kpdata2'].value}
           
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
            # field_item = form[field]
            # print(field_item)

            # Regular form value
            # print("no file dta")
            out.write('\t{}={}\n'.format(field, form[field].value))

        # Disconnect our encoding wrapper from the underlying
        # buffer so that deleting the wrapper doesn't close
        # the socket, which is still being used by the server.
        out.detach()
        
# Creating GET request using the parameters sent by Controller
def getRequest():
    global servername, filename
    url = "http://" + servername + ":8888/" + filename
    resp = requests.get(url)
    print(resp.text)

# Creating POST request using the parameters sent by Controller
def postRequest():
    global servername, filename, postdata
    url = "http://" + servername + ":8888/" + filename
    resp = requests.post(url, postdata)
    print(resp.text)


def Main():
    global requesttype
    try:
        PORT = 8890
        httpd = http.server.HTTPServer(("", PORT), ControllerHandler)
        print("Receiving from Controller at port", PORT)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" ^C pressed, Stopping the server...")
        httpd.socket.close()
        if str(requesttype) == "GET":
            getRequest()
        if str(requesttype) == "POST":
            postRequest()



if __name__ == '__main__':
    Main()
