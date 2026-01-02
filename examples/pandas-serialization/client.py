# -*- coding: utf-8 -*-

import Pyro5.api
import pandas as pd

# register the special serialization hooks
orient='tight'
def df_to_dict(df):
    print("DataFrame to dict")
    data = df.to_dict(orient=orient)
    data = {'__class__':'DataFrameDict','DataFrame':data}
    return data

def dict_to_df(classname, d):
    print("dict to Dataframe")
    data = pd.DataFrame.from_dict(d['DataFrame'],orient=orient)
    return data

def series_to_dict(series):
    print("Series to dict")
    print(series)

    data = series.to_frame().to_dict(orient=orient)
    data = {'__class__':'SeriesDict','Series':data}
    return data

def dict_to_series(classname, d):
    print("dict to Series")
    data = pd.DataFrame.from_dict(d['Series'],orient=orient).iloc[:,0]
    return data


Pyro5.api.register_class_to_dict(pd.core.frame.DataFrame, df_to_dict)
Pyro5.api.register_dict_to_class("DataFrameDict", dict_to_df)
Pyro5.api.register_class_to_dict(pd.core.frame.Series, series_to_dict)
Pyro5.api.register_dict_to_class("SeriesDict", dict_to_series)
Pyro5.api.config.SERIALIZER = 'serpent'

port = 44444
host = 'localhost'
name = 'MyClass'

myClass = Pyro5.api.Proxy(uri="PYRO:%s@%s:%s"%(name,host,port)) 
print(myClass.gen_DataFrame(1))
print(myClass.gen_DataFrame(2))
print(myClass.gen_DataFrame(3))
print(myClass.gen_Series())

