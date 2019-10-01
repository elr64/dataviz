#import packages
import pandas as pd
import matplotlib.pyplot as plt

#import dataset from excel sheet
energy=pd.read_excel('2_Energy_Consumption.xlsx')

#remove additional text at end of dataset
energy=energy.drop([52, 53, 54, 55])

#subset variables for analysis
energy=energy.drop(energy.columns[[7,10]], axis=1)

#create state abbreviation variable
energy['code']=['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI',
    'ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT',
    'NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD',
    'TN','TX','UT','VT','VA','WA','WV','WI','WY', 'US']

#rename colunms
energy.columns=['State', 'NG', 'DF', 'JF', 'MG', 'RF', 'O', 'Eth', 'E', 'Loss',
                'Total', 'code']

#select only row of U.S. total
us=energy.loc[51]
us=us[1:9]

#electricity makes up .0938% and therefore excluded from analysis
us=us[0:7]

#set colors using CO2 emissions transformed so that the darker the shade the 
# higher the value, while maintaining relative differences in value 
# (other is aviation gasoline, lubricants and LPG, which is a mix of 
#propane/butane, therefore color set using average of 3)
valcol=[(1-.5307**2), (1-.7315**2), (1-.709**2), (1-.713**2), (1-.7879**2), 
         (1-.6914**2), (1-.2703**2)]
rgbcol=[]
for col in valcol:
    i=(col, 0, 0)
    rgbcol.append(i)

#make donut chart
my_circle=plt.Circle( (0,0), 0.7, color='white')
plt.pie(us.values, labels=['Natural Gas', 'Distillate Fuel', 'Jet Fuel', 
                           'Motor Gasoline', 'Residual Fuel', 'Other', 
                           'Ethanol'], colors = rgbcol, 
                            textprops={'fontsize': 20}, 
                            wedgeprops = {'linewidth' : 8, 'edgecolor': 'white'})
p=plt.gcf()
p.set_size_inches(20,20)
p.suptitle("U.S. Energy Consumption", fontsize=35)
p.gca().add_artist(my_circle)
plt.savefig('usenergyconsumption.png')

#US Petroleum Fuel Usage by state
states=energy[['State','Total']]
states=states[0:51]
states=states.sort_values('Total')

#get the top 4 states
states1 = states[47:51].copy()

#combine other states
other = pd.DataFrame(data = {
    'State' : ['Rest of US'],
    'Total' : [states['Total'][:47].sum()]})

#combining top 4 with total of others
states1 = pd.concat([states1, other])

#set colors for visual
valcol=[.8, .7, .6, .5, .4, .9]
rgbcol=[]
for col in valcol:
    i=(col, 0, 0)
    rgbcol.append(i)

#create donut chart
my_circle=plt.Circle( (0,0), 0.7, color='white')
plt.pie(states1['Total'], labels=states1['State'], colors = rgbcol, textprops =
        {'fontsize': 20}, wedgeprops = {'linewidth' : 8, 'edgecolor': 'white'})
p=plt.gcf()
p.set_size_inches(20,20)
p.suptitle("State Energy Consumption", fontsize=35)
p.gca().add_artist(my_circle)
plt.savefig('stateconsumption.png')
