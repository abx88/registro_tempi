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

def on_change_add(text):
    ora = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.contatore+=1
    n=st.session_state.contatore
    ingresso = st.session_state.stringa_lav.split(maxsplit=4)
    st.session_state.lista_lav.append((n, ingresso, ora))
    del st.session_state.stringa_lav
    
    
if 'stringa_lav' not in st.session_state:
    st.session_state.stringa_lav = ""
    
if 'lista_lav' not in st.session_state:
    st.session_state.lista_lav = []

if 'contatore' not in st.session_state:
    st.session_state.contatore = 0
    
input_lavorazione = st.text_input("stringa lavorazione", key='stringa_lav')

if input_lavorazione:
    on_change_add(input_lavorazione)
    st.rerun()

log_df = pd.DataFrame(st.session_state.lista_lav, columns=('ID', 'lotto', 'macchina', 'start/stop', 'op', 'data-ora'))

#st.dataframe(st.session_state.lista_lav, use_container_width=True) 
st.dataframe(log_df, use_container_width = True)
