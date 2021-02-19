# Reddit_Bot_Data_Analysis

# In-Brief
### A bot when prompted, will show graphs about user-activity and information on reddit.


# About
 Hey all!! I made a reddit bot which uses Reddits own api called PRAW and imgurs api, when prompted will show your reddit details plus your reddit stats in graphs, i.e it includes your most used words, the top 10 subreddits where you had spent most of your time, made a word-cloud which shows your most used words, plus a sentiment analysis graph of your comments!!
The bot is currently deployed on Heroku and runs with a 5min cooldown after running through the list of subreddits I provided it.

# How to use it?
*  Enter your client id, client password, your reddit username & password on line 26.
*  After that enter your subreddit list where the bot will be active.
*  Then you just need to write **!Givestats**, this will show the stats of your profile
*  For other profile you need to write **!Givestats Username**, here Username is the reddit username of the person, you are trying to search. For eg: If i want to search a name Abcd, I'll write !Givestats Abcd.
* The result images, the bot will reply with an imgur link!!

# Using the bot to check your own stats:

 ![alt text](https://i.imgur.com/pMG3y6k.png)

# Using the bot to check another users stats:

 ![alt text](https://i.imgur.com/BsAAlD4.png)

# Most Used Words:-
 ![alt text](https://i.imgur.com/yagzMFd.png)

# Activity Graph:-
 ![alt text](https://i.imgur.com/pDOOnHk.png)

# Word Cloud:-
 ![alt text](https://i.imgur.com/V3CWqdm.png)

# Sentiment Analysis
![alt text](https://i.imgur.com/fQvjcW6.png)




 Feel free to use the bot, i want to credit https://github.com/akashsara, I took some reference from his code plus got the idea of imgur api implementation.

