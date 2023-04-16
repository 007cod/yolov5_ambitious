import numpy as np
import yaml
from mypredict import *

class pre(object):
    def __init__(self, predict1, predictor1, preprocess1, im_size1):
        self.predict = predict1
        self.im_size = im_size1
        self.preprocess = preprocess1
        self.predictor = predictor1

    def __call__(self, img):
        scale_factor = np.array([self.im_size * 1. / img.shape[0], self.im_size * 1. / img.shape[1]]).reshape((1, 2)).astype(
            np.float32)
        im_shape = np.array([self.im_size, self.im_size]
                            ).reshape((1, 2)).astype(np.float32)
        data = self.preprocess(img, self.im_size)
        result = self.predict(self.predictor, [im_shape, data, scale_factor])
        return result
def get_model(arg):
    global label_list ,num_classes
    model_file = './inference_model_PPYOLOTiny/ppyolo/inference_model/model.pdmodel'
    params_file = './inference_model_PPYOLOTiny/ppyolo/inference_model/model.pdiparams'
    model_yml_path = './inference_model_PPYOLOTiny/ppyolo/inference_model/model.yml'
    infer_cfg = open(model_yml_path)
    data = infer_cfg.read()
    yaml_reader = yaml.full_load(data)
    label_list = yaml_reader['_Attributes']['labels']
    num_classes = yaml_reader['_Attributes']['num_classes']
    predictor = predict_config(model_file, params_file)
    infer_model = pre(predict, predictor, preprocess, arg['im_size'])
    return infer_model