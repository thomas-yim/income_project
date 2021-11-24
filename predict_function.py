# -*- coding: utf-8 -*-
"""Predict Function.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UmUHCHusjFi8-P--yuNbPWHTGB7R6ZVK
"""

# Commented out IPython magic to ensure Python compatibility.
# this mounts your Google Drive to the Colab VM.
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

# enter the foldername in your Drive where you have saved the unzipped
# workshop folder, e.g. 'acmlab/workshops/week1'
FOLDERNAME = 'acmlab/project/project'
assert FOLDERNAME is not None, "[!] Enter the foldername."

# now that we've mounted your Drive, this ensures that
# the Python interpreter of the Colab VM can load
# python files from within it.
import sys
sys.path.append('/content/drive/My Drive/{}'.format(FOLDERNAME))

# %cd /content/drive/My\ Drive/$FOLDERNAME/

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# Importing the standard ML libraries...
# %load_ext autoreload
# %reload_ext autoreload

import pandas as pd                     # to process our data
import matplotlib.pyplot as plt         # graphing
# from utils import decision_boundary     # for plotting
from sklearn.linear_model import LogisticRegression # our shallow neural network
from PIL import Image


import torch
import numpy as np
import matplotlib.pyplot as plt
import util
import webmercator
import os
from PIL import Image
import json
import torchvision
from torchvision import transforms
from tqdm import tqdm
import random

import torch.nn as nn
import torch.nn.functional as F

class ConvolutionalNeuralNet(nn.Module):
  def __init__(self):
    super(ConvolutionalNeuralNet, self).__init__()
    self.conv1 = nn.Conv2d(3, 10, 5)
    self.pool = nn.MaxPool2d(2, 2)
    self.conv2 = nn.Conv2d(10, 20, 5)
    self.conv3 = nn.Conv2d(20, 40, 5)
    self.fc1 = nn.Linear(31360, 200)
    self.fc2 = nn.Linear(200, 1)

  def forward(self, x):
    x = self.pool(F.relu(self.conv1(x)))
    x = self.pool(F.relu(self.conv2(x)))
    x = self.pool(F.relu(self.conv3(x)))
    x = x.view(x.shape[0], -1)
    x = F.relu(self.fc1(x))
    x = self.fc2(x)
    return x

# take advantage of GPU if available
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

cnn_model = torch.load("model.pt")

def predict(path_to_image):
  device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
  trans = transforms.Compose([transforms.ToTensor()])
  image = Image.open(path_to_image).convert("RGB")
  tensorImage = trans(image)
  with torch.no_grad():
    plt.imshow(image)
    tensorImage = torch.unsqueeze(tensorImage, dim=0)
    print(tensorImage.shape)
    output = cnn_model(tensorImage.to(device=device))
    predicted = output.data
    return predicted.data

print(predict("imagery/14_2799_6543.jpg"))

model = torch.load("chocolate_croissants_model.pth");

model.eval()

class TestDataset(torch.utils.data.Dataset):
  def __init__(self, data):
    self.images = []
    self.labels = []
    self.transform = transforms.Compose([transforms.ToTensor()])
    
    for key in tqdm(data):
      image = Image.open("imagery/" + key).convert("RGB")
      
      self.images.append(self.transform(image))
      self.labels.append(float(data[key]))


  def __len__(self):
    return len(self.images)
  def __getitem__(self, idx):
    return self.images[idx], self.labels[idx]

testset = torch.load("testset.pt")

with torch.no_grad():
  device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
  for image, label in testset:
    image = torch.unsqueeze(image, dim=0)
    pred = model(image.to(device=device))
    print(pred.data - label)

