from extractScrappedJsons   import getAllContributions, getContribsFromMatchingMembers

sessionsPaths = ['../national_assembly_sessions.json', '../senate_sessions.json']
membersPaths = ['../senators.json', '../deputies.json']

def getVisualizationsNLP():
    allContribs = getAllContributions()
    print(allContribs)

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