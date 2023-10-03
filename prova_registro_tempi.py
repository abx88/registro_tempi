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
import os

st.set_page_config(
    page_title="AnalisiTempi",
    layout="wide")
st.header("Analisi tempi lavorazione cuccanza")

expander_registro = st.expander("log_tempi_registrati")

nome_file = "C:\\Users\\Andrea\\Documents\\PythonScripts\\BackupTempi.txt"
registro_tempi = pd.read_csv(nome_file, delimiter='\,')
registro_tempi_mod = expander_registro.data_editor(registro_tempi, use_container_width = True)
registro_tempi_mod['ora'] = pd.to_datetime(registro_tempi_mod['ora'], format='%H:%M:%S')

# Funzioni per esportare il DataFrame come file di testo
def converti_df(df):
    return df.to_csv().encode('utf-8')

def converti_df_senza_int(df):
    return df.to_csv(index=False, header=False, sep=';').encode('utf-8')


def export_to_text(df, destination_folder, file_name):
    # Esporta il DataFrame come un file CSV (Comma-Separated Values)
    csv_file_path = os.path.join(destination_folder, file_name + '.csv')
    df.to_csv(csv_file_path, sep=',', index=False)  # Utilizza il separatore '\t' per il file di testo
    txt_file_path = os.path.join(destination_folder, file_name + '.txt')
    os.rename(csv_file_path, txt_file_path)

    return txt_file_path

destination_folder = "C:\\Users\\Andrea\\Documents\\PythonScripts\\"
if st.button("Esporta DataFrame"):
    file_name = "BackupTempi_agg"
    txt_file_path = export_to_text(registro_tempi_mod, destination_folder, file_name)
    
#tabella controllo ultimo lotto per operatore/macchinario
pivot_log = pd.pivot_table(registro_tempi_mod,  values=["lotto_ora"], index="macchina", columns="op", aggfunc='last')

#tabella conteggio inizio/fine per lotto
controllo_lotti = pd.pivot_table(registro_tempi_mod,  values="ora", 
                                 index=["data",  "lotto"], columns="inizio_fine", aggfunc='count')
controllo_lotti = controllo_lotti.sort_index(axis=1, ascending=False)

#track lotti inizio - fine
track_lotti = pd.pivot_table(registro_tempi_mod,  values="ora", 
                             index=[ "data","op", "macchina","lotto","ID"], columns="inizio_fine", aggfunc='last')
track_lotti = track_lotti.sort_index(axis=1, ascending=False)

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


df_calcoli['tempo'] = (df_calcoli['F'] - df_calcoli['I']).dt.total_seconds() 
   

st.subheader("riepilogo tempi per lotto")
st.dataframe(df_calcoli, use_container_width = True)

# Dizionario di mapping
mapping_M = {'GR': '<M-GRAZIANO', 
           'TO': '<M-TOVAGLIERI', 
           'ME': '<M-MERLI',
           'WI': '<M-WISCONSIN'}

mapping_OP = {'DD': '<D-DANI', 
           'CS': '<D-CONTINI', 
           'MO': '<D-MORI',
           'CA': '<D-CELA'}

df_importazioni = df_calcoli
df_importazioni['macchina_imp'] = df_importazioni['macchina'].map(mapping_M)
df_importazioni['op_imp'] = df_importazioni['op'].map(mapping_OP)
df_importazioni['tempo'] = (df_importazioni['F'] - df_importazioni['I']).dt.total_seconds() 

df_importazioni_macchina = df_importazioni.drop(columns = ['ID','macchina','op','op_imp','data','I', 'F'])
df_importazioni_macchina = df_importazioni_macchina[['lotto','macchina_imp','tempo']]
df_importazioni_macchina['lotto'] = df_importazioni_macchina['lotto'].apply(lambda x: x.strip())
df_importazioni_macchina['macchina_imp'] = df_importazioni_macchina['macchina_imp'].apply(lambda x: x.strip())


df_importazioni_operatore = df_importazioni.drop(columns = ['ID','macchina','op','macchina_imp','data','I', 'F'])
df_importazioni_operatore = df_importazioni_operatore[['lotto','op_imp','tempo']]
df_importazioni_operatore['lotto'] = df_importazioni_operatore['lotto'].apply(lambda x: x.strip())
df_importazioni_operatore['macchina_imp'] = df_importazioni_operatore['op_imp'].apply(lambda x: x.strip())
#df_importazioni_totale = pd.concat([df_importazioni_macchina, df_importazioni_operatore], ignore_index=True)

col1, col2 = st.columns(2)

col1.subheader("export macchinari")
col1.dataframe(df_importazioni_macchina, use_container_width = True)
csv = converti_df_senza_int(df_importazioni_macchina)
scarica_file_macchinari = col1.download_button("download riepilogo macchine", data=csv, file_name="export_macchine.csv", mime = 'text/csv')

col2.subheader("export operatore")
col2.dataframe(df_importazioni_operatore, use_container_width = True)
csv = converti_df_senza_int(df_importazioni_operatore)
scarica_file_operatore = col2.download_button("download riepilogo op", data=csv, file_name="export_op.csv", mime = 'text/csv')
