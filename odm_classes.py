# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:03:39 2022

@author: nato
"""

import mongoengine as me
import datetime
import pandas as pd

def queryset_pandas(queryset):
    l = list(queryset)
    print(l)
    return pd.DataFrame(l)

class DatasetQuerySet(me.QuerySet):
    def to_dataframe(self):
        return queryset_pandas(self)

class DataOriginQuerySet(me.QuerySet):
    pass

class TagQuerySet(me.QuerySet):
    pass

