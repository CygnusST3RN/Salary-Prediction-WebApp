import streamlit as st
import numpy as np
import pickle

def load_model():
    #to load the model
    with open('saved_steps.pkl' , 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
regressor = data['model']
le_country = data['le_country']
le_education = data['le_education']

def show_page_predict():
    #Page for the predict interface
    st.title("Software Development Salary Prediction 2023")
    st.write("""### Please select the required options to calculate the estimated salary""") #three hashtags used to make the text h3 text
    
    countries = ("India",
                 "United Kingdom of Great Britain and Northern Ireland" , 
                 "United States",
                 "Germany",
                 "Canada",
                 "France",
                 "Netherlands",
                 "Australia",
                 "Brazil",
                 "Spain",
                 "Sweden",
                 "Italy",
                 "Poland",
                 "Switzerland",
                 "Denmark",
                 "Norway",
                 "Israel",
                 )
    
    education = (
        "Less than Bachelor",
        "Bachelor's Degree",
        "Master's Degree",
        "Post Grad",
    )
    cont = st.selectbox("Country " , countries)
    ed = st.selectbox("Education" , education)
    exp = st.slider("Years of Experience", 0 , 50 , 3)
    ok = st.button("Calculate Salary")
    
    X = np.array([[cont , ed , exp]])
    X[:,0] = le_country.transform(X[:,0])
    X[:,1] = le_education.transform(X[:,1])
    
    X = X.astype(float)
    
    salary = regressor.predict(X)
    st.subheader(f"The estimated salary is ${salary[0]:.2f}")
    