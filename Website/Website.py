#when we import hydralit, we automatically get all of Streamlit
import hydralit as hy
import streamlit as st

app = hy.HydraApp(title='Simple Multi-Page App')

@app.addapp(title='🏠')
def Home():
 hy.info('Your are at home')

# Movie Wazar page.
@app.addapp(title='🧙🏼Movie Wizard')
def MovieWizard(): 

 hy.info('In order to recommend you movies, please answer the following questions:')
 st.title('Select platforms:')


 st.multiselect('', ['Disney+', 'Hulu', 'Netflix','Prime']); # Platforms selection.
 #st.select_slider('Pick a size', ['S', 'M', 'L'])
 
 st.title("Select Region: ") # Region Selection
 checkEurope = st.checkbox('Europe')
 checkNAmerica = st.checkbox('North America')
 checkSAmerica = st.checkbox('South America')
 checkMiddleEast = st.checkbox('Middle East')
 checkAsia = st.checkbox('Asia')
 checkSAsia = st.checkbox('South Asia')

 st.title("Do you care about movie's scores?") # Movie's score
 st.radio('Pick one', ['Yes', 'No']);


 st.title("Select age rating: ") # Age rating
 r7 = st.checkbox('+7')
 r13 = st.checkbox('+13')
 r16 = st.checkbox('+16')
 all = st.checkbox('All')


 st.title("Select favorite genres: ") # Select of genres

@app.addapp()
def Explore():
 hy.info('Explore the data')

@app.addapp()
def Statistics():
 hy.info('Lets see some visualizations')


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
