import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class TextAnalyzer:
    def __init__(self):
        # Load the pre-trained BERT models and tokenizer
        self.tokenizer_sa = BertTokenizer.from_pretrained("bert-base-uncased", use_fast=True)

        # Load sentiment model
        self.model_sa = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

        # Define labels for sentiment analysis
        self.labels_sentiment = ['Negative', 'Positive']

        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer()

    def analyze_sentiment(self, text):

        # Tokenize the tweet text and convert to input features
        encoded_input = self.tokenizer_sa.encode_plus(text, padding='max_length', truncation=True, max_length=128,
                                                      return_tensors='pt')

        # Sentiment analysis
        with torch.no_grad():
            outputs_sentiment = self.model_sa(**encoded_input)
            logits_sentiment = outputs_sentiment.logits
        probabilities_sentiment = torch.softmax(logits_sentiment, dim=1).squeeze()
        sentiment_index = torch.argmax(probabilities_sentiment).item()
        sentiment_label = self.labels_sentiment[sentiment_index]

        return sentiment_label

    def calculate_subjectivity_polarity(self, text):

        inputs = self.tokenizer_sa.encode_plus(text, add_special_tokens=True, truncation=True, padding=True,
                                               return_tensors="pt")
        logits = self.model_sa(**inputs).logits
        probabilities = torch.softmax(logits, dim=1).squeeze(0)
        subjectivity = probabilities[1].item()
        polarity = probabilities[1].item() - probabilities[0].item()

        return subjectivity, polarity

    # def calculate_mean_tfidf(self, tweet_data):
    #
    #     tfidf_matrix = self.tfidf_vectorizer.fit_transform(
    #         tweet_data['Full_Text'].apply(self.processed_text)).toarray()
    #     reprocessed_texts = tweet_data['Full_Text'].apply(self.preprocess_text)
    #
    #     mean_tfidf_values = np.mean(tfidf_matrix, axis=1)
    #
    #     return mean_tfidf_values

    def calculate_mean_tfidf(self, tweet_data):
        # Preprocess the text column
        preprocessed_texts = tweet_data

        # Fit and transform the TF-IDF vectorizer
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(preprocessed_texts).toarray()

        # Calculate the mean TF-IDF values
        mean_tfidf_values = np.mean(tfidf_matrix, axis=1)

        return mean_tfidf_values

