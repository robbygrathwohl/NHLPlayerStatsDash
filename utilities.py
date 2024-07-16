from dash import html, dcc, Input, Output, Patch
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from config import teams_color, stats_map


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
        dcc.Graph(id=f'{position.lower()}-chart'),
        dcc.Dropdown(
            id=f'{position.lower()}-stat-dropdown',
            options=[{'label': format_stat_name(stat), 'value': stat} for stat in stats],
            value=stats[0],
            className='btn w-100 mb-4'
        ),
        dcc.Dropdown(
            id=f'{position.lower()}-player-dropdown',
            options=[{'label': player, 'value': player} for player in df['name'].unique()],
            value=top_players,
            multi=True,
            className='mb-3'
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
        [Input(f'{position.lower()}-stat-dropdown', 'value'),
         Input(f'{position.lower()}-player-dropdown', 'value'),
         Input("color-mode-switch", "value")]
    )
    def update_chart(selected_stat, selected_players, switch_on):
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
        hover_template = '<b>%{meta}</b>' + '<br>Icetime : %{x} min'+ '<br>' + selected_stat + ' : %{y}'
        #template = pio.templates["minty"] if switch_on else pio.templates["minty_dark"]
        template = pio.templates["minty"]
    

        fig = go.Figure()
        fig.add_trace(go.Scatter(meta=filtered_df.name, x=filtered_df.icetime/60, y=filtered_df[selected_stat], mode='markers', marker_color=filtered_df['team'].map(teams_color)))
        fig.update_layout(title=f'{position} {format_stat_name(selected_stat)}', plot_bgcolor= '#343A40', paper_bgcolor= '#2B3035', font_color= '#eee')
        fig.update_traces(hovertemplate = hover_template)

        fig.update_traces(marker_line_width=1, marker_size=10)
        fig.update_yaxes(title_text=format_stat_name(selected_stat))
        fig.update_xaxes(title_text='Icetime (minutes)')
        fig["layout"]["template"] = template
        
        return fig
    return update_chart