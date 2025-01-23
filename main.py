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
    dcc.Graph(id='windrose'),
    html.Div(children='Выберите время суток для розы ветров:'),
    html.Div(className='row', style={'textAlign': 'center'}, children=dcc.RadioItems(
        options=[{'label': 'День', 'value': 'WindinessDay'},
                 {'label': 'Вечер', 'value': 'WindinessEvening'}],
        value='WindinessDay',
        inline=True,
        id='WindChoice'))
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

@callback(
    Output(component_id='windrose', component_property='figure'),
    Input(component_id='citySelection', component_property='value'),
    Input(component_id='WindChoice', component_property='value')
)
def updateRose(cityID, windTime):
    dff = df[df.CityID == cityID]
    wind_data = dff[windTime].dropna()

    def parse_wind(entry):
        try:
            if pd.isna(entry) or 'м/с' not in entry:
                return None, None
            parts = entry.split()
            if len(parts) < 2:
                return None, None
            direction = parts[0]
            speed = float(parts[1].replace('м/с', ''))
            return direction, speed
        except (IndexError, ValueError):
            return None, None

    wind_data_parsed = wind_data.apply(parse_wind)
    parsed_data = wind_data_parsed.dropna()

    if parsed_data.empty:
        return go.Figure(go.Barpolar(r=[], theta=[], name='Нет данных о ветре'))

    directions, speeds = zip(*parsed_data)
    wind_df = pd.DataFrame({'Direction': directions, 'Speed': speeds})
    wind_summary = wind_df.groupby('Direction').agg({'Speed': 'mean'}).reset_index()

    fig = go.Figure(go.Barpolar(
        r=wind_summary['Speed'],
        theta=wind_summary['Direction'],
        name='Средняя скорость ветра',
        marker_color='blue',
        opacity=0.7
    ))

    fig.update_layout(
        title="Роза ветров",
        polar=dict(
            angularaxis=dict(
                direction="clockwise",
                categoryorder="array",
                categoryarray=['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
            )
        )
    )

    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
