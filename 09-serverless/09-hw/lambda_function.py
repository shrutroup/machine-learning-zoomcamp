from re import L
import onnxruntime as ort
from io import BytesIO
from urllib import request

from PIL import Image
import numpy as np


onnx_model_path = "hair_classifier_empty.onnx"
target_size = (200, 200)

# Create an inference session
session = ort.InferenceSession(onnx_model_path, providers=['CPUExecutionProvider'])
inputs = session.get_inputs()
outputs = session.get_outputs()

input_name = inputs[0].name
output_name = outputs[0].name


def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_pytorch_style(X):
    X = X / 255.0 # convert to tensor, value between 0 and 1

    mean = np.array([0.485, 0.456, 0.406]).reshape(1, 3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(1, 3, 1, 1)

    # convert (batch, height, width, channels) to (batch, channels, height, width)
    X = X.transpose(0, 3, 1, 2)
    # Normalize
    X = (X - mean) / std
    return X.astype(np.float32)


def lambda_handler(event, context):
    url = event['url']
    print(f'Parameters: {url}')
    
    print(f'Downloading the image from {url}')
    img = download_image(url)
    
    print(f'Resizing the image to {target_size}')
    img = prepare_image(img, target_size)
    X = np.array(img)
    X = np.expand_dims(X, axis=0)
    print(f"X Shape After batch dim added: {X.shape}")  # (1, 200, 200, 3)
    
    print(f'Preprocessing the image for inference')
    X = preprocess_pytorch_style(X)
    print(f"X Shape After preprocessing: {X.shape}")

    print(f'Running inference on the image')
    result = session.run([output_name], {input_name: X})
    predictions = result[0][0].tolist()
    print(f'Prediction: {predictions[0]}')
    return predictions[0]