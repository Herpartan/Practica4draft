# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 19:07:34 2021

@author: herna
"""

import json
import pandas as pd
import requests
from datetime import date, timedelta

def lambda_handler(event, context):
    # Datos iniciales
    url = 'https://api.esios.ree.es/archives/70/download_json?locale=es&date='
    fecha1_dt = date.today() + timedelta(days=1)
    fecha1_str = fecha1_dt.strftime('%Y-%m-%d')

    # Carga el historico
    tabla_precios = 'LLAMADA A LA BBDD----------------------------------------'
    
    # Actualiza el historico
    response = requests.get(url+fecha1_str)
    df = pd.DataFrame(response.json()['PVPC'])
    # Si los datos son antiguos y sale el precio GEN lo cambiamos a PCB
    if (('PCB' in df.columns.tolist()) == False):
        df = df[['Dia', 'Hora', 'GEN']]
        df.rename(columns = {'GEN': 'PCB'}, inplace=True)
    
    # Primero sustituye , por . y luego lo transforma en float
    df['PCB'] = df['PCB'].apply(lambda x: x.replace(',','.'))
    df['PCB'] = df['PCB'].apply(lambda x: float(x))
    # Trata las fechas
    df.Dia = pd.to_datetime(df.Dia, format='%d/%m/%Y')
    df.Hora = [int(h[:2]) for h in df.Hora]
    df.Hora = pd.to_timedelta(df.Hora, unit='h')
    df.Dia = df.Dia + df.Hora
    df.set_index('Dia', drop=True, inplace=True)
    df.drop('Hora', axis=1, inplace=True)
    # Mete en el historico
    tabla_precios = tabla_precios.append(df.loc[:, ['PCB']])
    csv_precios = tabla_precios.copy()
    csv_precios.index = csv_precios.index.strftime('%Y-%m-%d %H:%M')
    print('Historico actualizado')
    
    # Exporta el historico
    'LLAMADA A LA BBDD--------------------------------------------------------'
    print('Historico actualizado y exportado')