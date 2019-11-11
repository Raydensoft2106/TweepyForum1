import re
import tweepy
from flask import Flask, render_template, request
from tweepy import OAuthHandler
from textblob import TextBlob
import private
import time
import matplotlib.pyplot as plt

app = Flask(__name__)


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = private.consumer_key
        consumer_secret = private.consumer_secret
        access_key = private.access_key
        access_secret = private.access_secret

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_key, access_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # saving other details of tweet
                parsed_tweet['text'] = tweet.text
                parsed_tweet['user'] = tweet.user.name
                parsed_tweet['user_statuses_count'] = tweet.user.statuses_count
                parsed_tweet['user_followers'] = tweet.user.followers_count
                parsed_tweet['user_location'] = tweet.user.location
                parsed_tweet['user_verified'] = tweet.user.verified
                parsed_tweet['fav_count'] = tweet.favorite_count
                parsed_tweet['rt_count'] = tweet.retweet_count
                parsed_tweet['tweet_date'] = tweet.created_at

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


# class TwitterClient2(object):
#     def __init__(self):
#         # keys and tokens from the Twitter Dev Console
#         consumer_key = private.consumer_key
#         consumer_secret = private.consumer_secret
#         access_key = private.access_key
#         access_secret = private.access_secret
#
#         try:
#             # create OAuthHandler object
#             self.auth = OAuthHandler(consumer_key, consumer_secret)
#             # set access token and secret
#             self.auth.set_access_token(access_key, access_secret)
#             # create tweepy API object to fetch tweets
#             self.api = tweepy.API(self.auth)
#         except:
#             print("Error: Authentication Failed")
#
#         def clean_tweet(self, tweet):
#             '''
#             Utility function to clean tweet text by removing links, special characters
#             using simple regex statements.
#             '''
#             return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

global Topic1
global Topic2


@app.route('/')
def hello_world():
    return render_template("index.html")


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    global Topic1, tweets, ptweets, ntweets, neutweets, \
        positive, negative, neutral, \
        PtweetsAvg, PtweetsFolList
    # calling function to get tweets
    tweets = api.get_tweets(query=Topic1, count=200)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    positive = (" Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # picking neutral tweets from tweets
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    negative = (" Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print(
        "Neutral tweets percentage: {} % \ ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))
    neutral = (
        "Neutral tweets percentage: {} % \ ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
        # print(tweet['user'])

    # for tweet in ptweets[:10]:
    #     PtweetsFolList = [int(tweet['user_followers'])]

    return Topic1, tweets, ptweets, ntweets, neutweets, positive, negative, neutral  # , PtweetsFolList


def main2():
    api = TwitterClient()
    global Topic2, tweets2, ptweets2, ntweets2, neutweets2, \
        positive2, negative2, neutral2, \
        PtweetsAvg2, PtweetsFolList2

    tweets2 = api.get_tweets(query=Topic2, count=200)

    ptweets2 = [tweet for tweet in tweets2 if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(ptweets2) / len(tweets2)))
    positive2 = (" Positive tweets percentage: {} %".format(100 * len(ptweets2) / len(tweets2)))

    ntweets2 = [tweet for tweet in tweets2 if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(ntweets2) / len(tweets2)))
    negative2 = (" Negative tweets percentage: {} %".format(100 * len(ntweets2) / len(tweets2)))

    neutweets2 = [tweet for tweet in tweets2 if tweet['sentiment'] == 'neutral']
    print("Neutral tweets percentage: {} % \ ".format(100 * (len(tweets2) - (len(ntweets2) + len(ptweets2))) / len(tweets2)))
    neutral2 = ("Neutral tweets percentage: {} % \ ".format(100 * len(neutweets2) / len(tweets2)))

    print("\n\nPositive tweets:")
    for tweet in ptweets2[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets2[:10]:
        print(tweet['text'])

    return Topic2, tweets2, ptweets2, ntweets2, neutweets2, positive2, negative2, neutral2


@app.route('/middle', methods=['POST', 'GET'])
def process():
    global Topic1
    global Topic2
    errors = ""

    if request.method == 'POST':
        Topic1 = None
        Topic2 = None
        try:
            Topic1 = request.form["Topic1"]
            Topic2 = request.form["Topic2"]
            main()
            main2()
        except:
            errors += "<p>{!r} is not a string.</p>\n".format(request.form["Topic1"])
            errors += "<p>{!r} is not a string.</p>\n".format(request.form["Topic2"])

        print(Topic1)
        #time.sleep(5)
        print(Topic2)
        #time.sleep(5)
        return render_template('middle.html', Topic1=Topic1, Topic2=Topic2)

    return 'Only access through POST request'


@app.route('/endpoint', methods=['POST', 'GET'])
def process2():
    if request.method == 'POST':
        #time.sleep(7.5)
        return render_template('endpoint.html', Topic1=Topic1, Topic2=Topic2, tweets=tweets,
                               ptweets=ptweets, ntweets=ntweets, neutweets=neutweets,
                               positive=positive, negative=negative, neutral=neutral,
                               tweets2=tweets2,
                               ptweets2=ptweets2, ntweets2=ntweets2, neutweets2=neutweets2,
                               positive2=positive2, negative2=negative2, neutral2=neutral2
                               )

    return 'Only accessible through POST method'


@app.route('/Button1')
def Button1():
    global tweets
    global ptweets
    global ntweets
    global neutweets

    # x-coordinates of left sides of bars
    left = [1, 2, 3]

    # heights of bars
    height = [len(ptweets), len(ntweets), len(neutweets)]

    # labels for bars
    tick_label = ['positive', 'negative', 'neutral']

    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['red', 'green'])

    # naming the x-axis
    plt.xlabel('x - axis')
    # naming the y-axis
    plt.ylabel('y - axis')
    # plot title
    plt.title('Bar chart for ' + Topic1 + ' Tweets!')

    # function to show the plot
    plt.show()


@app.route('/Button2')
def Button2():
    global tweets2
    global ptweets2
    global ntweets2
    global neutweets2

    # x-coordinates of left sides of bars
    left = [1, 2, 3]

    # heights of bars
    height = [len(ptweets2), len(ntweets2), len(neutweets2)]

    # labels for bars
    tick_label = ['positive', 'negative', 'neutral']

    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['red', 'green'])

    # naming the x-axis
    plt.xlabel('x - axis')
    # naming the y-axis
    plt.ylabel('y - axis')
    # plot title
    plt.title('Bar chart for ' + Topic2 + ' Tweets!')

    # function to show the plot
    plt.show()


if __name__ == '__main__':
    app.run(port=5001, debug=True)
