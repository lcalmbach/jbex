"""
Diese App erlaubt die Suche nach Jahrbüchern ab 2021, welche als pdf-Dateien hinterlegt sind.
"""
import io
import pandas as pd
import streamlit as st

from const import *
import jbex_find


__author__ = 'Lukas Calmbach'
__version__ = '0.0.8'
version_date = '2021-09-28'
my_name = 'Jahrbuch Explorer'
my_name_short = 'JBEx'


def get_app_info():
    """
    Zeigt die Applikations-Infos verwendeter Datenbankserver etc. an.
    """

    text = f"""
    <style>
        #appinfo {{
        font-size: 11px;
        background-color: lightblue;
        padding-top: 10px;
        padding-right: 10px;
        padding-bottom: 10px;
        padding-left: 10px;
        border-radius: 10px;
    }}
    </style>
    <div id ="appinfo">
    App: {my_name}<br>
    App-Version: {__version__} ({version_date})<br>
    Implementierung App: Statistisches Amt Basel-Stadt<br>
    Kontakt: <a href="mailto:nathalie.grillon@bs.ch">Nathalie Grillon</a><br>
    </div>
    """
    return text

@st.cache 
def get_data():
    metadata = pd.read_csv(TABELLEN_FILE, sep='\t')
    return metadata

def main():
    st.set_page_config(page_title=my_name_short, page_icon='./images/favicon.png', layout='wide', initial_sidebar_state='auto') 
    st.markdown(f"### 📚 {my_name} v{__version__}""", unsafe_allow_html=True)
    metadata = get_data()
    app = jbex_find.App(metadata)
    app.show_menu()
    text = get_app_info()
    st.markdown(text, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
