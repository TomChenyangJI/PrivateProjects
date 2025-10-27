import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from transformers import AdamW
from tqdm import tqdm


# Example dataset (texts and their corresponding labels)
texts = ["I love this product", "Worst purchase ever", "Highly recommend it", "Not worth the money"]
labels = [1, 0, 1, 0]  # 1 for positive, 0 for negative sentiment

# Train-test split
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2)


tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Tokenize the texts
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)


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

# Create Dataset objects
train_dataset = TextDataset(train_encodings, train_labels)
val_dataset = TextDataset(val_encodings, val_labels)


model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

optimizer = AdamW(model.parameters(), lr=1e-5)

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

# Training loop
for epoch in range(3):  # 3 epochs
    model.train()
    total_train_loss = 0

    for batch in tqdm(train_loader):
        batch = {k: v.to(device) for k, v in batch.items()}  # Move batch to GPU if available
        optimizer.zero_grad()  # Clear previous gradients

        # Forward pass
        outputs = model(**batch)
        loss = outputs.loss
        total_train_loss += loss.item()

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

    avg_train_loss = total_train_loss / len(train_loader)
    print(f"Epoch {epoch + 1}, Training Loss: {avg_train_loss}")


model.eval()
total_val_loss = 0
correct_predictions = 0

with torch.no_grad():
    for batch in tqdm(val_loader):
        batch = {k: v.to(device) for k, v in batch.items()}  # Move batch to GPU if available

        # Forward pass
        outputs = model(**batch)
        loss = outputs.loss
        logits = outputs.logits

        total_val_loss += loss.item()
        # Convert logits to predictions
        predictions = torch.argmax(logits, dim=-1)
        print("logits is ", logits)
        print("prediction is ", predictions)
        correct_predictions += (predictions == batch["labels"]).sum().item()

avg_val_loss = total_val_loss / len(val_loader)
accuracy = correct_predictions / len(val_texts)
print(f"Validation Loss: {avg_val_loss}")
print(f"Validation Accuracy: {accuracy}")

model.save_pretrained("sentiment_classifier_model")
tokenizer.save_pretrained("sentiment_classifier_model")
