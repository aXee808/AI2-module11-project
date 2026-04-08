import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import requests
from sim.simulator import extract_sensors_min_max,generate_sensors_readings

API_URL = "http://127.0.0.1:8000/predict"

# chargement des fichiers telemetry & metadata
# activation du cache pour limiter le temps de chargement à chaque refresh
@st.cache_data
def load_data():
    dftele = pd.read_csv("../machines_telemetry.csv")
    dfmeta = pd.read_csv("../machines_metadata.csv")
    machines_data_list = list(dftele.machine_id.unique())
    dfmeta = dfmeta[dfmeta['machine_id'].isin(machines_data_list)].reset_index()
    dfmeta = extract_sensors_min_max(dfmeta,dftele,machines_data_list)
    return dfmeta

# fonction pour interroger l'api (pour une machine)
def post_api(data):
    url = API_URL
    response = requests.post(url,json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# fonction pour interroger l'api pour l'ensemble des machines 
def predict_loop(timestamp):
    last_readings = readings_db[str(timestamp)]
    alerts = {}
    for machine in last_readings.items():
        prediction = post_api(machine[1])
        if prediction['prediction'] == 1:
            alerts[machine[0]] = 1
    return alerts

# récupération des 10 dernieres mesures (pour l'affichage des line chart)
# on retourne un dataframe
def last_ten_readings(machine_id):
    i = 0
    t_list = []
    temp_list = []
    vib_list = []
    pres_list = []
    pwr_list = []
    for cle,valeur in sorted(readings_db.items(),reverse=True):
        i += 1
        if i<11:
            for c,v in valeur.items():
                if v['machine_id']==machine_id:
                    t_list.append(cle)
                    temp_list.append(v['temperature_celsius'])
                    vib_list.append(v['vibration_mm_s'])
                    pres_list.append(v['pressure_bar'])
                    pwr_list.append(v['power_consumption_kw'])
    
    df = pd.DataFrame({'timestamp':t_list,'temperature':temp_list,'vibration':vib_list,'pressure':pres_list,"power consumption":pwr_list})
    return df

# variables session (listes des mesures collectées, et des alertes du modèle ML)
if "readings_db" not in st.session_state:
    readings_db = {}
    st.session_state["readings_db"] = readings_db
else:
    readings_db = st.session_state["readings_db"]


if "alerts_db" not in st.session_state:
    alerts_db = {}
    st.session_state["alerts_db"] = alerts_db
else:
    alerts_db = st.session_state["alerts_db"]

# chargement des données
dfmeta = load_data()
# date heure lors du chargement de la page
timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
# récupération d'une salve de mesures capteurs aléatoires
readings_db[str(timestamp)] = generate_sensors_readings(dfmeta)
st.session_state["readings_db"] = readings_db

# Config page
st.set_page_config(page_title="Dashboard - Supervision Machines",
                   page_icon="🏭",
                   layout="wide")
st.title("🏭 Supervision Machines")
st.write(f"🗓️🕝 date et heure : {timestamp}")

# bouton refresh
if st.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()

# affichage indicateurs nombre de machines
st.write("### PARC MACHINES")
dfkpi = dfmeta.groupby(['machine_type']).agg({'machine_id': 'count'}).to_dict()['machine_id']
pcol1, pcol2, pcol3, pcol4 = st.columns(4)
pcol1.metric("Nb machines CNC",f"{dfkpi['CNC']}","",border=True)
pcol2.metric("Nb machines PRESS",f"{dfkpi['PRESS']}","",border=True)
pcol3.metric("Nb machines ASSEMBLY",f"{dfkpi['ASSEMBLY']}","",border=True)
pcol4.metric("Nb machines ROBOT",f"{dfkpi['ROBOT']}","",border=True)

# affichage des mesures
st.write("### SUIVI ACTIVITE CAPTEURS")
with st.expander("Dernières mesures capteurs"):
    st.write(readings_db[str(timestamp)])

# affichage des alertes (après appel de l'API)
st.write("### ALERTES PREDICTIVES")
alerts = predict_loop(timestamp)
alerts_db[str(timestamp)] = alerts
st.session_state["alerts_db"] = alerts_db

if len(alerts) == 0:
    st.info("Aucunes alertes sur les dernières mesures")
for alert in alerts.items():
    st.error(f"ALERTE PANNE machine {alert[0]}")

# affichage du détail pour une machine (line chart évolution valeurs capteurs)
st.write("### DETAIL Machine")
machine = st.selectbox("Identifiant machine",dfmeta['machine_id'].to_list())
dcol1, dcol2, dcol3, dcol4 = st.columns(4)
dfdetail = last_ten_readings(machine)
dfdetail.set_index('timestamp',inplace=True)
dcol1.write("Temperature")
dcol1.line_chart(data=dfdetail[['temperature']],color=["#FF0000"],
                          x_label="Jour & heure",
                          y_label="°C")

dcol2.write("Vibration")
dcol2.line_chart(data=dfdetail[['vibration']],color=["#0FF0F0"],
                          x_label="Jour & heure",
                          y_label="mm/s")

dcol3.write("Pression")
dcol3.line_chart(data=dfdetail[['pressure']],color=["#0000FF"],
                          x_label="Jour & heure",
                          y_label="bar")

dcol4.write("Power Consumption")
dcol4.line_chart(data=dfdetail[['power consumption']],color=["#00FF00"],
                          x_label="Jour & heure",
                          y_label="kW")
