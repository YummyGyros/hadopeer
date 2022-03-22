import sys
import json
from os import path
import bs4
from find_debate import find_debate
from ScrapRaports import scrapSenat, scrapAN
from ScrapDeputy import other_scrap, vote_Senator, ScrapDeputy

tmpFileName_senat = 'lectures_senat.json'
tmpFileName_AN = 'lectures_AN.json'
pb = noL = noS = True
opt = 0


def hadopeer():
    if sys.argv.__len__() != 1 + opt:
        raise Exception("wrong number of argument")
    urlSenat, urlAN = find_debate(
        "http://www.senat.fr/dossier-legislatif/pjl07-405.html", "https://www.assemblee-nationale.fr/13/dossiers/internet.asp")
    if path.isfile(tmpFileName_senat) is False:
        open(tmpFileName_senat, "x")
    if path.isfile(tmpFileName_AN) is False:
        open(tmpFileName_AN, "x")
    lectures_senat, SenatorNom = scrapSenat(urlSenat, pb)
    lectures_AN, DeputyName = scrapAN(urlAN, pb)
    if noL:
        with open(tmpFileName_senat, 'w') as json_file:
            json.dump(lectures_senat, json_file,
                      indent=4,
                      separators=(',', ': '))
        with open(tmpFileName_AN, 'w') as json_file:
            json.dump(lectures_AN, json_file,
                      indent=4,
                      separators=(',', ': '))
    if noS:
        vote_Senator.scrutin = dict()
        vote_Senator.lst_senator = []
        vote_Senator.first = 0
        vote_Senator(1)
        vote_Senator(2)
        other_scrap(SenatorNom, pb, vote_Senator.scrutin)
        ScrapDeputy.first = True
        ScrapDeputy.page = 1
        DeputyName = list(dict.fromkeys(DeputyName))
        print(DeputyName)
        ScrapDeputy("", DeputyName, [])



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
        sys.stderr.write(
            '\033[91mUnexpected error: \033[0m' + str(err.args[0]) + '\n')
        sys.exit(84)
