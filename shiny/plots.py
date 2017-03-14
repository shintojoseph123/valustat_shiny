from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np
import glob
import os
import datetime

from plotly.tools import FigureFactory as FF



def table(percent_array,years):

    mat = [years]

    if not len(percent_array)==0:
        ro = len(percent_array)
        col = len(percent_array[0])


        index = ["80","60","40","20","5"]

        for i in range(col):
            sel = []
            sel.append(index[i])
            for j in range(ro):
                sel.append(percent_array[j,i])
            mat.append(sel)


    data_matrix = mat

    table = FF.create_table(data_matrix)

    plot_div = plot(table, output_type='div', include_plotlyjs=False)
    return plot_div


def tabe_graph(mat,years,col):

    data = []
    color = ['rgba(14, 127, 0, .5)', 'rgba(14, 127, 0, .5)',
           'rgba(110, 154, 22, .5)', 'rgba(170, 202, 42, .5)',
           'rgba(202, 209, 95, .5)', 'rgba(210, 206, 145, .5)','rgba(232, 226, 202, .5)', 'rgba(204,204,204,1)']

    for i in range(1,col+1):

        trace = go.Bar(
            x=years[1:],
            y=mat[i],
            name=' ',
            showlegend = False,
            hoverinfo = 'none',
            marker=dict(color=str(color[i]) ),
        )

        data.append(trace)

    layout = go.Layout(
        title='Good / Bad Scenarios',
        height=600,
        xaxis=dict(
            autorange=True
        ),
        yaxis=dict(
            autorange=True
        )
    )

    fig = go.Figure(data=data, layout=layout)
    # plot(fig, filename='tabe_graph.html')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div

def spline(x_axis,loop,column,spline_percent,final_row):

    data = []

    final_row = final_row
    spline_percent = spline_percent

    for i in range(column):
        graph_fill = loop[i]
        if graph_fill[final_row] >= spline_percent[0]:

            line=dict(color='rgba(14, 127, 0, 0.498039)')
        elif graph_fill[final_row] >= spline_percent[1]:

            line=dict(color='rgba(110, 154, 22, 0.498039)')
        elif graph_fill[final_row] >= spline_percent[2]:

            line=dict(color='rgba(170, 202, 42, 0.498039)')
        elif graph_fill[final_row] >= spline_percent[3]:

            line=dict(color='rgba(202, 209, 95, 0.498039)')
        elif graph_fill[final_row] >= spline_percent[4]:

            line=dict(color='rgba(210, 206, 145, 0.498039)')

        if i==0:
            trace = go.Scatter(
            x = x_axis,
            y = loop[i],
            fill = None,
            mode ='lines',
            line=line,
            hoverinfo = 'none',
            showlegend = False
            )
        else:
            trace = go.Scatter(
            x = x_axis,
            y = loop[i],
            line=line,

            fill = 'tonexty',
            mode ='lines',
            hoverinfo = 'none',
            showlegend = False
            )

        data.append(trace)

    layout = go.Layout(
        title='Projected value of capital',
        height=600,
        xaxis=dict(
            autorange=True
        ),
        yaxis=dict(
            autorange=True
        )
    )
    fig = go.Figure(data=data, layout=layout)
    # plot(fig, filename='spline.html')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div

def guage():
    base_chart = {
    "values": [40, 10, 10, 10, 10, 10, 10],
    "labels": ["-", "0", "20", "40", "60", "80", "100"],
    "domain": {"x": [0, .48]},
    "marker": {
        "colors": [
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)'],
        "line": {
            "width": 1
            }},
    "name": "Gauge",
    "hole": .4,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 108,
    "showlegend": False,
    "hoverinfo": "none",
    "textinfo": "label",
    "textposition": "outside"}

    meter_chart = {
    "values": [50, 10, 10, 10, 10, 10],
    "labels": ["Probability", "0 - 20", "21 - 40", "41 - 60", "61 - 80", "81 - 100"],
    "marker": {
        'colors': [
            'rgba(255, 255, 255, 0)',
            'rgb(232,226,202)',
            'rgba(202, 209, 95, .5)',
            'rgba(170, 202, 42, .5)',
            'rgba(110, 154, 22, .5)',
            'rgba(14, 127, 0, .5)']
            },
    "domain": {"x": [0, 0.48]},
    "name": "Gauge",
    "hole": .3,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 90,
    "showlegend": False,
    "textinfo": "label",
    "textposition": "inside",
    "hoverinfo": "none"
    }

    layout = {
    'xaxis': {
        'showticklabels': False,
        'autotick': False,
        'showgrid': False,
        'zeroline': False,
        },
    'yaxis': {
        'showticklabels': False,
        'autotick': False,
        'showgrid': False,
        'zeroline': False,
        },
    'shapes': [{
            'type': 'path',
            'path': 'M 0.235 0.5 L 0.5 0.65 L 0.245 0.5 Z',
            'fillcolor': 'rgba(44, 160, 101, 0.5)',
            'line': {
                'width': 0.5
            },
            'xref': 'paper',
            'yref': 'paper'
        }],
    'annotations': [{
            'xref': 'paper',
            'yref': 'paper',
            'x': 0.23,
            'y': 0.45,
            'text': '50',
            'showarrow': False
            }]
            }
    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0
    fig = {"data": [base_chart, meter_chart],
           "layout": layout}
    plot(fig, filename='guage.html')
    py.iplot(fig, filename='gauge-meter-chart')
