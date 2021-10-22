#when we import hydralit, we automatically get all of Streamlit
import hydralit as hy
import streamlit as st

app = hy.HydraApp(title='Simple Multi-Page App')

@app.addapp(title='🏠')
def Home():
 hy.info('Your are at home')

@app.addapp(title='🧙🏼Movie Wizard')
def MovieWizard():
 hy.info('In order to recommend you movies, please answer the following questions:')
 st.multiselect('Select one or more platforms:', ['Disney+', 'Hulu', 'Netflix','Prime']);
 st.select_slider('Pick a size', ['S', 'M', 'L'])
 st.checkbox(('I agree'),('testing'));
 st.radio('Pick one', ['cats', 'dogs']);


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
