import streamlit as st
import base64
import sklearn
import numpy as np
import pickle as pkl
from sklearn.preprocessing import MinMaxScaler

scal=MinMaxScaler()
#Load the saved model
model = pkl.load(open("rf_model.pkl", "rb"))

st.set_page_config(page_title="Passenger Satisfaction App",page_icon="⚕️",layout="centered",initial_sidebar_state="expanded")

def preprocess(distance ,depDelay ,arrDelay ,gender ,cusType ,age ,typetrvl ,wifi ,timeConve ,booking ,food ,board ,seat ,entertain ,onboard ,leg ,bag ,checkin ,inflight ,clean ,cusClass ):   

    if gender == "Male":
        gender = 1
    else:
        gender = 0
    if cusType == "disloyal Customer":
        cusType = 0
    else:
        cusType = 1
    if typetrvl == "Business travel":
        typetrvl = 0
    else:
        typetrvl = 1

    li_class = { "Business": 0, "Eco": 0, "Eco Plus": 0}
    if cusClass in li_class:
        li_class[cusClass] = 1


    user_input=[distance,depDelay,arrDelay,gender,cusType,age,typetrvl,wifi,timeConve ,booking ,food ,board ,seat ,entertain ,onboard ,leg ,bag ,checkin ,inflight ,clean ,li_class["Eco"], li_class["Eco Plus"], li_class["Business"] ]
    user_input=np.array(user_input)
    user_input=user_input.reshape(1,-1)
    user_input=scal.fit_transform(user_input)
    prediction = model.predict(user_input)

    return prediction

    # front end elements of the web page 
html_temp = """ 
    <div style ="background-color:pink;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Healthy Heart App</h1> 
    </div> 
    """
      
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True) 
st.subheader('by Quynh Hoa')
      
# following lines create boxes in which user can enter data required to make prediction
distance=st.number_input('Insert flight distance')
depDelay = st.number_input('Insert Departure Delay in Minutes')
arrDelay = st.number_input('Insert Arrival Delay in Minutes')
gender = st.radio("Select Gender: ", ('Male', 'Female'))
cusType = st.radio("Customer Type?",("Loyal Customer", "disloyal Customer"))
age=st.selectbox ("Age",range(1,121,1))
typetrvl = st.radio("Type of travel?",("Business travel", "Personal Travel"))
wifi = st.select_slider("Inflight wifi service?",options=[1,2, 3, 4,5])
timeConve = st.select_slider("Departure/Arrival time convenient?",options=[1,2, 3, 4,5])
booking = st.select_slider("Ease of Online booking?",options=[1,2, 3, 4,5])
food = st.select_slider("Food and drink?",options=[1,2, 3, 4,5])
board = st.select_slider("Online boarding?",options=[1,2, 3, 4,5])
seat = st.select_slider("Seat comfort?",options=[1,2, 3, 4,5])
entertain= st.select_slider("Inflight entertainment?",options=[1,2, 3, 4,5])
onboard = st.select_slider("On-board service?",options=[1,2, 3, 4,5])
leg = st.select_slider("Leg room service?",options=[1,2, 3, 4,5])
bag = st.select_slider("Baggage handling?",options=[1,2, 3, 4,5])
checkin = st.select_slider("Checkin service?",options=[1,2, 3, 4,5])
inflight = st.select_slider("Inflight service?",options=[1,2, 3, 4,5])
clean = st.select_slider("Cleanlines?",options=[1,2, 3, 4,5])
cusClass = st.selectbox('Customer Class?',("Business", "Eco", "Eco Plus")) 


pred=preprocess(distance ,depDelay ,arrDelay ,gender ,cusType ,age ,typetrvl ,wifi ,timeConve ,booking ,food ,board ,seat ,entertain ,onboard ,leg ,bag ,checkin ,inflight ,clean ,cusClass )


if st.button("Predict"):    
  if pred[0] == 0:
    st.error('neutral or dissatisfied')
    
  else:
    st.success('satisfied')


st.sidebar.info("This web app is helps you to find out whether passenger would be satisfied or not.")
st.sidebar.info("Enter the required fields and click on the 'Predict' button to check answer.")

