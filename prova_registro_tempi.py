#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

st.set_page_config(
    page_title="RegistroTempi",
    layout="wide")

st.header("Registro Tempi lavorazione")

reset_session_state = st.button("reset session state")
if reset_session_state:
    for key in st.session_state.keys():
        del st.session_state[key]

def on_change_add(text):
    st.session_state.contatore+=1
    n=st.session_state.contatore
    ingresso = st.session_state.stringa_lav.split()
    n_split = len(ingresso)
    if n_split == 4:
        ingresso_0 = ingresso[0]
        ingresso_1 = ingresso[1]
        ingresso_2 = ingresso[2]
        ingresso_3 = ingresso[3]
        ingresso_4 = "no_errori"
    if n_split >4:
        ingresso_0 = ""
        ingresso_1 = ""
        ingresso_2 = ""
        ingresso_3 = ""
        ingresso_4 = str(ingresso)
    if n_split <4:
        ingresso_0 = ""
        ingresso_1 = ""
        ingresso_2 = ""
        ingresso_3 = ""
        ingresso_4 = str(ingresso)
    data_ora = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_ora_split = data_ora.split(" ")
    ora = str(data_ora_split[1])
    data = str(data_ora_split[0])
    lotto_ora = str(ingresso_0)+" "+ora + " " + str(ingresso_2)
    st.session_state.lista_lav.append((n, ingresso_0, ingresso_1, ingresso_2, ingresso_3, ingresso_4, ora, data, lotto_ora))
    #procedura backup stringa\
    nome_file = "C:\\Users\\Andrea\\Documents\\PythonScripts\\BackupTempi.txt"
    with open(nome_file, "a") as file:
        file.write(str(n) + " "
                   + str(ingresso_0)+ "," 
                   + str(ingresso_1)+ "," 
                   + str(ingresso_2)+ "," 
                   + str(ingresso_3)+ "," 
                   + str(ingresso_4) + ","
                   + ora +","+ data + "\n")
        #cancellazione text input
    del st.session_state.stringa_lav
    

def converti_df(df):
    return df.to_csv().encode('utf-8')

      
    
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

log_df = pd.DataFrame(st.session_state.lista_lav, columns=('ID', 'lotto', 'macchina', 'inizio_fine', 
                                                           'op', 'errore', 'ora',  'data', 'lotto_ora'))

pivot_log = pd.pivot_table(log_df,  values=["lotto_ora"], index="macchina", columns="op", aggfunc='last')
controllo_lotti = pd.pivot_table(log_df,  values="ora", index=["data",  "lotto"], columns="inizio_fine", aggfunc='count')
controllo_lotti = controllo_lotti.sort_index(axis=1, ascending=False)
track_lotti = pd.pivot_table(log_df,  values="ora", index=[ "data","op", "macchina","lotto","ID"], columns="inizio_fine", aggfunc='last')
track_lotti = track_lotti.sort_index(axis=1, ascending=False)


#csv = converti_df(log_df)
#scarica_file = st.download_button("download", data=csv, file_name="registro_tempi.csv", mime = 'text/csv')

st.subheader("ultimo lotto in lavorazione per macchina/operatore con ora inserimento operazione")
st.dataframe(pivot_log, use_container_width = True)


col1, col2 = st.columns(2)
col1.subheader("lotti in lavorazione inizio, fine (elenco)")
col1.dataframe(track_lotti, use_container_width = True)
csv = converti_df(track_lotti)
scarica_file = st.download_button("download tracking", data=csv, file_name="track_tempi.csv", mime = 'text/csv')
col2.subheader("conteggio q. inizio/fine per lotti")
col2.dataframe(controllo_lotti, use_container_width = True)

df_calcoli= track_lotti.reset_index()
df_calcoli = df_calcoli.ffill(axis=0, inplace=False, limit=1)
selezionarighe = st.toggle("seleziona righe pari")
if selezionarighe == True:
    df_calcoli = df_calcoli[df_calcoli.index % 2 == 0]
else:
    df_calcoli = df_calcoli[df_calcoli.index % 2 != 0]
#df_calcoli['I'] = pd.to_datetime(df_calcoli['I'], format='%H:%M')
#df_calcoli['F'] = pd.to_datetime(df_calcoli.F, format='%H:%M:%S')
#df_calcoli['durata_op']=df_calcoli['F']-df_calcoli['I']    


st.subheader("riepilogo tempi per lotto")
csv = converti_df(df_calcoli)
scarica_file = st.download_button("download riepilogo", data=csv, file_name="registro_tempi.csv", mime = 'text/csv')
st.dataframe(df_calcoli, use_container_width = True)

#st.dataframe(log_df, use_container_width = True)

