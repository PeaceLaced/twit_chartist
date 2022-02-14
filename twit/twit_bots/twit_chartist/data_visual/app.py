# -*- coding: utf-8 -*-
'''
https://github.com/theo-brown/dash-examples/blob/7dbd25c758b370dbbbae454cb147d64ea0ea2d95/basic-realtime-plot.py
'''
import dash
#import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pytz
#import numpy as np
from time import time
#from random import randrange, uniform
from datetime import datetime, timedelta, date
#from twit.progress_report.api_progress_report import Progress as progress

'''
Default template: 'plotly'
Available templates: ['ggplot2', 'seaborn', 'simple_white', 'plotly',
                      'plotly_white', 'plotly_dark', 'presentation', 
                      'xgridoff', 'ygridoff', 'gridon', 'none']
'''
import plotly.io as pio
pio.templates.default = "plotly_dark"

REFRESH_RATE_MS = 1000

start_time = time()
since_start = time() - start_time
generated_date = date.today().strftime('%d-%b-%Y')

def generate_data():
    
    # ???_dd-mmm-yyyy.log (dd-mmm-yyyy)
    # TODO: set ??? for data filename
    manually_set_file_date = False
    
    if not manually_set_file_date:
        file_name = 'twit/data_visual/data_dump/???_' + generated_date + '.log'
        
    if manually_set_file_date:
        file_name = 'twit/data_visual/data_dump/???_' + manually_set_file_date + '.log'
  
    # READ DATA FROM FILE

    f = open(file_name, 'r')
    read_file_data = f.readline()
    f.close()
    
    return datetime.now(pytz.timezone('US/Eastern')) - timedelta(since_start), read_file_data

app = dash.Dash(__name__, update_title=None)

#figure_margin = go.layout.Margin(b=0, l=0, r=0, t=0) 

# TODO: set ??? for x/y axis headers
fig = go.Figure(go.Scatter(x=[], y=[], mode='lines'), 
                layout={'xaxis_title': "???",
                        'yaxis_title': "???",
                        'font_family': 'Nunito, sans-serif',
                        'font_size': 12,
                        #'margin': figure_margin
                        'margin_b':25,
                        'margin_l':25,
                        'margin_r':25,
                        'margin_t':25})

live_update_graph_1 = dcc.Graph(id='live_update_graph_1',
                                animate=False,
                                style={'width': '100%'},
                                config={'displayModeBar': False,
                                        'staticPlot': True},
                                figure=fig)
# TODO: set ??? for header
app.layout = html.Div([
                 html.Div([
                     html.H2("???"),
                     live_update_graph_1, # dcc.Graph()
                     dcc.Interval(id='update_timer_1', interval=REFRESH_RATE_MS)])])
    
# when input is changed, output changes automatically
                    # component_id, component_property
@app.callback(Output('live_update_graph_1', 'extendData'),
              Input('update_timer_1', 'n_intervals'))

# automatically called when then input changes
def update_graph_1(n_intervals: int):

    new_x, new_y = generate_data()
    # when False is passed to new_x/y, nothing should happen
    if new_x:
        if new_y:
            return {'x': [[new_x]],
                    'y': [[new_y]]}, [0], None
    # because extendData is the component_property of output
    # new_x and new_y are appended to the trace at component_id live_update_graph_1

app.run_server(debug=True, port=8051)