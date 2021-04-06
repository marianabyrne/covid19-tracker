import dash_bootstrap_components as dbc
import dash_html_components as html
####################### Corporate css formatting
corporate_colors = {
    'dark-blue-grey' : 'rgb(62, 64, 76)',
    'medium-blue-grey' : 'rgb(77, 79, 91)',
    'superdark-green' : 'rgb(41, 56, 55)',
    'dark-green' : 'rgb(57, 81, 85)',
    'medium-green' : 'rgb(93, 113, 120)',
    'light-green' : 'rgb(186, 218, 212)',
    'pink-red' : 'rgb(255, 101, 131)',
    'dark-pink-red' : 'rgb(247, 80, 99)',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : 'rgb(208, 206, 206)'
}
externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['dark-blue-grey'],
    'background-color' : corporate_colors['dark-blue-grey'],
    'box-shadow' : '0px 0px 17px rgba(186, 218, 212, .5)',
    'padding-top' : '10px'
}
navbarcurrentpage = {
    'text-decoration' : 'underline',
    'text-decoration-color' : corporate_colors['medium-blue-grey'],
    'text-shadow': '0px 0px 1px rgb(251, 251, 252)',
    'font_family':'Arial'
    }
filterdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['dark-blue-grey'],
    'background-color' : corporate_colors['dark-blue-grey']
    }

def header():
    header = html.Div([
        html.Div([
            html.H1(children='COVID-19 Monitoring Dashboard',
                    style = {
                        'textAlign' : 'center',
                        'font_family':'Arial'}
            )],
            className='col-12',
            style = {'padding-top' : '1%'}
        ),
    ], style = {'height' : '4%',
                'background-color' : corporate_colors['dark-blue-grey']})
    return header
def Navbar(page = 'tracker'):
    navbar_tracker = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink(html.H4(children = 'Tracker',
                            style = navbarcurrentpage), href="/tracker")),
                dbc.NavItem(dbc.NavLink(html.H4(children ="Policy Response", style = {'font_family':'Arial'}), href="https://covid19-policy-response.herokuapp.com/"))
            ],
            sticky="top",
            className='col-8'
        )
    ],
    style = {'height' : '2%', 'background-color' : corporate_colors['white']})
    navbar_response = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink(html.H4(children = 'Tracker', style = {'font_family':'Arial'}), href="/tracker")),
                dbc.NavItem(dbc.NavLink(html.H4(children ="Policy Response", style = navbarcurrentpage), href="https://covid19-policy-response.herokuapp.com/"))
            ],
            sticky="top",
            className = 'col-8'
        )
    ],
    style = {'height' : '2%', 'background-color' : corporate_colors['white']})
    if page == 'tracker':
        return navbar_tracker
    else:
        return navbar_response
