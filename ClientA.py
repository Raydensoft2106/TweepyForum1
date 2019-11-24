import re
import tweepy
from flask import Flask, render_template, request
from tweepy import OAuthHandler
from textblob import TextBlob
import private

import matplotlib

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

plt.style.use('ggplot')

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
        PtweetsAvg, pTweetsFolList, nTweetsFolList, \
        neuTweetsFolList, topic1RTList, topic1StatusesList, topic1FolList
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

    # Take the followers value from each tweet in the positive tweets and place them into a list.
    pTweetsFolList = [tweet['user_followers'] for tweet in tweets if tweet['sentiment'] == 'positive']
    nTweetsFolList = [tweet['user_followers'] for tweet in tweets if tweet['sentiment'] == 'negative']
    neuTweetsFolList = [tweet['user_followers'] for tweet in tweets if tweet['sentiment'] == 'neutral']
    topic1FolList = [tweet['user_followers'] for tweet in tweets]  # This list can be used for totals/averages

    # Take the retweets value from each tweet in the positive tweets and place them into a list.
    pTweetsRTList = [tweet['user_followers'] for tweet in tweets if tweet['sentiment'] == 'positive']
    nTweetsRTList = [tweet['user_followers'] for tweet in tweets if tweet['sentiment'] == 'negative']
    neuTweetsRTList = [tweet['user_followers'] for tweet in tweets if tweet['sentiment'] == 'neutral']
    topic1RTList = [tweet['rt_count'] for tweet in tweets]  # This list can be used for totals/averages

    # Take the verfified? boolean value from each tweet in the positive tweets and place them into a list. SCATTER PLOT
    pTweetsVerList = [tweet['user_verified'] for tweet in tweets if tweet['sentiment'] == 'positive']
    nTweetsVerList = [tweet['user_verified'] for tweet in tweets if tweet['sentiment'] == 'negative']
    neuTweetsVerList = [tweet['user_verified'] for tweet in tweets if tweet['sentiment'] == 'neutral']
    topic1VerList = [tweet['user_verified'] for tweet in tweets]  # This list can be used for totals/averages
    topic1StatusesList = [tweet['user_statuses_count'] for tweet in tweets if tweet['user_verified'] == 'True']
    topic1StatusesListNV = [tweet['user_statuses_count'] for tweet in tweets if tweet['user_verified'] == 'False']

    return Topic1, tweets, ptweets, ntweets, neutweets, positive, negative, neutral, \
           pTweetsFolList, nTweetsFolList, neuTweetsFolList, topic1FolList, pTweetsRTList, \
           nTweetsRTList, neuTweetsRTList, topic1RTList, topic1StatusesList, topic1StatusesListNV


def main2():
    api = TwitterClient()
    global Topic2, tweets2, ptweets2, ntweets2, neutweets2, \
        positive2, negative2, neutral2, \
        PtweetsAvg2, PtweetsFolList2, topic2RTList, topic2FolList

    tweets2 = api.get_tweets(query=Topic2, count=200)

    ptweets2 = [tweet for tweet in tweets2 if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(ptweets2) / len(tweets2)))
    positive2 = (" Positive tweets percentage: {} %".format(100 * len(ptweets2) / len(tweets2)))

    ntweets2 = [tweet for tweet in tweets2 if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(ntweets2) / len(tweets2)))
    negative2 = (" Negative tweets percentage: {} %".format(100 * len(ntweets2) / len(tweets2)))

    neutweets2 = [tweet for tweet in tweets2 if tweet['sentiment'] == 'neutral']
    print("Neutral tweets percentage: {} % \ ".format(
        100 * (len(tweets2) - (len(ntweets2) + len(ptweets2))) / len(tweets2)))
    neutral2 = ("Neutral tweets percentage: {} % \ ".format(100 * len(neutweets2) / len(tweets2)))

    print("\n\nPositive tweets:")
    for tweet in ptweets2[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets2[:10]:
        print(tweet['text'])

    PtweetsFolList2 = [tweet['user_followers'] for tweet in tweets2 if tweet['sentiment'] == 'positive']
    nTweetsFolList2 = [tweet['user_followers'] for tweet in tweets2 if tweet['sentiment'] == 'negative']
    neuTweetsFolList2 = [tweet['user_followers'] for tweet in tweets2 if tweet['sentiment'] == 'neutral']
    topic2FolList = [tweet['user_followers'] for tweet in tweets2]  # This list can be used for totals/averages

    pTweetsRTList2 = [tweet['user_followers'] for tweet in tweets2 if tweet['sentiment'] == 'positive']
    nTweetsRTList2 = [tweet['user_followers'] for tweet in tweets2 if tweet['sentiment'] == 'negative']
    neuTweetsRTList2 = [tweet['user_followers'] for tweet in tweets2 if tweet['sentiment'] == 'neutral']
    topic2RTList = [tweet['rt_count'] for tweet in tweets2]  # This list can be used for totals/averages

    return Topic2, tweets2, ptweets2, ntweets2, neutweets2, positive2, negative2, neutral2, \
           PtweetsFolList2, nTweetsFolList2, neuTweetsFolList2, topic2FolList, pTweetsRTList2, \
           nTweetsRTList2, neuTweetsRTList2, topic2RTList


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
        # time.sleep(5)
        print(Topic2)
        # time.sleep(5)
        return render_template('middle.html', Topic1=Topic1, Topic2=Topic2)

    return 'Only access through POST request'


@app.route('/endpoint', methods=['POST', 'GET'])
def process2():
    if request.method == 'POST':
        # time.sleep(7.5)
        graph()
        return render_template('endpoint.html', Topic1=Topic1, Topic2=Topic2, tweets=tweets,
                               ptweets=ptweets, ntweets=ntweets, neutweets=neutweets,
                               positive=positive, negative=negative, neutral=neutral,
                               tweets2=tweets2, pTweetsFolList=pTweetsFolList,
                               nTweetsFolList=nTweetsFolList, neuTweetsFolList=neuTweetsFolList,
                               topic2RTList=topic2RTList, topic1RTList=topic1RTList,
                               topic1FolList=topic1FolList, topic2FolList=topic2FolList,
                               ptweets2=ptweets2, ntweets2=ntweets2, neutweets2=neutweets2,
                               positive2=positive2, negative2=negative2, neutral2=neutral2)

    return 'Only accessible through POST method'


@app.route('/graph')
def graph(chartID='chart_ID', chart_type='line', chart_height=500):
    global pTweetsFolList, nTweetsFolList
    if len(pTweetsFolList) < 10 or len(nTweetsFolList) < 10:
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
        series = [{"name": 'PtweetsFollowersCount', "data": [pTweetsFolList[0], pTweetsFolList[1], pTweetsFolList[2],
                                                             pTweetsFolList[3], pTweetsFolList[4]]},
                  {"name": 'NtweetsFollowersCount', "data": [nTweetsFolList[0], nTweetsFolList[1], nTweetsFolList[2],
                                                             nTweetsFolList[3], nTweetsFolList[4]]},
                  {"name": 'NeutweetsFollowersCount',
                   "data": [neuTweetsFolList[0], neuTweetsFolList[1], neuTweetsFolList[2],
                            neuTweetsFolList[3], neuTweetsFolList[4]]}]
        title = {"text": 'Follower Counts Per Sentiment - ' + Topic1}
        xAxis = {"categories": ['Tweet 1', 'Tweet 2', 'Tweet 3', 'Tweet 4', 'Tweet 5']}
        yAxis = {"title": {"text": 'Followers'}}

        return render_template('endpoint.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                               yAxis=yAxis, Topic1=Topic1, Topic2=Topic2, tweets=tweets,
                               ptweets=ptweets, ntweets=ntweets, neutweets=neutweets,
                               positive=positive, negative=negative, neutral=neutral,
                               tweets2=tweets2,
                               ptweets2=ptweets2, ntweets2=ntweets2, neutweets2=neutweets2,
                               positive2=positive2, negative2=negative2, neutral2=neutral2,
                               pTweetsFolList=pTweetsFolList, nTweetsFolList=nTweetsFolList,
                               neuTweetsFolList=neuTweetsFolList)

    elif len(pTweetsFolList) < 15 or len(nTweetsFolList) < 15:
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
        series = [{"name": 'PtweetsFollowersCount', "data": [pTweetsFolList[0], pTweetsFolList[1], pTweetsFolList[2],
                                                             pTweetsFolList[3], pTweetsFolList[4], pTweetsFolList[5],
                                                             pTweetsFolList[6], pTweetsFolList[7], pTweetsFolList[8],
                                                             pTweetsFolList[9]]},
                  {"name": 'NtweetsFollowersCount', "data": [nTweetsFolList[0], nTweetsFolList[1], nTweetsFolList[2],
                                                             nTweetsFolList[3], nTweetsFolList[4], nTweetsFolList[5],
                                                             nTweetsFolList[6], nTweetsFolList[7], nTweetsFolList[8],
                                                             nTweetsFolList[9]]},
                  {"name": 'NeutweetsFollowersCount',
                   "data": [neuTweetsFolList[0], neuTweetsFolList[1], neuTweetsFolList[2],
                            neuTweetsFolList[3], neuTweetsFolList[4], neuTweetsFolList[5],
                            neuTweetsFolList[6], neuTweetsFolList[7], neuTweetsFolList[8],
                            neuTweetsFolList[9]]}]
        title = {"text": 'Follower Counts Per Sentiment - ' + Topic1}
        xAxis = {"categories": ['Tweet 1', 'Tweet 2', 'Tweet 3', 'Tweet 4', 'Tweet 5', 'Tweet 6', 'Tweet 7', 'Tweet 8',
                                'Tweet 9', 'Tweet 10', 'Tweet 11', 'Tweet 12', 'Tweet 13', 'Tweet 14', 'Tweet 15']}
        yAxis = {"title": {"text": 'Followers'}}
        return render_template('endpoint.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                               yAxis=yAxis, Topic1=Topic1, Topic2=Topic2, tweets=tweets,
                               ptweets=ptweets, ntweets=ntweets, neutweets=neutweets,
                               positive=positive, negative=negative, neutral=neutral,
                               tweets2=tweets2,
                               ptweets2=ptweets2, ntweets2=ntweets2, neutweets2=neutweets2,
                               positive2=positive2, negative2=negative2, neutral2=neutral2,
                               pTweetsFolList=pTweetsFolList, nTweetsFolList=nTweetsFolList,
                               neuTweetsFolList=neuTweetsFolList)

    elif len(pTweetsFolList) > 15 or len(nTweetsFolList) > 15:
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
        series = [{"name": 'PtweetsFollowersCount', "data": [pTweetsFolList[0], pTweetsFolList[1], pTweetsFolList[2],
                                                             pTweetsFolList[3], pTweetsFolList[4], pTweetsFolList[5],
                                                             pTweetsFolList[6], pTweetsFolList[7], pTweetsFolList[8],
                                                             pTweetsFolList[9]]},
                  {"name": 'NtweetsFollowersCount', "data": [nTweetsFolList[0], nTweetsFolList[1], nTweetsFolList[2],
                                                             nTweetsFolList[3], nTweetsFolList[4], nTweetsFolList[5],
                                                             nTweetsFolList[6], nTweetsFolList[7], nTweetsFolList[8],
                                                             nTweetsFolList[9]]},
                  {"name": 'NeutweetsFollowersCount',
                   "data": [neuTweetsFolList[0], neuTweetsFolList[1], neuTweetsFolList[2],
                            neuTweetsFolList[3], neuTweetsFolList[4], neuTweetsFolList[5],
                            neuTweetsFolList[6], neuTweetsFolList[7], neuTweetsFolList[8],
                            neuTweetsFolList[9]]}]
        title = {"text": 'Follower Counts Per Sentiment - ' + Topic1}
        xAxis = {"categories": ['Tweet 1', 'Tweet 2', 'Tweet 3', 'Tweet 4', 'Tweet 5', 'Tweet 6', 'Tweet 7', 'Tweet 8',
                                'Tweet 9', 'Tweet 10', 'Tweet 11', 'Tweet 12', 'Tweet 13', 'Tweet 14', 'Tweet 15']}
        yAxis = {"title": {"text": 'Followers'}}
        return render_template('endpoint.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                               yAxis=yAxis, Topic1=Topic1, Topic2=Topic2, tweets=tweets,
                               ptweets=ptweets, ntweets=ntweets, neutweets=neutweets,
                               positive=positive, negative=negative, neutral=neutral,
                               tweets2=tweets2,
                               ptweets2=ptweets2, ntweets2=ntweets2, neutweets2=neutweets2,
                               positive2=positive2, negative2=negative2, neutral2=neutral2,
                               pTweetsFolList=pTweetsFolList, nTweetsFolList=nTweetsFolList,
                               neuTweetsFolList=neuTweetsFolList)


@app.route('/graph2')
def graph2(chartID='chart_ID2', chart_type='line', chart_height=500):
    global topic1RTList, topic2RTList
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    series = [{"name": 'topic1RTList', "data": [topic1RTList[0], topic1RTList[1], topic1RTList[2],
                                                topic1RTList[3], topic1RTList[4], topic1RTList[5],
                                                topic1RTList[6], topic1RTList[7], topic1RTList[8],
                                                topic1RTList[9], topic1RTList[10], topic1RTList[11],
                                                topic1RTList[12], topic1RTList[13], topic1RTList[14],
                                                topic1RTList[15], topic1RTList[16], topic1RTList[17],
                                                topic1RTList[18], topic1RTList[19]]},
              {"name": 'topic1RTList', "data": [topic2RTList[0], topic2RTList[1], topic2RTList[2],
                                                topic2RTList[3], topic2RTList[4], topic2RTList[5],
                                                topic2RTList[6], topic2RTList[7], topic2RTList[8],
                                                topic2RTList[9], topic2RTList[10], topic2RTList[11],
                                                topic2RTList[12], topic2RTList[13], topic2RTList[14],
                                                topic2RTList[15], topic2RTList[16], topic2RTList[17],
                                                topic2RTList[18], topic2RTList[19]]}]
    title = {"text": 'Retweet Counts Per Topic - ' + Topic1 + " & " + Topic2}
    xAxis = {"categories": ['Tweet 1', 'Tweet 2', 'Tweet 3', 'Tweet 4', 'Tweet 5', 'Tweet 6', 'Tweet 7', 'Tweet 8',
                            'Tweet 9', 'Tweet 10',
                            'Tweet 11', 'Tweet 12', 'Tweet 13', 'Tweet 14', 'Tweet 15', 'Tweet 16', 'Tweet 17',
                            'Tweet 18', 'Tweet 19', 'Tweet 20']}
    yAxis = {"title": {"text": 'Followers'}}
    return render_template('endpoint.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis, Topic1=Topic1, Topic2=Topic2, tweets=tweets,
                           ptweets=ptweets, ntweets=ntweets, neutweets=neutweets,
                           positive=positive, negative=negative, neutral=neutral,
                           tweets2=tweets2,
                           ptweets2=ptweets2, ntweets2=ntweets2, neutweets2=neutweets2,
                           positive2=positive2, negative2=negative2, neutral2=neutral2,
                           topic1RTList=topic1RTList, topic2RTList=topic2RTList)


@app.route('/scatterplot1')
def scatterplot1():  # chartID='chart_ID3', chart_type='scatter', chart_height=500):
    global topic1StatusesList, topic1FolList, topic1StatusesListNV
    followers_range = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
    plt.scatter(followers_range, topic1StatusesList[:, 0], color='r')
    plt.scatter(followers_range, topic1StatusesListNV[:, 0], color='g')
    plt.xlabel('Followers range')
    plt.ylabel('Followers')
    plt.show()


def Average(lst):
    return sum(lst) / len(lst)


@app.route('/avgPlot')
def avgPlot():
    global topic1FolList, topic2FolList, topic1RTList, topic2RTList
    figure(num=None, figsize=(65, 6), dpi=80, facecolor='w', edgecolor='k')
    x = ['Average '+Topic1+' Tweets Followers', 'Average Topic2 '+Topic2+' Tweets Folowers', 'Average '+Topic1+' User Retweets',
         'Average '+Topic2+' User Retweets']
    averages = [Average(topic1FolList), Average(topic2FolList), Average(topic1RTList), Average(topic2RTList)]

    x_pos = [i for i, _ in enumerate(x)]

    plt.bar(x_pos, averages, color='green')
    plt.xlabel(Topic1 + " & " + Topic2 + "Drill-down")
    plt.ylabel("Followers (1 & 2), Retweets (3 & 4)")
    plt.title("Average number of followers and retweets")
    plt.xticks(x_pos, x)
    plt.show()

    return render_template('endpoint.html', Topic1=Topic1, Topic2=Topic2, tweets=tweets,
                           ptweets=ptweets, ntweets=ntweets, neutweets=neutweets,
                           positive=positive, negative=negative, neutral=neutral,
                           tweets2=tweets2, pTweetsFolList=pTweetsFolList,
                           nTweetsFolList=nTweetsFolList, neuTweetsFolList=neuTweetsFolList,
                           topic2RTList=topic2RTList, topic1RTList=topic1RTList,
                           topic1FolList=topic1FolList, topic2FolList=topic2FolList,
                           ptweets2=ptweets2, ntweets2=ntweets2, neutweets2=neutweets2,
                           positive2=positive2, negative2=negative2, neutral2=neutral2)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
