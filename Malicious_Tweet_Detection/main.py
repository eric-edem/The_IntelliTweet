import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from zprops.featureSelectionResults import feature_columns, prediction_prop
from tests import validationIntellitweet
from data_collection.crawling_twitter import TwitterCrawller
from  src.feature_engineering.url_feature_extraction import CheckUrlFeature,run,fix_url
from src.models import textAnalyst, Modelling
from data_collection import text_preprocessor
from tldextract import extract
theIntellitweet = joblib.load('saved_models/intelliTweetModel.pkl')

# main.py
def run_Validate_IntelliTweet():
    return validationIntellitweet.main()
# run_Validate_IntelliTweet()

def read_api_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials

def read_path(file_path):
    path = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            path[key] = value
    return path


def main():
    #This portion crawls Twitter and fetches tweets
    
    #Read your API credentials from zprops file
    api_credentials_file = "zprops/api_credentials"
    api_credentials = read_api_credentials(api_credentials_file)
    api_key = api_credentials['API_KEY']
    api_key_secret = api_credentials['API_KEY_SECRET']
    access_token = api_credentials['ACCESS_TOKEN']
    access_token_secret = api_credentials['ACCESS_TOKEN_SECRET']

    # Crawl Twitter
    detector = TwitterCrawller(api_key, api_key_secret, access_token, access_token_secret)
    # detector.authenticate() #Uncommented this part once you have your credentials set up 

    # Define your keywords as a query and the number of tweets to fetch
    query = "phishing"  # Modify the query as needed
    num_tweets = 100  # Modify the number of tweets to fetch as needed

    # Fetch and analyze tweets using MaliciousTweetDetector
    # detector.fetch_tweets(query, num_tweets) #Uncommented this part once you have your credentials set up 

#Getting Twitter features
    # twitter_data = detector.fetch_tweets(query, num_tweets)  #Uncommented this part once you have your credentials set up 
    data_paths = read_path("zprops/paths")
    # value = data_paths['test_tweet_path']
    twitter_data = pd.read_csv('tests/single_tweet_test.csv') #For test purposes if you dont have twitter credentials

#Getting UrlFeatures
    url_tests = []
    for j, i in enumerate(list(twitter_data['URLs'])):
        print(i)
        try:
            if "http" not in i:
                trial = run(fix_url(i))
                print(trial)
                print(" ")
                url_tests.append(trial)
            else:

                trial = run(i)
                print(j, trial)
                print(" ")
                url_tests.append(trial)
        except:
            print('check Urls')
            continue

    twitter_Url_test1 = pd.DataFrame()

    for i, j in enumerate(url_tests):
        df_dictionary = pd.DataFrame([j])
        twitter_Url_test1 = pd.concat([twitter_Url_test1, df_dictionary], ignore_index=True)

    # print(twitter_Url_test1)
    print(list(twitter_data.Full_Text))

#Getting TextAnalysis Features
    # Analyze sentiment
    myTextAnalyst = textAnalyst.TextAnalyzer()

    sent = []
    sub = []
    pol = []

    for i in twitter_data['Full_Text']:
        i = text_preprocessor.preprocess_data(i)
        sentiment, (subjectivity, polarity) = myTextAnalyst.analyze_sentiment(i), myTextAnalyst.calculate_subjectivity_polarity(i)
        sent.append(sentiment)
        sub.append(subjectivity)
        pol.append(polarity)

    mean_tfidf_values = myTextAnalyst.calculate_mean_tfidf(
        twitter_data['Full_Text'].apply(text_preprocessor.preprocess_data))

    twitter_data['TFIDF'] = mean_tfidf_values.tolist()
    twitter_data['sentiment_label'] = sent
    twitter_data['subjectivity'] = sub
    twitter_data['polarity'] = pol

#Getting All Features
    resultdata = pd.concat([twitter_data, twitter_Url_test1], axis=1)
    print(resultdata)

#Model Prediction
    x_pred = resultdata[feature_columns]
    x_pred['sentiment_label'] = x_pred['sentiment_label'].replace(['Negative', 'Positive'], [1, 0])
    scale = StandardScaler()
    scaledX_pred = scale.fit_transform(x_pred)
    x_pred_ = pd.DataFrame(scaledX_pred, columns=feature_columns)
    y_pred_proba = theIntellitweet.predict_proba(x_pred_)
    y_pred  = theIntellitweet.predict(x_pred_)
    print(y_pred_proba)
    if y_pred ==1:
        print(prediction_prop[0])
    else:
        print(prediction_prop[1])


if __name__ == "__main__":
    main()
