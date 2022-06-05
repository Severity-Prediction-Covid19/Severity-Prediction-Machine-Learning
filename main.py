from flask import Flask, make_response, request, render_template
import io
from io import StringIO
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import os
from keras.models import load_model
from flask_preprocess import preprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "C22-PS273"

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == 'POST':
        f = request.files['data_file']
        if not f:
            return "No file"
        
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    stream.seek(0)
    result = stream.read()
    data = pd.read_csv(StringIO(result))
    model = load_model('model_percobaan', compile=False)
    df = preprocess(data)
    prediction = model.predict(df)
    df_predict = pd.DataFrame(prediction, columns=[['Severity_Mild','Severity_Moderate','Severity_None','Severity_Severe']])
    df_predict.to_csv("prediction.csv", index=False, header=False, encoding='utf8')
    
    response = make_response(df_predict.to_csv())
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response

if (__name__ == "__main__"):
     app.run(host="0.0.0.0", port = 5000, debug=False)