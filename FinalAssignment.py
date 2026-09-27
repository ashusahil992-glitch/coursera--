import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

year_list = [i for i in range(1980, 2024, 1)]

data = pd.read_csv('historical_automobile_sales.csv')

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([html.H1('Automobile Sales Statistics Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                    'font-size': 24}),
    html.Div([
                     
                    html.Div([ 
                     dcc.Dropdown(id='dropdown-statistics',
                   options=[
                           {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                           {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                           ],
                  placeholder='Select a report type', value='Select Statistics',
                  style={'width':'80%', 'padding' : '3px', 'size' : '20px', 'text-align-last' : 'centre' })]),
    html.Div([       dcc.Dropdown(id='select-year', 
                   options=[{'label': i, 'value': i} for i in year_list],
                  placeholder='Select-year', value='Select-year',
                  style={'width':'80%', 'padding' : '3px', 'size' : '20px', 'text-align-last' : 'centre' })])
                    ]),

    html.Div([
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])

])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True


@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        


        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))


        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                           
        R_chart2  = dcc.Graph(figure=px.bar(average_sales, x= 'Vehicle_Type', y= 'Automobile_Sales',
                title='Average Number of Vehicles Sold by Type'))
        

        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
                    figure=px.pie(exp_rec,
                    values='Advertising_Expenditure',
                 names='Vehicle_Type',
                 title="Total Expenditure by Vehicle Type"
                ))

        unemp_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
                    figure=px.bar(unemp_data,
                    x='Vehicle_Type',
                    y='Automobile_Sales',
                    color='unemployment_rate',
                    title='Effect of Unemployment Rate on Vehicle Type and Sales'
                    ))


        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display':'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display':'flex'})
            ]
                       
    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]
                              

        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales'))
            
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x= 'Month', y='Automobile_Sales',
            title= 'Total Monthly Automobile Sales'))

        avr_vdata=yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph( figure =px.bar(avr_vdata,x='Year', y='Automobile_Sales',title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values = 'Advertising_Expenditure', names='Vehicle_Type'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
            ]
        

if __name__ == '__main__':
    app.run_server(debug=True)