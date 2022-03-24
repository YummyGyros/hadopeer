from faunadb import query as q

from faunaTools             import getFaunaDbInstance
from faunaDbCollections     import createCollections
from faunaDbIndexes         import createIndexes
from visualizations         import getVisualizationsNLP

if __name__ == "__main__":
    client = getFaunaDbInstance()
    createCollections(client)
    createIndexes(client)
    # groups = client.query(q.paginate(q.match(q.index('elected_members_group'))))['data']
    visus = getVisualizationsNLP()
    # for elem in visus:
    #     client.query(q.create(
    #         q.collection('visualizations'), {'data': elem})
    #     )