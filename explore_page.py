import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def shortenCategories(category , limit):
    category_map = {}
    for i in range(len(category)):
        if(category.values[i] >= limit):
            category_map[category.index[i]] = category.index[i]
        else:
            category_map[category.index[i]] = 'others'
    return category_map

def cleanExperience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)
    
def cleanEducation(x):
    if 'Bachelor' in x:
        return "Bachelor's Degree"
    if 'Master' in x:
        return "Master's Degree"
    if "Professional" in x or "Doctoral" in x:
        return "Post Grad"
    return "Less than Bachelor"

@st.cache_data #A decorator to avoid all these prior steps again and again while loading the page
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[['Country' , 'EdLevel', 'YearsCodePro' , 'Employment' , 'ConvertedCompYearly']] #to make it simple and keep the important attributes
    df = df.rename({'ConvertedCompYearly' : 'Salary'} , axis = 1)
    df['Country'] = df['Country'].replace({'United States of America' : 'United States'})
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]        #To select only the full time developers
    df = df.drop("Employment", axis=1) 
    country_map = shortenCategories(df['Country'].value_counts() , 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] >= 10000]
    df = df[df['Salary'] <= 0.5e6]
    df = df[df['Country'] != 'others']
    
    df["YearsCodePro"] = df["YearsCodePro"].apply(cleanExperience) 
    df['EdLevel'] = df["EdLevel"].apply(cleanEducation)
    
    return df

df = load_data()

def show_page_explore():
    st.title("Explore Software Engineer Salaries")
    st.write("""### Stack Overflow Developer Survey 2023""")
    
    data = df['Country'].value_counts()
    
    fig1 , ax1 = plt.subplots()
    
    ax1.pie(data , labels = data.index , autopct="%1.1f%%" , shadow=True , startangle=90)
    #ax1.axis("equal")
    
    st.write("""### Number of data from different countries""")
    st.pyplot(fig1)
    
    st.write("""### Country-wise Mean Salary""")
    
    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)
    
    st.write("""### Experience-wise Mean Salary""")
    
    data = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)
    
    
    
