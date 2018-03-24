import os
import io
import keras
import sklearn
import cv2
from statistics import mean
from tkinter import filedialog
from tkinter import *

from zoo import *
from paths import *

keras.backend.set_learning_phase(0)

def get_model(cnn):
    from keras.layers.core import Reshape
    model = get_pretrained_model(cnn, num_classes)
    if os.path.isfile(os.getcwd() + '/models/' + cnn + '_best.h5'):
        model.load_weights(os.getcwd() + '/models/' + cnn + '_best.h5')
    elif os.path.isfile(os.getcwd() + '/models/' + cnn + '_temp.h5'):
        model.load_weights(os.getcwd() + '/models/' + cnn + '_temp.h5')
    else:
        return model

    return model

def get_all_input_shape(models):
    return [get]

def voting_classifier(models):
    from sklearn.ensemble import VotingClassifier
    estimators = [(model, get_model(model)) for model in models]

    vc = VotingClassifier(estimators=estimators, voting='soft')

    return vc

def averaging_model(models):
    from keras.layers import average, concatenate, Input
    from keras.models import Model
    input_test = Input(shape=(None, None, 3))
    inputs = []
    outputs = []
    for model in models:
        hi = get_input_shape(model)
        inp = Input(shape=(hi[0], hi[1], 3))
        cnn = get_model(model)
        out = cnn(inp)
        inputs.append(inp)
        outputs.append(out)

    x = average(outputs)

    model = Model(inputs, outputs)

    return model

def individual_models():
    models = []
    for inp in paths.models:
        model = get_model(inp)
        models.append(model)
    return models


def predict_some_stuff():

    inputs = []
    root = Tk()
    root.img_path = filedialog.askopenfilename(initialdir = "~/Desktop/projects/test_images/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
    for inp in paths.models:
        model = get_model(inp)
        hi = get_input_shape(inp)
        img = cv2.resize(cv2.imread(root.img_path), hi, cv2.INTER_LANCZOS4)
        img = np.reshape(img,(-1, hi[0], hi[1], 3))
        pred = model.predict(img)
        inputs.append(pred)

    return np.mean(inputs, axis=0)

if __name__ == '__main__':
    print(paths.models)
    print(os.getcwd())
    #model = averaging_model(paths.models)

    print(predict_some_stuff())
