import sys
sys.path.append('/code/')
from app import *
from app import application


def create():
    print('Initializing!')
    load_model()
    application.run(host='127.0.0.1', port=5000)
