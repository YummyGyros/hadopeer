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

if __name__ == "__main__":
    files = ['national_assembly_sessions.json']
    for i in range(len(files)):
        files[i] = '../save_valid_json/' + files[i]

    allContribs = getAllContributions(files)
    allDateContribs = getAllDateContributions(files)

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