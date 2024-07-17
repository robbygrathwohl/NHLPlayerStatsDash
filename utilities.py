from dash import html, dcc, Input, Output, Patch
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from config import teams_color, stats_map
import json


def load_data(file_path):
    """
    Load data from a CSV file with error handling.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        Exception: If the file is not found, empty, or cannot be parsed.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise Exception(f"The data file '{file_path}' was not found.")
    except pd.errors.EmptyDataError:
        raise Exception('The data file is empty.')
    except pd.errors.ParserError:
        raise Exception('Error parsing the data file.')
    return df

def format_stat_name(stat_name):
    """
    Format a statistic name to be more readable.

    Args:
        stat_name (str): The statistic name in snake_case.

    Returns:
        str: The formatted statistic name.
    """
    #return ' '.join(word.capitalize() for word in stat_name.split('_'))
    return stats_map[stat_name]

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem"
    #"background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

def get_player_id(player_name, df):
    return 0

def player_profile_card(player_id):
    return 0

def create_sidebar():
    sidebar = html.Div([
        html.H2("Player", className="display-4"),
        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
            dcc.Markdown(id='sidebar')
        ], className='three columns'),
    ], style=SIDEBAR_STYLE)
    return sidebar


def create_sidebar_callback(app, position, df):
    @app.callback(
        Output('click-data', 'children'),
        #Output('sidebar', 'children'),
        Input(f'{position.lower()}-chart', 'clickData'),
        prevent_initial_callbacks=True)
    def display_click_data(clickData):
        player_name=clickData['points'][0]['meta']
        player = df[(df['name']==player_name)]
        return player.to_json()
        
        #return answer
    return display_click_data

def create_tab_content(app, position, stats, top_players, df):
    """
    Create the HTML content for each position tab.

    Args:
        position (str): The position (e.g., 'C', 'RW', 'LW', 'D', 'All Skaters').
        stats (list): List of statistics to display.
        top_players (list): List of top players' names.
        df (pd.DataFrame): DataFrame containing the data for the position.

    Returns:
        html.Div: The HTML content for the position tab.
    """

    return html.Div([
        dcc.Graph(id=f'{position.lower()}-chart', className='mb-3'),
        html.H5('X-axis Select:'),
        dcc.Dropdown(
            id=f'{position.lower()}-stat-dropdown-x',
            options=[{'label': format_stat_name(stat), 'value': stat} for stat in stats],
            value=stats[1],
            className='btn w-100 mb-4',
        ),
        html.H5('Y-axis Select:'),
        dcc.Dropdown(
            id=f'{position.lower()}-stat-dropdown-y',
            options=[{'label': format_stat_name(stat), 'value': stat} for stat in stats],
            value=stats[0],
            className='btn w-100 mb-4',
        ),
        html.H5('Player Select:'),
        dcc.Dropdown(
            id=f'{position.lower()}-player-dropdown',
            options=[{'label': player, 'value': player} for player in df['name'].unique()],
            value=top_players,
            multi=True,
            className='mb-3',
            style={'padding': '10px'}
        )
    ], className="dash-bootstrap")

def create_player_callback(app, position, df):
    """
    Create a callback for updating player charts based on the selected stat and player(s).

    Args:
        app (Dash): The Dash app instance.
        position (str): The position (e.g., 'C', 'RW', 'LW', 'D').
        df (pd.DataFrame): DataFrame containing the data for the position.

    Returns:
        function: The callback function for updating the chart.
    """
    @app.callback(
        Output(f'{position.lower()}-chart', 'figure'),
        [Input(f'{position.lower()}-stat-dropdown-x', 'value'),
         Input(f'{position.lower()}-stat-dropdown-y', 'value'),
         Input(f'{position.lower()}-player-dropdown', 'value'),
         Input("color-mode-switch", "value")]
    )
    def update_chart(selected_stat_x, selected_stat_y, selected_players, switch_on):
        """assets
        Update the player chart based on the selected stat and player(s).

        Args:
            selected_stat (str): The selected statistic to display.
            selected_players (list): The selected players' names.

        Returns:
            plotly.graph_objs._figure.Figure: The updated line chart figure.
        """
        dbc.Label(className="Player_Stats_Scatter", html_for="scatter")
        filtered_df = df[df['name'].isin(selected_players)]
        filtered_df = filtered_df[filtered_df['situation']=='all']
        filtered_df.icetime = round(filtered_df.icetime/60)
        filtered_df.timeOnBench = round(filtered_df.timeOnBench/60)
        #template = pio.templates["minty"] if switch_on else pio.templates["minty_dark"]
        template = pio.templates["minty"]
        hover_template = '<b>%{meta}</b>' + '<br>' + format_stat_name(selected_stat_x) + ' : %{x} min'+ '<br>' + format_stat_name(selected_stat_y) + ' : %{y}'

        fig = go.Figure()
        fig.add_trace(go.Scatter(meta=filtered_df.name, x=filtered_df[selected_stat_x], y=filtered_df[selected_stat_y], mode='markers', marker_color=filtered_df['team'].map(teams_color)))
        fig.update_layout(title=f'{position} - {format_stat_name(selected_stat_x)} vs {format_stat_name(selected_stat_y)}', plot_bgcolor= '#343A40', paper_bgcolor= '#2B3035', font_color= '#eee')
        fig.update_traces(hovertemplate = hover_template)
        fig.update_traces(marker_line_width=1, marker_size=10, name="")
        fig.update_yaxes(title_text=format_stat_name(selected_stat_y))
        fig.update_xaxes(title_text=format_stat_name(selected_stat_x))
        fig["layout"]["template"] = template
        
        return fig
    return update_chart