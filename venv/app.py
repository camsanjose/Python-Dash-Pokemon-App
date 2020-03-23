#import http.client

#conn = http.client.HTTPSConnection("pokemon-go1.p.rapidapi.com")

#headers = {
#    'x-rapidapi-host': "pokemon-go1.p.rapidapi.com",
#    'x-rapidapi-key': "11a0831306msh85289b71ee29d28p1b0d2ajsnd56ec6de06bd"
#    }

#conn.request("GET", "/pokemon_stats.json", headers=headers)

#res = conn.getresponse()
#data = res.read()

#print(data.decode("utf-8"))

#print(type(data))
import os
import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
    html.H2('Pokemon',style={
            'textAlig':"center",
            'color': 'lightblue'
            }),
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