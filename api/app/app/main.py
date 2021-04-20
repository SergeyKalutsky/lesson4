import os
import cv2
import torch
import torchvision
import numpy as np
import torch.nn as nn
from torchvision.models import resnet50
import torchvision.transforms as transforms
from flask import render_template, Flask, jsonify

app = Flask(__name__)

filepath = '/app/app/static/data/best_model.pth'

device = torch.device('cpu')
model = resnet50(pretrained=False)
model.fc = nn.Sequential(
    nn.Linear(2048, 1, bias=True),
    nn.Sigmoid()
)
model.load_state_dict(torch.load(filepath, map_location=device))
model.eval()


def read_img_test(path):
    # Reading, converting and normalizing image
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
    img = img[..., np.newaxis]
    img = torch.from_numpy(img).permute(3, 2, 0, 1)
    img.to(device)
    return img


def predict_img(img, model):
    with torch.no_grad():
        percentage = round(model(img).item(), 4)
        if percentage >= 0.5:
            return 'Dog'
        return 'Cat'


@app.route('/')
def hello_world():
    return 'Hello world'


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    path = '/app/app/static/data/images/cat.jpg'
    img = read_img_test(path)
    res = predict_img(img, model)
    return jsonify({'class_name': res})
