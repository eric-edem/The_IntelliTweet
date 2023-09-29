from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def calculate_metrics(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    report = classification_report(y_true, y_pred)
    return accuracy, precision, recall, f1, report

def get_Confmetrics(Sent_CM):
    TN = Sent_CM[2][2] + Sent_CM[2][1] + Sent_CM[1][2] + Sent_CM[1][1]
    FN = Sent_CM[0][1] + Sent_CM[0][2]
    TP = Sent_CM[0][0]
    FP = Sent_CM[2][0] + Sent_CM[1][0]
    return TP, FP, TN, FN

def calculate_fpr(TP, FP, TN, FN):
    fpr = FP / (FP + TN)
    return fpr

def weighted_evaluation_metric(weights, precision, recall, f1_score, false_positive_rate):
    weights = {
        'precision': 0.4,
        'recall': 0.1,
        'f1_score': 0.1,
        'false_positive_rate': 0.4
    }
    weighted_precision = weights['precision'] * precision
    weighted_recall = weights['recall'] * recall
    weighted_f1_score = weights['f1_score'] * f1_score
    weighted_false_positive_rate = weights['false_positive_rate'] * false_positive_rate

    weighted_sum = weighted_precision + weighted_recall + weighted_f1_score - weighted_false_positive_rate

    return weighted_sum