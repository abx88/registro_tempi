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
    st.session_state.contatore+=1
    n=st.session_state.contatore
    ingresso = st.session_state.stringa_lav.split(maxsplit=4)
    ingresso_0 = ingresso[0]
    ingresso_1 = ingresso[1]
    ingresso_2 = ingresso[2]
    ingresso_3 = ingresso[3]
    data_ora = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_ora_split = data_ora.split(" ")
    ora = str(data_ora_split[1])
    data = str(data_ora_split[0])
    st.session_state.lista_lav.append((n, ingresso_0, ingresso_1, ingresso_2, ingresso_3, ora, data))
    with open('registro_tempi.txt', 'w') as file:
        file.write(st.session_state.stringa_lav)
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

log_df = pd.DataFrame(st.session_state.lista_lav, columns=('ID', 'lotto', 'macchina', 'inizio/fine', 'op', 'ora', 'data'))

#st.dataframe(st.session_state.lista_lav, use_container_width=True) 
st.dataframe(log_df, use_container_width = True)
