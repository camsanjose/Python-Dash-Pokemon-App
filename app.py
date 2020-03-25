import http.client
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import dash_table

df_url = "https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv"
df = pd.read_csv(df_url)

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
    dash_table.DataTable(
        id='table',
        columns=[{"name":i,"id":i} for i in df.columns],
        data=df.to_dict('records')
        ),
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


if __name__ == '__main__':
    app.run_server(debug=True)