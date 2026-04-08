import pandas as pd
import random
from datetime import datetime

# Extraire les informations capteurs (les min/max)
# à partir du fichier telemtry
# pour pouvoir générer des valeurs aléatoires réalistes
def extract_sensors_min_max(dfmeta,dftele,machlist):
    
    list_min_temp = []
    list_max_temp = []
    list_min_vibr = []
    list_max_vibr = []
    list_min_pres = []
    list_max_pres = []
    list_min_pwr = []
    list_max_pwr = []
    
    for machine in machlist:
        dftemp = dftele[dftele['machine_id']==machine]
        list_min_temp.append(dftemp['temperature_celsius'].min())        
        list_max_temp.append(dftemp['temperature_celsius'].max())
        list_min_vibr.append(dftemp['vibration_mm_s'].min())
        list_max_vibr.append(dftemp['vibration_mm_s'].max())
        list_min_pres.append(dftemp['pressure_bar'].min())
        list_max_pres.append(dftemp['pressure_bar'].max())
        list_min_pwr.append(dftemp['power_consumption_kw'].min())
        list_max_pwr.append(dftemp['power_consumption_kw'].max())
        
    dfmeta['min_temp'] = list_min_temp
    dfmeta['max_temp'] = list_max_temp
    dfmeta['min_vibr'] = list_min_vibr
    dfmeta['max_vibr'] = list_max_vibr
    dfmeta['min_pres'] = list_min_pres
    dfmeta['max_pres'] = list_max_pres
    dfmeta['min_pwr'] = list_min_pwr
    dfmeta['max_pwr'] = list_max_pwr

    dfmeta=dfmeta.drop(columns=['index'])
    
    return dfmeta

# génération de valeurs capteurs aléatoires en utilisant
# les min/max récoltées 
def generate_sensors_readings(dfmeta):
    dict_readings = {}
    machines_dict = dfmeta.to_dict("records")
    for machine in machines_dict:
        temp_value = round(random.uniform(machine['min_temp'], machine['max_temp']), 2)
        temp24_value = round(random.uniform(machine['min_temp']+2, machine['max_temp']-2), 2)
        temp48_value = round(random.uniform(machine['min_temp']+2, machine['max_temp']-2), 2)
        vibr_value = round(random.uniform(machine['min_vibr'], machine['max_vibr']), 2)
        vibr24_value = round(random.uniform(machine['min_vibr'], machine['max_vibr']), 2)
        vibr48_value = round(random.uniform(machine['min_vibr'], machine['max_vibr']), 2)
        pres_value = round(random.uniform(machine['min_pres'], machine['max_pres']), 2)
        pwr_value = round(random.uniform(machine['min_pwr'], machine['max_pwr']), 2)
        delta = datetime.now() - datetime.strptime(machine['install_date'], "%Y-%m-%d")
        age = int(abs(delta.days)/365)

        reading = {'machine_id':machine['machine_id'],
                   'temperature_celsius':temp_value,
                   'temperature_celsius_mean_24h':temp24_value,
                   'temperature_celsius_mean_48h':temp48_value,                       
                   'vibration_mm_s':vibr_value,
                   'vibration_mm_s_mean_24h': vibr24_value,
                   'vibration_mm_s_mean_48h': vibr48_value,
                   'pressure_bar':pres_value,
                   'power_consumption_kw':pwr_value,
                   'age':age
                  }
        
        dict_readings[machine['machine_id']] = reading

    return dict_readings

