selected_columns = ['Message Lenght', 'account_age', 'Follower Count','Following Count', 'User Favourite Count','no_lists', 'Retweet Count',
                'no_hashtag', 'no_mentions','Tweet Favourite Count', 'no_digit', 'no_urls', 'having_IP_Address', 'having_At_Symbol', 
                'Prefix_Suffix', 'having_Sub_Domain',  'Domain_registeration_length', 'Request_URL', 'Google_Index',
                'URL_of_Anchor', 'Redirect', 'RightClick', 'popUpWidnow', 'Iframe', 'on_mouseover', 'Favicon', 'age_of_domain', 'DNSRecord',
                'web_traffic', 'Page_Rank', 'subjectivity', 'polarity', 'sentiment_label','TFIDF', 'Tweet_Label']

feature_columns = ['Message Lenght', 'account_age', 'Follower Count','Following Count', 'User Favourite Count','no_lists', 'Retweet Count',
                'no_hashtag', 'no_mentions','Tweet Favourite Count', 'no_digit', 'no_urls', 'having_IP_Address', 'having_At_Symbol', 
                'Prefix_Suffix', 'having_Sub_Domain',  'Domain_registeration_length', 'Request_URL', 'Google_Index',
                'URL_of_Anchor', 'Redirect', 'RightClick', 'popUpWidnow', 'Iframe', 'on_mouseover', 'Favicon', 'age_of_domain', 'DNSRecord',
                'web_traffic', 'Page_Rank', 'subjectivity', 'polarity', 'sentiment_label','TFIDF']

augmentation_columns = ['account_age', 'Follower Count', 'Following Count',
                      'User Favourite Count', 'no_lists']


prediction_prop = ['Malicious Tweet !', 'Non-malicious Tweet']
