#create ui page using streamlit for food delivery policy
import streamlit as st
from ragapp.utils.rag_engine import receive_prompt
#to run 
# streamlit run src/ragapp/views/app.py

#design the ui page layout
st.set_page_config(
    page_title="Food Delivery Policy Assistant",    
    page_icon="🍔",
    layout="wide"
)

#set css style for the page
#title color should be radial gradient from red to orange
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f0f0;
    }
    
    .stTitle{
        background: radial-gradient(circle, skyblue, navyblue);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#add title and description
st.markdown('<h1 class="stTitle">Food Delivery Policy Assistant</h1>', unsafe_allow_html=True)
st.write(
    """
    Ask any question related to our Food Delivery Policy, and I'll provide you with the information you need.
    """
)
#add input box for user to ask question
user_question = st.text_input("Enter your question about the Food Delivery Policy:")
if user_question:
    with st.spinner("Fetching answer..."):
        answer = receive_prompt(user_question)
    st.markdown(f"**Answer:** {answer}")
    st.balloons()
