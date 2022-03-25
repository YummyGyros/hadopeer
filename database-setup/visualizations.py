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
        O.append(occurence * 900)
    print(O)

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
#    fig.write_image("fig1.png")
    return fig.to_json()

def createVisuWordFrequency(nlpData, contribGroup):
    occ = []
    date = [d[0] for d in contribGroup ]
    df = pd.DataFrame(columns=["date", "occurence", "mots"])

    print(nlpData)
    for res in nlpData:
        print(res)
        occ = [x[1] for x in nlpData[res]]

        df = df.append(pd.DataFrame({
            "date": date,
            "occurence": occ,
            "mots": res
        }))

    fig = px.line(df, x="date", y="occurence", color='mots')
#    print("JSON HERE: ", fig.to_json())
#    fig.write_image("fig1.png")
    return fig.to_json()
#    fig.write_json("nlp_j.json", pretty=True)