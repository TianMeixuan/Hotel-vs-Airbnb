# How to Run The Code
open terminal 

cd into SMM635_Group_6 folder/Airbnb_vs_Hotel

type bokeh serve --show main.py

# File Specifiction 
Data cleaning code are saved in folder Data

Airbnb_vs_Hotel fold the main.py with CSV files and Shapefile that are required to run main.py

A jupyter notebook equivalent to main.py is also saved in the Airbnb_vs_Horel folder

# Exectutive Summary
Airbnb began in 2008 and millions of hosts and travellers choose Airbnb to list their space and book unique accommodation anywhere in the world.Airbnb successfully leveraged the benefits of the sharing economy business model by joining customers and host in its online platform. New York is one of the biggest markets of Airbnb. This project analyses the evolution of Airbnb in Manhattan between 2015 and 2019 in comparison with hotels. The insights drawn from the analyses show the impact of the sharing economy business model on traditional business model with a focus on the aspect of location and offer type (Airbnb room type). The findings are also effective for lobbying for policies favouring the traditional hotel industry as crime index and legitimacy of Airbnb are considered in the analyses. 
## Key Insights:
1. A great number of Airbnbs rooms are located across Manhattan. The number of Airbnbs fluctuate in the past five years. Clusters of Airbnbs could be found around areas where hotels are densely located. The majority of Airbnbs are Entire places and Private rooms. Four clusters of Entire places could be found in lower Manhattan. There are two clusters of Entire rooms in lower Manhattan and Entire rooms are densely located in upper Manhattan. Shared rooms are sparsely located in Manhattan. The locations of Airbnb hotel rooms are very close to the locations of hotels. 

2. Airbnb market may have reached saturation in Manhattan. A higher Airbnb/Hotel ratio could be identified in North Manhattan, indicating higher market traction, whereas the ratio is smaller in South Manhattan. Meanwhile, despite neighbourhoods in South Manhattan has a lower Airbnb/Hotel ratio, a higher growth rate could be identified implying a growing competition. 

3. In Manhattan, a great proportion of Airbnbs are located in areas with higher crime index, which may increase public security concerns. 

4. The lawsuit between Airbnb and New York City is not effective as the illegal listings on Airbnb did not reduce in the past 12 months. Airbnb policy did not comply with the law and Airbnb is likely to help the hosts avoid tax. 

# Scope of Data
We assumed the number and locations of hotels in Manhattan are static. For Airbnb, we used September data of each year (2015-2019) for all analyses to show the flow of change apart from the Airbnb legitimacy analyses. In order to provide a more in-depth insight of Airbnb legitimacy in Manhattan, we used data of the past 12 months to illustrate the change due to the increasing press coverage of the case since January this year. 

In order to provide an insightful analyses, we visualized the data using the exact location and neighbourhood of each Airbnb and hotel. We categorised each location into 10 distinctive Manhattan neighbourhoods according to public government information available online. We also deployed the crime index data online in order to show the relationship between airbnb location and crime index of each zip. In terms of the legitimacy of Airbnb, we classify an Airbnb is illegal if the room type is entire place and the minimum nights are less than 30 days according to the New York City Law (Weiser and Goodman, 2019). 

1. Airbnb data source: http://insideairbnb.com/get-the-data.html

2. Hotel data source: https://github.com/priyasrivast/WebscrapingAirBnbAndHotels

3. New York neighbourhood and zip: https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm 

4. Crime index data: https://www.bestplaces.net/crime/city/new_york/new_york

# Tab Overview and Findings
## Tab1
<img src="/Image/Figure0.png" alt="Figure0"
 title="Figure0" width="300" />

The first graph is aimed to show the overall distribution of Airbnb and hotels in Manhattan from 2015 to 2019, the density of this figure is very high. 

We plotted the locations of Airbnb and hotels to show the overall evolution of Airbnb and the competition between Airbnb and hotels from 2015 to 2019.

<img src="/Image/Figure1.png" alt="Figure1"
 title="Figure1" width="600" />
 
It can be seen from the figure that Airbnbs are densely located in various places of Manhattan. In spite of little fluctuations, little change could be identified in terms of the number of Airbnbs in Manhattan from 2015 to 2019. Airbnbs are more clustered in lower Manhattan.
Most hotels are densely located around Midtown and Lower Manhattan,and the others are scattered across Manhattan. It’s also worth noting that a few Airbnb can are found in Midtown whereas hotel is densely located in this area. 

In order to have a closer look of the relationship between Airbnb and hotels, we observed locations of 4 different Airbnb room types and contrasted them with hotels separately.

<img src="/Image/Figure2.png" alt="Figure2"
 title="Figure2" width="600" />
 
Entire home or apartment (Entire place) has the highest number of rooms spreading across Manhattan. More specifically, Entire rooms formed 4 distinct clusters in Midtown and lower Manhattan where majority of the hotels were located. There are also many Entire places  aggregated in Upper East and Upper West. Entire places in upper Manhattan are relatively sparse.

<img src="/Image/Figure3.png" alt="Figure3"
 title="Figure3" width="600" />
 
Private room is the second-popular room type and two distinct clusters can be observed in middle and lower Manhattan. It also could be noticed that the density of Private rooms is much higher than that of Entire places in Upper Manhattan. Besides, the proportion of private rooms around the two sides of Central Park is lower than the proportion of the entire place.

<img src="/Image/Figure4.png" alt="Figure4"
 title="Figure4" width="600" />
 
The number of shared room is much less than the two room types aforementioned and scattered sparsely throughout Manhattan.
 
<img src="/Image/Figure5.png" alt="Figure5"
 title="Figure5" width="600" />
 
The number of Airbnb hotel rooms are really small as it is firstly introduced to Airbnb in 2019. The locations of Airbnb hotel rooms are very close to the locations of hotels. 

## Tab2

<img src="/Image/Figure6.png" alt="Figure6"
 title="Figure6" width="300" />
<img src="/Image/Figure7.png" alt="Figure7"
 title="Figure7" width="300" /> 

Ths dimension of this figure is quite high with the coordinates of the map, count of Airbnb in each neighbourhood and zip code of each zone.

In order to illustrate the evolution of Airbnb in Manhattan over the five years in comparison with hotels, firstly we designed the top left graph to visualise the distribution of hotel by neighbourhood in Manhattan. The map of manhattan is drawn based on zips. Colormap is used to explain the count of hotels in different neighbourhood, the darker the color, the more hotels could be found in the neighbourhood. The name of the neighbourhood, the count of hotel in the neighbourhood and the zipcode of the place could be found using hover tool. 

<img src="/Image/Figure8.png" alt="Figure8"
 title="Figure8" width="300" /> 
 
<img src="/Image/Figure9.png" alt="Figure9"
 title="Figure9" width="500" />
 
The third and fourth figures are designed to show the statistical analysis within neighbourhoods so the abstraction degree in this figure is very high.
WIth the reference of the hotel heatmap on top left, the top right graph illustrates the growth rate of different Airbnb room types by neighbourhood. The corresponding lines of the legends can be hidden by clicking the legend, which can be very useful while analysing one single neighbourhood or make comparisons between 2 or more neighbourhoods. The colors of the lines also matches with the color of neighbourhood in top left graph. The green lines provide a benchmark for all neighbourhoods, which is the average growth rate of the whole Manhattan area. For each neighbourhood, there are four lines illustrating the growth rate of the entire place(solid lines), private rooms(dotted lines) and shared rooms (dashdot lines). 

It could be found in the graph that most room types in most neighbourhoods follow a similar pattern in the past five year. In most cases, the number of Airbnb rooms increase positively in 2016 followed by a slight drop in 2017. The growth rate rebounded in 2018 to positive and a negative growth rate are found in 2019. It could be concluded that count of Airbnb fluctuate across the 5 years. From the aspect of room type, in general, private rooms and shared rooms have higher growth rate in 2016, but entire places increase faster from 2017. The general patterns illustrate that the Airbnb market in Manhattan may have reached a saturation. Especially, the highest growth rate of entire places imply that the penetration of Airbnb placed a fierce competition on hotels. To highlight, there are some special cases in terms growth rate in the past 5 years. For example:

1.The growth rate of Airbnb entire place in Lower Manhattan increased both in 2018 and 2019 and the growth rate peaked in 2019 with more than 50%. Airbnb shared rooms in Chelsea and Clinton increased almost 40% in 2019. A more severe competition between hotels and airbnbs may be seen in Lower Manhattan area and the Chelsea and Clinton area in the past 2 years. 

2.In Gramercy Park and Murray Hill area, despite the pattern of the growth rates follows most of neighbourhoods and room types in Manhattan, its growth rates are much higher. Airbnb entire rooms in the neighbourhood increased around 60% in 2018 whereas the average growth rate of Manhattan is only 30%. 

3.In Central Harlem area, although the general pattern looks similar to the general pattern, the growth rate change more drastic compared with other neighbourhoods. For instance, In 2016, shared rooms in the area are more than doubled but the number decreased ever since. 

<img src="/Image/Figure10.png" alt="Figure10"
 title="Figure10" width="300" /> 
<img src="/Image/Figure11.png" alt="Figure11"
 title="Figure11" width="800" />
 
The bottom graph illustrates the ratio between Airbnb and hotel in different neighbourhoods throughout the 5 years. It could be found Inwood and Washington Heights has the highest ratio, implying a high market traction and severe competition in the neighbourhood. The ratios in Central Harlem, Upper West Side, East Harlem and Lower East Side are also high. In contrast, at the lower end, Chelsea and Clinton has the lowest Airbnb/Hotel ratio, following by Gramercy Park and Murray Hill and Lower Manhattan. It could be interpreted that the competition in the areas are less fierce. 

From the aspect of YoY change, it could be found that in most neighbourhoods the Airbnb/Hotel ratio is increasing from 2015 to 2018, followed by a slight drop in 2019. In Greenwich Village and Soho and Lower East side, the ratios fluctuate through the five years. 

Together with the evidence from the top right graph, it could be concluded that the Airbnb market may have reached saturation in Manhattan. A higher Airbnb/Hotel ratio could be identified in North Manhattan, indicating higher market traction, whereas the ratio is smaller in South Manhattan. Meanwhile, despite neighbourhoods in South Manhattan has a lower Airbnb/Hotel ratio, a higher growth rate could be identified implying an increasing competition.

## Tab3

<img src="/Image/Figure12.png" alt="Figure12"
 title="Figure12" width="300" /> 
 
<img src="/Image/Figure13.GIF" alt="Figure13"
 title="Figure13" width="500" />
 
We want to create a map to show the relationship between crime index and count of Airbnb in each zip code zone. A great amount of information need to be plotted on the map to visualise the relationship. Thus this figure is inclined to multidimensional, original and light.

We created a crime map to visualise the relationship between the crime index and the count of Airbnbs with different zip in Manhattan. The underlying colormap illustrated the crime index. The higher the crime index, the darker the colour. The size of the circle represents the total amount of Airbnb with different zip and neighbourhoods that the zip belongs to are distinguished by colour. The locations of the circles are calculated by the mean of all the Airbnb rooms’ coordinates in the same zip  In addition, the exact crime index of each zip and the zip of the place could be found using hover tool. 

According to the visualisation, a great proportion of Airbnbs are located in less safe areas such as Lower East Side, Inwoods,Washington Heights, Chelsea and Clinton and Central Harlem. Airbnbs are less regulated than hotels and the phenomenon aforementioned may bring more public security concerns. Consequently, crimes and other security related issues could bring more pressure to the Metropolitan Police. Therefore, the visualization can be used to lobby for a more strict regulation of Airbnb activities in Manhattan from the aspect of public security. 

## Tab4

<img src="/Image/Figure14.png" alt="Figure14"
 title="Figure14" width="300" />

The sixth figure is aimed to show the distribution of legal and illegal Airbnbs in Manhattan. Thus the functionality and density are relatively high in this graph.

The battle between Airbnb and New York city has lasted a few years. It is illegal under state law to rent out apartments in most buildings for fewer than 30 days unless the permanent tenant is present when a guest is renting. From the aspect of tax, it is believed that some Airbnbs are geared toward getting around city regulations that are intended to keep blocks of apartments from being turned into makeshift hotels that avoid lodging taxes and oversight.
We classified Airbnbs as illegal if the room type is entire place and the minimum nights required is less than 30 days. (Ferré-Sadurní,2019) 

The battle is escalated In January 2019 as Airbnb was embroiled in a lawsuit brought by New York City government alleging that an illegal hotelkeeper used Airbnb platform to make 21 million dollars in illicit profit over a long period of time. (Luis, 2019) In order to get a better understanding of the legitimacy of Airbnb rooms and whether they were affected by the lawsuit in January, we visualized legal and illegal Airbnb rooms on Google map to present the change between October 2018 to September 2019. The change by month can be clearly reflected by the slider at the bottom. 

According to the visualisation, illegal Airbnbs are more condensed in lower Manhattan and the clusters are identical to the clusters of entire places. Meanwhile, legal Airbnbs could be found in upper Manhattan. 

 <img src="/Image/Figure15.png" alt="Figure15"
 title="Figure15" width="500" />
 <img src="/Image/Figure16.png" alt="Figure16"
 title="Figure16" width="500" />
 
It could be found from the graph that around half of Airbnbs in Manhattan are illegal, indicating a break of law and potential tax loss of the government. Most importantly, The number of illegal Airbnb’s rooms did not change much between October 2018 and September 2019, suggesting that this lawsuit did not put a big impact on Airbnb. Thus, the graph is effective for hotel industry to argue for more favourable policy towards hotels as Airbnb policy did not comply with the law and Airbnb is likely to help the hosts avoid tax. 

# Limitation

1.We used count of hotels as a benchmark while comparing hotels with airbnbs. However, the analyses would be more precise if we compare hotel rooms with airbnbs. 

2.The accuracy of the analyses is restrained by the assumption that the data of Manhattan hotels do not change over the 5 years.

3.New York is one of the first few markets of Airbnb, however, we only analysed the recent 5 years data of Airbnb. In addition, we only used September data of each year for the analyses, whereas the seasonality pattern of Airbnb listing is not considered. Therefore, the accuracy of the analyses are subject to the limitation. 

# Reference
Weiser, B. and Goodman,J., (2019). Judge Blocks New York City Law Aimed at Curbing Airbnb Rentals. The New York Times [online]. 3 January. 4 Jan  2019. p.17. Available from: https://www.nytimes.com/2019/01/03/nyregion/nyc-airbnb-rentals.html (Accessed on 12 Dec 2019 ).

Ferré-Sadurní, F., (2019).New York Empire of Illegal Airbnb Rentals Booked 75,000 Guests, Suit Says. The New York Times [online]. 14 Jan. 15 Jan 2019. p.20. Available from: https://www.nytimes.com/2019/01/14/nyregion/airbnb-illegal-brokers-real-estate.html (Accessed on 12 Dec 2019 ).

Ferré-Sadurní, F., (2019). Inside the Rise and Fall of a Multimillion-Dollar Airbnb Scheme. The New York Times [online]. 23 Feb. 24 Feb 2019. p.1. Available from: https://www.nytimes.com/2019/02/23/nyregion/airbnb-nyc-law.html (Accessed on 12 Dec 2019 ).
