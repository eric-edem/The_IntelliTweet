import torch
from torch.utils.data import DataLoader
from transformers import BertForSequenceClassification, BertTokenizer, AdamW
from sklearn.model_selection import train_test_split


def load_data(bert_intent_train4):
    # Load and preprocess your training data
    return list(zip(bert_intent_train4["Full_Text"], bert_intent_train4['Tweet_Label']))


def prepare_datasets(texts, intents):
    train_texts, val_texts, train_intents, val_intents = train_test_split(texts, intents, test_size=0.2,
                                                                          random_state=42)
    return train_texts, val_texts, train_intents, val_intents


def tokenize_texts(texts):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    tokenized_texts = tokenizer(texts, padding='max_length', truncation=True, max_length=128, return_tensors='pt')
    return tokenized_texts


def create_data_loaders(train_texts, val_texts, train_intents, val_intents, batch_size=32):
    train_tokenized_texts = tokenize_texts(train_texts)
    val_tokenized_texts = tokenize_texts(val_texts)

    train_dataset = torch.utils.data.TensorDataset(train_tokenized_texts['input_ids'],
                                                   train_tokenized_texts['attention_mask'],
                                                   torch.tensor(train_intents))
    val_dataset = torch.utils.data.TensorDataset(val_tokenized_texts['input_ids'],
                                                 val_tokenized_texts['attention_mask'],
                                                 torch.tensor(val_intents))

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    return train_loader, val_loader


def train_intent_model(train_loader, val_loader, intent_labels):
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(intent_labels))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    optimizer = AdamW(model.parameters(), lr=2e-5)
    num_epochs = 3

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        for input_ids, attention_mask, intents in train_loader:
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            intents = intents.to(device)
            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask=attention_mask, labels=intents)
            loss = outputs.loss
            train_loss += loss.item()
            loss.backward()
            optimizer.step()

        model.eval()
        val_loss = 0.0
        correct_predictions = 0
        total_predictions = 0
        with torch.no_grad():
            for input_ids, attention_mask, intents in val_loader:
                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)
                intents = intents.to(device)
                outputs = model(input_ids, attention_mask=attention_mask, labels=intents)
                loss = outputs.loss
                val_loss += loss.item()
                logits = outputs.logits
                _, predicted_labels = torch.max(logits, dim=1)
                correct_predictions += (predicted_labels == intents).sum().item()
                total_predictions += len(intents)

        train_loss /= len(train_loader)
        val_loss /= len(val_loader)
        accuracy = correct_predictions / total_predictions * 100

        print(f'Epoch {epoch + 1}/{num_epochs}:')
        print(f'Train Loss: {train_loss:.4f}')
        print(f'Val Loss: {val_loss:.4f}')
        print(f'Accuracy: {accuracy:.2f}%')
        print('-------------------')

    return model
