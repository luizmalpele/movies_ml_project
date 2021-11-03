#when we import hydralit, we automatically get all of Streamlit
import hydralit as hy
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px 
import plotly.graph_objects as go

from library_streamlit import *

# ---- Hacks for removing `Streamlit` decoration and footer, `Plotly` icon, and adjusting content area width ----
st.markdown('<style>div.decoration {visibility: hidden}</style>', unsafe_allow_html=True)
st.markdown('<style>footer {visibility: hidden}</style>', unsafe_allow_html=True)
st.markdown('<style>.modebar-group:last-of-type {visibility: hidden}</style>', unsafe_allow_html=True)
st.markdown('<style>.reportview-container .main .block-container {max-width: 80%}</style>', unsafe_allow_html=True)

# Paths
#movies_data_path = './data/movies_streaming_platforms.csv'
movies_cleaned_data_path = 'C:/Users/luizg/Desktop/Poly/movies_ml_project/website/data/movies_streaming_platforms_cleaned.csv'
#user_vector_path = '../data/user_vector_baseline.csv'

movies_data = read_cleaned_movies_dataframe(path = movies_cleaned_data_path)

app = hy.HydraApp(title='Simple Multi-Page App')

@app.addapp(title='🏠')
def Home():
    hy.info('Your are at home')
    
    with st.form(key='quiz_form'):
        hy.info('In order to recommend you movies, please answer the following questions:')
        st.title('Select platforms:')
        st.multiselect('', ['Disney+', 'Hulu', 'Netflix','Prime']); # Platforms selection.

        st.title("Select Region: ") # Region Selection
        checkEurope = st.checkbox('Europe')
        checkNAmerica = st.checkbox('North America') 
        checkSAmerica = st.checkbox('South America')
        checkMiddleEast = st.checkbox('Middle East')
        checkAsia = st.checkbox('Asia')
        checkSAsia = st.checkbox('South Asia')

        st.title("Do you care about movie's scores?") # Movie's score
        st.radio('Pick one', ['Yes', 'No'])
        st.title("Select age rating: ") # Age rating
        all = st.checkbox('PG')
        r7 = st.checkbox('+7')
        r13 = st.checkbox('+13')
        r16 = st.checkbox('+16')
        r18 = st.checkbox('+18')

        st.title("Select genre: ") # Select genre
        genres = st.multiselect('', ['Action','Adventure','Animation', 'Biography',
        'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir','Game-Show',
        'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV','Romance','Sci-Fi',
        'Short','Sport','Talk-Show','Thriller','War','Western','Other Genres'])

        submit_button = st.form_submit_button() # Submit form button

# Movie Wazar page.
@app.addapp(title='🧙🏼Movie Wizard')
def MovieWizard():
    st.form('movie_wizard')

@app.addapp()
def Explore():
    hy.info('Explore the data')

@app.addapp()
def Statistics():
    hy.info('Lets see some visualizations')
    st.title('Explore Statistics behind the Streaming Platform and Film Industry')
    #st.write(movies_data)
    fig_scores = plot_scores_distribution(movies_data = movies_data)
    st.plotly_chart(fig_scores)
    fig_platform = plot_scores_per_platform(movies_data)
    st.plotly_chart(fig_platform)
    fig_runtime = plot_runtime_distribution(movies_data = movies_data)
    st.plotly_chart(fig_runtime)
    
    with st.form(key='quiz_form'):
        hy.info('In order to explore key features behind the film industry, use the Exploration Interactive Tool:')

        st.title("Select Region: ") # Region Selection
        arg_slider_column_list = st.slider('Choose the filtering value for System\'s filtering slope', 1, 30, 10, step = 1)

        st.title('Select a Column to Visualize') # Movie's score
        arg_column_list = st.selectbox('Pick one', ['genres', 'language', 'directors','contry'], key=1)
        
        submit_button = st.form_submit_button() # Submit form button
        
    fig_column_list = plot_column_list(movies_data, column_name = arg_column_list, top = arg_slider_column_list)
    st.plotly_chart(fig_column_list)
    
@app.addapp()
def Disney():
    hy.info('Movies from Disney+')

@app.addapp()
def Hulu():
    hy.info('Movies from Hulu')

@app.addapp()
def Netflix():
    hy.info('Movies from Netflix')

@app.addapp()
def Prime():
    hy.info('Movies from Prime')

#Run the whole lot, we get navbar, state management and app isolation, all with this tiny amount of work.

app.run()