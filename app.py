import http.client
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import dash_table
from dash.dependencies import Input, Output

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
        'color': 'lightblue',
        'textAlig':"center",
    }),
    html.Div(children=['''
    Hello! Welcome to the Dash Pokemon app.  
    This will help you to get to know in-depth all pokemon in hopes you can 
    choose which one is best for you.
    ''']),
    html.Div(children=['''
    There are three types of main characteristics
    in all Pokemon: stamina, defense, and attack. 
    ''']),
#    html.Label('Dropdown'),
#    dcc.Dropdown(
#        id='my-dropdown',
#        options=opt_vore,
#        value=db_vore[0]
#            ),
    html.Div(
        children=[
            dcc.Dropdown(
                id='filter_dropdown',
                options=[{'label':st, 'value':st} for st in states],
                value = states[0]
                ),
    dash_table.DataTable(
        id='table-container', 
        columns=[{'id': c, 'name': c} for c in df.columns.values])
        ]),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(dash.dependencies.Output('display-value', 'children'), [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output('table-container', 'data'),
    [Input('filter_dropdown', 'value') ] )
def display_table(states):
    dff = df[df['Name']==states]
    return dff.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)