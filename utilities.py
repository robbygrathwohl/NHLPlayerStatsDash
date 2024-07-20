from dash import html, dcc, dash_table, Input, Output, ctx, Patch
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import textwrap
from config import teams_color, stats_map, player_profile, styles
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
    return stats_map[stat_name]



def get_player_id(player_name, df):
    """
    Return the player ID given a player name

    Args:
        player_name (str): name of player with spaces.
        df (pd.DataFrame): pandas dataframe of all player data

    Returns:
        str: player ID
    """
    player_id = df.loc[(df['name']==player_name, 'playerId')].iloc[0]
    return player_id

def get_player_team(player_name, df):
    """
    Return the team abbreviation of a player given a player name

    Args:
        player_name (str): name of player with spaces.
        df (pd.DataFrame): pandas dataframe of all player data

    Returns:
        str: team abbreviation of player
    """
    team_abbr = df.loc[(df['name']==player_name, 'team')].iloc[0]
    return team_abbr

def get_player_mug(player_name, df):
    """
    Return the player mugshot (profile picture) link as a string

    Args:
        player_name (str): name of player with spaces.
        df (pd.DataFrame): pandast dataframe of all player data

    Returns:
        str: url link of player mugshot
    """
    player_id = get_player_id(player_name, df)
    player_team = get_player_team(player_name, df)
    return f'https://assets.nhle.com/mugs/nhl/20242025/{player_team}/{player_id}.png'

def get_player_team_logo(player_name, df):
    """
    Return the team logo svg link given a player's name

    Args:
        player_name (str): name of player with spaces.
        df (pd.DataFrame): pandast dataframe of all player data

    Returns:
        str: url link of player's team logo
    """
    player_team = get_player_team(player_name, df)
    return f'https://assets.nhle.com/logos/nhl/svg/{player_team}_light.svg'

def add_new_line(lst, string):
    """
    add new line html element to stats profile

    Args:
        lst (list): name of player with spaces.
        string (string): pandast dataframe of all player data

    Returns:
        str: url link of player's team logo
    """
    new_line = html.Br()
    lst.append(string)
    lst.append(new_line)
    return lst

def get_player_card_stats(player_name, df):
    """
    create the printed player stats for the last clicked on player from any scatterplot tab

    Args:
        player_name (str): name of player with spaces.
        df (pd.DataFrame): pandas dataframe of all player data

    Returns:
        str: stat details formatted for <p> child
    """
    df = df[df['name']==player_name]
    games_played = f'Games Played: {round(df.games_played.iloc[0])}'
    position = f'Position: {df.position.iloc[0]}'
    points = f'Points: {round(df.I_F_points.iloc[0])}'
    goals = f'Goals: {round(df.I_F_goals.iloc[0])}'
    assists = f'Assists: {round(df.I_F_primaryAssists.iloc[0]+df.I_F_secondaryAssists.iloc[0])}'
    paragraph = []
    paragraph = add_new_line(paragraph, games_played)
    paragraph = add_new_line(paragraph, position)
    paragraph = add_new_line(paragraph, points)
    paragraph = add_new_line(paragraph, goals)
    paragraph = add_new_line(paragraph, assists)

    return paragraph

def get_player_table(player_name, df):
    """
    create a DataTable with all stats for selected player

    Args:
        player_name (str): name of player with spaces.
        df (pd.DataFrame): pandast dataframe of all player data

    Returns:
        dash_table.DataTable: DataTable with all of the stats for the given player
    """
    df = df[df['name']==player_name]
    df_dict = df = df[df['name']==player_name].transpose().to_dict('records')

    return dash_table.DataTable(df_dict, style_header= {'display': 'True'}, virtualization=True, style_table={'overflowY':'scroll'})

def player_profile_card(player_name, df):
    """
    create te player profile card to be loaded to the sidebar

    Args:
        player_name (str): name of player with spaces.
        df (pd.DataFrame): pandast dataframe of all player data

    Returns:
        str: player name, str: url of team logo, str: url of player mugshot, list: summarized stats for player card 
    """
    player_card_mug = get_player_mug(player_name, df)
    player_card_team = get_player_team_logo(player_name, df)
    player_card_stats = get_player_card_stats(player_name, df)

    return player_name, player_card_team, player_card_mug, player_card_stats


def create_sidebar(player_name):
    """
    create sidebar elements that will show the player card

    Returns:
        html.Div: sidebar
    """
    sidebar = html.Div([
        html.H2("Player", className="display-4"),
        html.Div([
            html.Div([
                html.H4(id='player_name', style=styles['name'], children=player_name),
                html.Img(id='player_card_team', style=styles['img'], src=''),
                html.Img(id='player_card_mug', style=styles['img'], src=''),
                html.P(id='player_card_stats', style=styles['name']),
            ],id='player_card_div', **{"data-bs-theme": "dark"}),
        ]),
    ], style=styles['sidebar'], id='sidebar', className='dbc')
    return sidebar

def get_prop(child):
    """
    extracts meta property given the html element id

    Args:
        child (pd.DataFrame): df of selected playerf

    Returns:
        str: player_name
    """
    player_name = child['points'][0]['meta']
    return player_name

def create_sidebar_callback(app, df):

    @app.callback(
        [Output('player_name', 'children'),
        Output('player_card_team', 'src'),
        Output('player_card_mug', 'src'),
        Output('player_card_stats', 'children')],
        #Output('player_table', 'children')],
        [Input(f'c-chart', 'clickData'),
         Input(f'rw-chart', 'clickData'),
         Input(f'lw-chart', 'clickData'),
         Input(f'd-chart', 'clickData'),
         Input(f'all skaters-chart', 'clickData')],
        prevent_initial_callbacks=True)
    def display_click_data(clickData_c, clickData_rw, clickData_lw, clickData_d, clickData_a):
        if ctx.triggered_id == 'c-chart':
            player_name = get_prop(clickData_c)
        if ctx.triggered_id == 'rw-chart':
            player_name = get_prop(clickData_rw)
        if ctx.triggered_id == 'lw-chart':
            player_name = get_prop(clickData_lw)
        if ctx.triggered_id == 'd-chart':
            player_name = get_prop(clickData_d)
        if ctx.triggered_id == 'all skaters-chart':
            player_name = get_prop(clickData_a)
        return player_profile_card(player_name, df)
        
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
        html.Div([
            dcc.Graph(id=f'{position.lower()}-chart', className='mb-3', responsive=True, style=styles['graph'])
        ],className='mb-2', style={'height' : '550px'}),
        html.H5('X-axis Select:'),
        dcc.Dropdown(
            id=f'{position.lower()}-stat-dropdown-x',
            options=[{'label': format_stat_name(stat), 'value': stat} for stat in stats],
            value=stats[1],
            className='btn w-75 mb-1',
        ),
        html.H5('Y-axis Select:'),
        dcc.Dropdown(
            id=f'{position.lower()}-stat-dropdown-y',
            options=[{'label': format_stat_name(stat), 'value': stat} for stat in stats],
            value=stats[0],
            className='btn w-75 mb-4',
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

        hover_template = '<b>%{meta}</b>' + '<br>' + format_stat_name(selected_stat_x) + ' : %{x}'+ '<br>' + format_stat_name(selected_stat_y) + ' : %{y}'

        fig = go.Figure()
        fig.add_trace(go.Scatter(meta=filtered_df.name, x=filtered_df[selected_stat_x], y=filtered_df[selected_stat_y], mode='markers', marker_color=filtered_df['team'].map(teams_color)))
        fig.update_layout(title=f'{position} - {format_stat_name(selected_stat_x)} vs {format_stat_name(selected_stat_y)}', plot_bgcolor= '#343A40', paper_bgcolor= '#2B3035', title_font_color='#c9c9c9')
        fig.update_traces(hovertemplate = hover_template)
        fig.update_traces(marker_line_width=1, marker_size=10, name="")
        fig.update_yaxes(title_text=format_stat_name(selected_stat_y), title_font_color='#c9c9c9')
        fig.update_xaxes(title_text=format_stat_name(selected_stat_x), title_font_color='#c9c9c9')

        
        return fig
    return update_chart