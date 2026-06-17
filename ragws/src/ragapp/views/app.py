#create ui page using streamlit for food delivery policy
import streamlit as st
from ragapp.utils.rag_engine import receive_prompt

#design the ui page layout
st.set_page_config(
    page_title="Food Delivery Policy Assistant",    
    page_icon="🍔",
    layout="wide"
)