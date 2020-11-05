import praw
import time
import pandas as pd
import nltk
import requests
import json
import csv
import time
import datetime
import graphs
import re
import unicodedata
import wordcloud
import os
import seaborn as sns
import config
import matplotlib.pyplot as plt
import imgurpython
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from imgurpython import ImgurClient
from pprint import pprint
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from random import choice
from operator import itemgetter
reddit = praw.Reddit(user_agent='',
                  client_id='',
                  client_secret='',
                  username='',
                  password='')


currdir = path.dirname(__file__)

def addToSubredditList(subredditList, thing):
    '''
    If the subreddit exists in the list, increment the count by one.
    If the subreddit doesn't exist in the list, add the subreddit and set the count as 1.
    '''
    for subreddits in subredditList:
        if subreddits['Subreddit Name'] == thing.subreddit:
            subreddits['Count'] += 1
            break
    else:
        subredditList.append({'Subreddit Name': thing.subreddit, 'Count': 1})
    return subredditList

def mergeSubredditLists(comment, submission):
    '''
    Merge the two lists:
    If a subreddit in the second list already exists in the first list, the count of that subreddit is added to its counterpart in the first list.
    If a subreddit does not exist, it along with its count is added to the end of the list.
    Return the new list
    '''
    subredditList = comment
    for subreddit in submission:
        for subs in subredditList:
            if subreddit['Subreddit Name'] == subs['Subreddit Name']:
                subs['Count'] += subreddit['Count']
                break
        else:
            subredditList.append(subreddit)
    return subredditList


def getCommentData(redditor):
    '''
    Iterate through every available comment posted by the user and store each comment's text.
    Then pass the comment to addToSubredditList() to increment the counter for each subreddit's activity.
    Return both the list of comments and the subredditList.
    '''
    comment_List = []
    subreddit_List = []
    for comments in redditor.comments.new(limit=None):
        comment_List.append(comments.body)
        subreddit_List = addToSubredditList(subreddit_List, comments)
    return comment_List, subreddit_List

def getSubmissionData(redditor):
    '''
    Analyze every submission made by the redditor in descending order of karma. Add the text of each selfpost to the end of the list.
    Also count the number of links submitted.
    Call addToSubredditList() to increment or set up the counter.
    Return both the list of selfposts and the subredditList
    '''
    subreddit_List = []
    submission_List = []
    noLinks = 0
    for submissions in redditor.submissions.top('all'):
        if submissions.is_self:
            submission_List.append(submissions.selftext)
        else:
            if(submissions.selftext):
                submission_List.append(submissions.selftext)
            noLinks += 1
        subreddit_List = addToSubredditList(subreddit_List, submissions)
    return subreddit_List, submission_List, noLinks

def getWordFrequencyList(commentList):
    '''
    Create a regex expression to consider only alphanumeric characters I.E. remove special characters.
    For every comment made by the user split the comment into a list of individual words separated by spaces.
    For every word in the list, convert it to lower case and check if it is in the common word list. if yes, ignore it.
    If it isn't a common word, confirm that it has actual alphabets or numbers and add it to the list.
    Check if the word exists in the frequencyList, if yes increment its count.
    If it isn't in the list, add it to the list and give it a count of 1.
    Return the list after sorting in descending order.
    '''
    wordFile = open('commonWords.txt', 'r')
    commonWordsList = wordFile.read()
    wordFile.close()
    stripChars = re.compile(r'[a-zA-z0-9]+')
    frequencyList = []
    for comments in commentList:
        wordsList = comments.split(' ')
        for words in wordsList:
            words = words.lower()
            if words in commonWordsList:
                continue
            if(stripChars.search(words)):
                for existingWords in frequencyList:
                    if existingWords['Word'] == words:
                        existingWords['Count'] += 1
                        break
                else:
                    frequencyList.append({'Word': words.lower(), 'Count': 1})
    return sorted(frequencyList, key=itemgetter('Count'), reverse=True)

def getcomments(commentList):
    for comments in commentList:
        try:
            comments = unicodedata.normalize('NFKD', comments).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            # dirname = os.path.dirname(os.path.abspath(__file__))
            # csvfilename = os.path.join(dirname, "File" + ".txt")
            # file_exists = os.path.isfile(csvfilename)
            f = open('File.txt','a')
            f.write(comments)
        except BaseException as e:
            pass

def getcommentslinebyline(commentList):
    nltk.download('vader_lexicon')
    sia = SIA()
    a = ""
    results = []
    for comments in commentList:
        comments = unicodedata.normalize('NFKD', comments).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        pol_score = sia.polarity_scores(comments)
        pol_score['comment'] = comments
        results.append(pol_score)
        #pprint(results[:7], width=100)
    df1 = pd.DataFrame.from_records(results)
    df1['label'] = 0
    df1.loc[df1['compound'] > 0.2, 'label'] = 1
    df1.loc[df1['compound'] < -0.2, 'label'] = -1
    df1.head()
    sns.set(style='darkgrid', context='talk', palette='Dark2')
    fig, ax = plt.subplots(figsize=(8, 8))
    counts = df1.label.value_counts(normalize=True) * 100
    sns.barplot(x=counts.index, y=counts, ax=ax)
    ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
    ax.set_ylabel("Percentage")
    plt.savefig('sentiment.png')  


def imgurBot():
    client = ImgurClient(config.imgurId, config.imgurSecret)
    frequencyLink = (client.upload_from_path('wordFrequency.png', config=None, anon=True))['link']
    activityLink = (client.upload_from_path('mostActive.png', config=None, anon=True))['link']
    wordcloudLink = (client.upload_from_path('wc.png', config=None, anon=True))['link']
    sentimentLink = (client.upload_from_path('sentiment.png', config=None, anon=True))['link']
    return frequencyLink, activityLink, wordcloudLink, sentimentLink



def results(username):
    r = reddit.redditor(username)
    commentList, subredditListForComments = getCommentData(r)

    getcommentslinebyline(commentList)

    subredditListForSubmissions, submissionList, noLinks = getSubmissionData(r)
    subredditList = mergeSubredditLists(subredditListForComments, subredditListForSubmissions)
    noComments = len(commentList)
    noPosts = len(submissionList)

    getcomments(commentList)
    file_content=open ("File.txt").read()
    graphs.create_wordcloud(file_content)
    open('File.txt', 'w').close()
    frequencyList = getWordFrequencyList(commentList) + getWordFrequencyList(submissionList)
    graphs.wordFrequencyGraph(frequencyList[:10], noPosts + noComments)
    graphs.mostActiveChart(subredditList)
    frequencyLink, activityLink, wordcloudLink, sentimentLink = imgurBot()
    message = ('''Hey, I got stats of **/u/%s**! Thanks for calling me. These are the things i found:
\nI've found about **%s** comments and **%s** posts, **%s** of which were links. This makes for a total of **%s** submissions. That's awesome!
\nI've found out the most words that you have used and made a graph [Most Used Words](%s)\n
Also here are is a graph which shows where you spend the majority of your time! [Activity Graph](%s)
I also collected most used words and displayed it! [Word cloud](%s)
Plus i made a sentiment analysis chart [Click here to check out that chart.](%s)
\n\n---
[^(Message my Master)](https://www.reddit.com/message/compose?to=Nathuphoon) ^| [^(Source Code)](https://github.com/ArjunPrasadSarkhel) ^| [^(Credits for inspiration~)](https://github.com/akashsara)
    ''' %(username, noComments, noPosts, noLinks, noComments + noPosts, frequencyLink, activityLink, wordcloudLink, sentimentLink))
    return message

def runBot(reddit):
    subredditList = ['Botchecker', 'testingground4bots','AskReddit','pics','funny','memes','india','Indiangaming','redditdev','programming','indiandevs','pythoncoding','PythonProjects2','coding']
    keyWords = ['!Givestats', '!givestats', '!GiveStats', '!GIVESTATS', '!givestatS', '!GiveSTats']
    for subreddit in subredditList:
        print('Im on this subreddit -- ' + str(subreddit))
        for comment in reddit.subreddit(subreddit).comments(limit=None):
            if comment.saved:
                continue
            for keyWord in keyWords:
                if (keyWord in comment.body) and (comment.author != reddit.user.me()):
                    comment_id = comment
                    comment = reddit.comment(comment_id)
                    print(comment.body)
                    print(len(comment.body))
                    if(len(comment.body)>13):
                        # print(type(comment.body))
                        print("inside")
                        invalid_user_check=0
                        commentbodyauthor= comment.body
                        commentbodyauthor = commentbodyauthor.lower()
                        commentbodyauthor= commentbodyauthor.split("!givestats",1)[1]
                        # print(commentbodyauthor)
                        try:
                            message = results(str(commentbodyauthor))
                        except BaseException as e:
                            comment.reply("Make sure this user exists!! I can provide you more info then :D")
                            comment.save()
                            invalid_user_check = 1                       
                        if(invalid_user_check==0):
                            comment.reply(message)
                            comment.save()
                            print('Replied to post')
                    else:
                        
                        # if (keyWord in comment.body) and (comment.author != reddit.user.me()):
                             print("in single")
                             print('Found a post ' + str(comment.id) + ' by ' + str(comment.author))
                             message = results(str(comment.author))
                             comment.reply(message)
                             comment.save()
                             print('Replied to post!')


while True:
    runBot(reddit)
    time.sleep(300)
