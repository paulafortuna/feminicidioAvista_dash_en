#https://dash.plotly.com/layout

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from utils import colors
from utils import font_for_plots
import json

#################################
# Dash variables
#################################

app = dash.Dash(__name__)
app.title = 'Feminicídio à Vista'
server = app.server

#################################
# Load data
#################################


# Load news per year
with open('./data_to_visualize/dict_tables_news_per_year.json') as json_file:
    dict_tables_per_year = json.load(json_file)


min_year = min([int(i) for i in dict_tables_per_year.keys()])
df_table_temp = dict_tables_per_year[str(min_year)]

# Load news per location
with open('./data_to_visualize/dict_tables_news_per_district.json') as json_file:
    dict_tables_per_district = json.load(json_file)

df_crimes_continental_table_temp = dict_tables_per_district["LISBOA"]

#################################
# Load plots
#################################

# Animation plot
fig_anim = plotly.io.read_json('./data_to_visualize/plot_animation.json')

# Bar plot
fig = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_year.json')

# Cloropleth plot
fig_plot = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_district_bar.json')  # to bar
#fig_plot = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_district.json') # to cloropeth



###############################
# Layout
###############################

app.layout = html.Div(children=[
    html.Div(
        id='initial_page',
        children=[
            html.Div(
                id='container',
                children=[
                    html.H1(
                            id='pagename',
                            children='FEMINICÍDIO À VISTA',
                            ),
                    html.P(
                            id='pagedescription',
                            children='Feminicídio à Vista is a datactivism plataform. It calls attention '
                                     'and demands an answer to the violence against women in Portugal that leads to murder many times. '
                                     'It include itself in open-source movements to challenge existing power relations.',
                    ),

                ],
            ),# Change app order
            html.Div(
                    id='continue',
                    children='Continue down',
            ),
        ],
    ),
    html.Div(
        id='animation_plot_section_container',
        children=[
                html.Div(
                    id='animation_plot',
                    children=[
                        html.H3("NOT ONE WOMAN LESS!"),
                        html.P(
                            id='animation_description',
                            children='In the majority of feminicide cases, there is some type of relationship between the perpetrator and victim. '
                                     'However, there is a diversity of stories and crimes that we should not forget.',
                        ),
                        html.Div(id='animation_description_container_fill'),
                        html.Div(id='animation_container',
                                 children=[
                                    dcc.Graph(
                                        id='animation',
                                        figure=fig_anim,
                                    ),
                                 ],
                        ),
                    ],
                ),
        ],
    ),
    html.Div(
        id='frequencies_plot_section_container',
        children=[
                    html.Div(
                        id='frequencies_plot',
                        children=[
                            html.H3("NEWS IN TIME"),
                            html.P(
                                id='time_description',
                                children='The number of femicide cases seems to be increasing over time. '
                                         'This may indicate an increase on femicide number, an increased interest in the topic from media, '
                                         'or an increased data accessibiity for more recent material in Arquivo.pt.',
                            ),
                            dcc.Graph(
                                id='graph',
                                figure=fig,
                            ),
                            html.Div(
                                id='instruction_freq_plot_container',
                                children=[
                                    html.P(
                                        id="instruction_freq_plot",
                                        children="Press a plot bar to update the table with correspondent cases",
                                    ),
                                ],
                            ),
                            html.Div(id='instruction_freq_plot_container_fill'),
                            dash_table.DataTable(
                                id='table_year_output',
                                columns=[{"name": i, "id": i} for i in ['Notícia','Distrito']],
                                data=df_table_temp,
                                editable=False,
                                style_cell={'textAlign': 'left','backgroundColor': colors['table_background'],'color': colors['table_font_color_header']},
                                style_header={'backgroundColor': colors['table_background_header'],'fontWeight': 'bold','color': colors['table_font_color_header']},
                            ),
                        ],
                    ),
                ],
    ),
    html.Div(
        id='regions_plot_section_container',
        children=[
            html.Div(
                id='regions_plot',
                children=[
                    html.H3("NEWS BY DISTRICT"),
                    html.P(
                        id='regions_description',
                        children='The number of femicides is bigger in the regions where more people live. However, the relationship '
                                 'between crime and inhabitant number is not linear. For instance, Braga is the third city with more people. '
                                 'However, it appears behind Setúbal and Santarém districts with lessa cases.',
                    ),
                    dcc.Loading(
                        id="loading-1",
                        type="graph",
                        children=html.Div(id="loading-output-1"),
                    ),
                    dcc.Graph(
                        id='choropleth',
                        figure=fig_plot,
                    ),
                    html.Div(id='pre_instruction_map_container_fill'),
                    html.Div(
                        id='instruction_map_container',
                        children=[
                            html.P(
                                id="instruction_map",
                                children="Press a plot bar to update the table with correspondent cases",
                            ),
                        ],
                    ),
                    html.Div(id='instruction_map_container_fill'),
                    dash_table.DataTable(
                        id='table_region_output',
                        columns=[{"name": i, "id": i} for i in ['Notícia','Ano']],
                        data=df_crimes_continental_table_temp,
                        style_cell={'textAlign': 'left', 'backgroundColor': colors['table_background'],
                                    'color': colors['table_font_color_header']},
                        style_header={'backgroundColor': colors['table_background_header'], 'fontWeight': 'bold',
                                      'color': colors['table_font_color_header']},
                    ),
                ],
            ),
        ],
    ),
    html.Div(
        id='manifesto',
        children=[
            html.H3("MANIFESTO"),
            html.P(
                id='manifesto_description',
                children='The "Feminicídio à Vista" project goal is to bring attention to the femicide problem and not let '
                         'the murdered women forgotten. Arquivo.pt API allowed us to recover the those stories and '
                         'retrieve a femicide dataset that we make available to the community. '
                         'Those data can be used not only by researchers but also to build artificial intelligence models.'
                         ' With such tools it would be possible to find and annotate other femicide news.'
            ),
            html.P(
                id='manifesto_description2',
                children='Femicide is a relatively new term. It refers to extermination of women.'
                         ' These crimes can not be seen as disconnected from gender issues and intensions to control women behavior and existence.'
                         'In some countries femicide crime is now present in the law. '
                         'However, this is not the case in Portuguese. In Portugal there is a void in the law [1] and there are studies missing on this issue [2]. ',
            ),
            html.P(
                id='manifesto_description3',
                children= 'This project adds to other research efforts [3] and makes available '
                         'not only a dataset but also a open-source platform. In this it is possible '
                         'to not forget the victims, and see the relationship between news statistics and space and time. '
                        'The presented data refer to individual femicide cases. '
                         'However, femicide requires a collective societal response. For this '
                         'we need to act and the first steps are recognize femicide as a crime, collect data, '
                         'analyse those data for interventions planning. ',
            ),
            html.P(
                id='manifesto_description4',
                children= '*This project is not*: a set of official statistics about femicide in Portugal. '
                          'In this project we collected news on the Arquivo.pt. '
                          'This method has limitations and probably misses data. This project is only '
                          'an initial data collection effort, that points to the need of officially better document those crimes. ',
            )
        ],
    ),
    html.Div(
        id='contacto',
        children=[
            html.H3("+INFO"),
            html.P(
                id='contacto_description',
                children= ['If you want to know more about this project or author, please visit:',
                           dcc.Markdown('''[GitHub](https://github.com/paulafortuna/feminicidioAvista) and [LinkedIn](https://pt.linkedin.com/in/paula-fortuna-a6b75a7a).'''),
                            dcc.Markdown('''[PT](https://feminicidioavista.herokuapp.com/)'''),
                           ]
            )
        ],
    ),

])


@app.callback(Output('table_year_output', 'data'), [
    Input('graph', 'clickData')])
def update_output(*args):
    year = args[0]['points'][0]['x']
    return dict_tables_per_year[str(year)]


@app.callback(Output('table_region_output', 'data'), [
    Input('choropleth', 'clickData')])
def update_output(*args):
    #district = args[0]['points'][0]['location'] #instruction to cloropeth
    district = args[0]['points'][0]['x'] #instruction to barplot
    return dict_tables_per_district[district]


if __name__ == '__main__':
    app.run_server()
    app.run_server()