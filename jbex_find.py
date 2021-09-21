"""
Diese App erlaubt das Browsen von Jahrbüchern

Kontakt: lukas.calmbach@bs.ch
"""
from enum import Enum
import io
import pandas as pd
import streamlit as st
from datetime import datetime, date
from st_aggrid import GridUpdateMode
from const import *

import tools

CURRENT_YEAR = date.today().year
class App():
    def __init__(self, metadata):
        self.record = {}
        self.metadata_df = metadata
        self.metadata_filtered = self.metadata_df

    
    def get_metadata(self):
        sql = qry['metadata']
        df, ok, err_msg = db.get_recordset(self.conn, sql)
        return df


    def get_status_list(self):
        query = qry['lookup_code'].format(80) #category status
        result  = pd.DataFrame.from_dict({'id': [-1], 'value': ['<alle>']}, orient='columns')
        df, ok, err_msg = db.get_recordset(self.conn, query)
        if ok:
            result = result.append(df.set_index('id'))
        return result

    
    def get_filtered_tabs(self, filter):
        if filter['titel'] > '':
            self.metadata_filtered = self.metadata_filtered[self.metadata_filtered['Titel'].str.contains(pat = filter['titel'])]
        if filter['themenbereich'] != []:
            self.metadata_filtered = self.metadata_filtered[self.metadata_filtered['Themenbereich'].isin(filter['themenbereich'])]
                    
    def get_tabelle(self):
        def get_filter_description():
            text = """Sie haben noch keinen Filter eingegegeben, die untenstehende Liste enthält alle verfügbaren Jahrbuch-Tabellen. Verwenden sie obige Felder um die Auswahl 
            auf einen Themenbereich einzugrenzen oder suchen sie nach einem Ausdruck im Titel.
            """

            if f['themenbereich'] !=[]:
                liste_themenbereiche = ",".join(f['themenbereich'])
            if (f['titel'] > '') & (f['themenbereich'] == []):
                text = f"""Die untenstehende Liste enthält alle Tabellen welche den Ausdruck '{f['titel']}' im Titel enthalten. """
            elif (f['titel'] == '') & (f['themenbereich'] !=[]):
                 text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche `{liste_themenbereiche}`. """
            elif (f['titel'] > '') & (f['themenbereich'] !=[]):
                text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche `{liste_themenbereiche}`, welche auch den Ausdruck `{f['titel']}` im Titel enthalten."""
            
            text += ' Beim Selektieren eines Eintrags in der Liste werden alle Jahrbücher, welche die ausgewählte Tabelle enthalten, als interaktive Links angezeigt.'
            return text
        f = {}
        f['titel'] = st.text_input("🔎 Titel der Tabelle enthält:")
        f['themenbereich'] = st.multiselect('🔎 Themenbereich:',  options=THEMENBEREICHE)
        self.get_filtered_tabs(f)
        st.markdown(get_filter_description())
        st.markdown('### Tabellen')
        return tools.show_table(self.metadata_filtered, GridUpdateMode.SELECTION_CHANGED, 300)
        

    def show_jahrbuecher(self, tabelle):
        st.markdown('### Jahrbücher')
        text = f"Die Tabelle '{tabelle['Titel']}' wird in folgenden Jahrbüchern geführt, klicken sie auf den Link um die PDF-Datei zu öffnen:"
        st.markdown(text)
        jb_von = int(tabelle['JB-Start'])
        jb_bis = CURRENT_YEAR -1 if tabelle['JB-Ende'] == 'nan' else int(tabelle['JB-Ende'])
        liste = ''
        for jahr in range(jb_von, jb_bis + 1):
            url = f"{URL_BASE}{jahr}.pdf"
            name = f'Statistisches Jahrbuch des Kantons Basel-Stadt {jahr}'
            liste += f"- [{name}]({url}) \n"
        st.markdown(liste)

    def show_menu(self):
        selected = self.get_tabelle()
        if len(selected) > 0:
           self.show_jahrbuecher(selected[0])
    
