#this program is built with streamlit package
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from PIL import Image
import plotly.express as px
#this function does importnat calculation to change the mass units. It assumes that the surface area of glacier coverage is constant which isnt true, howver as this is no
#not a precise indevor it doesnt matter too much.
def glaciermass(df,value):
    if value == 0:
        return 0,0
    cmb_mw = df['Mean cumulative mass balance'][value]
    if value == 1:
        cmb_mw1 = 0
    else:
        cmb_mw1 = df['Mean cumulative mass balance'][value-1]
    rho_w = 997             #kg/m^3
    surarea = 525000        #m^2 estimate. 
    mass1 = cmb_mw * 1000 * rho_w * (surarea) #Order of magnitude simialar to that quoted in papers (chrome bookmark).
    mass2 = cmb_mw1 *1000*rho_w*(surarea)
    mass = mass1 - mass2
    volume = mass/rho_w
    return mass, volume

logo = st.sidebar.image('cardiff_uni_logo.png',width=100)

decription = st.sidebar.write('MSc Microproject Infographic. By Rhys Shaw and Kevin Lo \n')

add_description = st.sidebar.write(
    '\n In this infographic we can see how the total mass of Earths glaciers has changed scince 1945.\n \n Below, you can change the units for Mass and Volume relative to more familiar landmarks.')

add_unit_options = st.sidebar.radio('Mass Units',('Burj Khalifa','Pyrimid of Giza','Everest'))

add_unitvol_option = st.sidebar.radio('Volume Unit',('Olympic Swiming Pool','Lake Erie','Atlantic Ocean'))

# imports the glaciers data
df = pd.read_csv('glaciers_csv.csv')
#title of the page
st.markdown("<h1 style='text-align: center; color: black;'>MELTING GLACIERS!</h1>", unsafe_allow_html=True)

image = st.image('glac.jpg',use_column_width=True,caption='Mountain Glacier Melting into the sea')
#st.dataframe(df)

dz = pd.read_csv('reducedloc.csv')

st.header('Where are glaciers around the world?')
st.write('Below is a map of Northen hemisphere glaciers.')

fig = px.scatter_mapbox(dz, lat="Lat", lon="Long", size="Area",size_max=30,color_discrete_map="#9932CC", zoom=1,center={'lat':50,'lon':0})
fig.update_layout(mapbox_style='white-bg', mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ]
)
st.plotly_chart(fig)

st.header("How did the glaciers change between 1945 and 2014?")

fig = go.Figure(data=[go.Scatter(x=df['Year'],y=df['Mean cumulative mass balance'],mode='lines+text',opacity=0.8,marker={'size': 15,
                'line': {'width': 1.5, 'color': 'black'}},line={'color':'black','width':1.5})])
fig.update_layout(title='Glacier Mass Balance from 1945-2014.')
fig.update_xaxes(type='category',title_text='Year')
fig.update_yaxes(title_text="Glacier Mass Balance")
st.plotly_chart(fig)

st.write("How Much do we lose each year? Move the slider to find out how much Mass and volume of ice we lost from our glaciers.")

x = int(st.slider('Year',min_value=1945,max_value=2014,step=1))  # 👈 this is a widget

col1,col2,col3,col4 = st.beta_columns(4)   
col1.write('The selected year is')#, x)
value = x-1945

mass, volume = glaciermass(df,value)

col2.write(x)
col1.write('Glacier Mass Difference is ')#, round(abs(glaciermass(df,value)[0])/100000000000,2),'x10,000,000,000 Kg')
col2.write(round(mass/100000000000,2))
col2.write(' ')
col2.write(' ')
col3.write(' ')
col3.write(' ')
col3.write(' ')

col3.write('x10,000,000,000 Kg')
col3.write(' ')
col3.write(' ')
col4.write(' ')
kg = Image.open('kgcartoon.jpg')
col4.image(kg,width=60)
#sets up 2 columns for use in the sidebar
  

#options for the main body underneth the slider.

if add_unit_options =='Burj Khalifa':
    im = Image.open('burj1.jpg')
    col1.write('Mass difference In units of Burj Khalifa ')#,
    col2.write(round(mass/453592370,2))
    col2.write(' ')
    col3.write(' ')
    col3.write(' ')
    col3.write(' ')
    col4.image(im,width=60)
if add_unit_options =='Pyrimid of Giza':
    img = Image.open('pyr.jpg')
    col1.write('Mass difference In units of Pyrimid of Giza ')#,round(abs(glaciermass(df,value)[0]/5896700810),2))
    col2.write(round(mass/5896700810,2))
    col2.write(' ')
    col3.write(' ')
    col3.write(' ')
    col3.write(' ')
    col4.image(img,width=150)
if add_unit_options =='Everest':
    col1.write('Mass difference In units of Everest ')
    col2.write(round(mass/161932476090000 *100,2))
    col2.write(' ')
    col3.write('/100')
    col3.write(' ')
    col4.image('baseever.jpg',width=150)


if add_unitvol_option =='Olympic Swiming Pool':
    col1.write('Volume In Units of Olympic Swiming Pools')
    col2.write(round(volume/2500* 1/100000,2))
    col3.write('x100,000')
if add_unitvol_option =='Lake Erie':
    col1.write('Volume In Units of Lake Erie (One of Americas great lakes)')
    col2.write(round((volume/480000000000 *1000),2))
    col3.write('/1,000')
if add_unitvol_option =='Atlantic Ocean':
    col1.write('Volume In Units of Atlantic Oceans')
    col2.write(round(volume/310410900000000000 *1000000000,2))
    col3.write(' /1,000,000,000')
