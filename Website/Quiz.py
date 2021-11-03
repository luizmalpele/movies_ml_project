import streamlit as st
import numpy as np
import hydralit as hy

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
    
    

# Check selection for genre that is selected at least 1 and less than 4
while len(genres) < 20: 
    if len(genres) < 1:
    st.warning("Select at least one option")
    if len(genres) > 3:
    st.warning("Select less than 3 options")
    break



    

