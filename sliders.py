import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd



# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout and styling
app.layout = html.Div([
       # Sliders for C, P, G, R, N
    html.Label(id='C-label', style={'color': 'white', 'fontSize': '150%'}),
    dcc.Slider(id='C-slider', min=0, max=400, value=200, step=10, updatemode='drag'),

    html.Br(),

    html.Label(id='P-label', style={'color': 'white', 'fontSize': '150%'}),
    dcc.Slider(id='P-slider', min=0, max=200, value=75, step=5, updatemode='drag'),

    html.Br(),

    html.Label(id='G-label', style={'color': 'white', 'fontSize': '150%'}),
    dcc.Slider(id='G-slider', min=0, max=100, value=70, step=5, updatemode='drag'),

    html.Br(),

    html.Label(id='R-label', style={'color': 'white', 'fontSize': '150%'}),
    dcc.Slider(id='R-slider', min=0, max=3000, value=2000, step=100, updatemode='drag'),

    html.Br(),

    html.Label(id='N-label', style={'color': 'white', 'fontSize': '150%'}),
    dcc.Slider(id='N-slider', min=0, max=200, value=100, step=5, updatemode='drag'),

    html.Br(),

     # Flexbox container to hold both graphs
    html.Div([
        # Histogram for output indicators
        dcc.Graph(id='histogram', style={'flex': '1'}),  # First graph
        
        # Second bar chart
        dcc.Graph(id='bar-chart', style={'flex': '1'})  # Second graph
    ], style={'display': 'flex'}),
    

# Output indicators and R_Total section in a flexbox
html.Div([
    # Left section for Output indicators
    html.Div([
        html.Div(id='R_NFT-out', style={'color': 'lime'}),
        html.Div(id='R_Gas-out', style={'color': 'lime'}),
        html.Div(id='R_Prizes-out', style={'color': 'lime'}),
        html.Div(id='C_Total-out', style={'color': 'lime'}),
    ], style={'flex': '1'}),
    
    # Right section for R_Total
    html.Div([
        html.H3("R_Total should be bigger than C_Total + R_Prizes", style={'color': 'white'}),
        html.Div(id='R_Total-out', style={'color': 'lime'}),
        html.Div(id='sum_CTotal_RPrizes-out', style={'color': 'lime'}),
    ], style={'flex': '1'})
], style={'display': 'flex'}),
    
    
], style={'backgroundColor': 'black', 'padding': '20px'})

# Define callback to update outputs and labels
@app.callback(
    [Output('C-label', 'children'),
     Output('P-label', 'children'),
     Output('G-label', 'children'),
     Output('R-label', 'children'),
     Output('N-label', 'children'),
     Output('histogram', 'figure'),

    Output('R_NFT-out', 'children'),
    Output('R_NFT-out', 'style'),
    Output('R_Gas-out', 'children'),
    Output('R_Gas-out', 'style'),
    Output('R_Prizes-out', 'children'),
    Output('R_Prizes-out', 'style'),
    Output('C_Total-out', 'children'),
    Output('C_Total-out', 'style'),

    Output('bar-chart', 'figure'),

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

    # Create data for the histogram
    data = pd.DataFrame({
        'Metrics': ['R_NFT', 'R_Gas', 'R_Prizes', 'C_Total'],
        'Values': [R_NFT, R_Gas, R_Prizes, C_Total]
    })

    # Create the histogram figure using Plotly
    fig = px.bar(data, x='Metrics', y='Values', color='Metrics')

    fig.update_layout(autosize=False, width=500, height=400,
                      margin=dict(l=50, r=50, b=100, t=100, pad=4),
                      paper_bgcolor="Black", font=dict(color="White"))
    
    # Create data for the additional bar chart
    additional_data = pd.DataFrame({
        'Metrics': ['Total Revenue (R_Total)', 'C_Total + R_Prizes'],
        'Values': [R_Total, sum_CTotal_RPrizes]
    })
    
    # Create the additional bar chart
    additional_fig = px.bar(additional_data, x='Metrics', y='Values', color='Metrics')
    
    additional_fig.update_layout(autosize=False, width=500, height=400,
                      margin=dict(l=50, r=50, b=100, t=100, pad=4),
                      paper_bgcolor="Black", font=dict(color="White"))

    return (f"Cost to produce each car (C): {C}",
            f"Price of minting an NFT car (P): {P}",
            f"Price of a full tank of gas (G): {G}",
            f"Total prize pool for the top 10 players (R): {R}",
            f"Number of players in the monthly tournament (N): {N}",
            fig,
            f"Total Revenue from NFT Sales (R_NFT) = N * P: {R_NFT}", {'color': 'blue', 'fontSize': '150%'},
            f"Total Revenue from Gas (R_Gas) = N * G (assuming 1 purchase per player) : {R_Gas}", {'color': 'red', 'fontSize': '150%'},
            f"Total Prize Pool (R_Prizes) = R: {R_Prizes}", {'color': 'green', 'fontSize': '150%'},
            f"Total Costs (C_Total) = N * C: {C_Total}", {'color': 'magenta', 'fontSize': '150%'},
            additional_fig,
            f"Total Revenue (R_Total) = R_NFT + R_Gas: {R_Total}",
            f"C_Total + R_Prizes: {sum_CTotal_RPrizes}")

if __name__ == '__main__': 
    app.run_server(debug=True)
