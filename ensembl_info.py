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

    species = []

    for number in infospecies:
        name = number['common_name']
        species.append(name)

    return species


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
