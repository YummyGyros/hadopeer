import json

def getObjectFromJsonArrayFile(path):
  dataString = open(path, 'r')
  objects = json.load(dataString)
  return objects