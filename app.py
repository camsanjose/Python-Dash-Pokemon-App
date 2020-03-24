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
import base64


app = dash.Dash(__name__)
server = app.server
image_filename  = 'url(https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/1200px-International_Pok%C3%A9mon_logo.svg.png)'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div(
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),
    html.Div(children=['''
        Hello! Welcome to the Dash Pokemon app.  
        This will help you to get to know in-depth all pokemon in hopes you can 
        choose which one is best for you.
    ''']),
    html.Div(children=['''
        There are three types of main characteristics
        in all Pokemon: stamina, defense, and attack. 
    ''']),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(dash.dependencies.Output('display-value', 'children'), [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)