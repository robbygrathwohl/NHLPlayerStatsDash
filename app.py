from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from utilities import load_data, format_stat_name, create_tab_content, create_player_callback
from config import skater_stats, teams_color

# Load data with error handling
file_path = 'data/skaters.csv'
df = load_data(file_path)

# Initialize dash app with bootstrap theme
load_figure_template(['minty','minty_dark'])
#load_figure_template('darkly')
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME])
server = app.server




#color switcher
color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        #dbc.Switch( id="color-mode-switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Switch( id="color-mode-switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)





# Filter data for each position
df_c = df[df['position'] == 'C']
df_lw = df[df['position'] == 'L']
df_rw = df[df['position'] == 'R']
df_d = df[df['position'] == 'D']




# Filter data for each position and select top 10 based on key stats
top_a = df.groupby('name').sum().reset_index().nlargest(50, 'I_F_points')['name'].tolist()
top_c = df_c.groupby('name').sum().reset_index().nlargest(50, 'I_F_points')['name'].tolist()
top_rw = df_rw.groupby('name').sum().reset_index().nlargest(50, 'I_F_points')['name'].tolist()
top_lw = df_lw.groupby('name').sum().reset_index().nlargest(50, 'I_F_points')['name'].tolist()
top_d = df_d.groupby('name').sum().reset_index().nlargest(50, 'I_F_points')['name'].tolist()




# Create HTML Components
app.layout = dbc.Container([html.Div([
    color_mode_switch,
    # Dashboard section
    html.Div([
        html.H1(f'NHL Player Stats 2023-2024', className='text-center'),
        html.Div([
            html.Div([
                html.H2('Players Stats by Position', className='text-center'),
                dbc.Tabs(
                    id='position-tabs',
                    active_tab='C',
                    class_name='d-flex justify-content-center w-100',
                    children=[
                        dbc.Tab(
                            label='Centers',
                            tab_id='C',
                            children=create_tab_content(app, 'C', skater_stats, top_c, df_c)
                        ),
                        dbc.Tab(
                            label='Right Wingers',
                            tab_id='RW',
                            children=create_tab_content(app, 'RW', skater_stats, top_rw, df_rw)
                        ),
                        dbc.Tab(
                            label='Left Wingers',
                            tab_id='LW',
                            children=create_tab_content(app, 'LW', skater_stats, top_lw, df_lw)
                        ),
                        dbc.Tab(
                            label='Defenseman',
                            tab_id='D',
                            children=create_tab_content(app, 'D', skater_stats, top_d, df_d)
                        ),
                        dbc.Tab(
                            label='All Skaters',
                            tab_id='A',
                            children=create_tab_content(app, 'All Skaters', skater_stats, top_a, df)
                        )
                ])
            ], className='col-12 col-xl-12 px-12', style={'textAlign': 'center'}),
        ], className='row')
    ]),
    html.Footer([
        html.Div([
            html.A('Author: Robby G', href='https://github.com/robbygrathwohl'),
            html.Span('    |    '),
            html.A('Dataset Source - MoneyPuck', href='https://moneypuck.com/moneypuck/playerData/seasonSummary/2023/regular/skaters.csv')
        ], className='bg-dark text-light text-center py-3 fs-5')
    ])
])])



# Player stats by position line charts callback
create_player_callback(app, 'C', df_c)
create_player_callback(app, 'RW', df_rw)
create_player_callback(app, 'LW', df_lw)
create_player_callback(app, 'D', df_d)
create_player_callback(app, 'All Skaters', df)



# @callback(
#     Output("c-chart", "figure"),
#     Output("lw-chart", "figure"),
#     Output("rw-chart", "figure"),
#     Output("d-chart", "figure"),
#     Output("all skaters-chart", "figure"),
#     #Output("switch", "id"),
#     Input("color-mode-switch", "value"),
# )
# def update_figure_template(switch_on):
#     # When using Patch() to update the figure template, you must use the figure template dict
#     # from plotly.io  and not just the template name
#     template = pio.templates["minty"] if switch_on else pio.templates["minty_dark"]

#     patched_figure = Patch()
#     patched_figure["layout"]["template"] = template
#     return patched_figure



clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """
    ,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)



if __name__ == '__main__':
    app.run_server(debug=True)