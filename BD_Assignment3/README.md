# Assignment C

##### We have 2 csv files, crack_twtr.py and crack_twtr.ipyn:
- **csv files**:
  - [LoughranMcDonald_MasterDictionary_2014.csv](http://www3.nd.edu/~mcdonald/Word_Lists.html): 
  This provides positive and negative measures for a wide variety of words which you could add customized vocabulary to it
  - [close_price.csv](https://finance.yahoo.com/):
  This provides close price of the stock set
  
- **crack_twtr.ipyn**:
  - An initial version without logging
  - The result in the jupyter notebook is calculated from 20-day data (12/1/2016 ~ 12/30/2016)
  - Prediction result is printed on the screen and saved in the log file
  - Regression plot is saved
  
- **crack_twtr.py**:
  - running instruction: 
   ```
      python crack_twtr.py -p close_price.csv -w LoughranMcDonald_MasterDictionary_2014.csv
   ```
  
 ##### The idea behind:
 - Twitter information plays an important role in forecasting stock prices. There are many [researches](https://arxiv.org/pdf/1010.3003&) on that. Twitter data can be downloaded and the data structure of it can be found on the [link](https://dev.twitter.com/overview/api/tweets).
 - Four features are extracted: the number of positive words, negative words, mentioned specific stock and followers of one tweet.
 - Instead of regression on price, we use linear regression on returns. 


##### Environment set-up:
- pyspark:  [setup instruction](https://github.com/alfredzj/BigData/blob/master/BD_Assignment3/pyspark_setup_instruction.md)
- python packages:

  | packages   | Method                        |
  | :------ | :--------------------------------: |
  | statsmodels  | ```conda install -c statsmodels statsmodels=0.6.0_dev``` |
  | matplotlib  | ```conda install -c conda-forge matplotlib=2.0.0``` |
  | py4j  | ```conda install -c blaze py4j=0.9```|

