import torch
import numpy
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import LongformerForSequenceClassification, LongformerTokenizer, PreTrainedModel
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from transformers import AdamW
from tqdm import tqdm
from torch import nn


def to_bin(val):
    if type(val) == str:
        val = int(val)

    b = bin(val)
    b_i = b.index("b")
    b_v = b[b_i+1:]
    while True:
        if len(b_v) < 4:
            b_v = "0" + b_v
        else:
            break
    b_v = list(b_v)
    b_v = [int(i) for i in b_v]
    return b_v


def convert_label(val):
    if type(val) == str:
        val = int(val)
    # if val == 7:
    #     return [0, 0, 0, 1]
    # elif val == 8:
    #     return [0, 0, 1, 0]
    # elif val == 9:
    #     return [0, 1, 0, 0]
    # else:
    #     return [1, 0, 0, 0]
    return val - 7

def transfrom_data_from_database(data_from_database, label):
    data = []
    labels: torch.tensor
    for entry in data_from_database:
        cv, overview = entry
        data.append(cv+overview)
    # labels = torch.tensor(label, (len(data), ))
    # labels = numpy.array([int(label)] * len(data))

    # labels = [to_bin(label)] * len(data)
    labels = [convert_label(label)] * len(data)

    # labels_tensor = torch.tensor(labels, dtype=torch.float32)
    # # labels = torch.tensor(labels, dtype=torch.float32)
    # print("labels:")
    # print(labels_tensor)
    return data, labels


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


class MultiClassLongformer(PreTrainedModel):
    def __init__(self, model_name='allenai/longformer-base-4096', num_labels=4):
        super(MultiClassLongformer, self).__init__(config=LongformerForSequenceClassification.from_pretrained(model_name).config)
        self.model = LongformerForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    def forward(self, input_ids, attention_mask=None):
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        return logits