import streamlit as st
import requests

prediction_url = "http://127.0.0.1:8000/iris/predict/"

def main():
    st.markdown("# Predict flower")
    
    petal_length = st.number_input("petal_length", min_value=4.1, max_value=8, step=.1)
    petal_width = st.number_input("petal_width", min_value=1.9, max_value=4.6, step=.1)
    sepal_length = st.number_input("sepal_length", min_value=0.9, max_value=7, step=.1)
    sepal_width = st.number_input("sepal_width", min_value=0.1, max_value=2.6, step=.1)
    
    payload = {
        "petal_length": petal_length,
        "petal_width": petal_width,
        "sepal_length": sepal_length,
        "sepal_width": sepal_width
    }
    
    button = st.button("Predict flower")
    if button:
        response = requests.post(prediction_url, json=payload)
        st.markdown(response.json())
    
    
if __name__ == "__main__":
    main()