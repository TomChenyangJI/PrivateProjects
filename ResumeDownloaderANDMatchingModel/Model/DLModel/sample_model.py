import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
from transformers import AdamW
from tqdm import tqdm

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

def get_sentence_embedding(text, model):
    return model.encode(text, convert_to_tensor=True)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

texts = ["I love this product", "Worst purchase ever", "Highly recommend it", "Not worth the money"]
labels = [1, 0, 1, 0]

train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2)

train_encodings = {'input_ids': [get_sentence_embedding(text, sentence_model) for text in train_texts]}
val_encodings = {'input_ids': [get_sentence_embedding(text, sentence_model) for text in val_texts]}
print(train_encodings)

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

    for batch in train_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        optimizer.zero_grad()

        print(batch.keys())
        input_ids = batch['input_ids'].long()
        attention_mask = batch["attention_mask"].long()
        # outputs = model(**batch)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=batch['labels'])
        loss = outputs.loss
        total_train_loss += loss.item()

        loss.backward()
        optimizer.step()

    avg_train_loss = total_train_loss / len(train_loader)
    print(f"Epoch {epoch + 1}, Training Loss: {avg_train_loss}")

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
print(f"Validation Loss: {avg_val_loss}")
print(f"Validation Accuracy: {accuracy}")
