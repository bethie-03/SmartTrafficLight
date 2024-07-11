import pickle
import torch

MODEL_PATH = 'source/yolov5.pt'
POLY_REG_MODEL_PATH = 'source/polynomial_regression_model.pkl'

def load_regression_model(model_path):
    with open(model_path, 'rb') as file:
        polynomial_reg_model=pickle.load(file)
    return polynomial_reg_model

POLYNOMIAL_REG_MODEL = load_regression_model(POLY_REG_MODEL_PATH)
MODEL = torch.hub.load('ultralytics/yolov5', 'custom', MODEL_PATH, device = 'cuda:0', force_reload=True) 

        
