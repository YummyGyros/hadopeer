import sys
from os import path
from bs4 import BeautifulSoup
from detect_debat import detect_debat
from ScrapRaports import scrapSenat

tmpFileName = 'tmp.json'
urlSenat = []

def parsR(titreart):
    
    if path.isfile(tmpFileName) is False:
        open("tmp.json", "x")
    if titreart.find("seances") != -1:
        if titreart.get('href') != None:
            temp = titreart.get('href')
            urlSenat.append("http://www.senat.fr" + temp)
        else:
            urlSenat.append(titreart.text)
        
    # elif url.find("www.assemblee-nationale.fr") != -1:
    #     scrapAssembleeNationale(soup)
    # else:
    #     raise Exception("wrong url")

def hadopeer():
    if sys.argv.__len__() != 2:
        raise Exception("wrong number of argument")
    debat = detect_debat(sys.argv[1])
    for i in debat:
        for y in i:
            parsR(y)
    scrapSenat(urlSenat)

if __name__ == '__main__':
    try:
        hadopeer()
    except Exception as err:
        print('Unexpected error:', err)
        sys.exit(84)
