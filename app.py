import streamlit as st
from predict_page import show_page_predict
from explore_page import show_page_explore

page = st.sidebar.selectbox("Predict or Explore" , ("Predict" , "Explore"))
if page == "Predict":
    show_page_predict()
elif page == "Explore":
    show_page_explore()