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
df_type = df['Type 1'].dropna().sort_values().unique()
df.set_index('id', inplace=True, drop=False)
df_col= ['Total', 'Attack','Defense', 'Speed']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title= "My Pokemon Dash App"

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='About', 
        style= {'font-weight': 'bold',
                'background-image': 'url(https://i1.wp.com/republica.gt/wp-content/uploads/2017/10/pikachu.jpg?fit=1600%2C1436&ssl=1)',
                'background-size': '150px 100px'},
        children= [
    html.Div(children=['''
    Hello! Welcome to the Dash Pokemon app.
    ''']),
    html.Div(children=['''
    This will help you to get to know in-depth all pokemon in hopes you can 
    choose which one is best for you.  
    ''']),
        html.Div(children=['''
    In this section, you will get the chance to choose your own Pokemon and find out its Type, its total
    amount of points, and the level of Attack, Defense and Speed. There are many pokemon to choose from, 
    so pick wisely. A random Pokemon is chosen but please choose whatever Pokemon you want. 
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
        ]),
    html.Div(children=['''
        Click on the tabs at the top of the page to see other cool features!  
        ''']),
    ])]),
    dcc.Tab(label='Data',
    style= {'font-weight': 'bold',
            'background-image': 'url(https://i.redd.it/6to6dwa8v5241.jpg)',
            'background-size': '150px'},
    children= [
        html.Div(children=['''
        If you want to see how the Pokemon of your choice compares to others, you can do so with 
        the table and graphs below. When choosing any Pokemon in the table below, this will show 
        up in the graphs underneath with the color pink. 
        ''']),
        html.Div(children=['''
        The data is predetermined to be in alphabetical order. However, if you want to see how it compares to,
        lets say its Total points, click on the Pokemon you want (the box on your left) 
        and then click on the arrows next to the column header (in this case, Total). This way, 
        you can see where it stands in comparison to other Pokemon in the graphs underneath.      
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
        Here we can visually see how they are in comparison to the other Pokemon. The Pokemon 
        you choose will change to the color pink in all of the graphs. There are four graphs, 
        accounting for its Total points, as well as the attack, defense and speed levels.  
        ''']),
        html.Div(id='datatable-row-ids-container')
    ]), 
    dcc.Tab(label='Characteristic',
    style= {'font-weight': 'bold',
            'background-image': 'url(https://estaticos.muyinteresante.es/media/cache/1140x_thumb/uploads/images/gallery/5b0fcfa25bafe83df2c203b3/pokemon0_0.jpg)',
            'background-size': '150px'},
    children= [
        html.Div(children=['''
        In this section we will see global variables, were we will see the characteristics of the 
        Total points, the Attack levels, the Defense levels, the Speed levels, and see what type of 
        Pokemon is the most common or uncommon.  
        ''']), 
        dcc.Dropdown(
                id='type-of-pokemon',
                options=[{'label': i, 'value': i} for i in df_type],
                value='Water'
            ),
        dcc.RadioItems(
                id='variable',
                #crossfilter-yaxis-type
                options=[{'label': i, 'value': i} for i in df_col],
                value='Total',
                labelStyle={'display': 'inline-block'}
            )
    ]
    )]
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

#@app.callback(
#    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
#    [dash.dependencies.Input('crossfilter-column', 'value')])

#def update_graph(column_name, value):
#    dff = df[df['Year'] == value]
#    return dff.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)