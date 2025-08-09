import streamlit as st
from chatbot_main import workflow
from langchain_core.messages import HumanMessage


# st.session_state is a dictionary that does not rerun or refresh so now it stores sessions. only resets when when you mannualy refresh the page

CONFIG = {'configurable':{'thread_id':'thread_id'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type here")

if user_input:
    #add message_history first
    st.session_state['message_history'].append({'role':'user','content':user_input})

    # user message
    with st.chat_message('user'):
        st.text(user_input)
    
    response = workflow.invoke({'messages':[HumanMessage(content=user_input)]},config=CONFIG)

    ai_message = response['messages'][-1].content

    # bot message
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)
