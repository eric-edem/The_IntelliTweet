import pandas as pd
import numpy as np
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    confusion_matrix,
)
from sklearn.ensemble import RandomForestClassifier
from zprops.featureSelectionResults import selected_columns, augmentation_columns
from src.utils import plotting

def select_samples_randomized(df, label_column, labels_to_select, num_samples_per_label=2000):
    selected_samples = pd.DataFrame()

    for label in labels_to_select:
        label_samples = df[df[label_column] == label]
        if len(label_samples) <= num_samples_per_label:
            selected_samples = pd.concat([selected_samples, label_samples])
        else:
            selected_samples = pd.concat([selected_samples, label_samples.sample(n=num_samples_per_label, random_state=1)])

    return selected_samples

def dataAugmentation(data):
    dff = data[data["Tweet_Label"] != 0]
    d1 = data[data["Tweet_Label"] != 0]
    d2 = data[data["Tweet_Label"] == 0]


    dff = dff[augmentation_columns]
    np.random.seed(42)

    for j, i in enumerate(dff.columns):
        if dff[i].dtype.kind == 'i':
            count = 0
            for row in dff[i].values:
                x = np.random.randint(-5, 5)
                val = row + x

                if val < 0:
                    x = np.random.randint(0, 3)
                    val = row + x
                dff.iloc[count, j] = val
                count = count + 1

    d1[augmentation_columns] = dff.values
    data = pd.concat([d2, d1], ignore_index=True)


    return data

def split_data(data):
    x_feat = data[selected_columns].drop(columns=["Tweet_Label"])

    x_feat['sentiment_label'] = x_feat['sentiment_label'].replace(['Negative', 'Positive'], [1, 0])
    y_feat = data[["Tweet_Label"]]

    x_featt = x_feat.to_numpy()
    y_featt = y_feat.to_numpy()

    return x_feat, x_featt, y_feat, y_featt

def train_and_evaluate_model(x_train, y_train, x_test, y_test):
    clf = RandomForestClassifier(criterion="gini", max_features="log2", n_estimators=270, random_state=0)
    theIntellitweet = clf.fit(x_train, y_train)
    theIntellitweet_y_pred = theIntellitweet.predict(x_test)

    # print("Ytes",y_test)
    Sent_Accuracy = accuracy_score(y_test.replace([0, 1, 2], [0, 1, 0]), theIntellitweet_y_pred)
    Sent_Recall = recall_score(y_test.replace([0, 1, 2], [0, 1, 0]), theIntellitweet_y_pred, average='macro')
    Sent_Precision = precision_score(y_test.replace([0, 1, 2], [0, 1, 0]), theIntellitweet_y_pred, average='macro')
    Sent_F1 = f1_score(y_test.replace([0, 1, 2], [0, 1, 0]), theIntellitweet_y_pred, average='macro')

    Sent_cmx = confusion_matrix(y_test.replace([0, 1, 2], [0, 1, 0]), [0 if x == 2 else x for x in theIntellitweet_y_pred], labels=[1, 0])
    print(plotting.plot_confusion_matrix(Sent_cmx, classes=['malicious=1', 'non-malicious=0'], normalize=False,title='Confusion matrix without '))

    return Sent_Accuracy, Sent_Recall, Sent_Precision, Sent_F1, Sent_cmx


def main():
    # Load your data (Tweet_data1) here
    Tweet_data1 = pd.read_csv("zprops/Tweets_.csv")

    # Preprocessing
    data = select_samples_randomized(Tweet_data1, 'Tweet_Label', [0, 1, 2], num_samples_per_label=2000)
    data = dataAugmentation(data)

    data = data[selected_columns]

    # Split data into features and labels
    x_train, xx, y_train, yy = split_data(data)
    feature_columns = data.drop(columns=["Tweet_Label"]).columns  # Get the column names from your DataFrame

    # Initialize RepeatedStratifiedKFold
    rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)

    for train_index, test_index in rskf.split(xx, yy):

        x_test = xx[test_index]
        y_test = yy[test_index]
        x_train_split = xx[train_index]
        y_train_split = yy[train_index]

        # Create DataFrames for x_test and x_train_split with correct column names
        x_test = pd.DataFrame(x_test, columns=feature_columns)
        x_train_split = pd.DataFrame(x_train_split, columns=feature_columns)
        y_test = pd.DataFrame(y_test, columns=y_train.columns).replace([0, 1, 2], [0, 1, 0])
        y_train_split = pd.DataFrame(y_train_split, columns=y_train.columns).replace([0, 1, 2], [0, 1, 0])


        # Train and evaluate the model
        Sent_Accuracy, Sent_Recall, Sent_Precision, Sent_F1, Sent_cmx = train_and_evaluate_model(x_train_split, y_train_split, x_test, y_test)
        print(Sent_Accuracy, Sent_Recall, Sent_Precision, Sent_F1, Sent_cmx)

        # Print or save evaluation metrics as needed

    # Calculate and print the average confusion matrix here


