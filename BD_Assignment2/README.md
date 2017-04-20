# Assignment B

The assignment is divided into two parts:
>
- answer the following question using own logic:
  - By when (what year) will all bitcoins have been mined? And how many?
  - How many bitcoin spendable units are there currently? How does that compare with spendable units available in the world economy today? This is like asking: "could bitcoin be used as a global currency?"
  - What's the current size of the bitcoin blockchain? How quickly is it growing?
  - What does the blockchain verification cycle say about how quickly transactions can be verified?
  - What's the theoretical maximum transaction throughput of the bitcoin payments network?
  - What's the market capitalization of bitcoin as measured in US $ ? 
- Write a simple program in Python using the blockchain.info "Blockchain Data API" that will sum up the total quantity of bitcoin transactions (how many bitcoins moved between addresses in a 24 hour period) on any given day,


The first part is done using jupyter notebook (python) and has been uploaded as BD_Assignment2_part1.ipynb. The second part is done by python and has been upload as daily_btc.py.


### Tip:
* There are some hyperlinks in the first part which contain the websites of reference. e.g. median-confirmation-time.csv is one of them and you can click blockchain.info in the jupyter notebook.

* You can run daily_btc.py in the terminal like this(Be careful with the date format: YYYYMMDD)
```
python daily-btc.py -d 20170220
```
* Output of the daily_btc.py :
  - the number of transcations on that day
  - the total value of transcations on that day you enter
  - a log file

