#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 13:05:10 2023

Estratificacion de la poblacion beneficiada

@author: claudia
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


df=pd.read_excel (r'beneficiarios_clean.xlsx')
df.to_csv (r'population_data.csv', index = None, header=True)

#exploring the popultion
benef = df.drop(['N°','Fecha', 'Nombres', 'Apellidos','CI', 'hora_dormir'], axis=1)
desc=benef.describe()
desc_obj= benef.describe(include=['object'])

#selecting useful variables
benef_clean = benef.drop(['sexo_cabeza','edad_cabeza','ocupacion','hijos_0_5','hijos_5_17','adultos_17_59','adultos_mas_60','agri_gan','trab_hogar_agr_gan','sin_actividad','hijos_en_escuela','miembros','apoyo_eco','habitaciones','migracion_temporal','Periodo de migracion','panel_solar','iluminacion','gasto_mens_iluminacion','horario_imp','equipos','cocina','gasto_comb','agua','freq_agua_sem'], axis=1)
benef_clean.loc[df['ingreso_mensual'] <= 100, 'ingreso_mensual'] = 'A'
benef_clean.loc[(df['ingreso_mensual']<=250) & (df['ingreso_mensual']>100) , 'ingreso_mensual'] = 'B'
benef_clean.loc[df['ingreso_mensual'] > 250, 'ingreso_mensual'] = 'C'


def __smpl_size(population, size):
    '''
    Sampling size will be calculated using Cochran adjusted sampling formula:
        cochran_n = (Z**2 * p * q) /e**2
        where:
            - Z is the z-value. In this case we use 1.96 representing 95%
            - p is the estimated proportion of the population which has an
                attribute. In this case we use 0.5
            - q is 1-p
            - e is the margin of error
        This formula is adjusted as follows:
        adjusted_cochran = cochran_n / 1+((cochran_n -1)/N)
        where:
            - cochran_n = result of the previous formula
            - N is the population size

    '''
    if size is None:
        cochran_n = round(((1.96)**2 * 0.5 * 0.5)/ 0.05**2)
        n = round(cochran_n/(1+((cochran_n -1) /population)))
    elif size >= 0 and size < 1:
        n = round(population * size)
    elif size < 0:
        raise ValueError('Parameter "size" must be an integer or a proportion between 0 and 0.99.')
    elif size >= 1:
        n = size
    return n


def stratified_sample_report(df, strata, size=None):
    population = len(df)
    size = __smpl_size(population, size)
    tmp = benef_clean[strata]
    tmp['size'] = 1
    tmp_grpd = tmp.groupby(strata).count().reset_index()
    tmp_grpd['samp_size'] = round(size/population * tmp_grpd['size']).astype(int)
    return tmp_grpd

def stratified_sample(df, strata, size=None, seed=None, keep_index= True):
    population = len(df)
    size = __smpl_size(population, size)
    tmp = df[strata]
    tmp['size'] = 1
    tmp_grpd = tmp.groupby(strata).count().reset_index()
    tmp_grpd['samp_size'] = round(size/population * tmp_grpd['size']).astype(int)

    # controlling variable to create the dataframe or append to it
    first = True 
    for i in range(len(tmp_grpd)):
        # query generator for each iteration
        qry=''
        for s in range(len(strata)):
            stratum = strata[s]
            value = tmp_grpd.iloc[i][stratum]
            n = tmp_grpd.iloc[i]['samp_size']

            if type(value) == str:
                value = "'" + str(value) + "'"
            
            if s != len(strata)-1:
                qry = qry + stratum + ' == ' + str(value) +' & '
            else:
                qry = qry + stratum + ' == ' + str(value)
        
        # final dataframe
        if first:
            stratified_df = df.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
            first = False
        else:
            tmp_df = df.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
            stratified_df = stratified_df.append(tmp_df, ignore_index=True)
    
    return stratified_df



size1 = __smpl_size(population=100, size=None)

strat = stratified_sample_report(df=benef_clean, strata=['comunidad','tipo_familia','ingreso_mensual'], size= 0.3)

strat_sample = stratified_sample(df=benef_clean, strata=['comunidad','tipo_familia','ingreso_mensual'], size = 96)