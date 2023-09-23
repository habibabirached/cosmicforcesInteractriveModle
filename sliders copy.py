import dash
from dash import dcc, html, Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    # Sliders for C, P, G, R, N
    html.Label('Cost to produce each car (C)'),
    dcc.Slider(id='C-slider', min=0, max=1000, value=200, step=10, updatemode='drag'),

    html.Label('Price of minting an NFT car (P)'),
    dcc.Slider(id='P-slider', min=0, max=200, value=75, step=5, updatemode='drag'),

    html.Label('Price of a full tank of gas (G)'),
    dcc.Slider(id='G-slider', min=0, max=100, value=70, step=5, updatemode='drag'),

    html.Label('Total prize pool for the top 10 players (R)'),
    dcc.Slider(id='R-slider', min=0, max=5000, value=2000, step=100, updatemode='drag'),

    html.Label('Number of players in the monthly tournament (N)'),
    dcc.Slider(id='N-slider', min=0, max=200, value=100, step=5, updatemode='drag'),

    # Output indicators
    html.Div(id='R_NFT-out'),
    html.Div(id='R_Gas-out'),
    html.Div(id='R_Prizes-out'),
    html.Div(id='C_Total-out'),

    # Bottom section
    html.Div([
        html.Hr(),
        html.H3("R_Total should be bigger than C_Total + R_Prizes"),
        html.Div(id='R_Total-out'),
        html.Div(id='sum_CTotal_RPrizes-out'),
    ])
])

@app.callback(
    [Output('R_NFT-out', 'children'),
     Output('R_Gas-out', 'children'),
     Output('R_Prizes-out', 'children'),
     Output('C_Total-out', 'children'),
     Output('R_Total-out', 'children'),
     Output('sum_CTotal_RPrizes-out', 'children')],
    [Input('C-slider', 'value'),
     Input('P-slider', 'value'),
     Input('G-slider', 'value'),
     Input('R-slider', 'value'),
     Input('N-slider', 'value')]
)
def update_output(C, P, G, R, N):
    R_NFT = N * P
    R_Gas = N * G  # Assuming one additional gas purchase per player
    R_Prizes = R
    C_Total = N * C
    R_Total = R_NFT + R_Gas
    sum_CTotal_RPrizes = C_Total + R_Prizes

    return (f"Total Revenue from NFT Sales (R_NFT): {R_NFT}",
            f"Total Revenue from Gas (R_Gas): {R_Gas}",
            f"Total Prize Pool (R_Prizes): {R_Prizes}",
            f"Total Costs (C_Total): {C_Total}",
            f"Total Revenue (R_Total): {R_Total}",
            f"C_Total + R_Prizes: {sum_CTotal_RPrizes}")

if __name__ == '__main__':
    app.run_server(debug=True)
