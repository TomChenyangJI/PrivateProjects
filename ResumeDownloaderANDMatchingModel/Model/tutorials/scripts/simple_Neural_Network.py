import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import pandas as pd


# create a model class that inherits nn.Module
class Model(nn.Module):
    def __init__(self, in_features=4, h1=8, h2=9, out_features=3):
        super().__init__()
        self.fc1 = nn.Linear(in_features, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.out = nn.Linear(h2, out_features)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.out(x)
        
        return x

# pick a manual seed for randomization
torch.manual_seed(41)
# create an instance of model
model = Model()

url = "./iris.csv"
my_df = pd.read_csv(url)
# change last column from string to integers
my_df['species'] = my_df['species'].replace("setosa", 0.0)
my_df['species'] = my_df['species'].replace("versicolor", 1.0)
my_df['species'] = my_df['species'].replace("virginica", 2.0)

# Train Test Split
X = my_df.drop("species", axis=1)
y = my_df["species"]

# convert these to numpy arrays
X = X.values
y = y.values

from sklearn.model_selection import train_test_split
# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)
# convert these features and labels to float tensors
X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)
y_train = torch.LongTensor(y_train)
y_test = torch.LongTensor(y_test)

# set the criterion of model to measure the eror, hwo far off the predicitons are from the data
criterion = nn.CrossEntropyLoss()
# Choose Adam Optimizer, lr = learning rate (if error doesn't go down after a bunch of iterations (epochs), lower our learning rate)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
# print(list(model.parameters()))

# train our model
# epochs? (one run thru all the training data in our network)
epochs = 200
losses = []
for i in range(epochs):
    # go forward and get a prediction
    y_pred = model.forward(X_train)  # get predicted results

    # measure the loss/error, gonna be high at first
    loss = criterion(y_pred, y_train)  # predicted values vs the y_train

    # keep track of our losses
    losses.append(loss.detach().numpy())

    # print every 10 epoch
    if i % 10 == 0:
        print(f"Epoch: {i} and loss: {loss}")

    # do some back propagation: take the error rate of forward propagation and feed it back
    # thru the network to fine tune the weights
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# graph it out
plt.plot(range(epochs), losses)
plt.ylabel("Loss/error")
plt.xlabel("Epoch")
# plt.show()

# evaluate model on test data set (validate model on test set)
with torch.no_grad():
    y_eval = model.forward(X_test)  # X_test area feataures from out test set, y_eval will be the predictions
    loss = criterion(y_eval, y_test)  # find the loss or error
print(loss)

correct = 0
with torch.no_grad():
    for i, data in enumerate(X_test):
        y_val = model.forward(data)
        print(f"{i+1}.)  {str(y_val)} \t {y_test[i]}")

        # correct or not
        if y_val.argmax().item() == y_test[i]:
            correct += 1

print(f"we got {correct} correct")

# save out NN model
torch.save(model.state_dict(), "../My_really_awesome_iris_model.pt")

# Load saved model
new_model = Model()
new_model.load_state_dict(torch.load("../My_really_awesome_iris_model.pt"))

print(new_model.eval())
