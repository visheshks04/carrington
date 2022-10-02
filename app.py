from flask import Flask, jsonify
import tensorflow as tf
import joblib
import numpy as np

def preprocess(data):
    scaler = joblib.load('scaler')
    B1F1 = np.float64(data[0])
    B1GSEx = np.float64(data[1])
    B1GSEy = np.float64(data[2])
    B1GSEz = np.float64(data[3])

    X = scaler.transform([[B1F1, B1GSEx, B1GSEy, B1GSEz]])

    return X


app = Flask(__name__)

@app.route('/predict/<string:data>')
def predictor(data):

    data = data.split('_')
    X = preprocess(data)

    N_model = tf.keras.models.load_model('N_model')
    V_model = tf.keras.models.load_model('V_model')
    W_model = tf.keras.models.load_model('W_model')

    n = N_model.predict(X)
    v = V_model.predict(X)
    w = W_model.predict(X)

    result = {'n': float(n), 'v': float(v), 'w': float(w)}

    return jsonify(result)


app.run(debug=True)