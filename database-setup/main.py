from faunadb import query as q

from jsonTools              import getObjectFromJsonFile
from faunaTools             import getFaunaDbInstance
from faunaDbCollections     import createCollections
from faunaDbIndexes         import createIndexes
from extractScrappedJsons   import getContributionsSamples, getDateContributionsSamples
from nlp                    import processTopicModelling, processWordFrequency
from visualizations         import createVisuTopicModelling, createVisuWordFrequency
import warnings
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)

# considers there s no array
def extractVisualizationsNLP(client):
    visualizations = []
    searchedWord = ["ministre", "artiste", "numerique", "danger"]
    for sample in getContributionsSamples("tto"):#client):
#        print("contrib: ", sample)
        nlpData = processTopicModelling(sample[1])
        visu = createVisuTopicModelling(nlpData)
        # visualizations.append({
        #   'type': 'topic_modelling',
        #   'sample': sample[0],
        #   'graph': visu
        # })
    for sample in getDateContributionsSamples("tot"):
    #    print("date contrib: ", sample[1])
        
        nlpData = processWordFrequency(sample[1], searchedWord)
        visu = createVisuWordFrequency(nlpData)
        # visualizations.append({
        #   'type': 'frequency',
        #   'sample': sample[0],
        #   'graph': visu
        # })
    return visualizations

if __name__ == "__main__":
    print("WARNING: this script assumes you have the 5 files from scrapping at \"../\"")
    client = getFaunaDbInstance()
    # createCollections(client)
    # createIndexes(client)
    # visus = extractVisualizationsNLP(client)
    # for elem in visus:
    #     client.query(q.create(
    #         q.collection('visualizations'), {'data': elem})
    #     )