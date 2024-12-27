import pandas as pd
from dash import Dash

df = pd.read_csv('https://raw.githubusercontent.com/saesaki/Dashboards/refs/heads/main/data.csv')
app = Dash()

app.layout = html.Div([
    html.H1(children='Погода в Комсомольске-на-Амуре', style={'textAlign': 'center'}),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),

])


if __name__ == '__main__':
    app.run(debug=True)