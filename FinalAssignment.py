import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

year_list = list(range(1980, 2024, 1))
data = pd.read_csv('historical_automobile_sales.csv')

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1(
        'Automobile Sales Statistics Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}
    ),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown-statistics',
                options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
                placeholder='Select a report type',
                value='Yearly Statistics',
                style={'width': '80%', 'padding': '3px', 'text-align-last': 'centre'}
            )
        ]),
        html.Div([
            dcc.Dropdown(
                id='select-year',
                options=[{'label': year, 'value': year} for year in year_list],
                placeholder='Select year',
                value=2020,
                style={'width': '80%', 'padding': '3px', 'text-align-last': 'centre'}
            )
        ])
    ]),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ])
])


@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    return True


@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'),
        Input(component_id='select-year', component_property='value')
    ]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        r_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales fluctuation over Recession Period'
            )
        )

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        r_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Number of Vehicles Sold by Type'
            )
        )

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        r_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Expenditure by Vehicle Type'
            )
        )

        unemp_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        r_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='Vehicle_Type',
                y='Automobile_Sales',
                color='unemployment_rate',
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=r_chart1), html.Div(children=r_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=r_chart3), html.Div(children=r_chart4)],
                style={'display': 'flex'}
            )
        ]

    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title='Average Annual Automobile Sales')
        )

        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        y_chart2 = dcc.Graph(
            figure=px.line(
                monthly_sales,
                x='Month',
                y='Automobile_Sales',
                title=f'Total Monthly Automobile Sales in {input_year}'
            )
        )

        avr_vdata = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Year',
                y='Automobile_Sales',
                title=f'Average Vehicles Sold in {input_year}'
            )
        )

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title=f'Advertising Expenditure by Vehicle Type in {input_year}'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=y_chart1), html.Div(children=y_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=y_chart3), html.Div(children=y_chart4)],
                style={'display': 'flex'}
            )
        ]

    return []


if __name__ == '__main__':
    app.run_server(debug=True)