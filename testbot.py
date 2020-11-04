import praw, re, requests, os, time



#Functions to get karma by subreddit for comments and posts separately and then combine them
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

#Functions for retrieving data
def getCommentData(redditor):
    '''
    Iterate through every available comment posted by the user and store each comment's text.
    Then pass the comment to addToSubredditList() to increment the counter for each subreddit's activity.
    Return both the list of comments and the subredditList.
    '''
    commentList = []
    subredditList = []
    for comments in redditor.comments.new(limit=None):
        commentList.append(comments.body)
        subredditList = addToSubredditList(subredditList, comments)
    return commentList, subredditList

def getSubmissionData(redditor):
    '''
    Analyze every submission made by the redditor in descending order of karma. Add the text of each selfpost to the end of the list.
    Also count the number of links submitted.
    Call addToSubredditList() to increment or set up the counter.
    Return both the list of selfposts and the subredditList
    '''
    subredditList = []
    submissionList = []
    noLinks = 0
    for submissions in redditor.submissions.top('all'):
        if submissions.is_self:
            submissionList.append(submissions.selftext)
        else:
            if(submissions.selftext):
                submissionList.append(submissions.selftext)
            noLinks += 1
        subredditList = addToSubredditList(subredditList, submissions)
    return subredditList, submissionList, noLinks

#Word frequency analysis and graph creation functions


#Driver functions


def executeOrder66(username):
    r = reddit.redditor(username)
    commentList, subredditListForComments = getCommentData(r)
    subredditListForSubmissions, submissionList, noLinks = getSubmissionData(r)
    subredditList = mergeSubredditLists(subredditListForComments, subredditListForSubmissions)
    noComments = len(commentList)
    noPosts = len(submissionList)
    message = ('''Hi **/u/%s**! Thanks for calling me. Here's what I've got for you:
\nI've found about **%s** comments and **%s** posts, **%s** of which were links. This makes for a total of **%s** submissions. Great job!
\nI've also taken the liberty of analysing your frequently used words and made a handy chart! [Click here to check it out.](%s)\nAnd since I like making charts, I even made one to show where you spend the majority of your time! [Click here to check out that chart.](%s)
\n\n---
[^(Message my Master)](https://www.reddit.com/message/compose?to=DarkeKnight) ^| [^(Source Code)](https://github.com/akashsara/reddit-comment-analysis-bot)
    ''' %(username, noComments, noPosts, noLinks, noComments + noPosts))
    return message

def runBot(reddit):
    subredditList = ['Botchecker']
    keyWords = ['!!AnalyseMe', '!!AnalyzeMe', '!!analyseme', '!!ANALYSEME', '!!analyzeme', '!!ANALYZEME']
    for subreddit in subredditList:
        print('On ' + str(subreddit))
        for comment in reddit.subreddit(subreddit).comments(limit=None):
            if comment.saved:
                continue
            for keyWord in keyWords:
                if (keyWord in comment.body) and (comment.author != reddit.user.me()):
                    print('Found a post ' + str(comment.id) + ' by ' + str(comment.author))
                    message = executeOrder66(str(comment.author))
                    comment.reply(message)
                    comment.save()
                    print('Replied to post!')

reddit = praw.Reddit('Reddit Bot', user_agent = 'Desktop:(by github.com/akashsara):Reddit Comment Analyzer Bot')

while True:
    runBot(reddit)
    time.sleep(300)