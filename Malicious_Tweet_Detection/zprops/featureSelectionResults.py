selected_columns = ['account_age', 'Follower Count', 'Following Count', 'User Favourite Count', 'noTweet', 'Retweet Count',
                        'no_hashtag', 'no_mentions', 'Tweet Favourite Count', 'no_digit', 'having_IP_Address', 'having_At_Symbol',
                        'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain',  'Domain_registeration_length', 'port',
                        'HTTPS_token', 'Request_URL', 'URL_of_Anchor', 'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow',
                        'Iframe', 'age_of_domain', 'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'subjectivity', 
                        'polarity', 'sentiment_label', 'TFIDF', 'Tweet_Label']

feature_columns = ['account_age', 'Follower Count', 'Following Count', 'User Favourite Count', 'noTweet', 'Retweet Count',
                        'no_hashtag', 'no_mentions', 'Tweet Favourite Count', 'no_digit', 'having_IP_Address', 'having_At_Symbol',
                        'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain',  'Domain_registeration_length', 'port',
                        'HTTPS_token', 'Request_URL', 'URL_of_Anchor', 'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow',
                        'Iframe', 'age_of_domain', 'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'subjectivity',
                        'polarity', 'sentiment_label', 'TFIDF']

augmentation_columns = ['account_age', 'Follower Count', 'Following Count',
                      'User Favourite Count', 'no_lists', 'noTweet']


prediction_prop = ['Malicious Tweet !', 'Non-malicious Tweet']
