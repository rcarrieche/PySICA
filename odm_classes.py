# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:03:39 2022

@author: nato
"""

import mongoengine as me
import datetime
import pandas as pd

def queryset_pandas(queryset):
    return pd.DataFrame(list(queryset))
    pass

class DatasetQuerySet(me.QuerySet):
    pass

class DataOriginQuerySet(me.QuerySet):
    pass

class TagQuerySet(me.QuerySet):
    pass



