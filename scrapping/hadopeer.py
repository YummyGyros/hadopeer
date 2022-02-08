import sys
import json
from os import path
import bs4
from detect_debat import detect_debat
from ScrapRaports import scrapSenat, scrapAssembleeNationale

tmpFileName = 'tmp.json'
urlSenat = []
urlAssembleeNationale = []


def parsR(row):
    if (type(row) == bs4.element.Tag):
        if 'lecture' in row.text or 'seances' in row.get('href'):
            if row.get('href') != None:
                urlSenat.append("http://www.senat.fr" + row.get('href').split("#")[0])
            else:
                urlSenat.append(row.text)
        elif 'Rapport' in row.text:
            urlAssembleeNationale.append(row.get('href'))


def hadopeer():
    if sys.argv.__len__() != 1:
        raise Exception("wrong number of argument")
    debat = detect_debat("http://www.senat.fr/dossier-legislatif/pjl07-405.html")
    if path.isfile(tmpFileName) is False:
        open("lectures_senat.json", "x")
    for i in debat:
        for y in i:
            parsR(y)
    data = {
        "lectures_senat": scrapSenat(urlSenat)
    }
    # "lectures_assemblee_Nationale": scrapAssembleeNationale(urlAssembleeNationale)
    with open(tmpFileName, 'w') as json_file:
        json.dump(data, json_file,
                  indent=4,
                  separators=(',', ': '))
    # return json.dumps(retSenat, indent=4,
    #                   separators=(',', ': '))


if __name__ == '__main__':
    try:
        hadopeer()
    except Exception as err:
        print('Unexpected error:', err)
        sys.exit(84)
