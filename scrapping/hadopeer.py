import sys
import json
from os import path
import bs4
from detect_debat import detect_debat
from ScrapRaports import scrapSenat, scrapAssembleeNationale
from ScrapDeputy import other_scrap

tmpFileName = 'lectures_senat.json'
urlSenat = []
urlAssembleeNationale = []
pb = noL = noS = True
opt = 0


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
    if sys.argv.__len__() != 1 + opt:
        raise Exception("wrong number of argument")
    debat = detect_debat("http://www.senat.fr/dossier-legislatif/pjl07-405.html")
    if path.isfile(tmpFileName) is False:
        open("lectures_senat.json", "x")
    for i in debat:
        for y in i:
            parsR(y)
    lectures_senat, SenatorNom = scrapSenat(urlSenat, pb)
    data = {
        "lectures_senat": lectures_senat
    }
    # "lectures_assemblee_Nationale": scrapAssembleeNationale(urlAssembleeNationale)
    if noL:
        with open(tmpFileName, 'w') as json_file:
            json.dump(data, json_file,
                    indent=4,
                    separators=(',', ': '))
    if noS:
        other_scrap(SenatorNom, pb)


if __name__ == '__main__':
    try:
        if '-pb' in sys.argv:
            opt += 1
            pb = False
        if '-noL' in sys.argv:
            opt += 1
            noL = False
        if '-noS' in sys.argv:
            opt += 1
            noS = False
        hadopeer()
    except Exception as err:
        print('Unexpected error:', err)
        sys.exit(84)
