# Database 
MONGO_DATABASE = "BancoPySICA_Teste_2"

# gui
MAIN_TITLE = "PySICA v0.0.1"

# PATHS
SICA_DIR = 'C:\\Users\\nato\\Pysica\\data\\SICA\\'
SICA_TAGFILE = SICA_DIR+'Analogicas.txt'
SICA_IMPORT_DIR = SICA_DIR+'\\import\\'
OVATION_DIR = 'C:\\Users\\nato\\Pysica\\data\\Ovation\\'
SIMULADOR_DIR = 'C:\\Users\\nato\\Pysica\\data\\Simulador\\'
SIMULADOR_OVATION_DIR = 'C:\\Users\\nato\\Pysica\\data\\Simulador Ovation\\'
OSCILOSCOPIO_DIR = 'C:\\Users\\nato\\Pysica\\data\\Oscilógrafo\\'

# Data_filler
TAGVAR_DVR = {
    'name': ['Measurement', 'Mea_Acc', 'Validated','Val_Acc', 'Penalty', 'Status', 'Mea_Fil', 'Acc_Fil', 'Gain', 'Used_Pen', 'VDI_Pen', 'InUse', 'Filtered', 'Compensated', 'Eliminated'], 
    'mea_unit':['var', '', 'var', '','','Int', 'var','','','','','Int','Int','Int','Int']
    }
     
     

TAGVAR_SICA1_SQL = {'name':['Value_Average'], 'mea_unit':['var']}
    

TAGVAR_SICA_TXT = {'name':['Valor', 'Status'], 'mea_unit':['var', 'Int']}

ORIGENS = [
    {'name':"SICA1_SQL", 'description': "Banco de dados com médias do SICA para reconciliação "},
    {'name':"ANGRA1_DVR",'description': "Banco de dados de reconciliação Belsim/ValiPerformnce"},
    {'name':"SICA_TXT",'description': "Arquivos de texto do SICA"},
    {'name':"UPRATE",'description': "Dados do Aumento de Potência"},
    {'name':"SIMULADOR_A1",'description': "Arquivos de dados do Simulador de Angra 1"},
    {'name':"OVATION",'description': "Arquivos de dados do Ovation"},
    {'name':"SIMULADOR_OVATION",'description': "Arquivos de dados do Ovation"},
    {'name':"MAXIMO",'description': "Banco de dados do Máximo"},
    {'name':"OSCILOSCOPIO",'description': "Leituras do oscilógrafo"},
    {'name':"LV",'description': "Listagem de Válvulas"},
    {'name':"LSPR",'description': "Lista de Set Points e Ranges"},
    {'name':"SISTEMAS_A1",'description': "lista de sistemas de Angra 1"},
    {'name':"FLUXOGRAMAS",'description': "Fluxogramas A1: metadados do PDF"},
    {'name':"EMSO",'description': "Arquivos de simulação do EMSO"},    
]