#import packages
import chart_studio
chart_studio.tools.set_credentials_file(username='xxxxxx', api_key='xxxxxx')
import chart_studio.plotly as py
import plotly.graph_objs as go
import pandas as pd

#import dataset from excel sheet
energy=pd.read_excel('2_Energy_Consumption.xlsx')

#remove additional text at end of dataset
energy=energy.drop([51, 52, 53, 54, 55])

#subset variables for analysis
energy=energy.drop(energy.columns[[1,8,9,10,11,12]], axis=1)

#create state abbreviation variable
energy['code']=['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI',
    'ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT',
    'NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD',
    'TN','TX','UT','VT','VA','WA','WV','WI','WY',]

#rename colunms
energy.columns=["State", "DF", "JF", "MG", "RF", "O", "TP", "code"]

#convert columns to strings for usability in hover
for col in energy.columns:
    energy[col] = energy[col].astype(str)
    
#set hover info for choropleth map
energy['hover']=energy['State'] + '<br>' + 'Distillate Fuel' + '&nbsp;' + \
                energy['DF'] + '<br>' +'Jet Fuel' + '&nbsp;' + energy['JF'] + \
                '<br>' + 'Motor Gasoline' + '&nbsp;' + energy['MG'] + '<br>' \
                + 'Residual Fuel' + '&nbsp;' + energy['RF'] + '<br>' + 'Other' \
                + '&nbsp;' + energy['O']

#create choropleth map
fig = go.Figure(data=go.Choropleth(
    locations=energy['code'],
    text=energy['hover'],
    z = energy['TP'].astype(float),
    locationmode = 'USA-states',
    autocolorscale=False,
    colorscale = 'Reds',
    colorbar=dict(title = "Trillion Btu"),))

fig.update_layout(
    title_text = 'Petroleum Fuel Consumption by State<br>(Hover for fuel breakdown)',
    geo_scope='usa')

plot_url = py.plot(fig, filename='Pythonfuelusagechoropleth')
