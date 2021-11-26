# Streanlit and Hydralit
import hydralit as hy
import streamlit as st

# Data Manipulation modules
import numpy as np
import pandas as pd
import math

# Data Visualization Modules
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Machine Learning
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

# Paths
movies_data_path = '../data/movies_streaming_platforms.csv'
movies_cleaned_data_path = 'C:/Users/luizg/Desktop/Poly/movies_ml_project/website/data/movies_streaming_platforms_cleaned.csv'
user_vector_path = 'C:/Users/luizg/Desktop/Poly/movies_ml_project/website/data/user_vector_baseline_t.csv'
## =======================================
## Preprocessing helper functions
## =======================================

def read_movies_dataframe(path:str):
    '''
    Takes the DataFrame paths' as argment and does basic preprocessing to 
    the movies DataFrame like dropping columns and chaging datatypes.
    '''
    # Reading Movies' DataFrame
    df = pd.read_csv(path, index_col = 'index',
                              names = ['index', 'id', 'title', 'year', 'age', 'imdb', 
                                       'rotten_tomatoes', 'netflix' , 'hulu', 'prime_video', 
                                       'disney', 'type', 'directors', 'genres', 'country', 
                                       'language','runtime'], 
                              skiprows = 1,
                              dtype =  {'netflix': bool, 'hulu': bool,
                                        'prime_video':bool, 'disney':bool})
    
    # Dropping Id and Type Columns
    df = df.drop(['id', 'type'], axis=1)
    return df

def fill_nan_values(df:pd.DataFrame):
    '''
    Fill Null-Value elemens according the columns' necessity. 
    Categorical columns received 'Other' as an additional category, 
    while numerical columns received an empty string.
    '''
    # Fills NaN values with 'Other' 
    df['genres'] = df['genres'].fillna('Other Genres')
    df['language'] = df['language'].fillna('Other Languages')
    df['directors'] = df['directors'].fillna('Other Directors')
    df['country'] = df['country'].fillna('Other Country')
    df['age'] = df['age'].fillna('18+')
    df['rotten_tomatoes'] = df['rotten_tomatoes'].fillna('52/100')
    df['imdb'] = df['imdb'].fillna('6.3/10')
    
    return df

def get_comma_separated_to_list(df:pd.DataFrame):
    '''
    Transforms columns by spliting comma separated elements 
    and transforming into list-based columns.
    '''
    # Initializing an empty list
    df['genres'] = df['genres'].str.split(',', expand = False)
    df['language'] = df['language'].str.split(',', expand = False)
    df['directors'] = df['directors'].str.split(',', expand = False)
    df['country'] = df['country'].str.split(',', expand = False)
    return df

def get_numeric_scores(df:pd.DataFrame):
    '''
    Transform string-based scores into float-based scores.
    '''
    # Erares the number the '/10' or '/100' from string-based columns
    for i in range(len(df)):
        df.loc[i, 'rotten_tomatoes'] = df['rotten_tomatoes'][i][:-4]
        df.loc[i, 'imdb'] = df['imdb'][i][:-3]
        
    # Changes empty strings back to NaN values 
    df['imdb'] = df['imdb'].replace('', np.nan, regex=True)
    df['rotten_tomatoes'] = df['rotten_tomatoes'].replace('', np.nan, regex=True)
    
    # Convert string-columns to float data-type
    df['imdb'] = df['imdb'].astype(float)
    df['rotten_tomatoes'] = df['rotten_tomatoes'].astype(float)
    
    # Changes empty strings back to NaN values 
    df['imdb'] = df['imdb'].fillna(df['imdb'].median())
    df['rotten_tomatoes'] = df['rotten_tomatoes'].fillna(df['rotten_tomatoes'].median())
    
    # Sets numeric scores to integer values 
    df['rotten_tomatoes'] = df['rotten_tomatoes'].astype(int)
    df['imdb'] = df['imdb'].map(lambda x:x*10).astype(int)
    
    return df

def prepare_movies_dataframe(path:str, to_csv:bool = False):
    '''
    Calls all preprocessing funtions to prepare and cleanse the movies DataFrame.
    '''
    movies_data = read_movies_dataframe(path = movies_data_path)
    movies_data = fill_nan_values(df = movies_data)
    #movies_data = get_comma_separated_to_list(df = movies_data)
    movies_data = get_numeric_scores(df = movies_data)
    
    #Creates a csv file on the data directory
    if to_csv:
        movies_data.to_csv('../data/movies_streaming_platforms_cleaned.csv')
        
    #Returns the cleaned dataframe
    return movies_data

def read_cleaned_movies_dataframe(path:str = movies_cleaned_data_path):
    '''
    Takes the cleaned DataFrame paths' as argment and returns the DataFrame
    '''
    # Reading Movies' DataFrame
    movies_data = pd.read_csv(path, index_col = 'index')
    
    # Get comma separated values to lists
    movies_data = get_comma_separated_to_list(movies_data)

    return movies_data

def unique_list_elements(movies_data:pd.DataFrame, column_name:{'genres', 'directors', 'country', 'language'}):
    '''
    Fills the empty lists with unique elements for country, genres, director, and language columns
    '''
    #Initializes empty list
    unique_list = []

    #List comprehension operation to look for unique elements
    [unique_list.append(list_element) for sublist in movies_data[column_name] for list_element in sublist if not(list_element in unique_list)]

    return unique_list

def get_column_dummies_from_list(movies_data:pd.DataFrame, column_name:{'genres', 'directors', 'country', 'language'}, merge_dummies:bool = False):
    '''
    Converts list-based columns to dummy dataframe and joins to the original movies_data
    '''
    #Converts country column-list to pd.Series indexed by the df index
    column_series = pd.Series(movies_data[column_name], index = movies_data.index)

    #apply(Series) converts the series of lists to a dataframe
    #stack() puts everything in one column again (creating a multi-level index)
    #pd.get_dummies( ) creating the dummies
    #sum(level=0) for remerging the different rows that should be one row (by summing up the second level, 
    #only keeping the original level (level=0))
    column_dummies = pd.get_dummies(column_series.apply(pd.Series).stack()).sum(level=0)

    #Inner Join
    if merge_dummies:
        merged_movies_data = pd.merge(movies_data, column_dummies, on = 'index', how= 'inner')
        
    return merged_movies_data

## =======================================
## Visualizations helper functions
## =======================================

def get_color_palette():
    '''
    Standard color palette used for visualization and UI
    '''
    #Standard Color Palette
    color_light_blue = '#0194ED'
    color_dark_blue = '#294D6E'
    color_red = '#FF494E'
    color_gray = '#F0F9FF'
    return color_light_blue, color_dark_blue, color_red, color_gray

def get_color_platforms_palette():
    '''
    Standard color palette used for platforms-related visualization and UI
    '''
    #Standard Color Palette
    color_netflix = '#E50914'
    color_hulu = '#3DBB3D'
    color_prime_video = '#00A8E1'
    color_disney = '#332765'
    return color_netflix, color_hulu, color_prime_video, color_disney

def plot_column_list(movies_data:pd.DataFrame, column_name:{'genres', 'directors', 'country', 'language'}, top:int):
    '''
    Plots a bar chart for list-based columns.
    '''
    #Gets unique list elements
    unique_list = unique_list_elements(movies_data, column_name = column_name)

    #Generates dummy variables
    movies_data = get_column_dummies_from_list(movies_data, column_name = column_name, merge_dummies = True)
    
    #Get color palette
    color_light_blue, color_dark_blue, color_red, color_gray = get_color_palette()

    #Starts an empty list
    elements_series = pd.Series(dtype = 'float64')

    #Creates a list of the aggregated output of the dummy columns
    for unique_element in unique_list:
        elements_aggregation = movies_data[unique_element].sum()
        elements_series[unique_element] = elements_aggregation  
    elements_series = elements_series.sort_values(ascending = False).head(top)

    #Starts Visualizations
    fig_aggregated = go.Figure()
    
    #Adds the data for the bar chart
    fig_aggregated.add_trace(go.Bar(x = elements_series.index,
                                    y = elements_series.values,
                                    marker_color = color_red))
                             
    #Update Y-axis Labels for figure 1
    fig_aggregated.update_yaxes(title_text='Frequency')
    
    #Standard Figure Layout for Data Visualization
    fig_aggregated.update_layout(
        dict(
            height=600, 
            width=1000,
            plot_bgcolor = "#F1F1F3",
            paper_bgcolor = 'white',
            #xaxis_tickformat = '%d %B <br>%Y',
            title = 'Bar Chart of all ' + str(column_name)))
    
    return fig_aggregated

def plot_scores_distribution(movies_data:pd.DataFrame):
    '''
    Plots Histograms for Scores Movies' Distribution
    '''
    #Get color palette
    color_light_blue, color_dark_blue, color_red, color_gray = get_color_palette()
    
    fig_scores = make_subplots(rows=1, cols=2,
                               subplot_titles=('Distribution of IMDB Scores', 'Distribution of Rotten Tomato Scores'),
                               #shared_xaxes=True,
                               vertical_spacing = 0.05)
    
    #Creates Histogram for the distribution of IMDB Scores
    fig_scores.add_trace(go.Histogram(x = movies_data['imdb'],
                                      marker_color = color_red,
                                      opacity = 0.85,
                                      showlegend = False), 
                         row=1, col=1) # Row 1, Column 1
    
    #Creates Histogram for the distribution of Rotten Tomato Scores
    fig_scores.add_trace(go.Histogram(x=movies_data['rotten_tomatoes'],
                                      marker_color= color_dark_blue,
                                      showlegend = False,
                                      opacity=0.85), 
                         row=1, col=2) # Row 1, Column 2
    
    #Update Y-axis Labels for figure 1
    fig_scores.update_yaxes(title_text='Frequency', row=1, col=1)
    
    #Update Y-axis Labels for figure 2
    fig_scores.update_yaxes(title_text='Frequency', row=1, col=2)
    
    #Standard Figure Layout for Data Visualization
    fig_scores.update_layout(
        dict(
            height=600, 
            width=1000,
            plot_bgcolor = "#F1F1F3",
            paper_bgcolor = 'white',
            #xaxis_tickformat = '%d %B <br>%Y',
            title = 'Frequency Distribution of Critics\' scores'))
    
    #Returns Fig Scores
    return fig_scores

def plot_scores_per_platform(movies_data:pd.DataFrame):
    '''
    Plots Box-Plots for Scores Movies' Distribution per platforms.
    '''
    #Get color palette
    color_netflix, color_hulu, color_prime_video, color_disney = get_color_platforms_palette()
    
    fig_scores = make_subplots(rows=2, cols=1,
                               subplot_titles=('Boxplot of Rotten Tomatoes Scores', 'Boxplot of IMDB Scores'),
                               #shared_xaxes=True,
                               vertical_spacing = 0.2)
    
    #Creates Histogram for the distribution of IMDB Scores
    fig_scores.add_trace(go.Box(x = movies_data['rotten_tomatoes'][movies_data['netflix'] == True],
                                marker_color = color_netflix,
                                #opacity = 0.85,
                                showlegend = False,
                                name = 'Netflix'), row=1, col=1) # Row 1, Column 1
    
    fig_scores.add_trace(go.Box(x = movies_data['rotten_tomatoes'][movies_data['disney'] == True],
                                marker_color = color_disney,
                                #opacity = 0.85,
                                showlegend = False,
                                name = 'Disney+'), row=1, col=1) # Row 1, Column 1
    
    fig_scores.add_trace(go.Box(x = movies_data['rotten_tomatoes'][movies_data['hulu'] == True],
                                marker_color = color_hulu,
                                opacity = 0.85,
                                showlegend = False,
                                name = 'Hulu'), row=1, col=1) # Row 1, Column 1

    fig_scores.add_trace(go.Box(x = movies_data['rotten_tomatoes'][movies_data['prime_video'] == True],
                                marker_color = color_prime_video,
                                #opacity = 0.85,
                                showlegend = False,
                                name = 'Prime Video'), row=1, col=1) # Row 1, Column 1
        
    #Creates Histogram for the distribution of Rotten Tomato Scores
    fig_scores.add_trace(go.Box(x = movies_data['imdb'][movies_data['netflix'] == True],
                                marker_color = color_netflix,
                                #opacity = 0.85,
                                showlegend = False,
                                name = 'Netflix'), row=2, col=1) # Row 1, Column 1
    
    fig_scores.add_trace(go.Box(x = movies_data['imdb'][movies_data['disney'] == True],
                                marker_color = color_disney,
                                #opacity = 0.85,
                                showlegend = False,
                                name = 'Disney+'), row=2, col=1) # Row 1, Column 1
    
    fig_scores.add_trace(go.Box(x = movies_data['imdb'][movies_data['hulu'] == True],
                                marker_color = color_hulu,
                                #opacity = 0.85,
                                showlegend = False,
                                name = 'Hulu'), row=2, col=1) # Row 1, Column 1
    
    fig_scores.add_trace(go.Box(x = movies_data['imdb'][movies_data['prime_video'] == True],
                                marker_color = color_prime_video,
                                #opacity = 0.85,
                                showlegend = False,
                                name = 'Prime Video'), row=2, col=1) # Row 1, Column 1
    
    #Update Y-axis Labels for figure 1
    fig_scores.update_xaxes(title_text='Critics\' Score', row=1, col=1)
    
    #Update Y-axis Labels for figure 2
    fig_scores.update_xaxes(title_text='Critics\' Score', row=2, col=1)
    
    #Standard Figure Layout for Data Visualization
    fig_scores.update_layout(
        dict(
            height=700, 
            width=1000,
            plot_bgcolor = "#F1F1F3",
            paper_bgcolor = 'white',
            #xaxis_tickformat = '%d %B <br>%Y',
            title = 'Boxplot of Critics\' scores per Streaming Platform'))
    
    #Returns Fig Scores
    return fig_scores

def plot_runtime_distribution(movies_data:pd.DataFrame):
    '''
    Plots Histograms for Run-time variable
    '''
    #Get color palette
    color_light_blue, color_dark_blue, color_red, color_gray = get_color_palette()
    
    fig_runtime = make_subplots(rows=1, cols=1,
                               #subplot_titles=('Distribution of Run Time'),
                               #shared_xaxes=True,
                               vertical_spacing = 0.05)
    
    #Creates Histogram for the distribution of Run Time
    fig_runtime.add_trace(go.Histogram(x = movies_data['runtime'],
                                      marker_color= color_dark_blue,
                                      opacity=0.85), 
                         row=1, col=1) # Row 1, Column 1
    
    
    #Update Y-axis Labels for figure 3
    fig_runtime.update_yaxes(title_text='Frequency', row=1, col=1)

    
    
    #Standard Figure Layout for Data Visualization
    fig_runtime.update_layout(
        dict(
            height=600, 
            width=1000,
            plot_bgcolor = "#F1F1F3",
            paper_bgcolor = 'white',
            #xaxis_tickformat = '%d %B <br>%Y',
            title = 'Frequency Distribution of Run Time'))
 
    
    #Returns Fig Run Time
    return fig_runtime

def plot_platforms_distribution(movies_data:pd.DataFrame):
    '''
    Plots Histograms for Run-time variable
    '''
    #Get color palette
    color_light_blue, color_dark_blue, color_red, color_gray = get_color_palette()
    
    fig_platforms = make_subplots(rows=1, cols=4,
                               subplot_titles=('Netflix','Hulu','Prime','Disney'),
                               #shared_xaxes=True,
                               vertical_spacing = 0.05)
    
    #Creates Histogram for the distribution of IMDB Scores
    fig_platforms.add_trace(go.Histogram(x = movies_data['netflix'],
                                      marker_color= color_dark_blue,
                                      opacity=0.85),
                         row=1, col=1) # Row 1, Column 1
    
    
    fig_platforms.add_trace(go.Histogram(x = movies_data['hulu'],
                                      marker_color= color_red,
                                      opacity=0.85), row=1, col=2)
    
    fig_platforms.add_trace(go.Histogram(x = movies_data['prime_video'],
                                      marker_color= color_gray,
                                      opacity=0.85), row=1, col=3)
        
    fig_platforms.add_trace(go.Histogram(x = movies_data['disney'],
                                      marker_color= color_light_blue,
                                      opacity=0.85), row=1, col=4)
    
    #Update Y-axis Labels for figure 1
    fig_platforms.update_yaxes(title_text='Frequency', row=1, col=1)
    
    #Update Y-axis Labels for figure 2
    fig_platforms.update_yaxes(title_text='Frequency', row=1, col=2)
    
    #Standard Figure Layout for Data Visualization
    fig_platforms.update_layout(
        dict(
            height=600, 
            width=1000,
            plot_bgcolor = "#F1F1F3",
            paper_bgcolor = 'white',
            #xaxis_tickformat = '%d %B <br>%Y',
            title = 'Frequency Distribution of Platforms'))
    
    #Returns Fig Scores
    return fig_platforms

def plot_age_distribution(movies_data:pd.DataFrame):
    '''
    Plots Histograms 
    '''
    #Get color palette
    color_light_blue, color_dark_blue, color_red, color_gray = get_color_palette()
    
    fig_age = make_subplots(rows=1, cols=1,
                               subplot_titles=('Distribution of Age'),
                               #shared_xaxes=True,
                               vertical_spacing = 0.05)
    
    #Creates Histogram for the distribution of Age
    fig_age.add_trace(go.Histogram(x = movies_data['age'],
                                      marker_color= color_dark_blue,
                                      opacity=0.85), 
                         row=1, col=1) # Row 1, Column 1
    
    
    #Update Y-axis Labels for figure 3
    fig_age.update_yaxes(title_text='Frequency', row=1, col=1)

    
    
    #Standard Figure Layout for Data Visualization
    fig_age.update_layout(
        dict(
            height=600, 
            width=1000,
            plot_bgcolor = "#F1F1F3",
            paper_bgcolor = 'white',
            #xaxis_tickformat = '%d %B <br>%Y',
            title = 'Frequency Distribution of Age'))
 
    
    #Returns Fig Age
    return fig_age

## =======================================
## Machine Learning helper functions
## =======================================

def update_user_vector(df:pd.DataFrame, genres_display:list, age_display:str):
    '''
    Updates user vector values based on the quiz responses 
    '''
    pd.options.mode.chained_assignment = None
    if age_display == 'PG':
        age_display = 'all'

    df['genres']['User'] = genres_display
    df['age']['User'] = age_display
    df[age_display]['User'] = 1
    
    for genre in genres_display:
        df[genre]['User'] = 1
    
    return df

def read_append_user_vector(user_vector_path:str, df:pd.DataFrame):
    '''
    Reads User Vector and Appends to movies_data
    '''
    user_vector = pd.read_csv(user_vector_path, index_col = 'index')
    df = df.drop(columns=['hulu', 'disney', 'netflix', 'prime_video', 'country', 
                          'runtime', 'language', 'directors'])

    df = pd.concat([df, user_vector], join = 'inner')
    df.index = df.index.map(str)
    
    return df

def get_features_column_list(df:pd.DataFrame):
    '''
    Get features from dataframe which will be used to create dummies
    '''
    #Select the features on the basis of which you want to cluster
    remove_list = ['hulu', 'disney', 'netflix', 'prime_video', 'country', 
                   'runtime', 'directors', 'language', 
                   '7+','13+','16+','18+','all', 'title', 'age', 'genres']
    
    #Passes all DataFrames columns to a list
    column_list = df.columns.to_list()
    
    #Remove columns from remove list
    for remove_element in remove_list:
        if remove_element in column_list:
            column_list.remove(remove_element)
        
    #Returns column list which will serve as features
    return column_list

def get_features(df:pd.DataFrame):
    '''
    Get Features to t-SNE
    '''
    column_list = get_features_column_list(df = df)
    features = df[column_list].astype(int)
    return features

def generate_tsne_transfomation(features:pd.DataFrame, df:pd.DataFrame):
    '''
    Applies t-SNE, maps the N-dimensional data to 2D, and returns a t-sne dataframe
    '''
    #Scaling the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features)

    #Using TSNE
    tsne = TSNE(n_components=2)
    transformed_genre = tsne.fit_transform(scaled_data)

    #Kmeans
    cluster = KMeans(n_clusters=23)
    group_pred = cluster.fit_predict(scaled_data)

    
    #Consider adding the genre
    tsne_df = pd.DataFrame(np.column_stack((transformed_genre, group_pred, df['title'], df['genres'], df['age'])),
                                            columns=['X','Y','Group','Title','Genres','Age'])

    return tsne_df

def get_recommendations(df:pd.DataFrame, refresher_counter:int = 0):
    '''
    Calculates the Euclidian distance of the User Vector to other t-SNE points and generates the top 10 recommendations.
    It also allows the user to refresh the recommendations and get the other 10 closest points to the User Vector.
    '''
    tsne_user_x = float(df[df['Title'] == 'User Vector']['X'])
    tsne_user_y = float(df[df['Title'] == 'User Vector']['Y'])
    # df['UserDistance'] = np.sqrt(np.square(df['X'] - tsne_user_x) + np.square(df['Y'] - tsne_user_y))
    df['UserDistance'] = ((df['X'] - tsne_user_x)**2 + (df['Y'] - tsne_user_y)**2)**.5

    df = df.sort_values(by=['UserDistance'])
    if refresher_counter == 0:
        recommendations_df = df[1:11]
    else:
        recommendations_df = df[1+10*refresher_counter:11+10*refresher_counter]
    return recommendations_df

def generate_tsne_visualization(df:pd.DataFrame):
    tsne_user_x = df[df['Title'] == 'User Vector']['X']
    tsne_user_y = df[df['Title'] == 'User Vector']['Y']

    # Build figure
    fig = go.Figure()

    # Add scatter trace with medium sized markers
    fig.add_trace(
        go.Scatter(
            mode = 'markers',
            x = df['X'],
            y = df['Y'],
            customdata = df,
            marker = dict(
                color = df['Group'],
                colorscale='Viridis'
            ),
            hovertemplate =
                '<b>%{customdata[3]} </b><br><br>' +
                'Location: (%{customdata[0]:.2f},%{customdata[1]:.2f})<br>' +
                'Genres: %{customdata[4]}<br>' +
                'Age: %{customdata[5]}<br>' + 
                'Group: %{customdata[2]}<extra></extra>',
            showlegend = False))

    fig.add_trace(
        go.Scatter(
            mode = 'markers',
            marker_symbol = 'circle-open-dot',
            marker_line_width = 5,
            x = tsne_user_x,
            y = tsne_user_y,
            marker = dict(size=[40],
            color = 'red'),
            name = 'User Profile'
        ))

    #Standard Figure Layout for Data Visualization
    fig.update_layout(
        dict(
            height=700, 
            width=1000,
            plot_bgcolor = "#F1F1F3",
            paper_bgcolor = 'white',
            xaxis_title = 'Dimension 1',
            yaxis_title = 'Dimension 2',
            title={'text' : 't-SNE Results and User Vector Location',
                   'x':0.5,
                   'xanchor': 'center'})
    )

    return fig

## =======================================
## Functionalities helper functions
## =======================================

def filter_by_platforms(df:pd.DataFrame, platforms_list:list,hulu_display:bool = None, netflix_display:bool = None, 
                        prime_video_display:bool = None, disney_display:bool = None):
    '''
    Filtering platform functio - Takes user input to which platform to filter or displays everything
    '''
    
    for platform in platforms_list:
        if platform == 'Hulu':
            hulu_display = True
        elif platform == 'Prime':
            prime_video_display = True
        elif platform == 'Disney+':
            disney_display = True
        elif platform == 'Netflix':
            netflix_display = True
        elif not platforms_list:
            display_all = True
    
    #Display All Platforms if list is empty
    if not platforms_list:
        hulu_display = True 
        netflix_display = True 
        prime_video_display = True
        disney_display = True
        
    #Filters Platforms by User input condition
    df = df[(df['hulu'] == hulu_display) | 
            (df['netflix'] == netflix_display) | 
            (df['prime_video'] == prime_video_display) | 
            (df['disney'] == disney_display)]
    
    return df

def filter_by_age(df:pd.DataFrame, display_7:bool = None, display_13:bool = None, 
                        display_16:bool = None, display_18:bool = None, display_pg:bool = None):
    '''
    Filtering by Age limit function - Takes user input to which PG Rating the user can watch
    '''
        
    #Filters Platforms by User input condition
    df = df[(df['7+'] == display_7) | 
            (df['13+'] == display_13) | 
            (df['16+'] == display_16) | 
            (df['18+'] == display_18) |
            (df['all'] == display_pg)]
    
    return df

def get_posters(dataset, rec):
    titles = rec["Title"].to_numpy()
    matches = []
    for id, title in dataset[["id", "title"]].to_numpy():
        if title in titles:
            print("match")
            matches.append([id, title])
    return matches