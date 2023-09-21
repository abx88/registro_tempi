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
        del st.session_state[key]
        
cancella_stringa = st.button("cancella text box")
if cancella_stringa:
    del st.session_state['stringa_lav']       

if 'stringa_lav' not in st.session_state:
    st.session_state.stringa_lav = ""

if 'contatore' not in st.session_state:
    st.session_state.contatore = 0
    

lista_lavorazione = []

lista_lavorazione = st.session_state

def on_text_input_change(text):
    ora = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.contatore+=1
    n=st.session_state.contatore
    lista_lavorazione.append((n, text, ora))
    lista_lavorazione = st.session_state
 


   
    
input_lavorazione = st.text_input("stringa lavorazione", key='stringa_lav')

if input_lavorazione:
    on_text_input_change(input_lavorazione)
   
    
st.dataframe(st.session_state, use_container_width=True) 
