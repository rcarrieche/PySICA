# -*- coding: utf-8 -*-
"""
Created on Sat May  7 11:13:22 2022

@author: nato
"""
import pandas as pd
from pymongo import MongoClient
import datetime
from pprint import pprint
from matplotlib import pyplot as plt
import pint 
import numpy as np
import seaborn as sns

def plot_runs(dataset):
    #plt.rcParams["figure.figsize"] = (40,20)
    colunas = ['NFLAG', 'EXITCODE', 'NACQISS', 'NBAD', 'NERF', 'NERR', 'NERS', 'NFILT', 'NOUTOFRANGE', 'NRELAX']
    sns.color_palette("Spectral", as_cmap=True)
    for col in colunas:
        #plt.rcParams["figure.figsize"] = (400,20)
        grafico = sns.relplot(
            data=dataset.data_run,
            x="date", y="QUALITY", hue=col, palette="Spectral"
        )
        for ind, label in enumerate(grafico.ax.get_xticklabels()):
            if ind % 2 == 0:
                label.set_visible(True)
            else:
                label.set_visible(False)
        
def plot_run(dataset):
    #plt.rcParams["figure.figsize"] = (3,150)
    xxx = sns.relplot(
        data=dataset.data_run,
        x="date", y="QUALITY", hue='NFLAG'
    )
    for ind, label in enumerate(xxx.ax.get_xticklabels()):
        if ind % 2 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    #print(ind)
    #xxx.set_xticklabels(dataset.datarun['date'])
        
       
def plot_qualitycw(dataset):
    sns.color_palette("Spectral", as_cmap=True)
    # insere os dados da água do mar nos runs
    #localizando TE1940C, TE1942C, TE1944C, TE1946C
    list_cwit = ['TE1940C', 'TE1942C', 'TE1944C', 'TE1946C']
    filtro = (dataset.data_var['name'].isin(list_cwit))
    df_cw = dataset.data_var.loc[filtro]
    #df_cw['CWIT'] = 
    dfgb = df_cw.groupby('date')[['val']].mean()
    df_completo = pd.merge(dataset.data_run, dfgb, on='date', how='left' )
    df_completo.rename(columns={'val':'CWIT'}, inplace=True)
    filtro2 = df_completo['CWIT'] < 1000
    df_completo = df_completo.loc[filtro2]
    #print(df_completo)
    
    xxx = sns.relplot(
        data=df_completo,
        x="date", y="QUALITY", hue='CWIT'
        )
    for ind, label in enumerate(xxx.ax.get_xticklabels()):
        if ind % 2 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
            
    yyy = sns.relplot(
        data=df_completo,
        x="CWIT", y="QUALITY")
    
    for ind, label in enumerate(yyy.ax.get_xticklabels()):
        if ind % 2 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    #return dataset.data_run
        
def plot_tr(dataset):
    df_valores = pd.merge()
    list_cx1 = ['TE1940C', 'TE1941C']
    filtro = (dataset.data_var['name'].isin(list_cx1))&(dataset.data_var['val'] < 1000)&(dataset.data_var['data_origin'] == 'SICA1_SQL')
    df_cx1 = dataset.data_var.loc[filtro]
    gb = df_cx1.groupby('date', axis=1)
    df_cx1['Tr'] = df_cx1['TE1941C'] - df_cx1['TE1940C']
    xxx = sns.relplot(
        data=df_cx1,
        x="date", y="Tr"
        )