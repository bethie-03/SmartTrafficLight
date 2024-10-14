import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
import os

def count_total_weather(folder):
    one = 0
    two = 0
    for sub_folder in os.listdir(folder):
        if len(os.listdir(os.path.join(folder, sub_folder))) == 1:
            one += 1
        elif len(os.listdir(os.path.join(folder, sub_folder))) == 2:
            two += 1
    return one, two

def find_cameras(folder):
    camera_one = []
    camera_two = []
    for sub_folder in os.listdir(folder):
        if len(os.listdir(os.path.join(folder, sub_folder))) == 1:
            camera_one.append(sub_folder)
        elif len(os.listdir(os.path.join(folder, sub_folder))) == 2:
            camera_two.append(sub_folder)
    return camera_one, camera_two

folder_night = r"C:\Users\phuon\Downloads\Weather\Night"
folder_daylight = r"C:\Users\phuon\Downloads\Weather\Daylight"
folder_cameras = r"C:\Users\phuon\Downloads\Weather\Cameras"

colors = ['#94AAD6','#7388C1']
one, two = count_total_weather(folder_cameras)
camera_one, camera_two = find_cameras(folder_cameras)

fig = go.Figure(data=go.Bar(x=['Daylight', 'Night'], 
                            y=[len(os.listdir(folder_daylight)), len(os.listdir(folder_night))], 
                            marker_color=colors, 
                            width=0.3,
                            text=[len(os.listdir(folder_daylight)), len(os.listdir(folder_night))],  
                            textposition='outside'))

fig.update_layout( margin=dict(l=80, r=50, t=20, b=50), 
                  height=520,
                  xaxis_title='Observations', 
                  yaxis_title='Weather',
                  xaxis=dict(tickfont=dict(size=12)), 
                  yaxis=dict(tickfont=dict(size=12)),
                  showlegend=False, 
                  font=dict(family='Georgia', size=12))

fig1 = go.Figure(data=go.Pie(labels=['Daylight', 'Night'], 
                             values=[len(os.listdir(folder_daylight)), 
                                     len(os.listdir(folder_night))],
                             hole=0.6))
fig1.update_layout(margin=dict(l=50, r=80, t=20, b=80),
                   height=520,
                   showlegend=True, 
                   font=dict(family='Georgia', size=12))

fig1.update_traces(marker=dict(colors=colors))

fig2 = go.Figure(data=go.Bar(x=['Cameras contain both weather types', 'Cameras contain one weather type'], 
                            y=[one, two],
                            marker_color=colors, 
                            width=0.3,
                            text=[one, two],  
                            textposition='outside'))

fig2.update_layout( margin=dict(l=80, r=50, t=20, b=50), 
                  height=520,
                  xaxis_title='Number of cameras', 
                  yaxis_title='Number of weathers',
                  xaxis=dict(tickfont=dict(size=12)), 
                  yaxis=dict(tickfont=dict(size=12)),
                  showlegend=False, 
                  font=dict(family='Georgia', size=12))

fig3 = go.Figure(data=go.Pie(labels=['Cameras contain both weather types', 'Cameras contain one weather type'], 
                             values=[one, two],
                             hole=0.6))
fig3.update_layout(margin=dict(l=50, r=80, t=20, b=80),
                   height=520,
                   showlegend=True, 
                   font=dict(family='Georgia', size=12))

fig3.update_traces(marker=dict(colors=colors))

header = dict(values=['Cameras contain both weather types', 'Cameras contain one weather type'],
              fill=dict(color=colors[1]),
              font=dict(color='white'))
cells = dict(values=[camera_one, camera_two],
             height=30,
             font=dict(color=['black', 'black']))
table = go.Table(header=header, cells=cells)
fig4 = go.Figure(data=table)
fig4.update_layout(
margin=dict(l=50, r=50, t=0, b=0),height=700,
font=dict(family='Georgia', size=13))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        html.H1('WEATHER ANALYSIS DASHBOARD',
                style={'textAlign': 'center', 'font-family': 'Georgia', 'font-size': 50,'font-style': 'bold'}),
        html.P('(Write statistics based on data collected phase 1).',
               style={'textAlign': 'center', 'font-size': 15, 'font-style': 'italic'}),
        html.H3('COMPARISION OF OBSERVATION BETWEEN DAYLIGHT AND NIGHT',
                style={'textAlign': 'center', 'font-family': 'Georgia', 'font-size': 25,'font-style': 'bold'}),
        html.Div(
            className='row',
            style={'margin-bottom': '20px'},
            children=[
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='day_night_bar', figure=fig)
                    ]
                ),
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='day_night_pie', figure=fig1),

                    ]
                )
            ]
        ),
        html.P(
            [
                'These are two charts showing the comparison between the total number of images taken during the daytime (Daylight) and at night (Night). We can see that the total for Daylight is 8,744, while Night has a total of 7,280.',
                html.Br(),
                'Although there is a discrepancy favoring Daylight, the percentage difference is only 9.2%, which is not a very large number and is still acceptable.'
            ],
            style={'textAlign': 'center', 'fontSize': 15, 'fontFamily': 'Georgia'}
        ),
        html.H3('COMPARISION OF CAMERAS CONTAIN BOTH DAYLIGHT AND NIGHT AND CAMERAS CONTAIN ONE',
                style={'textAlign': 'center', 'font-family': 'Georgia', 'font-size': 25,'font-style': 'bold'}),
            html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='one_two_bar', figure=fig2)
                    ]
                ),
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='one_two_pie', figure=fig3),

                    ]
                )
            ]
        ),
        html.P(
            [
                'These are two charts showing the comparison in quantity between cameras that include both types of weather and those that only include one type. We want all cameras to include both types of weather; the existence of some cameras that only capture either daytime or nighttime will affect the quality of the model.',
                html.Br(),
                'Specifically, there are a total of 28 camera ID codes, of which 6 cameras do not have both types of weather, and in the next round, we will make sure to supplement them.'
            ],
            style={'textAlign': 'center', 'fontSize': 15, 'fontFamily': 'Georgia'}
        ),
        html.P(''),
        html.P('This table below lists the specific cameras belong to two mentioned categories',
               style={'textAlign': 'center', 'fontSize': 15, 'fontFamily': 'Georgia'}),
        dcc.Graph(figure=fig4),
        html.P(''),
        html.Div(["COMPARISION OF OBSERVATION BETWEEN DAYLIGHT AND NIGHT, CAMERA ID: ",dcc.Input(id='input-cameraid', value='5deb576d1dc17d7c5515ad19', type='text',style={'height':'30px','font-size':20,'font-family': 'Georgia'}),
                                                ],
                                                style={'font-size':25,
                                                       'font-family': 'Georgia',
                                                       'color': 'midnightblue', 
                                                       'textAlign': 'center'}),
                                        html.Div(
            className='row',
            style={'margin-bottom': '20px'},
            children=[
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='cameras_bar')
                    ]
                ),
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='cameras_pie'),

                    ]
                )
            ]
        )
            ]
        )

@app.callback(Output(component_id='cameras_bar',component_property='figure'),
              Input(component_id='input-cameraid',component_property='value'))
def get_graph(entered_camerid):
    folder_name = entered_camerid
    folder_path = os.path.join(folder_cameras, folder_name)
    
    night_count = len(os.listdir(os.path.join(folder_path, 'Night')))
    daylight_count = len(os.listdir(os.path.join(folder_path, 'Daylight')))
    
    fig5 = go.Figure(data=go.Bar(x=['Daylight', 'Night'], 
                            y=[daylight_count, night_count], 
                            marker_color=colors, 
                            width=0.3,
                            text=[daylight_count, night_count],  
                            textposition='outside'))

    fig5.update_layout( margin=dict(l=80, r=50, t=20, b=50), 
                    height=520,
                    xaxis_title='Observations', 
                    yaxis_title='Weather',
                    xaxis=dict(tickfont=dict(size=12)), 
                    yaxis=dict(tickfont=dict(size=12)),
                    showlegend=False, 
                    font=dict(family='Georgia', size=12))
    return fig5

@app.callback(Output(component_id='cameras_pie',component_property='figure'),
              Input(component_id='input-cameraid',component_property='value'))
def get_graph(entered_camerid):
    folder_name = entered_camerid
    folder_path = os.path.join(folder_cameras, folder_name)
    
    night_count = len(os.listdir(os.path.join(folder_path, 'Night')))
    daylight_count = len(os.listdir(os.path.join(folder_path, 'Daylight')))
    
    fig6 = go.Figure(data=go.Pie(labels=['Daylight', 'Night'], 
                             values=[night_count, daylight_count],
                             hole=0.6))
    fig6.update_layout(margin=dict(l=50, r=80, t=20, b=80),
                    height=520,
                    showlegend=True, 
                    font=dict(family='Georgia', size=12))

    fig6.update_traces(marker=dict(colors=colors))
    return fig6

if __name__ == '__main__':
    app.run_server(debug=True)
