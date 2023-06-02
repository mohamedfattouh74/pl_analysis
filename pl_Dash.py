from dash import Dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from PIL import Image
from dash import dash_table

pd.set_option("display.max_columns", None)
pl_logo = Image.open('C:/Users/LENOVO/Downloads/Data analysis/PL_analysis/pl_logo.png')
pl_df = pd.read_csv('C:/Users/LENOVO/Downloads/Data analysis/PL_analysis/pl_stats.csv')

pl_df["season"] = pl_df["season"].astype('str')
pl_df["season"] = pl_df["season"].str.split('-').str[0]
# print(pl_df.head())
dbc_css="https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ,dbc_css])
load_figure_template('QUARTZ')

app.layout = html.Div([

    html.Header(
        style={'display': 'flex',
               'background-color': '#38003c',
               'margin-bottom':'10px'},
        children=[
            html.Img(src=pl_logo,
                     style={'width': '400px',
                            'height': '100px',
                            'margin-left': '10px'}),
            html.H1("Premier League stats (2002-2022)",
                    style={
                        'text-align': 'center',
                        'margin': 'auto'})
        ]
    ), dbc.Row([
        dbc.Col([html.Div([
            html.H4("Choose a Team"),
            dcc.Dropdown(id='team-kpis',
                         options=pl_df['title'].unique(),
                         value='Arsenal',
                         className='dbc'),
            html.Br(),
            html.H4("Choose a Season"),
            dcc.Dropdown(id='season-kpis',
                         options=pl_df['season'].unique(),
                         value='2022',
                         className='dbc'), ])], width=2),
        dbc.Col([dbc.Row([dbc.Col(html.H3("Position")),
                          dbc.Col(html.H3("Points")),
                          dbc.Col(html.H3("Wins")),
                          dbc.Col(html.H3("Losses")),
                          dbc.Col(html.H3("Draws"))]),

                 dbc.Row(
                     style={'font-size': '30px',
                            'text-align': 'center',
                            'gap': '11.5%'},
                     children=[
                         dbc.Col(dbc.Card(dbc.Col(id="position")), width=1),
                         dbc.Col(dbc.Card(dbc.Col(id="kpi-1")), width=1),
                         dbc.Col(dbc.Card(dbc.Col(id="kpi-2")), width=1),
                         dbc.Col(dbc.Card(dbc.Col(id="kpi-3")), width=1),
                         dbc.Col(dbc.Card(dbc.Col(id="kpi-4")), width=1)
                     ])], style={'margin-top': '30px',
                                 'margin-left': '50px'})
    ]),

    html.Hr(),

    dbc.Row(

        children=[
            dbc.Col(dbc.Col([
                html.H4("Choose a Team"),
                dcc.Dropdown(id="team-options",
                             options=pl_df['title'].unique(),
                             value='Arsenal',
                             className='dbc'),
                html.Br(),

                dcc.RadioItems(id="category-options",
                               options=pl_df.select_dtypes(include='number').columns[2:5],
                               value="wins")
            ], width=9)),
            dbc.Col(dbc.Col([
                dcc.Graph(id="line-chart",
                          style={'width': "1200px",
                                 'margin-right': '50px'})
            ]))
        ]

    ),

    html.Hr()
    ,
    dbc.Row(

        children=[
            dbc.Col(dbc.Col([
                html.H4("Choose a season"),
                dcc.Dropdown(id="season-options",
                             options=pl_df['season'].unique(),
                             value='2022',
                             className='dbc'),
                html.Br(),
                html.Br(),
                html.Div(id='table', style={'margin-left': '40px'})
            ], width=6)),

            dbc.Col(dbc.Col([
                dcc.Graph(id="bar-chart"),
                html.Br(),
                dcc.Graph(id="bar2-chart")
            ]))
        ]

    ),

    html.Hr(),

    dbc.Row([
        dbc.Col(dbc.Col([
            html.H4("Choose a season"),
            dcc.Dropdown(id="season-options-dist",
                         options=pl_df['season'].unique(),
                         value='2021',
                         className='dbc')
        ]), width=3),
        dbc.Col(dbc.Col([dcc.Graph(id='histogram')])),
        dbc.Col(dbc.Col([dcc.Graph(id='histogram2')]))
    ])

]
)


@app.callback(
    Output('position', 'children'),
    Output('kpi-1', 'children'),
    Output('kpi-2', 'children'),
    Output('kpi-3', 'children'),
    Output('kpi-4', 'children'),
    Output('line-chart', 'figure'),
    Output('bar-chart', 'figure'),
    Output('bar2-chart', 'figure'),
    Output('table', 'children'),
    Output('histogram', 'figure'),
    Output('histogram2', 'figure'),
    Input('team-kpis', 'value'),
    Input('season-kpis', 'value'),
    Input('team-options', 'value'),
    Input('category-options', 'value'),
    Input("season-options", 'value'),
    Input("season-options-dist", 'value')
)
def build_Dash(team, season, teamBar, barOption, seasonOption, seasonDistribution):
    kpi_position = pl_df.query("title==@team and season==@season")['position']
    kpi1 = pl_df.query("title==@team and season==@season")["points"]
    kpi2 = pl_df.query("title==@team and season==@season")["wins"]
    kpi3 = pl_df.query("title==@team and season==@season")["losses"]
    kpi4 = pl_df.query("title==@team and season==@season")["draws"]
    fig_df = pl_df.query("title ==@teamBar").sort_values('season',ascending=True)
    fig = px.line(fig_df,
                  x=fig_df["season"],
                  y=fig_df[barOption],
                  title=f"{barOption} per season for {teamBar} 2002-2022"
                  ).update_xaxes(showgrid=False)
    fig1_df = pl_df.query("season ==@seasonOption").sort_values("goals_for", ascending=False).head(5)
    fig1 = px.bar(fig1_df,
                  x=fig1_df["goals_for"],
                  y=fig1_df['title'],
                  title=f"Teams with most scored goals per season {seasonOption}",
                  orientation='h',
                  labels={'goals_for': 'Goals Scored'}
                  ).update_xaxes(showgrid=False)
    fig2_df = pl_df.query("season ==@seasonOption").sort_values("losses", ascending=False).head(5)
    fig2 = px.bar(fig2_df,
                  x=fig2_df["losses"],
                  y=fig2_df['title'],
                  title=f"Teams with most losses per season {seasonOption}",
                  orientation='h'
                  ).update_xaxes(showgrid=False)
    table_df = pl_df.query("season ==@seasonOption").drop(labels=["season", 'games_played', 'goals_diff',
                                                                  'goals_against', 'goals_for'], axis=1)
    table = dash_table.DataTable(
        columns=[{'name': i, 'id': i} for i in table_df.columns],
        data=table_df.to_dict("records"),
        sort_action='native',
        export_format="csv",
        style_data={
            'color': 'white',
            'background-color': '#686dc3',
            'text-align': 'center',
            'font-family': 'Arial',
            'font-size': '13px'
        },
        style_header={
            'color': 'white',
            'background-color': '#686dc3',
            'text-align': 'center',
            "text-transform": 'uppercase',
            'text-weight': 'bold',
            'font-family': 'Arial'
        },

    )

    fig3_df = pl_df.query("season ==@seasonDistribution")
    fig3 = px.histogram(fig3_df,
                        x=fig3_df["goals_for"],
                        title=f"Distribution of Goals scored at {seasonDistribution}",
                        labels={"goals_for": 'Goals Scored'}).update_yaxes(showgrid=False)

    fig4 = px.histogram(fig3_df,
                        x=fig3_df["points"],
                        title=f"Distribution of Points at {seasonDistribution}"
                        ).update_yaxes(showgrid=False)
    return kpi_position, kpi1, kpi2, kpi3, kpi4, fig, fig1, fig2, table, fig3,fig4


if __name__ == '__main__':
    app.run_server()
