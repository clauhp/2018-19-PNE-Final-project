import http.server
import http.client
import socketserver
import termcolor
from ensembl_info import speciesnames, get_karyotype, get_chlength


PORT = 8088                     #CHANGE PROT CHANGE PORT TO 8000

HOSTNAME = 'rest.ensembl.org'
ENDPOINTS = ['/info/species', '/info/assembly']
header = {"Content-Type": "application/json"}

htmlfile = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Response</title>
</head>
<body style="margin-left:50px">
  <h1>{}</h1>
  <p>{}</p>
  <a href="/">Main page</a>
</body>
</html>"""


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        termcolor.cprint(self.requestline, 'green')
        termcolor.cprint(self.path, 'blue')

        path = self.path
        contents = ""
        out = ""
        pathlist = path.split('=')

        if path == "/":
            f = open("mainpage.html", 'r')
            contents = f.read()

        elif path.startswith("/listSpecies"):
            f = open('output.html', 'w')
            limit = int(pathlist[1])
            species = speciesnames()
            h = "List of Species"

            if len(pathlist) == 2:                         # AQUI HAY ALGO QUE NO CHUTA
                species = species[:limit]
            elif len(pathlist) == 1:
                species = species

            for i in range(len(species)):
                out += species[i] + "<br>"

            output = htmlfile.format(h, out)

            f.write(output)
            f.close()
            d = open('output.html', 'r')
            contents = d.read()

        elif path.startswith("/karyotype"):
            f = open('output.html', 'w')

            msg = pathlist[1]
            karyotype = get_karyotype(msg)
            h = "Karyotype"

            for i in range(len(karyotype)):
                out += karyotype[i] + ', '              # THERE IS A FUCKING COMA I CANNOT GET RID OF

            output = htmlfile.format(h, out)

            f.write(output)
            f.close()
            d = open('output.html', 'r')
            contents = d.read()



        elif path.startswith("/chromosomeLength"):
            pass

        else:
            d = open("error.html", 'r')
            contents = d.read()


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
