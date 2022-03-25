from faunadb import query as q

from faunaTools             import getFaunaDbInstance
from faunaDbCollections     import createCollections
from faunaDbIndexes         import createIndexes
from extractScrappedJsons   import getContributionsGroups, getDateContributionsGroups
from nlp                    import processTopicModelling, processWordFrequency
from visualizations         import createVisuTopicModelling, createVisuWordFrequency
import warnings
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)



def extractVisualizationsNLP():
    visualizations = []
    for group in getContributionsGroups():
        print("contrib: ", group)
        nlpData = processTopicModelling(group)
        visu = createVisuTopicModelling(nlpData)
        visualizations.append(visu)
    for group in getDateContributionsGroups():
         print("date contrib: ", group)
         nlpData = processWordFrequency(group)
         visu = createVisuWordFrequency(nlpData)
         visualizations.append(visu)
    return visualizations

if __name__ == "__main__":
    #client = getFaunaDbInstance()
    # createCollections(client)
    # createIndexes(client)
    visus = extractVisualizationsNLP()
    # for elem in visus:
    #     client.query(q.create(
    #         q.collection('visualizations'), {'data': elem})
    #     )