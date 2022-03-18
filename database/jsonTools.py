import json

def addFieldToJsonArrayFile(filepath, field, value):
  dataString = open(filepath, 'r')
  objects = json.load(dataString)
  for object in objects:
    object[field] = value
  with open(filepath, "w") as file:
    json.dump(objects, file, ensure_ascii=True, indent=4, separators=(',', ': '))

def deleteFieldFromJsonArrayFile(filepath, field):
  dataString = open(filepath, 'r')
  objects = json.load(dataString)
  for object in objects:
    object.pop(field)
  with open(filepath, "w") as file:
    json.dump(objects, file, ensure_ascii=True, indent=4, separators=(',', ': '))

def addValueToArrayInObjectOfJsonArrayFile(filepath, fieldObj, valueObj, field, value):
  file = open(filepath, 'r')
  objects = json.load(file)
  for object in objects:
    if object[fieldObj] == valueObj.lower():
      object[field].append(value)
      break
  with open(filepath, "w") as file:
    json.dump(objects, file, ensure_ascii=True, indent=4, separators=(',', ': '))