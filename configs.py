import torch
import joblib

MODEL_PATH = 'source/yolov5.pt'
POLY_REG_MODEL_PATH = 'source/polynomial_regression_model.pkl'

SCALER = joblib.load('source/scaler_mlp.pkl')
MLP_REG_MODEL = joblib.load('source/mlp_regression_model.pkl')

MODEL = torch.hub.load('ultralytics/yolov5', 'custom', MODEL_PATH, device = 'cpu', force_reload=True) 

        
