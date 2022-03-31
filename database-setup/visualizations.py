import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random
import plotly.express as px
import pandas as pd

def createVisuTopicModelling(nlpData):
    colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
    W = []
    O = []
    for word, occurence in nlpData:
        W.append(word)
        O.append(occurence * 10000)

    data = go.Scatter(x=[random.random() for i in range(30)],
                     y=[random.random() for i in range(30)],
                     mode='text',
                     text=W,
                     marker={'opacity': 0.3},
                     textfont={'size': O,
                               'color': colors})
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    fig = go.Figure(data=[data], layout=layout)
    return fig.to_json()

def createVisuWordFrequency(nlpData, contribGroup):
    occ = []
    date = contribGroup
    df = pd.DataFrame(columns=["date", "occurence", "mots"])

    for res in nlpData:
        occ = [x[1] for x in nlpData[res]]

        df = df.append(pd.DataFrame({
            "date": date,
            "occurence": occ,
            "mots": res
        }))

    fig = px.line(df, x="date", y="occurence", color='mots')
    return fig.to_json()[0]