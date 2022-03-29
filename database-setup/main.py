from faunadb import query as q

from jsonTools              import getObjectFromJsonFile
from faunaTools             import getFaunaDbInstance
from faunaDbCollections     import createCollections
from faunaDbIndexes         import createIndexes
from extractScrappedJsons   import getContribSamples, getDateContribSamples
from nlp                    import processTopicModelling, processWordFrequency
from visualizations         import createVisuTopicModelling, createVisuWordFrequency
import warnings
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)

def getVisuObj(name, sampleName, data):
    return {'type': name, 'sample': sampleName, 'graph': data}

def appendTopicModellingVisu(visus, contribs):
    for sample in contribs:
        if sample[1] == None:
            continue
        nlpData = processTopicModelling(sample[1])
        visu = createVisuTopicModelling(nlpData)
        visus.append(getVisuObj('topic_modelling', sample[0], visu))

def appendWordFrequencyVisu(visus, contribs):
    words = ["ministre", "artiste", "numerique", "danger"]
    for sample in getDateContribSamples(client):
        if sample[1] == None:
            continue
        nlpData, date = processWordFrequency(sample[1], words)
        visu = createVisuWordFrequency(nlpData, date)
        visus.append(getVisuObj('word_frequency', sample[0], visu))

if __name__ == "__main__":
    print("WARNING: this script requires the 5 files from scrapping at \"../\"")
    client = getFaunaDbInstance()
    # createCollections(client)
    # createIndexes(client)
    visus = []
    contribs = getContribSamples(client)
    appendTopicModellingVisu(visus, contribs)
    contribs = getDateContribSamples(client)
    appendWordFrequencyVisu(visus, contribs)
    # for elem in visus:
    #     client.query(q.create(
    #         q.collection('NOT_YETvisualizations'), {'data': elem})
    #     )