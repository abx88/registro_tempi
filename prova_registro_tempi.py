#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

if 'stringa_lav' not in st.session_state:
    st.session_state.stringa_lav = ""
    
if 'lista' not in st.session_state:
    st.session_state.lista = []


def on_change_add(text):
    ora = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.lista_lav.append((text, ora))
    
input_lavorazione = st.text_input("stringa lavorazione", key='stringa_lav')

if input_lavorazione:
    on_text_input_change(input_lavorazione)
    
st.dataframe(st.session_state.lista, use_container_width=True) 
