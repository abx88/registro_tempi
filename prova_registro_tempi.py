#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt


def on_change_add(text):
    del st.session_state.stringa_lav
    ora = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.lista.append((text, ora))
    
if 'stringa_lav' not in st.session_state:
    st.session_state.stringa_lav = ""
    
if 'lista' not in st.session_state:
    st.session_state.lista = []

st.dataframe(st.session_state.lista, use_container_width=True) 

input_lavorazione = st.text_input("stringa lavorazione", key='stringa_lav')

if input_lavorazione:
    on_change_add(input_lavorazione)

del st.session_state.stringa_lav
