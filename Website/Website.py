# Application
import hydralit as hy
import streamlit as st
import pandas as pd

# Agrid
from st_aggrid import AgGrid

# Visualizations
from plotly.subplots import make_subplots
import plotly.express as px 
import plotly.graph_objects as go

# Machine Learning
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

from library_streamlit import *

# ---- Hacks for removing `Streamlit` decoration and footer, `Plotly` icon, and adjusting content area width ----
st.markdown('<style>div.decoration {visibility: hidden}</style>', unsafe_allow_html=True)
st.markdown('<style>footer {visibility: hidden}</style>', unsafe_allow_html=True)
st.markdown('<style>.modebar-group:last-of-type {visibility: hidden}</style>', unsafe_allow_html=True)
st.markdown('<style>.reportview-container .main .block-container {max-width: 80%}</style>', unsafe_allow_html=True)

# Paths
#movies_data_path = './data/movies_streaming_platforms.csv'
movies_cleaned_data_path = 'C:/Users/luizg/Desktop/Poly/movies_ml_project/website/data/movies_streaming_platforms_cleaned.csv'
user_vector_path = 'C:/Users/luizg/Desktop/Poly/movies_ml_project/website/data/user_vector_baseline_t.csv'

movies_data = read_cleaned_movies_dataframe(path = movies_cleaned_data_path)

app = hy.HydraApp(title='Simple Multi-Page App')

@app.addapp(title='🏠')
def Home():
    hy.info('Your are at home')
    

# Movie Wazar page.
@app.addapp(title='🧙🏼Movie Wizard')
def MovieWizard():
    st.form('movie_wizard')
    
    with st.form(key='quiz_form'):     
        st.markdown('#### In order to recommend you movies, please answer the following questions:')
        st.title('Select platforms:')
        hy.info('Blank response will select all automatically')
        arg_platform_display = st.multiselect('', ['Disney+', 'Hulu', 'Netflix','Prime']); # Platforms selection.

        st.title('Select Region: ') # Region Selection
        arg_region = st.multiselect('Select Region Preferences', ['Europe', 'North America', 'LATAM', 'Asia', 'Other'], key=1)

        st.title("Do you care about movie's scores?") # Movie's score
        st.radio('Pick one', ['Yes, of course(...)', 'Only to avoid bad movies','Not All!'])
        st.title("Select age rating: ") # Age rating
        arg_age_display = st.radio('Select Region Preferences', ['PG', '7+', '13+', '16+', '18+'])

        st.title("Select genre: ") # Select genre
        arg_genres_display = st.multiselect('', ['Action','Adventure','Animation', 'Biography',
        'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir','Game-Show',
        'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV','Romance','Sci-Fi',
        'Short','Sport','Talk-Show','Thriller','War','Western','Other Genres'])

        submit_button = st.form_submit_button() # Submit form button

    if submit_button:
        movies_data_filtered = filter_by_platforms(df = movies_data, platforms_list = arg_platform_display)
        movies_data_merged_genres = get_column_dummies_from_list(movies_data_filtered, column_name = 'genres', merge_dummies = True)
        movies_data_merged_genres_age = get_column_dummies_from_list(movies_data_merged_genres, column_name = 'age', merge_dummies = True)
        movies_data_user_vector = read_append_user_vector(user_vector_path, df = movies_data_merged_genres_age)
        movies_data_user_vector_updated = update_user_vector(df = movies_data_user_vector, genres_display = arg_genres_display, age_display = arg_age_display)
        features = get_features(movies_data_user_vector)
        tsne_df = generate_tsne_transfomation(features = features, df = movies_data_user_vector)
        st.markdown("<h2 style='text-align: center; color: black;'>Top 10 Movie Recommendations</h2>", unsafe_allow_html=True)
        recommendations_df = get_recommendations(df = tsne_df, refresher_counter = 1)
        AgGrid(recommendations_df)
        st.markdown("<h2 style='text-align: center; color: black;'>t-SNE 2-Dimensional Plane Visualization</h2>", unsafe_allow_html=True)
        fig_tnse_recommendations = generate_tsne_visualization(tsne_df)
        st.plotly_chart(fig_tnse_recommendations, use_container_width=True)

            
    
@app.addapp()
def Explore():
    st.markdown("<h1 style='text-align: center; color: black;'>Explore Statistics behind your Favourite Films</h1>", unsafe_allow_html=True)
    hy.info('The DataFrame is interactive and allows you to Sort, Filter, and apply various Exploratory function to the data!')
    AgGrid(movies_data)

@app.addapp()
def Statistics():
    hy.info('Lets see some visualizations')
    st.markdown("<h1 style='text-align: center; color: black;'>Explore Statistics behind the Streaming Platform and Film Industry</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Critics\'s scores Exploration</h2>", unsafe_allow_html=True)
    fig_scores = plot_scores_distribution(movies_data = movies_data)
    st.plotly_chart(fig_scores, use_container_width=True)
    fig_platform = plot_scores_per_platform(movies_data)
    st.plotly_chart(fig_platform, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Film\'s Information Exploration</h2>", unsafe_allow_html=True)
    fig_runtime = plot_runtime_distribution(movies_data = movies_data)
    st.plotly_chart(fig_runtime, use_container_width=True)
    
    with st.form(key = 'column_list_form'):
        hy.info('In order to explore key features behind the film industry, use the Exploration Interactive Tool:')

        st.markdown('### Number of Features')
        arg_slider_column_list = st.slider('Select the number of categories you want to visualize:', 1, 30, 15, step = 1)

        st.markdown('### Feature to Analyze')
        #st.title('Select a Column to Visualize') # Movie's score
        arg_column_list = st.selectbox('Select a colume to Visualize', ['genres', 'language', 'directors','country'], key=1)
        
        submit_button = st.form_submit_button() # Submit form button
        
        fig_column_list = plot_column_list(movies_data, column_name = arg_column_list, top = arg_slider_column_list)
        st.plotly_chart(fig_column_list, use_container_width=True)
    
@app.addapp()
def Disney():
    st.markdown("<h1 style='text-align: center; color: black;'>Disney+ Platform Exploration</h1>", unsafe_allow_html=True)
    hy.info('Movies from Disney+')
    movies_data_filtered = filter_by_platforms(df = movies_data, platforms_list = ['Disney+'])
    st.markdown("<h2 style='text-align: center; color: black;'>Critics\'s scores for Disney+</h2>", unsafe_allow_html=True)
    fig_scores = plot_scores_distribution(movies_data = movies_data)
    st.plotly_chart(fig_scores, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Film\'s Information Exploration</h2>", unsafe_allow_html=True)
    fig_runtime = plot_runtime_distribution(movies_data = movies_data_filtered)
    st.plotly_chart(fig_runtime, use_container_width=True)
    
    with st.form(key = 'column_list_form'):
        hy.info('In order to explore key features behind the film industry, use the Exploration Interactive Tool:')

        st.markdown('### Number of Features')
        arg_slider_column_list = st.slider('Select the number of categories you want to visualize:', 1, 30, 15, step = 1)

        st.markdown('### Feature to Analyze')
        #st.title('Select a Column to Visualize') # Movie's score
        arg_column_list = st.selectbox('Select a colume to Visualize', ['genres', 'language', 'directors','country'], key=1)
        
        submit_button = st.form_submit_button() # Submit form button
        
        fig_column_list = plot_column_list(movies_data_filtered, column_name = arg_column_list, top = arg_slider_column_list)
        st.plotly_chart(fig_column_list, use_container_width=True)

@app.addapp()
def Hulu():
    hy.info('Movies from Hulu')
    st.markdown("<h1 style='text-align: center; color: black;'>Hulu Platform Exploration</h1>", unsafe_allow_html=True)
    hy.info('Movies from Disney+')
    movies_data_filtered = filter_by_platforms(df = movies_data, platforms_list = ['Hulu'])
    st.markdown("<h2 style='text-align: center; color: black;'>Critics\'s scores for Hulu</h2>", unsafe_allow_html=True)
    fig_scores = plot_scores_distribution(movies_data = movies_data)
    st.plotly_chart(fig_scores, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Film\'s Information Exploration</h2>", unsafe_allow_html=True)
    fig_runtime = plot_runtime_distribution(movies_data = movies_data_filtered)
    st.plotly_chart(fig_runtime, use_container_width=True)
    
    with st.form(key = 'column_list_form'):
        hy.info('In order to explore key features behind the film industry, use the Exploration Interactive Tool:')

        st.markdown('### Number of Features')
        arg_slider_column_list = st.slider('Select the number of categories you want to visualize:', 1, 30, 15, step = 1)

        st.markdown('### Feature to Analyze')
        #st.title('Select a Column to Visualize') # Movie's score
        arg_column_list = st.selectbox('Select a colume to Visualize', ['genres', 'language', 'directors','country'], key=1)
        
        submit_button = st.form_submit_button() # Submit form button
        
        fig_column_list = plot_column_list(movies_data_filtered, column_name = arg_column_list, top = arg_slider_column_list)
        st.plotly_chart(fig_column_list, use_container_width=True)

@app.addapp()
def Netflix():
    st.markdown("<h1 style='text-align: center; color: black;'>Netflix Platform Exploration</h1>", unsafe_allow_html=True)
    hy.info('Movies from Netflix')
    movies_data_filtered = filter_by_platforms(df = movies_data, platforms_list = ['Netflix'])
    st.markdown("<h2 style='text-align: center; color: black;'>Critics\'s scores for Netflix</h2>", unsafe_allow_html=True)
    fig_scores = plot_scores_distribution(movies_data = movies_data)
    st.plotly_chart(fig_scores, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Film\'s Information Exploration</h2>", unsafe_allow_html=True)
    fig_runtime = plot_runtime_distribution(movies_data = movies_data_filtered)
    st.plotly_chart(fig_runtime, use_container_width=True)
    
    with st.form(key = 'column_list_form'):
        hy.info('In order to explore key features behind the film industry, use the Exploration Interactive Tool:')

        st.markdown('### Number of Features')
        arg_slider_column_list = st.slider('Select the number of categories you want to visualize:', 1, 30, 15, step = 1)

        st.markdown('### Feature to Analyze')
        #st.title('Select a Column to Visualize') # Movie's score
        arg_column_list = st.selectbox('Select a colume to Visualize', ['genres', 'language', 'directors','country'], key=1)
        
        submit_button = st.form_submit_button() # Submit form button
        
        fig_column_list = plot_column_list(movies_data_filtered, column_name = arg_column_list, top = arg_slider_column_list)
        st.plotly_chart(fig_column_list, use_container_width=True)

@app.addapp()
def Prime():
    st.markdown("<h1 style='text-align: center; color: black;'>Amazon Prime Video Platform Exploration</h1>", unsafe_allow_html=True)
    hy.info('Movies from Amazon Prime Video')
    movies_data_filtered = filter_by_platforms(df = movies_data, platforms_list = ['Prime'])
    st.markdown("<h2 style='text-align: center; color: black;'>Critics\'s scores for Amazon Prime Video</h2>", unsafe_allow_html=True)
    fig_scores = plot_scores_distribution(movies_data = movies_data)
    st.plotly_chart(fig_scores, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Film\'s Information Exploration</h2>", unsafe_allow_html=True)
    fig_runtime = plot_runtime_distribution(movies_data = movies_data_filtered)
    st.plotly_chart(fig_runtime, use_container_width=True)
    
    with st.form(key = 'column_list_form'):
        hy.info('In order to explore key features behind the film industry, use the Exploration Interactive Tool:')

        st.markdown('### Number of Features')
        arg_slider_column_list = st.slider('Select the number of categories you want to visualize:', 1, 30, 15, step = 1)

        st.markdown('### Feature to Analyze')
        #st.title('Select a Column to Visualize') # Movie's score
        arg_column_list = st.selectbox('Select a colume to Visualize', ['genres', 'language', 'directors','country'], key=1)
        
        submit_button = st.form_submit_button() # Submit form button
        
        fig_column_list = plot_column_list(movies_data_filtered, column_name = arg_column_list, top = arg_slider_column_list)
        st.plotly_chart(fig_column_list, use_container_width=True)


#Run the whole lot, we get navbar, state management and app isolation, all with this tiny amount of work.

app.run()