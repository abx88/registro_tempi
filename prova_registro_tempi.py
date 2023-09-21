#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt



reset_session_state = st.button("reset session state")
if reset_session_state:
    for key in st.session_state.keys():
        #del st.session_state[key]
        
 

if 'stringa_lav' not in st.session_state:
    st.session_state.stringa_lav = ""
    
if 'lista_lav' not in st.session_state:
    st.session_state.lista_lav = []

if 'counter' not in st.session_state:
    st.session_state.counter = 0

#st.session_state.lista_lav = []
    
def on_text_input_change(text):
    ora = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id = st.session_state.counter +=1
    st.session_state.lista_lav.append((id,text, ora))
   #del st.session_state['stringa_lav']
 
   
    
input_lavorazione = st.text_input("stringa lavorazione", key='stringa_lav')
#del st.session_state['stringa_lav']

if input_lavorazione:
    on_text_input_change(input_lavorazione)
    
    
st.dataframe(st.session_state.lista_lav, use_container_width=True) 

#del st.session_state.stringa_lav   
#st.dataframe(st.session_state, use_container_width=True) 

#st.write(st.session_state.stringa_lav)
#st.write(st.session_state.lista)

#del st.session_state['stringa_lav']
#st.write(lista_lavorazioni)



