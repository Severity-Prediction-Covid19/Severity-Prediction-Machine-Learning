import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.layers import IntegerLookup
from tensorflow.keras.layers import Normalization
from tensorflow.keras.layers import StringLookup
import warnings
warnings.filterwarnings('ignore')

def preprocess(filename):
    filename = filename.drop(["Country","Age_0-9","Age_10-19","Age_20-24","Age_25-59","Age_60+","Gender_Female","Gender_Male","Gender_Transgender","Contact_Dont-Know","Contact_No","Contact_Yes"], axis=1)
    
    def dataframe_to_dataset(dataframe):
        dataframe = dataframe.copy()
        labels = pd.concat([dataframe.pop(x) for x in ['Severity_Mild','Severity_Moderate','Severity_None','Severity_Severe']], axis=1)
        ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
        ds = ds.shuffle(buffer_size=len(dataframe))
        return ds
    
    ds = dataframe_to_dataset(filename)
    ds = ds.batch(32)
    return ds

def predict(data):
    prediction = model.predict(data)
    return prediction