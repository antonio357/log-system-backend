from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()

  def do_HEAD(self):
    self._set_headers()

  def do_GET(self):
    self._set_headers()
    print(self.path)
    print(self.path[2:])
    self.wfile.write(bytes("Get Request Received", "utf-8"))

  def do_POST(self):
    self._set_headers()
    form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD': 'POST'}
    )
    print(form.getvalue("foo"))
    print(form.getvalue("bin"))
    self.wfile.write(bytes("POST Request Received", "utf-8"))

if __name__ == "__main__":
  webServer = HTTPServer((hostName, serverPort), MyServer)
  print("Server started http://%s:%s" % (hostName, serverPort))

  try:
    webServer.serve_forever()
  except KeyboardInterrupt:
    pass

  webServer.server_close()
  print("Server stopped.")
