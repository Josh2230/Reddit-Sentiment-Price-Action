import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from nltk.sentiment import SentimentIntensityAnalyzer
import time
import random

'''responsible for taking comments and extracting data from comments to plot it on a live bar graph'''
class ChartPlotter:
    def __init__(self):

        ## bull and bear related variables
        self.bullList = ['bull','bulls','bullish','buy','moon','buls','call','calls','green','pump','pumps','vshape', 'v-shape','up','v','rip','long','longs']
        self.bearList = ['bear','bears','bearish','sell','puts','ber','bers','red','dump','dumps','put','puts','flat','down','drill','crash','short','shorts','shorting']

        ## investing related variables
        self.investWords = ['futures','futes','market',"market's",'stock','stocks']
        self.ticker = ['spce', 'amd', 'spy', 'amc', 'nvda', 'mu', 'aapl', 'msft', 'tsla', 'ccl', 'nke', 'jpm', 'bb', 'itm', 'cvna',	'joby', 'qqq', 'fr']

        ## keep track of point system
        self._bulls = 0
        self._bears = 0


        # initialize basic values for chart
        self.bars = ['1','2']
        self.y = [0, 0]
        self.y2 = [0,0]
        self.graph = []
        ## chart related variables
        self.fig, self.ax = plt.subplots()
        # self.bar_chart = self.ax.bar(range(len(self.bars)), self.y)
        self.ax.bar(self.bars, self.y)
        # self.ax.bar(self.bars, self.y2, color='red')
        # Set the x-axis labels
        self.ax.set_ylim(0, max(self.y) + 1)
        self.colors= ['green', 'red']
        self.animation = None

         # Store the artist objects for the bars
        self.bar_artists = self.ax.bar(self.bars, self.y, color=self.colors)

        # Create a legend for the bars
        self.ax.legend(self.bar_artists, ['Bulls', 'Bears'])
        

        ## time related variables 
        self.start_time = time.time()
        self.interval_minutes = 5

        ## storing units for point system
        self.bull_values = []
        self.bear_values = []
        self._counter = 0

        ## sentiment variables
        self.SENTIMENT = 0.05
        self.Vader = SentimentIntensityAnalyzer()

        ## range numbers for loop
        self.base = 0
        self.max = 2

        self.bar_width = .8
        self.bar_positions = [0, self.bar_width]

        self.type = []

        self.counter = 3
        self.position_counter = 0


    '''updateData is responsible for taking the comments and evaluating it to then call the point system method'''
    def updateData(self, comment):
        sentimentScores = self.Vader.polarity_scores(comment)
        compoundScore = sentimentScores['compound']

        # self.pointSystem(comment,compoundScore)
        # for i in range(self.base,self.max):
        #     if len(self.type) != 0:
        #         type = self.type.pop()
        #         if type == 'bull':
        #             if len(self.bull_values) != 0:
        #                 bull = self.bull_values.pop()
        #                 self.y[self.base] = bull
        #         elif type == 'bear':
        #             if len(self.bear_values) != 0:
        #                 bear = self.bear_values.pop()
        #                 self.y[self.max] = bear

        self.pointSystem(comment,compoundScore)
        print(self.y)
        for i in range(self.base,self.max):
            if i % 2 == 0:
                if len(self.bull_values) != 0:
                    bull = self.bull_values.pop()
                    self.y[i] = bull
            else:
                if len(self.bear_values) != 0:
                    bear = self.bear_values.pop()
                    self.y[i] = bear


    '''updateChart is responsible for checking if there are comments available and setting the chart up to plot'''


    def updateChart(self, frame, comment_queue):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= self.interval_minutes * 60:
            self.start_time = current_time

            # Add a single timestamp value to self.bars for the current iteration
            # current_time_str = time.strftime("%H:%M:%S", time.localtime(current_time))
            # self.bars.append(current_time_str)  # Add timestamp to self.bars for the current iteration
            # self.bars.append(current_time_str)

            for i in range(2):
                self.y.append(0)
                self.bars.append(str(self.counter))
                self.counter+=1
                self.base += 1
                self.max += 1
                self.bar_positions.append(self.bar_positions[self.position_counter] + 2)
                self.position_counter += 1
            ## reset point system for next chart

            self._bulls = 0
            self._bears = 0

            self.colors.append('green')
            self.colors.append('red')

            # self.bar_positions.append(self.bar_positions[self.position_counter] + 2)
            # self.position_counter += 1
            # self.bar_positions.append(self.bar_positions[self.position_counter] + 2)
            # self.position_counter+=1

            # # Add a single timestamp text for the current iteration
            # current_time_str = time.strftime("%H:%M:%S", time.localtime(current_time))
            # self.ax.text(sum(self.bar_positions) / 2, -0.1, current_time_str, ha='center', transform=self.ax.transData, fontsize=8)  # Add timestamp text under the bars



        while not comment_queue.empty():
            comment = comment_queue.get()
            self.updateData(comment)

       
        
        self.ax.clear()
        self.ax.bar(self.bars, self.y)
        self.ax.set_ylim(0, max(self.y) + 1)

        # Update the legend
        self.ax.legend(self.bar_artists, ['Bulls', 'Bears'])


        for bar, newValue, color, position in zip(self.ax.patches, self.y, self.colors, self.bar_positions):
            bar.set_height(newValue)
            bar.set_color(color)
            bar.set_x(position)

        self.fig.canvas.draw()


    '''plotChart is responsible for creating the animation of the chart for live updates'''
    def plotChart(self,comment_queue):


        self.ax.bar(self.bars, self.y)

        self.animation = FuncAnimation(self.fig, self.updateChart,fargs=(comment_queue,), interval=100)

        plt.show()


    '''pointSystem will evaluate each comment based on their words and sentiment'''
    def pointSystem(self,comment,compoundScore):
        for word in comment.split():
            word = word.lower()
            if compoundScore != 0:
                if word in self.ticker and compoundScore >= self.SENTIMENT:
                    print(comment,'score: ' ,compoundScore)
                    self._bulls += 1
                    self.bull_values.append(self._bulls)
                    self.type.append('bull')
                    break
                elif word in self.ticker and compoundScore <= -self.SENTIMENT:
                    print(comment,'score: ' ,compoundScore)
                    self._bears += 1
                    self.bear_values.append(self._bears)
                    self.type.append('bear')
                    break
                elif word in self.investWords and compoundScore >= self.SENTIMENT:
                    print(comment,'score: ' ,compoundScore)
                    self._bulls += 1
                    self.bull_values.append(self._bulls)
                    self.type.append('bull')
                    break
                elif word in self.investWords and compoundScore <= self.SENTIMENT:
                    print(comment,'score: ' ,compoundScore)
                    self._bears += 1
                    self.bear_values.append(self._bears)
                    self.type.append('bear')
                    break
                elif word in self.bullList and compoundScore >= self.SENTIMENT:
                    print(comment,'score: ' ,compoundScore)
                    self._bulls += 1
                    self.bull_values.append(self._bulls)
                    self.type.append('bull')
                    break
                elif word in self.bullList and compoundScore <= -self.SENTIMENT:
                    print(comment,'score: ' ,compoundScore)
                    self._bears += 1
                    self.bear_values.append(self._bears)
                    self.type.append('bear')
                    break
                elif word in self.bearList and compoundScore >= self.SENTIMENT:
                    print(comment,'score: ' ,compoundScore)
                    self._bears += 1
                    self.bear_values.append(self._bears)
                    self.type.append('bear')
                    break
                elif word in self.bearList and compoundScore <= -self.SENTIMENT:
                    print(comment,'score: ' ,compoundScore)
                    self._bulls += 1
                    self.bull_values.append(self._bulls)
                    self.type.append('bull')
                    break
                