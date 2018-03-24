num_classes = 15
epochs = 125
patience = 25
percent = 0.25
input_path = './chestxray'
history = './chestxray/models/history/'
model_path = './chestxray/models/'
model_single_path = './chestxray/models-single/'
history_single = './chestxray/models-single/history/'
models = ['INCEPTION_V3_DENSE_LAYERS', 'DENSENET_121', 'DENSENET_169', 'DENSENET_161', 'RESNET50_DENSE_LAYERS', 'RESNET101',
          'VGG16_KERAS', 'VGG19_KERAS', 'XCEPTION', 'INCEPTION_RESNET_V2']

models2 = ['INCEPTION_V3_DENSE_LAYERS', 'INCEPTION_V4', 'DENSENET_121', 'DENSENET_169', 'DENSENET_161', 'RESNET50_DENSE_LAYERS', 'RESNET101',
           'VGG16_KERAS', 'VGG19_KERAS', 'XCEPTION', 'INCEPTION_RESNET_V2']
