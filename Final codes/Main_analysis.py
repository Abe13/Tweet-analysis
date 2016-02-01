print "Loading packages..."

import time
import datetime
import urllib2
import numpy as np
#from scipy import stats
import pandas as pd
#import statsmodels.api as sm
#from pylab import *
#import matplotlib.pyplot as plt
import twitter
import re
from twitter import Api
import tweepy
import cleaning_validating_algorithm as cl
from bs4 import BeautifulSoup
import urllib
import xlwt
import csv
from time import sleep;
from string import punctuation

"Initialization is done"

def query(q, minTime, maxTime, timeWindow):
    print "helloo"

 #    q=term1+"+"+term2 #query

    #time loop
    time=minTime
    print minTime
    print maxTime

    while (time<maxTime):
        timeL=time
        timeU=time+timeWindow
        time=time+timeWindow

        #finding the pagae number
        i=1
        link="http://topsy.com/s/"+q+"/tweet?maxtime="+str(timeU)+"&mintime="+str(timeL)+"&offset="+str((i-1)*10)+"&page="+str(i)
        search = urllib2.urlopen(link)
        html = search.read()
        soup = BeautifulSoup(html)
        try:
            pageNumText=soup.find('span',{"class":"page-number"}).text # the text is "...about page#" or "... of page#"
        except:
            pageNumText=" "

        if (pageNumText.find('about')!=-1):
            pageIndex=pageNumText.find('about')+6
        elif ((pageNumText.find('of')!=-1)):
            pageIndex=pageNumText.find('of')+3
        #finding the maximum page#
        try:
            page=int(pageNumText[pageIndex:])
        except:
            page=2


        #page loop
        for i in range (1,page):

            link="http://topsy.com/s/"+q+"/tweet?maxtime="+str(timeU)+"&mintime="+str(timeL)+"&offset="+str((i-1)*10)+"&page="+str(i)
            print link
            search = urllib2.urlopen(link)
            html = search.read()
            soup = BeautifulSoup(html)

            #print soup

            for body in soup.findAll('div',class_="twitter-post-big"):#The body loop


                for tweet in body.findAll('span',{"class":"twitter-post-text translatable language-en"}):#The tweets loop
                    a = tweet.text
                    myfile.write(a.encode("utf-8")+'\n')
                    print a,'\n'
                    ValidatedTweet=cl.cleanseTweet(a)
                    tweets.append(tweet.text)


def sentAna():
    worktable = xlwt.Workbook(encoding='utf-8')
    sheet = worktable.add_sheet("sheet1")
    # open the Positvie an Negative list
    posfh = open("posi.txt",'r')
    negfh = open("nega.txt",'r')
    count_neg = 0
    count_pos = 0
    #The list of result
    index =[]
    positive_words = [word.strip() for word in posfh ]
    negative_words = [word.strip() for word in negfh ]
    for line in tweets:
        count_pos = 0
        count_neg = 0
        a = line.split(' ')
        for i in a:
            if (i in positive_words):
                count_pos = count_pos +1
            if (i in negative_words):
                count_neg = count_neg +1

        ratio = (float(count_pos)-float(count_neg))/len(a)
        index.append((float(count_pos)-float(count_neg))/len(a))
        #print float(len(set(a)))/float(len(a))

    for i in range(1,len(index)):
        sheet.write(i-1,0,tweets[i-1])
        sheet.write(i-1,1,index[i-1])
    worktable.save("result2")
    Positive_Tweets = 0
    Negative_Tweets = 0
    Natural_Tweets = 0
    for ind in index:
        if (ind>0):
            Positive_Tweets +=1
        if (ind<0):
            Negative_Tweets +=1
        if(ind==0):
            Natural_Tweets +=1
    Positive_Com.append(Positive_Tweets)
    Negative_Com.append(Negative_Tweets)

    print "The Number of Positive Tweets = ",Positive_Tweets,'\n'
    print "The Number of Negative Tweets = ", Negative_Tweets,'\n'
    print "The Number of Natural Tweets = " ,Natural_Tweets,'\n'
    print "The total tweets = ", len(index)

    a = "\n\n\nThe Number of Positive Tweets = "+str(Positive_Tweets)+'\n'
    a=a+"The Number of Negative Tweets = "+str( Negative_Tweets)+'\n'
    a=a+"The Number of Natural Tweets = " +str(Natural_Tweets)+'\n'
    a=a+"The total tweets = "+str(len(index))

    myfile.write(a.encode("utf-8")+'\n')

# the main function
if __name__ == "__main__":
    Positive_Com = []
    Negative_Com = []
    tweets  = []
    sMin = "17/9/2012 01:01:26 GMT" # the beginning time for search. the format is "%d/%m/%Y"
    sMax = "25/9/2012 01:21:26 GMT" # the end date for search. the format is "%d/%m/%Y"

    timeWindow= 24*60*60 #one day duration - maybe we need to play with this time window to make sure that the number of tweets
    #is less than 1000

    minTime = int(time.mktime(datetime.datetime.strptime(sMin, "%d/%m/%Y %H:%M:%S GMT").timetuple()))#1348542000 #1346472000 #Sep 1 2012 12 AM
    maxTime = int(time.mktime(datetime.datetime.strptime(sMax, "%d/%m/%Y %H:%M:%S GMT").timetuple()))#1348628400 #1366603200 #Apr 22 2013 12 AM

    keyfile = open("keywords.txt",'r')
    keywords = [word.strip() for word in keyfile ]
    for q in keywords:

        #q="obama" # this is the query that program will search for. it could be like "obama" or "obama + president" and so on

        print "searching for ", q
        fname="Database/tweets_"+q+'_'+str(minTime)+'_'+str(maxTime)+".txt"
        myfile = open(fname,'w')

        a = "From = "+sMin+' - '+"To "+sMax+'\n'

        myfile.write(a.encode("utf-8")+'\n')



        query(q, minTime, maxTime, timeWindow)# The first argument is the keyword we want to search, and the second argument is the number of pages you need.
        sentAna()

        myfile.close()

    print "Finished"





