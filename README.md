# The_IntelliTweet
A Multifaceted Feature Approach to Detect Malicious Tweets
This repository corresponds to our research paper submitted to the FPS 2023 Conference under the title "IntelliTweet: a A Multifaceted Feature Approach to Detect Malicious Tweets".
  
  ## How to install
You are required to install the following Python packages: nltk, whois, tldextract, fake-useragent, BeautifulSoup, pyquery, dnspython, pandas, dns, bs4, scikit-learn version 1.0.2, and itertools.

  ## How to run
To use our Tweet Crawler, you'll need a Twitter Developer Account to access the API and authentication, which can be obtained at https://developer.twitter.com/en. For establishing Ground Truth, we utilized VirusTotal, available at https://www.virustotal.com/gui/home/url. If you wish to adopt a similar approach, you'll need to register with VirusTotal to gain access to their URL scan API. Once these prerequisites are in place, refer to the comments within the main file to get started.
  
  ## Settings
  All credentials can be saved in the `zprops/api_credentials` file for both VirusTotal and Tweepy.
   
  ## Main Modules
Indeed, these classes play pivotal roles within the project, as each serves a unique purpose that collaborates with other methods to enhance the overall functionality of your system.
   * class TwitterCrawller
   * class LinkVerifier
   * class CheckUrlFeature
   * class MyRandomForestClassifier
   * class TextAnalyzer

