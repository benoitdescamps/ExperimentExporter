from datetime import datetime as dt
import pickle
from flask import jsonify

from sklearn.metrics import r2_score
from xgboost import XGBRegressor
import numpy as np
import pandas as pd

class ExperimentExporter():
    '''
    Make a log book of the evolution of the properties and performance of the model
    in time.
    This is supposed to help streamline the work of the team and help visualize 
    the progress
    '''
    def __init__(self,title_project):
        self.title_project = title_project
        self.start_date_project = dt.now()
        self.log = []
    def updateLog(self,model,X_train,X_test,metrics_values):
        self.log+=[{
            'days_since_start': int(np.random.rand() * 10),
            'timestamp': str(dt.now()),
            'model_properties':model.get_params(),
            'data_properties':{\
                               'N_features':X_train.shape[0],
                               'Train_size': X_train.shape[1],
                               'Test_size':X_test.shape[0],
                               #'Features':list(X_train.columns)
                                },
            'metrics':metrics_values
        }]
    def getLog(self):
        return {self.title_project: self.log}

def load_experiment(filename):
    N = 1000
    n = 10
    X = np.random.randn(N, n)
    df = pd.DataFrame(X)
    y = np.random.randn(N, )
    reg = XGBRegressor()
    reg.fit(X, y)

    rsquared = r2_score(y, reg.predict(X))

    myexporter = ExperimentExporter('new_project')
    myexporter.updateLog(reg, df, df, {'r2_score': rsquared+np.random.randn()/5})
    reg = XGBRegressor(n_estimators=10,max_depth=3)
    reg.fit(X, y)
    myexporter.updateLog(reg, df, df, {'r2_score': rsquared+np.random.randn()/5})
    reg = XGBRegressor(n_estimators=9, max_depth=2)
    reg.fit(X, y)
    myexporter.updateLog(reg, df, df, {'r2_score': rsquared+np.random.randn()/5})
    reg = XGBRegressor(n_estimators=8, max_depth=1)
    reg.fit(X, y)
    myexporter.updateLog(reg, df, df, {'r2_score': rsquared+np.random.randn()/5})
    reg = XGBRegressor(n_estimators=7, max_depth=3)
    reg.fit(X, y)
    myexporter.updateLog(reg, df, df, {'r2_score': rsquared+np.random.randn()/5})
    reg = XGBRegressor(n_estimators=6, max_depth=2)
    reg.fit(X, y)
    myexporter.updateLog(reg, df, df, {'r2_score': rsquared+np.random.randn()/5})
    reg = XGBRegressor(n_estimators=5, max_depth=1)
    reg.fit(X, y)
    myexporter.updateLog(reg, df, df, {'r2_score': rsquared+np.random.randn()/5})
    reg = XGBRegressor(n_estimators=4, max_depth=4)
    reg.fit(X, y)
    myexporter.updateLog(reg, df, df, {'r2_score': rsquared+np.random.randn()/5})


    #with open('app_data/data/'+filename, 'rb') as file:
    #    experiment = pickle.load(file)
    #print(experiment.getLog())
    return myexporter.getLog()