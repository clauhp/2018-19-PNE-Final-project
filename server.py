import http.server
import http.client
import socketserver
import termcolor
from ensembl_info import speciesnames, get_karyotype, get_chlength, get_geneid, get_geneSeq, get_geneInfo, get_names
from Seq_calc import Seq

PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

HOSTNAME = 'rest.ensembl.org'
ENDPOINTS = ['/info/species', '/info/assembly']
header = {"Content-Type": "application/json"}

htmlfile = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Response</title>
</head>
<body style="margin-left:50px;background-color:#B7BAFF">
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
        common, search = speciesnames()
        check = dict(zip(common, search))

        if path == "/":
            f = open("mainpage.html", 'r')
            contents = f.read()

        elif path.startswith("/listSpecies"):
            f = open('output.html', 'w')
            common_name, search_name = speciesnames()
            h = "List of Species"
            limit = pathlist[1]

            try:
                limit = int(limit)
            except ValueError:
                if limit == "":      # This is for when there is no limit
                    limit = len(common_name)
                else:
                    limit = 'Error'  # This prevents the program form collapsing if a non-integer character is introduced

            if limit == 'Error':
                out = "Incorrect value in the parameter 'limit'.<br>Please introduce an integer number"
            elif limit > 199:
                out = "Sorry, there are only 199 species in the database, so the limit cannot be above that number"

            else:
                common_name = common_name[:limit]

                for i in range(len(common_name)):
                    out += common_name[i] + "<br>"

            output = htmlfile.format(h, out)

            f.write(output)
            f.close()
            d = open('output.html', 'r')
            contents = d.read()

        elif path.startswith("/karyotype"):             # I NEED TO DO SOMETHING WITH THE ERRORS
            f = open('output.html', 'w')

            msg = pathlist[1]
            h = "Karyotype"

            try:
                karyotype = get_karyotype(msg)
                for i in range(len(karyotype)):
                    out += karyotype[i] + '  '              # THERE IS A FUCKING COMMA I CANNOT GET RID OF
            except KeyError:
                out = "Sorry, the name you introduced couldn't be found in our database"

            output = htmlfile.format(h, out)

            f.write(output)
            f.close()
            d = open('output.html', 'r')
            contents = d.read()

        elif path.startswith("/chromosomeLength"):
            f = open('output.html', 'w')

            msg1 = pathlist[1].split('&')[0]
            msg2 = pathlist[2]
            h = "Chromosome length"

            try:
                chr_length = get_chlength(msg1, msg2)

                if chr_length == "Error":
                    out = "Sorry, the data you introduced cannot be found in the database"
                else:
                    out = "The length of the chromosome {} of the {} species is {}".format(msg2, msg1, chr_length)
            except KeyError:
                out = "Sorry, the data you introduced cannot be found in the database"

            output = htmlfile.format(h, out)

            f.write(output)
            f.close()
            d = open('output.html', 'r')
            contents = d.read()

        elif path.startswith("/geneSeq"):           # INTENTAR JUNTAR geneSEQ Y geneINFO PARA QUE OCUPE MENOS
            f = open('output.html', 'w')
            genename = pathlist[1]
            h = "Human gene sequence"
            id = get_geneid(genename)

            if id == "Error":
                out = "Sorry, the name of the gene you introduced is not found in our database"
            else:
                geneseq = get_geneSeq(id)['seq']
                newseq = ""

                # This is for the sequence to appear in multiple lines instead of in an infinite long one.
                step = 100
                seqlist = [geneseq[i:i+step] for i in range(0, len(geneseq), step)]
                for x in seqlist:
                    newseq += x + '<br>'

                out = """<b>This is the DNA sequence for the gene you introduced:</b>
                 <br><br>
                 {}""".format(newseq)

            output = htmlfile.format(h, out)

            f.write(output)
            f.close()
            d = open('output.html', 'r')
            contents = d.read()

        elif path.startswith("/geneInfo"):              # ME FALTA PONER EL LENGTH
            f = open('output.html', 'w')
            genename = pathlist[1]
            h = "Human gene information"
            id = get_geneid(genename)

            if id == "Error":
                out = "Sorry, the name of the gene you introduced is not found in our database"
            else:
                geneinfo = get_geneInfo(id)
                out = """Start: {}<br>End: {}<br>Chromosome: {}<br>Length:""".format(geneinfo['start'], geneinfo['end'], geneinfo['chromo'])

            output = htmlfile.format(h, out)

            f.write(output)
            f.close()
            d = open('output.html', 'r')
            contents = d.read()

        elif path.startswith("/geneCalc"):          # ME FALTA PONER EL LENGTH
            f = open('output.html', 'w')
            genename = pathlist[1]
            h = "Human gene information"
            id = get_geneid(genename)

            if id == "Error":
                out = "Sorry, the name of the gene you introduced is not found in our database"
            else:
                geneseq = get_geneSeq(id)['seq']
                dna = Seq(geneseq)
                d_perc = {}

                for base in ['A', 'C', 'T', 'G']:
                    d_perc.update({base: dna.perc(base)})
                out = """The length of the sequence is {}<br><br>Base percentages
                <ul><li>Adenine: {}%</li><li>Guanine: {}%</li>
                <li>Thymine:{}%</li><li>Cytosine: {}%</li></ul>""".format(dna.len(), d_perc['A'], d_perc['G'], d_perc['T'], d_perc['C'])

                print(len(geneseq))
                info = get_geneInfo(id)
                length = int(info['end']) - int(info['start'])
                print(length)

            output = htmlfile.format(h, out)

            f.write(output)
            f.close()
            d = open('output.html', 'r')
            contents = d.read()

        elif path.startswith("/geneList"):
            f = open('output.html', 'w')
            chromo = pathlist[1].split('&')[0]
            start = pathlist[2].split('&')[0]
            end = pathlist[3]
            h = "Names of all the genes within a specific chromosome region"
            list_names = get_names(chromo, start, end)

            if len(list_names) == 0:
                out = "Sorry, there were no genes found in that area"
            else:
                out = "This is the list of gene names in that area: {}".format(list_names)

            output = htmlfile.format(h, out)

            f.write(output)
            f.close()
            d = open('output.html', 'r')
            contents = d.read()

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
