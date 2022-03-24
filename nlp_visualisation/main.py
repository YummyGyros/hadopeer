import jsonTools

def getAllContributions(filepaths):
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonArrayFile(path)
        contribs = []
        for object in objects:
            for contrib in object['contributions']:
                contribs.append(contrib['text'])
    return contribs

def getAllDateContributions(filepaths):
    for path in filepaths:
        objects = jsonTools.getObjectFromJsonArrayFile(path)
        tuples = []
        for object in objects:
            tuple = (object['date'], [])
            for contrib in object['contributions']:
                tuple[1].append(contrib['text'])
                break
            tuples.append(tuple)
    return tuples


def getContribsFromMatchingMembers(contribsPaths, membersPaths, field, value):
    # select names
    names = []
    contribs = []
    for path in membersPaths:
        members = jsonTools.getObjectFromJsonArrayFile(path)
        for member in members:
            if member[field] == value:
                names.append(member['name'])
    # get contribs from names
    for path in contribsPaths:
        objects = jsonTools.getObjectFromJsonArrayFile(path)
        for obj in objects:
            for contrib in obj['contributions']:
                if (name == obj['elected_member'] for name in names):
                    contribs.append(contrib['text'])

if __name__ == "__main__":
    contribsPaths = ['national_assembly_sessions.json']
    for i in range(len(contribsPaths)):
        contribsPaths[i] = '../save_valid_json/' + contribsPaths[i]

    membersPaths = ['deputies.json']
    for i in range(len(membersPaths)):
        membersPaths[i] = '../save_valid_json/' + membersPaths[i]
    # allContribs = getAllContributions(files)
    # allDateContribs = getAllDateContributions(files)
    deputiesContribs = getContribsFromMatchingMembers(contribsPaths, membersPaths, "job", "député")
    # ISSUES:
    #   - fonction très proche des autres: meilleure archi?
    #   - peu opti: pour les sessions du sénat, compare avec sénateurs et députés actuellement
    #   - recup DateContribs?
    #   - filtre soit Sénat soit UMP mais comment filtrer Sénat ET UMP (car groupe existe a l'AN aussi)

# main preprocess
# 1) getDataFromJsonScrapped
# 2) createVisualizationsFromNLP
# 3) fill_database

# main 
# visualizations = []
# visualizations.append(getVisuTopicModelling(getAllContributions()))
# visualizations.append(getVisuTopicModelling(getContributionsByAssembly("sénat"))
# for group in groups:
#   visualizations.append(getVisuTopicModelling(getContributionsBy(group))

# visualizations.append(getVisuFrequency(getAllContributions()))
# visualizations.append(getVisuFrequency(getContributionsByAssembly("sénat"))
# for group in groups:
#   visualizations.append(getVisuFrequency(getContributionsBy(group))

# for visu in visualizations:
#   put_in_db()