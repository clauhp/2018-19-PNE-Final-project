import json
import http.client

HOSTNAME = "rest.ensembl.org"
METHOD = "GET"


def speciesnames():
    conn = http.client.HTTPSConnection(HOSTNAME)

    ENDPOINT = "/info/species?content-type=application/json"
    # -- Send the request
    conn.request(METHOD, ENDPOINT, None)
    # -- Read the response message from the server
    r1 = conn.getresponse()
    # -- Read the response's body
    text_json = r1.read().decode("utf-8")
    conn.close()

    # -- Generate the object from the json file
    infospecies = json.loads(text_json)['species']

    c_name = []
    search_name = []

    for number in infospecies:
        name1, name2 = number['common_name'], number['name']
        c_name.append(name1)
        search_name.append(name2)

    return c_name, search_name


def get_karyotype(object):
    conn = http.client.HTTPSConnection(HOSTNAME)

    endpoint = "/info/assembly/" + object + "?content-type=application/json"

    conn.request(METHOD, endpoint, None)
    r1 = conn.getresponse()

    text_json = r1.read().decode("utf-8")
    conn.close()

    info_kar = json.loads(text_json)["karyotype"]

    return info_kar

def get_chlength(object1, object2):
    conn = http.client.HTTPSConnection(HOSTNAME)

    endpoint = "/info/assembly/" + object1 + "?content-type=application/json"

    conn.request(METHOD, endpoint, None)
    r1 = conn.getresponse()

    text_json = r1.read().decode("utf-8")
    conn.close()

    specie = json.loads(text_json)["top_level_region"]

    for x in specie:
        if x["name"] == object2:
            length = x["length"]
            return length

def get_geneid(name):
    conn = http.client.HTTPSConnection(HOSTNAME)
    endpoint = "/homology/symbol/human/" + name + "?content-type=application/json"

    conn.request(METHOD, endpoint, None)
    r1 = conn.getresponse()

    text_json = r1.read().decode("utf-8")
    conn.close()

    info = json.loads(text_json)

    try:
        geneid = info['data'][0]['id']

    except KeyError:
        geneid = "Error"

    return geneid

def get_geneSeq(id):
    conn = http.client.HTTPSConnection(HOSTNAME)
    endpoint = "/sequence/id/" + id + "?content-type=application/json"
    headers = {'User-Agent': 'http-client'}

    conn.request(METHOD, endpoint, None, headers)
    r1 = conn.getresponse()

    text_json = r1.read().decode("utf-8")
    conn.close()

    seq = json.loads(text_json)

    """newseq = ""

    step = 100
    seqlist = [seq[i:i + step] for i in range(0, len(seq), step)]
    for x in seqlist:
        newseq += x + '\n'"""

    return seq

def get_geneInfo(id):
    conn = http.client.HTTPSConnection(HOSTNAME)
    endpoint = "/overlap/id/" + id + "?feature=gene;content-type=application/json"
    headers = {'User-Agent': 'http-client'}

    conn.request(METHOD, endpoint, None, headers)
    r1 = conn.getresponse()

    text_json = r1.read().decode("utf-8")
    conn.close()

    info = json.loads(text_json)
    dd = {}

    for type in info:
        if type['id'] == id:
            d = {'start': type['start'], 'end': type['end'], 'chromo': type['seq_region_name']}
            dd.update(d)
        else:
            pass

    return dd

def get_names(chromo, start, end):
    conn = http.client.HTTPSConnection(HOSTNAME)
    endpoint = '/overlap/region/human/{}:{}-{}?feature=gene;content-type=application/json'.format(chromo, start, end)
    headers = {'User-Agent': 'http-client'}

    conn.request(METHOD, endpoint, None, headers)
    r1 = conn.getresponse()

    text_json = r1.read().decode("utf-8")
    conn.close()