# Endpoints

## Dates

**/dates**\
queryParams: none\
result: [["01/01/2000", "http://senat..."]]

## Votes

**/votes/context**\
queryParams: none\
result: [[“01/12/2000”, ”assemblée nationale”, 1]]

**/votes**\
queryParams:
- [required] number: vote number to get from /votes/context
- [required] assembly: "assemblée nationale" or "sénat"
- [optionnal] group: political group

result: { "pour": x, "contre": y, "none": z}

## Elected Members

**/elected_member**\
queryParams:
- [required] name: name of the elected member

result: {\
    "department": "x",\
    "group": "x",\
    "job": "x",\
    "mandate": "2000-2001",\
    "name": "x",\
    "vote_1": "none",\
    "vote_2": "none"\
}

**/elected_members**\
queryParams:
- none will list all elected members
- [optionnal] job: "sénateur" or "député"
- [optionnal] group: political group
- [optionnal] department: french department

result: [[name, job, group, deparment]]

## Visualization

**/visualization**\
queryParams:
- [required] type: type of visualization: "topic_modelling" or "word_frequency"
- [required] sample: sample of the visualization: "all", "sénat", "assemblée_nationale", political group name

result: {\
    "graph": {},\
    "sample": "x",\
    "type": "x",\
}

## Others

**/political_groups**\
queryParams: none\
result: ["political_group_name"]