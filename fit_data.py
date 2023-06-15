#!/usr/bin/env python
# coding: utf-8

# # Allgemeine Daten und Erklärung
# Extrahieren, Transformieren und in ein DataFrame Laden

# In[1]:


import pandas as pd
import altair as alt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import glob # Verzeichnis
import os # Verzeichnis 
from tqdm import tqdm # Ladebalken
import streamlit as st

"""
st.set_page_config(page_title="Dashboard",
                   page_icon=":house:",
                   layout="wide"
)
"""
# In[2]:


alt.data_transformers.disable_max_rows()


# ### FIT-Daten (Extrahieren)

# https://developer.garmin.com/fit/file-types

# In[10]:

import fitparse # Fit Format lesen

data_dir         = "00 Data"                                            # Verzeichnis mit den FIT-Dateien
fit_file_pattern = "*.fit"                                              # Muster für die Dateinamen
fit_files        = glob.glob(os.path.join(data_dir, fit_file_pattern))  # Durchsuchen der Verzeichnisse nach FIT-Dateien

fit_data         = []                                                   # Leere Liste zum Sammeln der Daten aus den FIT-Dateien
#file_id_data_list = []   
activity_data_list = []   
session_data_list= []
#lab_data_list = []
record_data_list = []
file_id          = 0  # Initialisiere file_id
progress_bar     = tqdm(total=len(fit_files), desc='Loading FIT Files') # Ladebalken initialisieren


for filepath in fit_files:                                      # Iteration über alle FIT-Dateien
    fitfile = fitparse.FitFile(filepath)                        # Laden der FIT-Datei
    file_id += 1                                                # Inkrementiere file_id bei jeder neuen Datei
    
    # FILE ID
    #for file_id in fitfile.get_messages("file_id"):
    #    file_id_data = {} 
    #    for data_point in file_id:
    #        file_id_data[data_point.name] = data_point.value
    #    file_id_data_list.append(file_id_data)
    
    # ACTIVITY
    for activity in fitfile.get_messages("activity"):
        activity_data = {"file_id": file_id} 
        for data_point in activity:
            if not data_point.name.startswith("unknown_"):      
                activity_data[data_point.name] = data_point.value
        activity_data_list.append(activity_data)
    
    # SESSION
    for session in fitfile.get_messages("session"):             # Iteration über alle Nachrichten vom Typ "session"
        session_data = {"file_id": file_id}                     # Füge die file_id dem session_data Dictionary hinzu
        for data_point in session:
            if data_point.name == "sport":  
    #        if not data_point.name.startswith("unknown_"):      
     #           session_data[data_point.name] = data_point.value
      #          if data_point.units:
       #             session_data[f"{data_point.name}_unit"] = data_point.units
                session_data[data_point.name] = data_point.value
        session_data_list.append(session_data)
        
    # LAB
    #for lab in fitfile.get_messages("lab"):
    #    lab_data = {"file_id": file_id}
    #    for data_point in lab:
    #        if not data_point.name.startswith("unknown_"):      
    #            lab_data[data_point.name] = data_point.value
    #    lab_data_list.append(lab_data)
        
    # RECORD
    for record in fitfile.get_messages("record"):                # Iteration über alle Nachrichten vom Typ "record"
        record_data = {}                                         # Records können mehrere Datenelemente enthalten (z.B. Timestamp, Latitude, Longitude usw.)
        record_data = {"file_id": file_id}                       # Füge die file_id dem record_data Dictionary hinzu
        for data_point in record:
            if not data_point.name.startswith("unknown_"):       # Überprüfen, ob der Datennamen mit "unknown_" beginnt
                record_data[data_point.name] = data_point.value  # das hinzufügen der Datennamen, -wert und -einheiten (falls vorhanden) dem record_data-Dictionary
                if data_point.units:
                    record_data[f"{data_point.name}_unit"] = data_point.units
        record_data_list.append(record_data) # das anhängen der record_data-Dictionary an die data-Liste
        
# Aktualisierung und Schließung der Ladebalken
    progress_bar.update(1)
progress_bar.close()


# Konvertieren Sie die Listen in DataFrames
activity_df = pd.DataFrame(activity_data_list)
session_df  = pd.DataFrame(session_data_list)
#lab_df      = pd.DataFrame(lab_data_list)
record_df   = pd.DataFrame(record_data_list)

fit_df      = pd.merge(session_df, record_df, on='file_id')                  # Verbinden Sie die DataFrames basierend auf der 'file_id'
fit_df      = pd.merge(fit_df, activity_df, on='file_id')


#lat long umberechnen
factor = 180 / 2**31
fit_df['position_lat'] = fit_df['position_lat'].mul(factor)
fit_df['position_long'] = fit_df['position_long'].mul(factor)



#st.dataframe(fit_df)
