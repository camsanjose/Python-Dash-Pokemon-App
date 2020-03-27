import http.client
import os
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go

df_url = "https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv"
df = pd.read_csv(df_url)
df= df[['Name', 'Type 1','Total', 'Attack','Defense', 'Speed']]
df= df.dropna().drop_duplicates(keep= 'first')
df= df.sort_values('Name')
states = df['Name'].unique().tolist()


app = dash.Dash(__name__)
server = app.server
app.title= "My Pokemon Dash App"

app.layout = html.Div(style= {'background-image': 'url(https://estaticos.muyinteresante.es/media/cache/1140x_thumb/uploads/images/gallery/5b0fcfa25bafe83df2c203b3/pokemon0_0.jpg)'},
children=[
    html.H1('Pokemon', style={
        'color': 'blue',
        'textAlig':"center",
        'background-image': 'url(https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/1200px-International_Pok%C3%A9mon_logo.svg.png)',
        'background-size': '200px 100px',
        'background-position': 'center',
    }),
    html.Div(children=['''
    Hello! Welcome to the Dash Pokemon app.  
    This will help you to get to know in-depth all pokemon in hopes you can 
    choose which one is best for you.
    ''']),
    html.Div(children=['''
    In order not to present to you a table with all the possible Pokemons, you 
    will get the chance to choose your own Pokemon and find out its Type, its total
    amount of points, and the level of Attack, Denfense and Speed. 
    ''']),
    html.Div(
        children=[
            dcc.Dropdown(
                id='filter_dropdown',
                options=[{'label':st, 'value':st} for st in states],
                value = states[113]
                ),
    dash_table.DataTable(
        id='table-container', 
        columns=[{'name': i, 'id': i, 'deletable': True} for i in df.columns]
        )
        ]),
    html.Div(children=['''
    Now that we have chosen our Pokemon to analyze more in-depth, we can now see how it compares
    with other Pokemon.  
    '''])
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(
    Output('table-container', 'data'),
    [Input('filter_dropdown', 'value') ] )
def display_table(states):
    dff = df[df['Name']==states]
    return dff.to_dict('records')

def update_Pgraph(data, input_value):
    if data is None:
        return {}, {}
    df.to_dict('records')
    return  {
                'data': [
                    go.Bar(
                        x=df[df['Name'] == i]['Total'] if i in input_value else [],
                        y=df[df['Name'] == i]['Name'] if i in input_value else [],
                        mode='markers',
                        marker={'size':15,
                                      'opacity':0.5,
                                      'line':{'width':0.5,'color':'green'}
                                }, name= i
                    ) for i in input_value
                ],
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'Total level'},
                    yaxis={'title': 'Total level'},
                    hovermode='closest'
                ),
            }



if __name__ == '__main__':
    app.run_server(debug=True)