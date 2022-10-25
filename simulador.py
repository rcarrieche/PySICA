
import pandas as pd
from pymongo import MongoClient
import datetime
from pprint import pprint
from matplotlib import pyplot as plt
import pint 
import numpy as np
import seaborn as sns
ur = pint.UnitRegistry()
ur.load_definitions('C:\\Users\\nato\\Pysica\\dev\\add_units.txt')
import pysica


Tmed = pd.read_csv('C:\\Users\\nato\\Pysica\\data\\simulador\\Tmed.txt', sep='\t')
PotEletrica = pd.read_csv('C:\\Users\\nato\\Pysica\\data\\simulador\\PotEletrica.txt', sep='\t')
PotTermica = pd.read_csv('C:\\Users\\nato\\Pysica\\data\\simulador\\PotEletrica.txt', sep='\t')
Gov1 = pd.read_csv('C:\\Users\\nato\\Pysica\\data\\simulador\\Gov1.txt', sep='\t')
Gov2 = pd.read_csv('C:\\Users\\nato\\Pysica\\data\\simulador\\Gov2.txt', sep='\t')
Gov1.rename(columns={'Date/Time             ':'dt_str'}, inplace=True)
Gov2.rename(columns={'Date/Time             ':'dt_str'}, inplace=True)


t = Tmed['TSIM (s)']
y1 = Tmed['TREF']
y2 = Tmed['Tmed leiolada']
fig, axs = plt.subplots(2, 1)
axs[0].plot(t, y1, label="TREF")
axs[0].plot(t, y2, label="Tmed leiolada")
axs[0].set_xlabel('t (s)')
axs[0].set_ylabel('T (grC)')
axs[0].grid(True)
axs[0].legend()


axs[1].plot(t, Tmed['TE-450A'], label="perna quente")
#axs[1].plot(t, Tmed['TE-450B'], label="perna fria")
axs[1].set_xlabel('t (s)')
axs[1].set_ylabel('T (grC)')
axs[1].grid(True)
axs[1].legend()

#Gov1['x'] = Gov1['dt_str'].str.split()
#Gov1['id'], Gov1['time_str']= map(Gov1['dt_str'].str.slice, [0, 4], [3, 28])
try:
    Gov1['datetime'] = pd.to_datetime(Gov1['dt_str'], format="%m/%D/%Y %I:%M:%S AM")
except Exception:
    pass
print(Gov1['dt_str'])

"""
tgov = Gov1.iloc[:,0].datetime() - Gov1.iloc[0,0]
axs[2].plot(tgov, Gov1.iloc[:,1], tgov, Gov2.iloc[:,1])
axs[2].set_xlabel('t (s)')
axs[2].set_ylabel('% abertura')
axs[2].grid(True)
"""
#fig.tight_layout()
plt.show()