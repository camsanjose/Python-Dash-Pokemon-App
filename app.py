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
df['id'] = df['Name']
df.set_index('id', inplace=True, drop=False)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title= "My Pokemon Dash App"

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='About', 
        children= [
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
        data= df.to_dict('records'),
        columns=[{'name': i, 'id': i, 'deletable': True} for i in df.columns
        if i != 'id'
        ])
    ])]),
    dcc.Tab(label='Pokemon',
    style= {'background-image': 'url(https://estaticos.muyinteresante.es/media/cache/1140x_thumb/uploads/images/gallery/5b0fcfa25bafe83df2c203b3/pokemon0_0.jpg)'},
    children= [
        html.Div(children=['''
        Now that we have chosen our Pokemon to analyze more in-depth, we can now see how it compares
        with other Pokemon.  
        ''']),
        dash_table.DataTable(
            id='datatable',
            columns=[
                {'name': i, 'id': i, 'deletable': True} for i in df.columns
            ],
            data=df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode='multi',
            row_selectable='multi',
            row_deletable=True,
            selected_rows=[],
            page_action='native',
            page_current= 0,
            page_size= 10,
        ),
        html.Div(children=['''
        Then we can visually see how they are in comparison to the other Pokemon. 
        ''']),
        html.Div(id='datatable-row-ids-container')
    ])]
)])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(
    Output('table-container', 'data'),
    [Input('filter_dropdown', 'value')] )
def display_table(states):
    dff = df[df['Name']==states]
    return dff.to_dict('records')

@app.callback(
    Output('datatable-row-ids-container', 'children'),
    [Input('datatable', 'derived_virtual_row_ids'),
     Input('datatable', 'selected_row_ids'),
     Input('datatable', 'active_cell')])

def update_graphs(row_ids, selected_row_ids, active_cell):
    selected_id_set = set(selected_row_ids or [])

    if row_ids is None:
        dff = df
        row_ids = df['id']
    else:
        dff = df.loc[row_ids]

    active_row_id = active_cell['row_id'] if active_cell else None

    colors = ['#FF69B4' if id == active_row_id
              else 'deeppink' if id in selected_id_set
              else '#0074D9'
              for id in row_ids]

    return [
        dcc.Graph(
            id=column + '--row-ids',
            figure={
                'data': [
                    {
                        'x': dff['Name'],
                        'y': dff[column],
                        'type': 'bar',
                        'marker': {'color': colors},
                    }
                ],
                'layout': {
                    'xaxis': {'automargin': True},
                    'yaxis': {
                        'automargin': True,
                        'title': {'text': column}
                    },
                    'height': 250,
                    'margin': {'t': 10, 'l': 10, 'r': 10},
                },
            },
        )
        for column in ["Total","Attack","Defense", "Speed"] if column in dff
    ]


if __name__ == '__main__':
    app.run_server(debug=True)