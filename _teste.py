# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 09:57:57 2022

@author: nato
"""

import numpy as np
from matplotlib import pyplot 
import pint
import sys, os
#import pysica_plots as psp
#import pysica_gui as pg
import datetime
import pandas as pd
import pysica_classes as psc
import pysica
import odm
from mongoengine.queryset.visitor import Q
from mongoengine import connect


ps = pysica.PySICA()
#ds_name = "TESTE"
#ds_description = "Teste para dataset"
#ds = ps.create_dataset(name=ds_name, description=ds_description)
ds = odm.Dataset.objects(_id="6372e9b0da1db9e12606ffaa").first()
list_tagnames = ["PI484", 'PI485','PI486', 'PI4695', 'PI4696', 'FI464', 'FI465', 'GOV', 'PI468A', 'PI469A','FI474', 'FI475',  'PI478A', 'PI479A', 'FI466', 'FI467', 'FI476', 'FI477', 'F1466A', 'F1468A', 'PI1311', 'PI1312', 'TR1315', 'TR1316', 'TI1313C', 'TI1314C', '6748', 'PIR08']
list_tag_ids = []
for name in list_tagnames:
    tags = odm.Tag.objects((Q(name__icontains=name)|Q(original_name__contains=name))|Q(description__contains=name))
    #print(tags.values_list('name'))
    new_tag_ids = list(tags.values_list('id'))
    print(new_tag_ids, type(new_tag_ids))
    list_tag_ids = list_tag_ids + new_tag_ids

print(list_tag_ids)
"""
#tags = odm.Tag.objects(Q(name__contains=list_tagnames)|Q(original_name__cointains=list_tagnames))
list_names = tags.values_list('name')
for name in list_names:
    print(name)
    pass
    #print(name)
print()
"""
ds.insert_tags(list_tag_ids)