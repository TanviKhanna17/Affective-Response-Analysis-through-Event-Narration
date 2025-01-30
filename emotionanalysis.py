import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from transformers import AutoTokenizer, AutoModel
from tqdm.notebook import tqdm
from torch.optim import Adam


# Model definition
class EmotionClassifier(nn.Module):
    def __init__(self, transformer, num_classes):
        super(EmotionClassifier, self).__init__()
        self.transformer = transformer
        self.dropout = nn.Dropout(0.2)
        self.fc1 = nn.Linear(transformer.config.hidden_size, 256)
        self.fc2 = nn.Linear(256, 128)
        self.out = nn.Linear(128, num_classes)

    def forward(self, input_ids, attention_mask):
        transformer_output = self.transformer(input_ids=input_ids, attention_mask=attention_mask)
        cls_token = transformer_output.last_hidden_state[:, 0, :]
        x = self.dropout(torch.relu(self.fc1(cls_token)))
        x = self.dropout(torch.relu(self.fc2(x)))
        return self.out(x)


def test_emotion_classifier(sentences):
    # Load model and tokenizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained('albert-base-v2')
    transformer_model = AutoModel.from_pretrained('albert-base-v2')
    
    model = EmotionClassifier(transformer_model, num_classes=13).to(device)
    model.load_state_dict(torch.load("emotion_classifier_model.pth", map_location=device))
    model.eval()

    # Sentiment mapping
    id_to_sent = {0: "empty", 1: "sadness", 2: "enthusiasm", 3: "neutral", 
                  4: "worry", 5: "surprise", 6: "love", 7: "fun", 
                  8: "hate", 9: "happiness", 10: "boredom", 11: "relief", 12: "anger"}

    # Encode sentences
    def encode_text(text):
        encoding = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
            return_attention_mask=True
        )
        return encoding['input_ids'].to(device), encoding['attention_mask'].to(device)

    # Predict emotions
    results = []
    with torch.no_grad():
        for sentence in sentences:
            input_ids, attention_mask = encode_text(sentence)
            output = model(input_ids, attention_mask)
            probabilities = torch.softmax(output, dim=1).cpu().numpy()[0]
            
            # Map probabilities to emotions and sort in descending order
            sorted_emotions = sorted(
                [(id_to_sent[idx], prob) for idx, prob in enumerate(probabilities)],
                key=lambda x: x[1], 
                reverse=True
            )

            results.append({
                'sentence': sentence, 
                'sorted_emotions': sorted_emotions
            })
    
    return results

