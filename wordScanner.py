import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

'''class will create a word dictionary for both bears and bulls'''

class WordDictionary():
    def __init__(self):
        #store main dictionary
        self._wordDict = {}
        #counter for bears
        self._bears = 0
        #counter for bulls
        self._bulls = 0

        self.Vader = SentimentIntensityAnalyzer()

        # sentiment constant
        self.SENTIMENT = 0.05

        self.bullList = ['bull','bulls','bullish','buy','moon','buls','call','calls','green','pump','pumps','vshape', 'v-shape']

        self.bearList = ['bear','bears','bearish','sell','put','puts','bers','red','dump','dumps','put','puts','flat']


        # set the variables needed for the chart
        self.bars = ['Bulls', 'Bears']

        self.y = [0,0]

        self.fig, self.ax = plt.subplots()

        #self.bars = self.ax.bar(self.x,self.y)

        # Adjust bar fx
        bar_color = 'green'  # Change the color as desired

        bar_width = 0.5  # Adjust the value as desired

        #self.bars = self.ax.bar(self.x, self.y, width=bar_width, color=bar_color)

        self.ax.set_ylim(0, 10)


    '''find words method will have multiple lists of words pertaining to the specific team 
        main purpose is to track how many comments contain the words in the corresponding word lists
        and collect data from those comments'''
    def findWords(self,comment):

        # main wordlist that will generalize every word related to trading
        wordList = ['bear', 'bears','bull','bulls','bearish', 'bullish','buy','sell',
                    'banbet','put','moon','bers','buls','call','calls','flat','green',
                    'red','spy','dump','pump','dumps','pumps','puts', 'v shape']
        
        #bull list will contain all words related to bulls
        #bullList = ['bull','bulls','bullish','buy','moon','buls','call','calls','green','pump','pumps','vshape', 'v-shape']

        # bearlist will contain all words related to bears
        #bearList = ['bear','bears','bearish','sell','put','puts','bers','red','dump','dumps','put','puts','flat']

        #for loop through all comments given from website reader
        for i in comment.split():
            i = i.lower()
            
            #if the word is in the word dictionary already, increment its counter
            if i in self._wordDict:
                self._wordDict[i] +=1

            if not i in self._wordDict:
                if i in wordList:
                    self._wordDict[i] = 1

                    
            #check if the word is in the bullList and keep counter of it
            if i in self.bullList:
                self._bulls +=1

            # check if the word is in the bearlist and keep counter of it
            if i in self.bearList:
                self._bears +=1
            

    ''' this method will print all data values that we want'''
    def getWordDict(self):
        pass
        # print('*** BULLS VS BEARS ***')
        # print('word dictionary: ' + str(self._wordDict))
        # print('bears: ' + str(self._bears))
        # print('bulls ' + str(self._bulls))
        # print()

    def getBears(self):
        return self._bears
    
    def getBulls(self):
        return self._bulls
    
    def getWords(self):
        return self._wordDict

