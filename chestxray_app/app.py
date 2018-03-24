import os
import io
import cv2
import numpy as np
from flask import Flask, request, render_template, jsonify
import urllib
import tensorflow as tf
import json

from paths import *
from zoo import *
from ensemble import *

application = Flask(__name__, static_url_path='')

UPLOAD_FOLDER = os.path.basename('uploads')

application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

models = None
graph = tf.get_default_graph()


def load_model():
    global models
    print("Loading the models...")
    models = individual_models()
    print("Models Loaded!")
    return None


def preprocess_image(cnn, image):
    input_size = get_input_shape(cnn)
    image = cv2.resize(image, input_size, cv2.INTER_LANCZOS4)
    image = np.reshape(image, (-1, input_size[0], input_size[1], 3))
    image = preprocess_input_overall(cnn, image)

    return image


def url_to_image(url):
    requested_url = urllib.urlopen(url)
    image_array = np.asarray(bytearray(requested_url.read()), dtype=np.uint8)
    img = cv2.imdecode(image_array, -1)
    return img


thres = 0.163
indexes = ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion', 'Emphysema', 'Fibrosis',
           'Hernia', 'Infiltration', 'Mass', 'No Finding', 'Nodule', 'Pleural_Thickening', 'Pneumonia', 'Pneumothorax']


def predict(image):
    preds = []
    for i in range(len(paths.models)):
        model = models[i]
        cnn = paths.models[i]
        img = image
        img = preprocess_image(cnn, image)

        with graph.as_default():
            prediction = model.predict(img)

        preds.append(prediction)

    full_pred = np.mean(preds, axis=0)
    return full_pred


@application.route("/", methods=['GET'])
def root():
    return render_template('index.html')


@application.route("/classify", methods=['GET', 'POST'])
def classify():
    file = request.files['image']
    imf = io.BytesIO()
    file.save(imf)
    data = np.fromstring(imf.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(data, 1)

    full_pred = predict(image)[0]
    a = full_pred
    print(a)
    pred = full_pred
    pred[pred > thres] = 1
    pred[pred <= thres] = 0
    print(pred)
    resp = []
    for val in range(0, len(pred)):
        if pred[val] == 1:
            resp.append(indexes[val])

    resp = {'results': resp}

    response = json.dumps(resp, sort_keys=False,
                          indent=4, separators=(',', ': '))

    return render_template('classify.html', response=response)


if __name__ == '__main__':
    load_model()
    print("Wait for the Model to load before running the web application")
    application.run(host='0.0.0.0')
