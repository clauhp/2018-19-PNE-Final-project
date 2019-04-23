import http.server
import http.client
import socketserver
import termcolor
import requests


PORT = 8080

HOSTNAME = 'rest.ensembl.org'
ENDPOINTS = ['/info/species', '/info/assembly']
header = {"Content-Type": "application/json"}


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')
        termcolor.cprint(self.path, 'blue')

        path = self.path
        contents = ""

        if path == "/":
            f = open("mainpage.html", 'r')
            contents = f.read()

        elif path == "/listSpecies":
            r = requests.get(HOSTNAME + ENDPOINTS[0], headers=header)
            decoded = r.json()

            limit = path.split('=')[1]

            number_species = decoded['species']
            species = []

            for number in number_species:
                name = number['common_name']
                species.append(name)


            content = """<!DOCTYPE html>
            <html lang="en">
            <head>
              <meta charset="utf-8">
              <title>listSpecies</title>
            </head>
            <body>
              <h1>List of all species</h1>
              <p>Sequence: {}</p>
              <p></p>
              <p>{}</p>
              <p></p>
              <a href="/">Main page</a>
            </body>
            </html>"""



        elif path == "/karyotype":
            pass

        elif path == "/chromosomeLength":
            pass

        self.send_response(200)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()

        # --Sending the body of the response message
        self.wfile.write(str.encode(contents))



with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT: {}".format(PORT))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()