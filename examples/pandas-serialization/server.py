# -*- coding: utf-8 -*-

import Pyro5.api
import pandas as pd
import numpy as np

length = 100
@Pyro5.api.expose
class MyClass():   
    def gen_DataFrame(self,variant=1):
        if variant == 1:
            data = pd.DataFrame({'A':1.2,'B':'Im a string','C':True,'D':[x for x in range(10)]})
        elif variant == 2:
            index = np.linspace(0,100,length)
            values = index*2
            data = pd.DataFrame({'current':values},index=index)
            data.index.name = 'voltage'
        elif variant == 3:
            time = np.linspace(0,100,length)
            x = np.linspace(0,1,length)
            X,T = np.meshgrid(x,time)
            voltage = -X**2+0.5+T
            data = pd.DataFrame(voltage,columns=x,index=time)
            data.columns.name = 'x'
            data.index.name = 'Time'
            data = data.stack()
            data.name = 'voltage'
            data = pd.DataFrame(data)
        elif variant == 4:
            time = np.linspace(0,100,length)
            x = np.linspace(0,1,length)
            X,T = np.meshgrid(x,time)
            voltage = -X**2+0.5+T
            current = (-X**2+0.5+T)*1000
            data = pd.DataFrame(voltage,columns=x,index=time)
            data.columns.name = 'x'
            data.index.name = 'Time'
            data = data.stack()
            data.name = 'voltage'
            data = pd.DataFrame(data)
        return data
    
    def gen_Series(self):
        time = np.linspace(0,100,length)
        x = np.linspace(0,1,100)
        X,T = np.meshgrid(x,time)
        voltage = -X**2+0.5+T
        data = pd.DataFrame(voltage,columns=x,index=time)
        data.columns.name = 'x'
        data.index.name = 'Time'
        data = data.stack()
        data.name = 'voltage'
        return data

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

if __name__ == "__main__":  
    port = 44444
    host = 'localhost'
    name = 'MyClass'
    Pyro5.api.serve({MyClass: name},host=host,port=port, use_ns=False)

    


