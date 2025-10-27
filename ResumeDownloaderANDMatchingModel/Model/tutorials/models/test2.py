import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from transformers import AdamW
from tqdm import tqdm


texts = ["I love this product", "Worst purchase ever", "Highly recommend it", "Not worth the money"]
labels = [1, 0, 1, 0]  # 1 for positive, 0 for negative sentiment

train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2)

tokenizers = BertTokenizer.from_pretrained("bert-base-uncased")

train_encodings = tokenizers(train_texts, truncation=True, padding=True, max_length=512)
val_encodings = tokenizers(val_texts, truncation=True, padding=True, max_length=512)

class TextDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = TextDataset(train_encodings, train_labels)
val_dataset = TextDataset(val_encodings, val_labels)

model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

optimizer = AdamW(model.parameters(), lr=1e-5)

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

for epoch in range(3):
    model.train()
    total_train_loss = 0

    for batch in tqdm(train_loader):
        batch = {k: v.to(device) for k, v in batch.items()}
        optimizer.zero_grad()  # clear previous gradients

        outputs = model(**batch)
        loss = outputs.loss
        total_train_loss += loss.item()

        loss.backward()
        optimizer.step()

    avg_train_loss = total_train_loss / len(train_loader)
    print(f"epoch {epoch + 1}, training loss: {avg_train_loss}")

model.eval()
total_val_loss = 0
correct_predictions = 0

with torch.no_grad():
    for batch in val_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        logits = outputs.logits

        total_val_loss += loss.item()
        predictions = torch.argmax(logits, dim=-1)
        correct_predictions += (predictions == batch["labels"]).sum().item()

avg_val_loss = total_val_loss / len(val_loader)
accuracy = correct_predictions / len(val_texts)
print(f"validation loss: {avg_val_loss}")
print(f"validation accuracy: {accuracy}")


"""
logic steps:
1. import modules
2. load data
3. form datasets
4. build dataloaders
5. build model ***
6. pass model to device (e.g., cpu or gpu)
7. pass data to device (through dataloader)
8. train the model ***
     in each epoch:
     set model.train() to mode:
        put the data dict to model
        get the loss, because the parameters are in the loss function (i.e., object function)
        using backpropagation to optimize the paramenters
        optimizer functioning
        clear previous gradients
9. evaluate the model
    set the model to eval mode: model.eval()
    pass the test data sample dict to model
    get the loss
    get the logits (the predicted possibilities of the classes)
    convert the possibilities to classes
10. save the model
"""