import tweepy
import pandas as pd
import requests
from urlextract import URLExtract
from dateutil import parser
import datetime
import csv
from tld import get_tld

class TwitterCrawller:
    def __init__(self, api_key, api_key_secret, access_token, access_token_secret):
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def authenticate(self):
        # Authentication
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def extract_url(self, text):
        extractor = URLExtract()
        urls = extractor.find_urls(text)
        return urls

    def get_domain_length(self, url):
        res = get_tld(url, as_object=True)
        domain = res.fld
        return len(domain)

    def fetch_tweets(self, query, num_tweets):
        tweet_data = pd.DataFrame()
        count = 1
        my_data = []
        filtered_data = []
        filtered_data_b = []

        for tweet in tweepy.Cursor(self.api.search_tweets, q=query, tweet_mode='extended').items(num_tweets):
            if not tweet.retweeted and 'RT @' not in tweet.full_text:
                tweet.full_text = tweet.full_text.replace("hxxp", "http").replace("hXXp", "http").replace('[', "").replace(']', "")
                print(count, " : ", tweet.full_text)

                my_data.append([
                    tweet.user.screen_name,
                    tweet.full_text,
                    len(tweet.full_text),
                    tweet.user.created_at,
                    tweet.user.followers_count,
                    tweet.user.friends_count,
                    tweet.user.favourites_count,
                    tweet.retweet_count,
                    tweet.favorite_count
                ])

                links = []
                for item in self.extract_url(tweet.full_text):
                    try:
                        resp = requests.head(item)
                        print(count, ":", resp.headers["Location"])
                        links.append(resp.headers["Location"])
                    except:
                        links.append(item)

                countt = 0
                domlist = []
                Domain_length = []
                URL_COUNT = []

                for link in links:
                    dom_len = self.get_domain_length(link)
                    countt = countt + 1
                    Domain_length.append(dom_len)

                URL_COUNT.append(countt)

                for l in links:
                    urll = 'https://www.virustotal.com/vtapi/v2/url/report'
                    params = {'apikey': 'YOUR_VIRUSTOTAL_API_KEY', 'resource': l}
                    response = requests.get(urll, params=params)

                    hashcount = len(tweet.entities.get('hashtags'))
                    no_urls = len(self.extract_url(tweet.full_text))
                    countl = 0
                    countn = 0
                    counto = 0

                    for ele in tweet.full_text:
                        if ele.isalpha():
                            countl += 1
                        elif ele.isdigit():
                            countn += 1
                        else:
                            counto += 1

                    no_char = countl
                    no_digit = countn
                    no_men = len(tweet.entities.get('user_mentions'))

                    try:
                        dat = parser.parse(tweet.user.created_at)
                        account_age = (datetime.datetime.today().replace(tzinfo=None) - dat.replace(tzinfo=None)).days
                    except:
                        dat = parser.parse(str(tweet.user.created_at))
                        account_age = (datetime.datetime.today().replace(tzinfo=None) - dat.replace(tzinfo=None)).days

                    try:
                        yes = response.json().get("scans").items()
                        for key, value in yes:
                            for k, v in value.items():
                                if v == True:
                                    new_path = open("datasets/Verified_Phish_VirusTotal.csv", "a")
                                    z = csv.writer(new_path)
                                    z.writerow([l, list((key, value))])
                                    new_path.close()

                                    new_path2 = open("datasets/Verified_Phish_Links.csv", "a")
                                    zz = csv.writer(new_path2)
                                    zz.writerow([l])
                                    new_path2.close()

                                    print("url -> ", l, " : ", key, value)

                                    hashcount = len(tweet.entities.get('hashtags'))
                                    no_urls = len(self.extract_url(tweet.full_text))
                                    countl = 0
                                    countn = 0
                                    counto = 0

                                    for ele in tweet.full_text:
                                        if ele.isalpha():
                                            countl += 1
                                        elif ele.isdigit():
                                            countn += 1
                                        else:
                                            counto += 1

                                    no_char = countl
                                    no_digit = countn
                                    no_men = len(tweet.entities.get('user_mentions'))

                                    try:
                                        dat = parser.parse(tweet.user.created_at)
                                        account_age = (datetime.datetime.today().replace(tzinfo=None) - dat.replace(tzinfo=None)).days
                                    except:
                                        dat = parser.parse(str(tweet.user.created_at))
                                        account_age = (datetime.datetime.today().replace(tzinfo=None) - dat.replace(tzinfo=None)).days

                                    filtered_data.append([
                                        links,
                                        URL_COUNT,
                                        Domain_length,
                                        tweet.user.screen_name,
                                        tweet.full_text,
                                        len(tweet.full_text),
                                        tweet.user.created_at,
                                        account_age,
                                        tweet.user.followers_count,
                                        tweet.user.friends_count,
                                        tweet.user.favourites_count,
                                        tweet.user.listed_count,
                                        tweet.user.statuses_count,
                                        tweet.retweet_count,
                                        hashcount,
                                        no_men,
                                        no_urls,
                                        no_char,
                                        no_digit,
                                        tweet.favorite_count
                                    ])
                    except:
                        print(response.json().get("verbose_msg"))
                        filtered_data_b.append([
                            links,
                            URL_COUNT,
                            Domain_length,
                            tweet.user.screen_name,
                            tweet.full_text,
                            len(tweet.full_text),
                            tweet.user.created_at,
                            account_age,
                            tweet.user.followers_count,
                            tweet.user.friends_count,
                            tweet.user.favourites_count,
                            tweet.user.listed_count,
                            tweet.user.statuses_count,
                            tweet.retweet_count,
                            hashcount,
                            no_men,
                            no_urls,
                            no_char,
                            no_digit,
                            tweet.favorite_count
                        ])
                        continue

                count = count + 1

        # Create dataframes
        columns = ['URLs', 'URL Count', 'Domain length', 'User', 'Full_Text', 'Message Lenght', 'Date created', "account_age",
                   'Follower Count', 'Following Count', 'User Favourite Count', 'no_lists', 'noTweet', 'Retweet Count',
                   'no_hashtag', 'no_mentions', 'no_urls', 'no_char', 'no_digit', 'Tweet Favourite Count']

        df_ = pd.DataFrame(filtered_data, columns=columns)
        df__ = pd.DataFrame(filtered_data_b, columns=columns)

        tweet_data = tweet_data.append(df__, ignore_index=True)
        # tweet_data = tweet_data.append(df_, ignore_index=True)

        return (tweet_data)
