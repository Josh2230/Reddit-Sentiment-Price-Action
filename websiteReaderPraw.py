import praw
import time
from wordScanner import *
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import date
from threading import Thread
import matplotlib
import matplotlib.pyplot as plt
from chartplotter import *
import multiprocessing
from multiprocessing import Process, Queue


class PrawWebsiteReader():

    def __init__(self):
        self._mood = 0
        self._prevNum = 0

    def writeDataToCSV(self, comment):
        CSV = comment.split()
        with open('Comments.CSV', "a+") as f:
            for i in CSV:
                i = i.lower()
                f.write(i + ' ')
            f.write('\n')


    """ saveData method will take the sentiment, bulls vs bears, and the wordDictionary """
    def saveData(self, wordDict, sentiment):
        # current date for file
        currentDate = date.today()

        # with open('data.txt' , 'w') as f:
        with open("data.txt", "a+") as f:
            f.write(str(currentDate) + '\n')
            f.write('Sentiment: ' + str(sentiment) + '\n')
            f.write('Bulls: ' + str(wordDict.getBulls()) + '\n')
            f.write('Bears: ' + str(wordDict.getBears()) + '\n')
            f.write('WordDict: ' + str(wordDict.getWords()) + '\n\n')
            f.close()

    
    """ accesspage method will access reddit API and gain access the the specific subreddit and process all the comments """
    def accessPage(self, comment_queue):

        # download vader sentence sentiment calculator
        nltk.download('vader_lexicon')

        with open('pw.txt', 'r') as f:
                    pw = f.read()

        reddit = praw.Reddit(client_id='BZZItfJWqBgZr9FjRyQOYA',
                            client_secret='HQI7Qmt6F9oNPs1q9puvrpCk83OzZA',
                            username='Prestigious-Seat9337',
                            password=pw,
                            user_agent='MyRedditClient/0.1')

        # Get the subreddit object
        subreddit = reddit.subreddit('wallstreetbets')

        # Get the submission object using the URL
        submission = reddit.submission(url='https://www.reddit.com/r/wallstreetbets/comments/16n0rfh/what_are_your_moves_tomorrow_september_20_2023/')

        # Get a stream of comments from the subreddit
        comment_stream = subreddit.stream.comments()

        self.scanPage(comment_stream,comment_queue,submission)

    '''scanPage will handle taking all the live comments and passing it into the queue'''
    def scanPage(self,comment_stream,comment_queue,submission):


        # Keep track of the comments we have already processed
        processed_comments = []

        # keep a counter for the comments
        num = 0

        # create a object of the word dictionary
        wordScanner = WordDictionary()

        # create an object of sentiment analyzer
        vader = SentimentIntensityAnalyzer()

        # get a reference time when program is run
        startTime = time.time()

        # 5 minutes
        timeInterval = 300

        # overall mood counter
        overallMood = 0


        # # SAVE CODE FOR TESTING PURPOSES
        # while True:
        #     try:
        #         comment = []

        #         with open('Comments.CSV','r') as f:
        #             for line in f:
        #                 comment.append(line)
                    
        #         for i in comment:
        #         # Check if we haven't processed this comment before
        #             if i not in processed_comments:
        #                 num += 1
   
        #                 comment_queue.put(i)

        #                 wordScanner.findWords(i)

        #                 processed_comments.append(i)

        #                 wordScanner.getWordDict()

        #                 sentimentScores = vader.polarity_scores(i)

        #                 compoundScore = sentimentScores['compound']

        #                 self._mood += compoundScore

        #                 overallMood += compoundScore

        # REAL CODE
        while True:
            try:
                # Check if 5 minutes have passed
                elapsed_time = time.time() - startTime

                # Get the newest comment from the stream
                comment = comment_stream.__next__()
                
                ## REAL CODE FOR USE
                if comment.submission.id == submission.id:

                    # Check if we haven't processed this comment before
                    if comment.id not in processed_comments:
                        num += 1
                        # Print the comment body and add it to the list of processed comments
                        # print('*** COMMENT ***')
                        # print('comment ' + str(num) + ' ' + comment.body + '\n')

                        comment_queue.put(comment.body)

                        wordScanner.findWords(comment.body)

                        processed_comments.append(comment.id)

                        wordScanner.getWordDict()

                        sentimentScores = vader.polarity_scores(comment.body)

                        compoundScore = sentimentScores['compound']

                        self._mood += compoundScore

                        overallMood += compoundScore
                    
                        # calculate the 5 minute sentiment and overall sentiment every 5 minutes
                        if (elapsed_time >= timeInterval):
                            fiveMinAvg = self._mood/(num - self._prevNum)
                            overallAvg = overallMood/num
                            # print('*** 5 MINUTES PASSED ***')
                            # print('5 min sentiment: ' + str(fiveMinAvg))
                            # print('overall sentiment: ' + str(overallAvg) + '\n')

                            self._mood = 0

                            self._prevNum = num 

                            startTime = time.time()

            # handle exceptions
            except KeyboardInterrupt:
                
                self.saveData(wordScanner,overallAvg)

                # Stop the loop if the user presses Ctrl-C
                break
            except Exception as e:
                # Handle any other exceptions that might occur
                print(e)

# set up a method to scan comments
def scan_comments(comment_queue):
    reader = PrawWebsiteReader()
    reader.accessPage(comment_queue)

# set up a method to plot data
def plot_chart(comment_queue):
    chartPlotter = ChartPlotter()
    chartPlotter.plotChart(comment_queue)



def main():
    comment_queue = Queue()
    comment_process = Process(target=scan_comments, args=(comment_queue,))
    chart_process = Process(target=plot_chart, args=(comment_queue,))
    
    comment_process.start()
    chart_process.start()

    comment_process.join()
    chart_process.join()

#### MAIN ####
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()