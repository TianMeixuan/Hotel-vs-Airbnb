#!/usr/bin/env python
# coding: utf-8

# In[1155]:


# import packages

import json
import os
import numpy as np
import pandas as pd
import geopandas as gpd
from bokeh.layouts import gridplot, column, grid, row, widgetbox, layout, Column
from bokeh.plotting import figure, show, output_file, gmap, curdoc
from bokeh.models.tickers import FixedTicker
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import show, output_file, curdoc
from bokeh.palettes import Spectral10, plasma, Spectral9,GnBu9
from bokeh.transform import factor_cmap, dodge
from bokeh.models.markers import Triangle
from bokeh.models import (CDSView, GMapOptions,ColumnDataSource, CustomJS,
                          CustomJSFilter, GeoJSONDataSource, HoverTool,ColorBar,Button, Label,
                          LinearColorMapper, Slider,Select, Legend,Range1d, ContinuousColorMapper)


# In[1156]:


# import data

AB = pd.read_csv('Airbnb.csv')
Hotel = pd.read_csv('hotel.csv')


# In[1157]:


a = AB['room_type'].unique()
AB['last_scraped'] = pd.to_datetime(AB['last_scraped'])
AB.loc[:,'year'] = AB['last_scraped'].dt.year


# # 1st plot

# In[1158]:


hotel = Hotel.lat_long.astype(str).str.replace('\[|\]|\'','')
Hotel3 = hotel.to_frame()

lat = []
lon = []

# For each row in a varible,
for row in Hotel3['lat_long']:
    lat.append(row.split(',')[0])
    lon.append(row.split(',')[1])

# Create two new columns from lat and lon
Hotel3['latitude'] = lat
Hotel3['longitude'] = lon

map_options = GMapOptions(lat=40.78353, lng=-73.96625, map_type="terrain", zoom=12)

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:
p1 = gmap("AIzaSyCmyNHNpIOODpU6bDWtqHqid18_9aKVADw", 
         map_options, toolbar_location = 'above',title="Manhattan",plot_height=750,plot_width=1000)

def pro_data():
    airbnb1 = AB[['latitude','longitude','year','room_type','neighbourhood_group']]
    a = []
    a.extend(AB.room_type.unique())
    roomtype_list = sorted(a)
    return airbnb1,roomtype_list

airbnb1,roomtype_list= pro_data()

def roomtype_data(roomtype, year):
    df_room = airbnb1.loc[airbnb1["room_type"] == roomtype]
    data_room = df_room.loc[df_room['year'] == year]
    return data_room

entire_src = ColumnDataSource(data=dict(x=[], y=[], year=[]))
hotel_src = ColumnDataSource(data=dict(x=[], y=[], year=[]))
private_src = ColumnDataSource(data=dict(x=[], y=[], year=[]))
shared_src = ColumnDataSource(data=dict(x=[], y=[], year=[]))



# Plots the Airbnb sites based on month in slider
Entire = p1.circle(x="x", y="y", source=entire_src, size=1.5,fill_color='#ff8080', line_color=None,
                line_width=0.3, line_alpha=0.5, fill_alpha=1)
Hotel_type = p1.circle(x="x", y="y", source=hotel_src, size=1.5,fill_color='#cc0000', line_color=None,
                line_width=0.3, line_alpha=0.5, fill_alpha=1)
Private = p1.circle(x="x", y="y", source=private_src, size=1.5,fill_color='orange', line_color=None,
                line_width=0.3, line_alpha=0.5, fill_alpha=1)
Shared = p1.circle(x="x", y="y", source=shared_src, size=1.5,fill_color='#ff3333', line_color=None,
                line_width=0.3, line_alpha=1, fill_alpha=1)
Hotelfix = p1.circle(x=Hotel3['longitude'],y=Hotel3['latitude'], size=2.5, fill_color='blue',line_color=None,
                    fill_alpha=1)
    

#legend
# Legend configuration
legend = Legend(
    items = [("Entire home/apt", [Entire]),
           ("Shared room", [Shared]),
           ("Private room", [Private]),
           ("Airbnb hotel", [Hotel_type])
           ],
    location="top_center", orientation="vertical",
)

p1.add_layout(legend, "right")
p1.legend.background_fill_alpha = 0.0
p1.legend.click_policy = "hide"

def animate_update1():
    year = slider1.value + 1
    if year > 2019:
        year = 2015
    slider1.value = year

def update():
    year = slider1.value
    
    room1 = roomtype_data('Entire home/apt',year)
    entire_src.data = dict(
        x=room1['longitude'],
        y=room1['latitude'],
        year=room1['year'])
    
    room2 = roomtype_data('Hotel room',year)
    hotel_src.data = dict(
        x=room2['longitude'],
        y=room2['latitude'],
        year=room2['year'])
    
    room3 = roomtype_data('Private room',year)
    private_src.data = dict(
        x=room3['longitude'],
        y=room3['latitude'],
        year=room3['year'])
    
    room4 = roomtype_data('Shared room',year)
    shared_src.data = dict(
        x=room4['longitude'],
        y=room4['latitude'],
        year=room4['year'])

    #set the starting point
slider1 = Slider(title="Year", start=2015, end=2019, value=2015, step=1)
slider1.on_change('value', lambda attr, old, new: update())

callback_id = None


# Set the speed for animation function here
def animate():
    global callback_id
    if button1.label == '► Play':
        button1.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update1, 500)
    else:
        button1.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)


button1 = Button(label='► Play', width=60)
button1.on_click(animate)


update()

l1 = layout([[p1], 
                 [slider1,button1],
                ],sizing_mode='fixed', name='layout')


# # 2nd plot

# In[1159]:


# set neighbourhood groups for hotels according to their zipcodes

def cut_to(x):
    if x in (10026, 10027, 10030, 10037, 10039):
        return 'Central Harlem'
    elif x in (10001, 10011, 10018, 10019, 10020, 10036):
        return 'Chelsea and Clinton'
    elif x in (10029, 10035):
        return 'East Harlem'
    elif x in (10010, 10016, 10017, 10022):
        return 'Gramercy Park and Murray Hill'
    elif x in (10012, 10013, 10014):
        return 'Greenwich Village and Soho'
    elif x in (10004, 10005, 10006, 10007, 10038, 10280):
        return 'Lower Manhattan'
    elif x in (10002, 10003, 10009):
        return 'Lower East Side'
    elif x in (10021, 10028, 10044, 10065, 10075, 10128):
        return 'Upper East Side'
    elif x in (10023, 10024, 10025):
        return 'Upper West Side'
    elif x in (10031, 10032, 10033, 10034, 10040):
        return 'Inwood and Washington Heights'


# In[1160]:


hotel_zip_count =pd.DataFrame(Hotel.groupby(['zip']).size())
hotel_zip_count = hotel_zip_count.reset_index()
hotel_zip_count = hotel_zip_count.rename(columns={0: 'count_Hotel'})
hotel_zip_count['neighbourhood_group'] =hotel_zip_count['zip'].map(cut_to)
hotel_zip_count['nb_count']=hotel_zip_count['count_Hotel'].groupby(hotel_zip_count['neighbourhood_group']).transform('sum')

fdr = 'nyu-2451-34509-shapefile'
in_f = 'nyu_2451_34509.shx'
target = os.path.join(fdr, in_f)
NY_zip = gpd.read_file(target)
# change the str to int
NY_zip['zcta'] = NY_zip['zcta'].str[:5]
NY_zip['zcta'] = NY_zip['zcta'].astype(int)
NY_zip=NY_zip.rename(columns={'zcta': 'zip'})

NY_zip_count = NY_zip.merge(hotel_zip_count,how='left',on='zip')

def rank_to(x):
    if x == 11:
        return '1'
    elif x==12:
        return '2'
    elif x==15:
        return '3'
    elif x==21:
        return '4'
    elif x==25:
        return '5'
    elif x==35:
        return '6'
    elif x==38:
        return '7'
    elif x==45:
        return '8'
    elif x==83:
        return '9'
    elif x==184:
        return '10'
    else:
        return '0'
    
NY_zip_count['color1']=NY_zip_count['nb_count'].map(rank_to)
values = {'neighbourhood_group': 'N/A', 'nb_count': 'N/A'}
NY_zip_count=NY_zip_count.fillna(value=values)
NY_zip_count

geosource1 = GeoJSONDataSource(geojson = NY_zip_count.to_json())

# Define color palettes
palette =['#300711', '#580C1F', '#CC0000','#9C0D38', '#FF5A5F', '#F26F80', 
          '#CC8B86', '#F9B5AC', '#FAC9C2', '#FCE6EC', '#E0E0E0']

# reverse order of colors so higher values have darker colors
palette = palette[::-1]

# Instantiate Categorical ColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette,low=0,high=10)

def map2():
#Create figure object
    p2 = figure(title = 'Hotels in Manhattan', 
           plot_height = 750 ,
           plot_width = 500, 
           x_range=(-74.04,-73.9), y_range=(40.65,40.9),
           toolbar_location = 'above',
           tools = "pan, wheel_zoom, reset")
    p2.xgrid.grid_line_color = None
    p2.ygrid.grid_line_color = None


# Add patch renderer to figure.
    zipcode= p2.patches('xs','ys', source = geosource1,
                   fill_color = {'field' :'color1', 'transform' : color_mapper},
                   line_color = 'white', line_width = 0.25, fill_alpha = 1)

# Add hover tool
    p2.add_tools(HoverTool(renderers = [zipcode],
                      tooltips = [('Neighbourhood name','@neighbourhood_group'),
                                  ('Hotel Count', '@nb_count'),
                                  ('Zipcode', '@zip')]))
    return(p2)


# # 3rd plot

# In[1161]:


# calculate the growth rate of the number of airbnb rooms by neighourhood groups and room types

AB1 = pd.DataFrame(AB.groupby(['year', 'neighbourhood_group','room_type']).size())
AB1=AB1.reset_index()
AB1 = AB1.rename(columns={0: 'count'})
AB1_growth=AB1.sort_values(by=['neighbourhood_group', 'room_type', 'year'])
AB1_growth.loc[:,'shift']=AB1_growth['count'].shift(1)
AB1_growth.loc[:,'growth_rate']=(AB1_growth['count']-AB1_growth['shift'])/AB1_growth['shift']
AB1_growth=AB1_growth.query("year != 2015")


# In[1162]:


# calculate the average growth rate of the number of airbnb rooms by room types

AB0 = pd.DataFrame(AB.groupby(['year','room_type']).size())
AB0 = AB0.reset_index()
AB0 = AB0.rename(columns={0: 'count'})
AB0_growth = AB0.sort_values(by=['room_type','year',])
AB0_growth.loc[:,'shift'] = AB0_growth['count'].shift(1)
AB0_growth.loc[:,'growth_rate'] = (AB0_growth['count']-AB0_growth['shift'])/AB0_growth['shift']
AB0_growth = AB0_growth.query("year != 2015")


# In[1163]:


Hotel.loc[:,'neighbourhood_group'] = Hotel['zip'].map(cut_to)


# In[1164]:


# the growth rate of the number of airbnb rooms by neighourhood groups and room types

Lower_Manhattan = AB1_growth.query("neighbourhood_group == 'Lower Manhattan'")
Greenwich_Village_and_Soho = AB1_growth.query("neighbourhood_group == 'Greenwich Village and Soho'")
Lower_East_Side = AB1_growth.query("neighbourhood_group == 'Lower East Side'")
Chelsea_and_Clinton = AB1_growth.query("neighbourhood_group == 'Chelsea and Clinton'")
Gramercy_Park_and_Murray_Hill = AB1_growth.query("neighbourhood_group == 'Gramercy Park and Murray Hill'")
Upper_West_Side = AB1_growth.query("neighbourhood_group == 'Upper West Side'")
East_Harlem = AB1_growth.query("neighbourhood_group == 'East Harlem'")
Upper_East_Side = AB1_growth.query("neighbourhood_group == 'Upper East Side'")
Central_Harlem = AB1_growth.query("neighbourhood_group == 'Central Harlem'")
Inwood_and_Washington_Heights = AB1_growth.query("neighbourhood_group == 'Inwood and Washington Heights'")

Lower_Manhattan_entire = Lower_Manhattan.query("room_type == 'Entire home/apt'")
Lower_Manhattan_hotel = Lower_Manhattan.query("room_type == 'Hotel room'")
Lower_Manhattan_private = Lower_Manhattan.query("room_type == 'Private room'")
Lower_Manhattan_shared = Lower_Manhattan.query("room_type == 'Shared room'")

Greenwich_Village_and_Soho_entire = Greenwich_Village_and_Soho.query("room_type == 'Entire home/apt'")
Greenwich_Village_and_Soho_hotel = Greenwich_Village_and_Soho.query("room_type == 'Hotel room'")
Greenwich_Village_and_Soho_private = Greenwich_Village_and_Soho.query("room_type == 'Private room'")
Greenwich_Village_and_Soho_shared = Greenwich_Village_and_Soho.query("room_type == 'Shared room'")

Lower_East_Side_entire = Lower_East_Side.query("room_type == 'Entire home/apt'")
Lower_East_Side_hotel = Lower_East_Side.query("room_type == 'Hotel room'")
Lower_East_Side_private = Lower_East_Side.query("room_type == 'Private room'")
Lower_East_Side_shared = Lower_East_Side.query("room_type == 'Shared room'")

Chelsea_and_Clinton_entire = Chelsea_and_Clinton.query("room_type == 'Entire home/apt'")
Chelsea_and_Clinton_hotel = Chelsea_and_Clinton.query("room_type == 'Hotel room'")
Chelsea_and_Clinton_private = Chelsea_and_Clinton.query("room_type == 'Private room'")
Chelsea_and_Clinton_shared = Chelsea_and_Clinton.query("room_type == 'Shared room'")

Gramercy_Park_and_Murray_Hill_entire = Gramercy_Park_and_Murray_Hill.query("room_type == 'Entire home/apt'")
Gramercy_Park_and_Murray_Hill_hotel = Gramercy_Park_and_Murray_Hill.query("room_type == 'Hotel room'")
Gramercy_Park_and_Murray_Hill_private = Gramercy_Park_and_Murray_Hill.query("room_type == 'Private room'")
Gramercy_Park_and_Murray_Hill_shared = Gramercy_Park_and_Murray_Hill.query("room_type == 'Shared room'")

Upper_West_Side_entire = Upper_West_Side.query("room_type == 'Entire home/apt'")
Upper_West_Side_hotel = Upper_West_Side.query("room_type == 'Hotel room'")
Upper_West_Side_private = Upper_West_Side.query("room_type == 'Private room'")
Upper_West_Side_shared = Upper_West_Side.query("room_type == 'Shared room'")

East_Harlem_entire = East_Harlem.query("room_type == 'Entire home/apt'")
East_Harlem_hotel = East_Harlem.query("room_type == 'Hotel room'")
East_Harlem_private = East_Harlem.query("room_type == 'Private room'")
East_Harlem_shared = East_Harlem.query("room_type == 'Shared room'")

Upper_East_Side_entire = Upper_East_Side.query("room_type == 'Entire home/apt'")
Upper_East_Side_hotel = Upper_East_Side.query("room_type == 'Hotel room'")
Upper_East_Side_private = Upper_East_Side.query("room_type == 'Private room'")
Upper_East_Side_shared = Upper_East_Side.query("room_type == 'Shared room'")

Central_Harlem_entire = Central_Harlem.query("room_type == 'Entire home/apt'")
Central_Harlem_hotel = Central_Harlem.query("room_type == 'Hotel room'")
Central_Harlem_private = Central_Harlem.query("room_type == 'Private room'")
Central_Harlem_shared = Central_Harlem.query("room_type == 'Shared room'")

Inwood_and_Washington_Heights_entire = Inwood_and_Washington_Heights.query("room_type == 'Entire home/apt'")
Inwood_and_Washington_Heights_hotel = Inwood_and_Washington_Heights.query("room_type == 'Hotel room'")
Inwood_and_Washington_Heights_private = Inwood_and_Washington_Heights.query("room_type == 'Private room'")
Inwood_and_Washington_Heights_shared = Inwood_and_Washington_Heights.query("room_type == 'Shared room'")


# average growth rate of the number of airbnb rooms by room types

AB0_growth_entire = AB0_growth.query("room_type == 'Entire home/apt'")
AB0_growth_hotel = AB0_growth.query("room_type == 'Hotel room'")
AB0_growth_private = AB0_growth.query("room_type == 'Private room'")
AB0_growth_shared = AB0_growth.query("room_type == 'Shared room'")


# In[1165]:


def growth():
    p3 = figure(plot_width=900, plot_height=750,y_range=(-1,1.5),x_range=(2015.9,2020.5))
    p3.title.text = 'Airbnb Growth Rate(Click on legend entries to hide the corresponding lines)'
    p3.xaxis.ticker = FixedTicker(ticks=[2016, 2017, 2018, 2019])

    for data, neighbourhood, color, line_dash in zip(
        [Lower_Manhattan_entire,Lower_Manhattan_hotel,Lower_Manhattan_private,Lower_Manhattan_shared, 
         Greenwich_Village_and_Soho_entire,Greenwich_Village_and_Soho_hotel,Greenwich_Village_and_Soho_private,
         Greenwich_Village_and_Soho_shared,
         Lower_East_Side_entire,Lower_East_Side_hotel,Lower_East_Side_private,Lower_East_Side_shared, 
         Chelsea_and_Clinton_entire,Chelsea_and_Clinton_hotel,Chelsea_and_Clinton_private,Chelsea_and_Clinton_shared,
         Gramercy_Park_and_Murray_Hill_entire, Gramercy_Park_and_Murray_Hill_hotel,Gramercy_Park_and_Murray_Hill_private,
         Gramercy_Park_and_Murray_Hill_shared,
         Upper_West_Side_entire,Upper_West_Side_hotel,Upper_West_Side_private,Upper_West_Side_shared,
         East_Harlem_entire,East_Harlem_hotel,East_Harlem_private,East_Harlem_shared,
         Upper_East_Side_entire,Upper_East_Side_hotel,Upper_East_Side_private,Upper_East_Side_shared,
         Central_Harlem_entire,Central_Harlem_hotel, Central_Harlem_private, Central_Harlem_shared, 
         Inwood_and_Washington_Heights_entire,Inwood_and_Washington_Heights_hotel,Inwood_and_Washington_Heights_private,
         Inwood_and_Washington_Heights_shared], 
        ['Lower Manhattan','Lower Manhattan','Lower Manhattan', 'Lower Manhattan',
         'Greenwich Village and Soho','Greenwich Village and Soho','Greenwich Village and Soho','Greenwich Village and Soho',
         'Lower East Side','Lower East Side','Lower East Side', 'Lower East Side',
         'Chelsea and Clinton','Chelsea and Clinton','Chelsea and Clinton','Chelsea and Clinton',
         'Gramercy Park and Murray Hill','Gramercy Park and Murray Hill','Gramercy Park and Murray Hill','Gramercy Park and Murray Hill',
         'Upper West Side','Upper West Side', 'Upper West Side', 'Upper West Side',
         'East Harlem', 'East Harlem','East Harlem','East Harlem',
         'Upper East Side', 'Upper East Side','Upper East Side','Upper East Side',
         'Central Harlem','Central Harlem','Central Harlem','Central Harlem',
         'Inwood and Washington Heights','Inwood and Washington Heights','Inwood and Washington Heights','Inwood and Washington Heights'], 
        ['#F26F80','#F26F80','#F26F80','#F26F80',
         '#9C0D38','#9C0D38','#9C0D38','#9C0D38',
         '#CC0000','#CC0000','#CC0000','#CC0000',
         '#300711','#300711','#300711','#300711',
         '#580C1F','#580C1F','#580C1F','#580C1F',
         '#CC8B86','#CC8B86','#CC8B86','#CC8B86',
         '#FAC9C2','#FAC9C2','#FAC9C2','#FAC9C2',
         '#FF5A5F','#FF5A5F','#FF5A5F','#FF5A5F',
         '#F9B5AC','#F9B5AC','#F9B5AC','#F9B5AC',
         '#FCE6EC','#FCE6EC','#FCE6EC','#FCE6EC'],
        ['solid','dashed','dotted','dashdot',
         'solid','dashed','dotted','dashdot',
         'solid','dashed','dotted','dashdot',
         'solid','dashed','dotted','dashdot',
         'solid','dashed','dotted','dashdot',
         'solid','dashed','dotted','dashdot',
         'solid','dashed','dotted','dashdot',
         'solid','dashed','dotted','dashdot',
         'solid','dashed','dotted','dashdot',
         'solid','dashed','dotted','dashdot']):
        df = pd.DataFrame(data)
        p3.line(df['year'], df['growth_rate'], color=color, line_dash=line_dash,
               line_width=2, alpha=0.8,legend_label=neighbourhood)

    p3.legend.location = 'top_right'
    p3.legend.click_policy="hide"

    x1 = AB0_growth_entire['year']
    y1 = AB0_growth_entire['growth_rate']
    
    x3 = AB0_growth_private['year']
    y3 = AB0_growth_private['growth_rate']

    x4 = AB0_growth_shared['year']
    y4 = AB0_growth_shared['growth_rate']

    r1 = p3.line(x1,y1,line_dash='solid',line_width=2,color='#09D291',legend_label='All')
    r3 = p3.line(x3,y3,line_dash='dotted',line_width=2,color='#09D291',legend_label='All')
    r4 = p3.line(x4,y4,line_dash='dashdot',line_width=2,color='#09D291',legend_label='All')

    legend3 = Legend(items=[("entire" , [r1]),
                       ("private",[r3]),("shared",[r4])],
                 location=(120,20), orientation="horizontal")
    p3.add_layout(legend3, 'center')
    
    return(p3)


# # 4th plot

# In[1166]:


# calculate the number of hotels by neighbourhood

Hotel1 = pd.DataFrame(Hotel.groupby(['neighbourhood_group']).size())
Hotel1 = Hotel1.reset_index()
Hotel1 = Hotel1.rename(columns={0: 'count_Hotel'})


# In[1167]:


# calculate the number of airbnb rooms by year and neighbourhood

AB2 = pd.DataFrame(AB.groupby(['year', 'neighbourhood_group']).size())
AB2 = AB2.reset_index()
AB2 = AB2.rename(columns={0: 'count_Airbnb'})


# In[1168]:


# calculate the airbnb listing / hotels ratio

Ratio = pd.merge(AB2, Hotel1, how='left', on=['neighbourhood_group'])
Ratio = Ratio.sort_values(by=['neighbourhood_group','year'])
Ratio.loc[:,'ratio'] = Ratio['count_Airbnb']/Ratio['count_Hotel']

Ratio1 = Ratio[['year','neighbourhood_group','ratio']]


# In[1169]:


Ratio1_2015 = Ratio1.query('year==2015')
Ratio1_2016 = Ratio1.query('year==2016')
Ratio1_2017 = Ratio1.query('year==2017')
Ratio1_2018 = Ratio1.query('year==2018')
Ratio1_2019 = Ratio1.query('year==2019')

Ratio1_2015 = Ratio1_2015.drop(['year'],axis=1)
Ratio1_2016 = Ratio1_2016.drop(['year'],axis=1)
Ratio1_2017 = Ratio1_2017.drop(['year'],axis=1)
Ratio1_2018 = Ratio1_2018.drop(['year'],axis=1)
Ratio1_2019 = Ratio1_2019.drop(['year'],axis=1)

Ratio1_2015 = Ratio1_2015.rename(columns={'ratio': 'r2015'})
Ratio1_2016 = Ratio1_2016.rename(columns={'ratio': 'r2016'})
Ratio1_2017 = Ratio1_2017.rename(columns={'ratio': 'r2017'})
Ratio1_2018 = Ratio1_2018.rename(columns={'ratio': 'r2018'})
Ratio1_2019 = Ratio1_2019.rename(columns={'ratio': 'r2019'})

Ratio_Final = pd.merge(Ratio1_2015, Ratio1_2016, how='left', 
               on=['neighbourhood_group'])
Ratio_Final = pd.merge(Ratio_Final, Ratio1_2017, how='left', 
               on=['neighbourhood_group'])
Ratio_Final = pd.merge(Ratio_Final, Ratio1_2018, how='left', 
               on=['neighbourhood_group'])
Ratio_Final = pd.merge(Ratio_Final, Ratio1_2019, how='left', 
               on=['neighbourhood_group'])

Ratio_Final = Ratio_Final.dropna()


# In[1170]:


def Ratio():
    NBHD = Ratio_Final['neighbourhood_group']
    r2015 = Ratio_Final['r2015'].tolist()
    r2016 = Ratio_Final['r2016'].tolist()
    r2017 = Ratio_Final['r2017'].tolist()
    r2018 = Ratio_Final['r2018'].tolist()
    r2019 = Ratio_Final['r2019'].tolist()

    data = {'NBHD':NBHD,
            '2015':r2015,
            '2016':r2016,
            '2017':r2017,
            '2018':r2018,
            '2019':r2019}

    source_ratio = ColumnDataSource(data=data)

    p4 = figure(x_range=(NBHD), y_range=(0, 200), plot_height=300,plot_width=1500,
                title="#Airbnb Listing/#Hotel Ratio")

    p4.vbar(x=dodge('NBHD', -0.3,range=p4.x_range), top='2015', width=0.1, 
        source=source_ratio, legend_label='2015',color='#B2414B')
    p4.vbar(x=dodge('NBHD', -0.15,range=p4.x_range), top='2016', width=0.1, 
        source=source_ratio, legend_label='2016',color='#FC6471')
    p4.vbar(x=dodge('NBHD', 0,range=p4.x_range), top='2017', width=0.1, 
        source=source_ratio, legend_label='2017',color='#EF798A')
    p4.vbar(x=dodge('NBHD', 0.15,range=p4.x_range), top='2018', width=0.1, 
        source=source_ratio, legend_label='2018',color='#FFA5A5')
    p4.vbar(x=dodge('NBHD', 0.3,range=p4.x_range), top='2019', width=0.1, 
        source=source_ratio, legend_label='2019',color='#FFCDCD')

    p4.x_range.range_padding = 0.1
    p4.xgrid.grid_line_color = None
    p4.legend.click_policy="hide"
    p4.legend.location = "top_left"
    p4.legend.orientation = "horizontal"
    p4.x_range.range_padding = 0.1
    p4.xaxis.major_label_text_font_size = "7pt"
    
    return(p4)


# In[1171]:


l2 = layout([map2(),growth()],[Ratio()],sizing_mode="fixed")


# # 5th plot

# In[1172]:


crime = pd.read_csv('Manhattan_crime.csv')
crime=crime.rename(columns={'zipcode': 'zip'})
crime = NY_zip.merge(crime, how='left', on='zip')
crime['violent_crime_index'] = crime['violent_crime_index'].replace(np.nan, 0)

geosource5 = GeoJSONDataSource(geojson = crime.to_json())


# In[1173]:


def pro_data3():
    airbnb3 = pd.read_csv('Airbnb.csv')
    
    airbnb3['last_scraped'] = pd.to_datetime(airbnb3['last_scraped'])
    airbnb3.loc[:,'year'] = airbnb3['last_scraped'].dt.year
    airbnb3 = airbnb3[['latitude','longitude','zipcode','year','neighbourhood_group','price']]
    a = []
    a.extend(airbnb3.neighbourhood_group.unique())
    neighbourhood = sorted(a)
    return airbnb3,neighbourhood

airbnb3,neighbourhood = pro_data3()


airbnb4=airbnb3.groupby(['year','neighbourhood_group','zipcode']).agg({'price':'size',
                                                                          'latitude':'mean',
                                                                          'longitude':'mean'})
airbnb4=airbnb4.rename(columns={'price':'count'})
airbnb4=airbnb4.reset_index()


def crime_data(neighbourhood, year):
    df_room = airbnb4.loc[airbnb4["neighbourhood_group"] == neighbourhood]
    data_room2 = df_room.loc[df_room['year'] == year]
    return data_room2


slider5 = Slider(title="Year", start=2015, end=2019, value=2015, step=1)

ch = ColumnDataSource(data=dict(x=[], y=[], size=[],year=[]))
cc = ColumnDataSource(data=dict(x=[], y=[], size=[], year=[]))
eh = ColumnDataSource(data=dict(x=[], y=[], size=[], year=[]))
gm = ColumnDataSource(data=dict(x=[], y=[], size=[], year=[]))
gs = ColumnDataSource(data=dict(x=[], y=[], size=[], year=[]))
iw = ColumnDataSource(data=dict(x=[], y=[], size=[], year=[]))
le = ColumnDataSource(data=dict(x=[], y=[], size=[], year=[]))
lm = ColumnDataSource(data=dict(x=[], y=[], size=[], year=[]))
ue = ColumnDataSource(data=dict(x=[], y=[], size=[], year=[]))
uw = ColumnDataSource(data=dict(x=[], y=[], size=[], year=[]))


# Define color palettes
palette2 = GnBu9
palette2 = palette2[::-1] # reverse order of colors so higher values have darker colors

# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper2 = LinearColorMapper(palette = palette2, low = 0, high = 80)

# Define custom tick labels for color bar.
tick_labels = {'0': '0', '5': '5',
 '10':'10', '15':'15',
 '20':'20', '25':'25',
 '30':'30', '35':'35',
 '40':'40'}

# Create color bar.
color_bar = ColorBar(color_mapper = color_mapper2, 
                     label_standoff = 8,
                     width = 400, height = 10,
                     border_line_color = None,
                     location = (0,0), 
                     orientation = 'horizontal',
                     major_label_overrides = tick_labels)


#Create figure object
p5 = figure(title = 'Crime Index VS. Airbnb Location', 
           plot_height = 800,
           plot_width = 800, 
           toolbar_location = 'above',
           tools = "pan, reset, wheel_zoom, box_zoom",
           x_range=(-74.04,-73.9), y_range=(40.70,40.9))
p5.xgrid.grid_line_color = None
p5.ygrid.grid_line_color = None

# Add patch renderer to figure.
zipcode1 = p5.patches('xs','ys', source = geosource5,
                   fill_color = {'field' :'violent_crime_index', 'transform' : color_mapper2},
                   line_color = '#cce5ff', line_width = 0.25, fill_alpha = 0.7)
# Set the label on the top left corner to indicate the current year the data is presenting
label1 = Label(x=-74.07, y=40.85, text=str(2015),text_font_size='50pt', text_color='white')
p1.add_layout(label1) 

# Plots
CH=p5.circle(x="x", y="y", source=ch, size="size",color='#FFCCCC',alpha=0.7)
CC=p5.circle(x="x", y="y", source=cc, size="size",color='#FFB3B3',alpha=0.7)
EH=p5.circle(x="x", y="y", source=eh, size="size",color='#FF9999',alpha=0.7)
GM=p5.circle(x="x", y="y", source=gm, size="size",color='#FF8080',alpha=0.7)
GS=p5.circle(x="x", y="y", source=gs, size="size",color='#FF6666',alpha=0.7)
IW=p5.circle(x="x", y="y", source=iw, size="size",color='#FF9966',alpha=0.7)
LE=p5.circle(x="x", y="y", source=le, size="size",color='#FF6A4D',alpha=0.7)
LM=p5.circle(x="x", y="y", source=lm, size="size",color='#FF5533',alpha=0.7)
UE=p5.circle(x="x", y="y", source=ue, size="size",color='#FF4D4D',alpha=0.7)
UW=p5.circle(x="x", y="y", source=uw, size="size",color='#FF3333',alpha=0.7)


#legend
# Legend configuration
legend5 = Legend(
    items=[('Central Harlem', [CH]),
           ('Chelsea and Clinton', [CC]),
           ('East Harlem', [EH]),
           ('Gramercy Park and Murray Hill', [GM]),
           ('Greenwich Village and Soho', [GS]),
           ('Inwood and Washington Heights', [IW]),
           ('Lower East Side', [LE]),
           ('Lower Manhattan', [LM]),
           ('Upper East Side', [UE]),
           ('Upper West Side', [UW])
           ],
    location="top_center", orientation="vertical",
)

p5.add_layout(legend5, "right")
p5.legend.background_fill_alpha = 0.0
p5.legend.click_policy = "hide"




def animate_update3():
    year = slider5.value + 1
    if year > 2019:
        year = 2015
    slider5.value = year

def update3():
    year = slider5.value
    label1.text = str(2015)

  
    n1 = crime_data('Central Harlem',year)
    ch.data = dict(
        x=n1['longitude'],
        y=n1['latitude'],
        size=n1['count']/40,
        year=n1['year'])
    
    n2 = crime_data('Chelsea and Clinton',year)
    cc.data = dict(
        x=n2['longitude'],
        y=n2['latitude'],
        size=n2['count']/40,
        year=n2['year'])
    
    n3 = crime_data('East Harlem',year)
    eh.data = dict(
        x=n3['longitude'],
        y=n3['latitude'],
        size=n3['count']/40,
        year=n3['year'])
    
    n4 = crime_data('Gramercy Park and Murray Hill',year)
    gm.data = dict(
        x=n4['longitude'],
        y=n4['latitude'],
        size=n4['count']/40,
        year=n4['year'])

    n5 = crime_data('Greenwich Village and Soho',year)
    gs.data = dict(
        x=n5['longitude'],
        y=n5['latitude'],
        size=n5['count']/40,
        year=n5['year'])
    
    n6 = crime_data('Inwood and Washington Heights',year)
    iw.data = dict(
        x=n6['longitude'],
        y=n6['latitude'],
        size=n6['count']/40,
        year=n6['year'])
    
    n7 = crime_data('Lower East Side',year)
    le.data = dict(
        x=n7['longitude'],
        y=n7['latitude'],
        size=n7['count']/40,
        year=n7['year'])
    
    n8 = crime_data('Lower Manhattan',year)
    lm.data = dict(
        x=n8['longitude'],
        y=n8['latitude'],
        size=n8['count']/40,
        year=n8['year'])
    
    n9 = crime_data('Upper East Side',year)
    ue.data = dict(
        x=n9['longitude'],
        y=n9['latitude'],
        size=n9['count']/40,
        year=n9['year'])
    
    n10 = crime_data('Upper West Side',year)
    uw.data = dict(
        x=n10['longitude'],
        y=n10['latitude'],
        size=n10['count']/40,
        year=n10['year'])    
    
slider5.on_change('value', lambda attr, old, new: update3())

# Specify layout
p5.add_layout(color_bar, 'below')
p5.background_fill_color = '#cce5ff'



# Create hover tool
p5.add_tools(HoverTool(tooltips = [('Zipcode','@zip'),
                                  ('Crime Index', '@violent_crime_index')]))


callback_id = None


# Set the speed for animation function here
def animate5():
    global callback_id
    if button5.label == '► Play':
        button5.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update3, 500)
    else:
        button5.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)


button5 = Button(label='► Play', width=60)
button5.on_click(animate5)

update3()

l3 = layout([
    [p5],
    [slider5,button5]],
    sizing_mode='fixed', name='layout')


# # 6th plot

# In[1174]:


AB_mom = pd.read_csv('airbnb_MOM.csv')


# In[1175]:


AB_mom.loc[:,'neighbourhood_group'] = AB_mom['zipcode'].map(cut_to)
AB_mom.dropna(axis=0,how='any')
AB_mom.loc[:,'date'] = AB_mom['last_scraped'].str.slice(0,7)
AB_mom['minimum_nights'].astype(int)

AB_mom1 = AB_mom[(AB_mom['minimum_nights']<31) & (AB_mom['room_type']=='Entire home/apt')]
AB_mom1.loc[:,'legality'] = 'no'


AB_mom2 = AB_mom.drop(AB_mom[(AB_mom.minimum_nights<31) & (AB_mom.room_type=='Entire home/apt')].index)
AB_mom2.loc[:,'legality'] = 'yes'


AB_l = AB_mom1.append(AB_mom2)

AB_l.loc[:,'price'] = AB_l['price'].str.split('$').str.get(1)
AB_l['price'] = AB_l['price'].str.replace(",","").astype(float)
AB_l.loc[:,'revenue'] = AB_l['price']*AB_l['availability_365']


# In[1176]:


def month(x):
    if x == '2018-10':
        return '-3'
    elif x == '2018-11':
        return '-2'
    elif x == '2018-12':
        return '-1'
    elif x == '2019-01':
        return '0'
    elif x == '2019-02':
        return '1'
    elif x == '2019-03':
        return '2'
    elif x == '2019-04':
        return '3'
    elif x == '2019-05':
        return '4'
    elif x == '2019-06':
        return '5'
    elif x == '2019-07':
        return '6'
    elif x == '2019-08':
        return '7'
    elif x == '2019-09':
        return '8'

    
AB_l.loc[:,'month'] = AB_l['date'].map(month)
AB_l['month'] = AB_l['month'].astype(int)


# In[1177]:


map_options2 = GMapOptions(lat=40.78353, lng=-73.96625, map_type="terrain", zoom=12)

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:

p6 = gmap("AIzaSyCmyNHNpIOODpU6bDWtqHqid18_9aKVADw", 
         map_options2, toolbar_location = 'above',
          title="Legitimacy of Airbnb(2018.10 - 2019.09)", plot_height=750, plot_width=1000)


# In[1178]:


def pro_data2():
    
    airbnb2 = AB_l[['latitude','longitude','month','legality','revenue']]
    a = []
    a.extend(AB_l.legality.unique())
    legality_list = sorted(a)
   
    return airbnb2,legality_list

airbnb2,legality_list = pro_data2()

#Create a month_list

months=[-3,-2,-1,0,1,2,3,4,5,6,7,8]

# Create a function to filter dataset by year
def legality_data(legality, month):
    df_legality = airbnb2.loc[airbnb2["legality"] == legality]
    data_legality = df_legality.loc[df_legality["month"] == month]
    return data_legality


illegal_src = ColumnDataSource(data=dict(x=[], y=[], month=[]))
legal_src = ColumnDataSource(data=dict(x=[], y=[], month=[]))





# Plot 


Legal = p6.circle(x="x", y="y", source=legal_src, size=1.5,fill_color= '#00cc66', line_color=None,
                line_width=0.3, line_alpha=0.5, fill_alpha=1)
Illegal = p6.circle(x="x", y="y", source=illegal_src, size=1.5,fill_color='#ff8080', line_color=None,
                line_width=0.3, line_alpha=0.5, fill_alpha=0.7)


#legend
# Legend configuration
legend6 = Legend(
    items=[("Legal", [Legal]),
           ("Illegal", [Illegal])],
    location="top_center", orientation="vertical"
)

p6.add_layout(legend6, "right")
p6.legend.background_fill_alpha = 0.0
p6.legend.click_policy = "hide"


def animate_update2():
    month = month_slider.value + 1
    if month > months[-1]:
        month = months[0]
    month_slider.value = month

def update2():
    
    month = month_slider.value
    
    legality1 = legality_data('yes', month)
    legal_src.data = dict(
        x=legality1['longitude'],
        y=legality1['latitude'],
        month=legality1['month']
        )
    
    legality2 = legality_data('no', month)
    illegal_src.data = dict(
        x=legality2['longitude'],
        y=legality2['latitude'],
        month=legality2['month']
        )

#set the starting point
month_slider = Slider(title="Month before/after The Milestone of Airbnb vs NYC ", 
                      start=months[0], end=months[-1], value=months[3], step=1,width=600)
month_slider.on_change('value', lambda attr, old, new: update2())

# Specify layout
p6.background_fill_color = '#cce5ff'


callback_id = None


# Set the speed for animation function here
def animate6():
    global callback_id
    if button6.label == '► Play':
        button6.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update2, 500)
    else:
        button6.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)


button6 = Button(label='► Play', width=60)
button6.on_click(animate6)





update2()

l4 = layout([
    [month_slider,button6]],
    [p6],
    sizing_mode='fixed', name='layout')


# In[1179]:


tab1 = Panel(child=l1,title="Hotel & AirBnB in Manhattan Overview")
tab2 = Panel(child=l2,title="The Evolution of Airbnb in Manhattan")
tab3 = Panel(child=l3,title="Manhattan Crime Index VS. AirBnB Location")
tab4 = Panel(child=l4,title="Legitimacy of Airbnb(2018.10 - 2019.09)")
tabs = Tabs(tabs=[ tab1, tab2, tab3,tab4 ])

curdoc().add_root(tabs)
curdoc().title = "SMM635_Group6_Final_Project"


# In[1180]:


show(tabs)


# In[ ]:





# In[ ]:




