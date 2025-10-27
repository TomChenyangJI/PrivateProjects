import torch
from transformers import LongformerTokenizer, LongformerForSequenceClassification
from transformers import Trainer, TrainingArguments
from datasets import load_dataset
from sklearn.model_selection import train_test_split
import numpy as np

# 1. Load the tokenizer and model
model_name = "allenai/longformer-base-4096"
tokenizer = LongformerTokenizer.from_pretrained(model_name)
model = LongformerForSequenceClassification.from_pretrained(model_name, num_labels=4)  # 4 labels for multi-label classification

# 2. Prepare your data
# For demonstration purposes, let's assume you have a dataset in CSV format with 'text' and 'labels' columns
# You can replace this with your actual dataset loading process

# For simplicity, assume `text_data` and `labels_data` are lists of strings and labels
text_data = ["Sample text 1", "Sample text 2", "Sample text 3"]  # Replace with your text data
labels_data = [[1, 0, 0, 1], [0, 1, 1, 0], [1, 1, 0, 0]]  # Example multi-label classification (4 labels)

# Split the data into train and test sets
train_texts, val_texts, train_labels, val_labels = train_test_split(text_data, labels_data, test_size=0.2)

# 3. Tokenize the text data
def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=4096)

train_encodings = tokenizer(train_texts, padding='max_length', truncation=True, max_length=4096)
val_encodings = tokenizer(val_texts, padding='max_length', truncation=True, max_length=4096)

# Convert labels to tensor
train_labels_tensor = torch.tensor(train_labels)
val_labels_tensor = torch.tensor(val_labels)

# 4. Create the dataset class
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

# 5. Create the train and validation datasets
train_dataset = CustomDataset(train_encodings, train_labels_tensor)
val_dataset = CustomDataset(val_encodings, val_labels_tensor)

# 6. Fine-tune the model
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # number of training epochs
    per_device_train_batch_size=4,   # batch size for training
    per_device_eval_batch_size=8,    # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    evaluation_strategy="epoch",     # evaluate every epoch
)

trainer = Trainer(
    model=model,                         # the instantiated 🤗 Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=val_dataset,            # evaluation dataset
)

# 7. Start training
trainer.train()

# 8. Evaluate the model (optional)
trainer.evaluate()
