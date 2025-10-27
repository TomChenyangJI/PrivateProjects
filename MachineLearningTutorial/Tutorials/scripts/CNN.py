import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.utils import make_grid

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


# convert MNIST Image files into a Tensor of 4-dimensions (# of images, height, Width, Color Channel)
transform = transforms.ToTensor()

# train data
train_data = datasets.MNIST(root="cnn_data", train=True, download=True, transform=transform)

# test data
test_data = datasets.MNIST(root="cnn_data", train=False, download=True, transform=transform)

print(train_data)
print(test_data)

# create a small batch size for iamges
train_loader = DataLoader(train_data, batch_size=10, shuffle=True)
test_loader = DataLoader(test_data, batch_size=10, shuffle=False)

# Define CNN model
# describe convolutional layer and what it's doing (2 convolutional layers)
conv1 = nn.Conv2d(1, 6, 3, 1)
conv2 = nn.Conv2d(6, 16, 3, 1)

# grab 1 MNIST record/image
for i, (X_Train, y_train) in enumerate(train_data):
    # print(X_Train.shape)
    # print(X_Train)
    x = X_Train.view(1, 1, 28, 28)
    # perform our first convolution
    x = F.relu(conv1(x))  # rectified linear unit for our activation function
    print(x.shape)
    # pass thru the pooling layer
    x = F.max_pool2d(x, 2, 2)  # kernel of 2 and stride 2
    print(x.shape)
    # perform our second convoluational layer
    x = F.relu(conv2(x))
    print(x.shape)  # we didn't set padding, so we lose 2 pixels around the outside of the image
    # pooling layer
    x = F.max_pool2d(x, 2, 2)
    print(x.shape)  # 11/2=5.5 but we have to round down, because we can't invent data to round up
    break


# Model Class
class ConvolutionalNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 3, 1)
        self.conv2 = nn.Conv2d(6, 16, 3, 1)
        # fully connected layer
        self.fc1 = nn.Linear(5 * 5 * 16, 120)  # 120 is the out_features
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, X):
        X = F.relu(self.conv1(X))
        X = F.max_pool2d(X, 2, 2)  # 2x2 kernel, and stride 2
        # second pass
        X = F.relu(self.conv2(X))
        X = F.max_pool2d(X, 2, 2)
        # re-view to flatten it out
        X = X.reshape(-1, 16*5*5)  # negative one so that we can vary the batch size

        # fully connected layers
        X = F.relu(self.fc1(X))
        X = F.relu(self.fc2(X))
        X = self.fc3(X)
        return F.log_softmax(X, dim=1)

# create an instance of the model
torch.manual_seed(41)
model = ConvolutionalNetwork()
print(model)

# loss function optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # smaller the learning rate, longer it's gonna tak to train

import time
start_time = time.time()

# create variables to track things
epochs = 3
train_losses = []
test_losses = []
train_correct = []
test_correct = []

# for loop of epochs
for i in range(epochs):
    trn_corr = 0
    tst_corr = 0

    # train
    for b, (X_train, y_train) in enumerate(train_loader):
        b += 1
        y_pred = model(X_train)  # get predicted values from the training set. not flattened
        loss = criterion(y_pred, y_train)  # how off are we? compare the predictions to correct answers in y_train

        predicted = torch.max(y_pred.data, 1)[1]  # add up the number of correct predictions. indexed off the first point
        batch_corr = (predicted == y_train).sum() # how many we got correct from this batch. True = 1, False = 0, sum those up
        trn_corr += batch_corr  # keep track as we go along in training

        # update out parameters
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # print out some results
        if b % 600 == 0:
            print(f"Epoch: {i} Batch: {b}  Loss: {loss.item()}")

        train_losses.append(loss)
        train_correct.append(trn_corr)

    # test
    with torch.no_grad(): # no gradient so we don't update our weights and biases with test data
        for b, (X_test, y_test) in enumerate(test_loader):
            y_val = model(X_test)
            predicted = torch.max(y_val.data, 1)[1]  # adding up correct predictions
            tst_corr += (predicted == y_test).sum()  # True = 1 False = 0 and sum away

    loss = criterion(y_val, y_test)
    test_losses.append(loss)
    test_correct.append(tst_corr)

current_time = time.time()
total_time = current_time - start_time
print(f"Training Took: {total_time/60} minutes")

# graph the loss at epoch
train_losses = [t.item() for t in train_losses]
plt.plot(train_losses, label="Training loss")
plt.plot(test_losses, label="Validation loss")
plt.title("Loss at Epoch")
plt.legend()
plt.show()

# graph the accuracy at the end of ecah epoch
plt.plot([t/600 for t in train_correct], label="Training Accuracy")
plt.plot([t/100 for t in test_correct], label="Validation Accuracy")
plt.title("Accuracy at the end of each epoch")
plt.legend()

test_load_everything = DataLoader(test_data, batch_size=10000, shuffle=False)
with torch.no_grad():
    correct = 0
    for X_test, y_test in test_load_everything:
        y_val = model(X_test)
        predicted = torch.max(y_val, 1)[1]
        print("------->")
        print(torch.max(y_val, 1))
        correct += (predicted == y_test).sum()

# did for correct
print(correct.item()/len(test_data) * 100)

# grab an image
print(test_data[4143])  # tensor with an image in it...at end, it shows the label
# grab just the data
print(test_data[4143][0])
# reshape it
print(test_data[4143][0].reshape(28, 28))
# show the image
plt.imshow(test_data[4143][0].reshape(28,28))
# pass the image thru the model
model.eval()
with torch.no_grad():
    new_prediction = model(test_data[4143][0].view(1, 1, 28, 28))  # batch size of 1, 1 color channel, 28 * 28 image
# checkt he new prediction ... get probabilities
print(new_prediction)
print(new_prediction.argmax())