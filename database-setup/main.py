from faunadb import query as q

from jsonTools              import getObjectFromJsonFile
from faunaTools             import getFaunaDbInstance
from faunaDbCollections     import createCollections
from faunaDbIndexes         import createIndexes
from extractScrappedJsons   import getContributionsSamples, getDateContributionsSamples
from nlp                    import processTopicModelling
from visualizations         import createVisuTopicModelling
import warnings
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)

# considers there s no array
def extractVisualizationsNLP(client):
    visualizations = []
    for sample in getContributionsSamples(client):
        print("contrib: ", sample)
        nlpData = processTopicModelling(sample[1])
        visu = createVisuTopicModelling(nlpData)
        # visualizations.append({
        #   'type': 'topic_modelling',
        #   'sample': sample[0],
        #   'graph': vis,
        #   'values': []
        # })
    for sample in getDateContributionsSamples():
    #    print("date contrib: ", sample[1])
        
        nlpData = processTopicModelling(sample[1])
        visu = createVisuTopicModelling(nlpData)
        # visualizations.append({
        #   'type': 'frequency',
        #   'sample': sample[0],
        #   'graph': vis,
        #   'values': add_array_from_file???
        # })
    return visualizations

if __name__ == "__main__":
    #client = getFaunaDbInstance()
    # createCollections(client)
    # createIndexes(client)
    visus = extractVisualizationsNLP(client)
    # for elem in visus:
    #     client.query(q.create(
    #         q.collection('visualizations'), {'data': elem})
    #     )