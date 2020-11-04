import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from os import path
from operator import itemgetter
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#Set up the words as x and its count as y

currdir = path.dirname(__file__)

def wordFrequencyGraph(wordList, noSubmissions):
    x = []
    y = []
    for words in wordList:
        x.append(words['Word'])
        y.append(words['Count'])
    makeGraph(x, y, 'Number of Uses', 'Most Used Words in ' + str(noSubmissions) + ' Submissions', 'wordFrequency.png')

def create_wordcloud(text):
	# create numpy araay for wordcloud mask image
	mask = np.array(Image.open(path.join(currdir, "cloud.png")))

	# create set of stopwords	
	stopwords = set(STOPWORDS)

	# create wordcloud object
	wc = WordCloud(background_color="white",
					max_words=200, 
					mask=mask,
	               	stopwords=stopwords)
	
	# generate wordcloud
	wc.generate(text)

	# save wordcloud
	wc.to_file(path.join(currdir, "wc.png"))





#Subreddit Name = x, Activity Count = y
def mostActiveChart(subredditList):
    finalList = []
    x = []
    y = []
    subredditList = sorted(subredditList, key=itemgetter('Count'), reverse=True)
    try:
        for i in range(0, 10):
            finalList.append({'Subreddit Name': subredditList[i]['Subreddit Name'].display_name, 'Count': subredditList[i]['Count']})
        z = 0
        for i in range(10, len(subredditList)):
            z += subredditList[i]['Count']
        finalList.append({'Subreddit Name': 'Other', 'Count': z})
        finalList = sorted(finalList, key=itemgetter('Count'), reverse=True)
    except IndexError:
        finalList = subredditList
    for items in finalList:
        x.append(items['Subreddit Name'])
        y.append(items['Count'])
    makeGraph(x, y, 'Amount of Submissions', 'Activity Graph', 'mostActive.png')


def makeGraph(x, y, label, title, saveAs):
        fig, ax = plt.subplots()
        y_pos = np.arange(len(y))
        ax.barh(y_pos, y)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(x)
        ax.invert_yaxis()
        ax.set_xlabel(label)
        ax.set_title(title)
        plt.tight_layout()
        plt.savefig(saveAs)

def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off")
    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='salmon', 
    colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(text)