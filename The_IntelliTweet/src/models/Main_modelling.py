# main.py

from data_processing import load_data, preprocess_data, split_data
from src.utils.plotting import plot_word_cloud, plot_confusion_matrix
from Modelling import MyRandomForestClassifier

# Load and preprocess data
data = load_data("your_data.csv")
preprocessed_data = preprocess_data(data)
X_train, X_test, y_train, y_test = split_data(preprocessed_data, test_size=0.2, random_state=42)

# Train a model
rf_classifier = MyRandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.train(X_train, y_train)

# Make predictions
y_pred = rf_classifier.predict(X_test)

# Calculate and print evaluation metrics
accuracy, precision, recall, f1, report = calculate_metrics(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")
print(report)

# Generate and display plots
plot_word_cloud(text_data)
plot_confusion_matrix(confusion_matrix, classes=['class1', 'class2'])
