#create ui page using streamlit for food delivery policy
import streamlit as st
from ragapp.utils.rag_engine import receive_prompt
#to run 
# streamlit run src/ragapp/views/app.py

#design the ui page layout
st.set_page_config(
    page_title="Food Delivery Policy Assistant",    
    page_icon="🍔",
    layout="wide",
    
)

#set css style for the page
#title color should be radial gradient from red to orange
#background color for the page multicolor radial gradient from light blue to dark blue
#apply main page css class to the whole page
st.markdown(
    """
    <style>
    /* Entire page */
    .stApp {
        background: linear-gradient(
            135deg,
            #ff9a9e 0%,
            #fad0c4 25%,
            #a8e6a1 50%,
            #dcedc1 75%,
            #ff9a9e 100%
        );
        background-size: cover;
        min-height: 100vh;
    }

    /* Remove default top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Optional: transparent main content */
    [data-testid="stAppViewContainer"] {
        background: transparent;
    }
    
    .stTitle{
        background: radial-gradient(circle, blue, red, orange, yellow, green);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: bold;
        text-align: center;
    }
    .stWelcome{
       color: blue;
       font-size: 48px;
       font-weight: bold;
       text-align: center;
    }
     .stAnswer{
        background: radial-gradient(circle, lightgreen, darkgreen);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
    }
     .stQuestion{
        background: radial-gradient(circle, lightcoral, darkred);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#apply main page css class to the whole page

#add title and description
st.markdown('<h1 class="stTitle">Food Delivery Policy Assistant</h1>', unsafe_allow_html=True)
#Welcome message with h2 tag and center aligned
st.markdown(
    """
    <h2 class="stWelcome">Welcome to the Food Delivery Policy Assistant!</h2>
    """,
    unsafe_allow_html=True
)
#add input box for user to ask question
user_question = st.text_input("Enter your question about the Food Delivery Policy:")
if user_question:
    with st.spinner("Fetching answer..."):
        answer = receive_prompt(user_question)
    st.markdown(f"**Answer:** {answer}")
    st.balloons()
