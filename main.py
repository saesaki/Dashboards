import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.graph_objects as go

df = pd.read_csv('https://raw.githubusercontent.com/saesaki/Dashboards/refs/heads/main/data.csv')
app = Dash()

translated_labels = {
    'TempDay': 'Температура днем',
    'PressureDay': 'Давление днем',
    'TempEvening': 'Температура вечером',
    'PressureEvening': 'Давление вечером',
    'CloudinessDay': 'Облачность днем',
    'CloudinessEvening': 'Облачность вечером'
}

app.layout = html.Div([
    html.H1(children='Погода в Комсомольске-на-Амуре', style={'textAlign': 'center'}),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    html.Div(children='Выберите ID города:'),
    dcc.Dropdown(df.CityID.unique(), '4853', id='citySelection'),
    dcc.Graph(id='graph'),
    html.Div(className='row', style={'textAlign': 'center'}, children=dcc.RadioItems(
        options=[{'label': translated_labels[i], 'value': i} for i in
                 ['TempDay', 'PressureDay', 'TempEvening', 'PressureEvening']],
        value='TempDay',
        inline=True,
        id='TempOrPresChoice')),
    dcc.Graph(id='pie'),
    html.Div(className='row', style={'textAlign': 'center'}, children=dcc.RadioItems(
        options=[{'label': translated_labels[i], 'value': i} for i in ['CloudinessDay', 'CloudinessEvening']],
        value='CloudinessDay',
        inline=True,
        id='CloudinessChoice')),
])

@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='citySelection', component_property='value'),
    Input(component_id='TempOrPresChoice', component_property='value')
)
def updateGraph(cityID, choiceRadio):
    dff = df[df.CityID == cityID].sort_values('Date')

    ymin = dff[choiceRadio].min()
    ymax = dff[choiceRadio].max()

    range_diff = ymax - ymin
    dtick = range_diff // 8

    fig = go.Figure(go.Scatter(x=dff['Date'], y=dff[choiceRadio], mode='lines+markers'))

    fig.update_layout(
        yaxis=dict(
            title=translated_labels[choiceRadio],
            tickmode='linear',
            tick0=ymin,
            dtick=dtick
        ),
        xaxis=dict(title='Data'),
        title='График данных'
    )

    return fig

@callback(
    Output(component_id='pie', component_property='figure'),
    Input(component_id='citySelection', component_property='value'),
    Input(component_id='CloudinessChoice', component_property='value')
)
def updatePie(cityID, choiceCloud):
    dff = df[df.CityID == cityID]
    value_counts = dff[choiceCloud].value_counts()

    fig = go.Figure(go.Pie(values=value_counts.values, labels=value_counts.index))
    fig.update_layout(title=translated_labels[choiceCloud])

    return fig




if __name__ == '__main__':
    app.run(debug=True)