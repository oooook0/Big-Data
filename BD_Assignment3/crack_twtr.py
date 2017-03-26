# import os
# import sys
#
# if 'SPARK_HOME' not in os.environ:
#     os.environ['SPARK_HOME'] = '/home/zijun/Downloads/spark-2.1.0'
#
# if '/home/zijun/Downloads/spark-2.1.0/python' not in sys.path:
#     sys.path.insert(0, '/home/zijun/Downloads/spark-2.1.0/python')


import re
import time
import logging
import argparse
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession


class crack_twtr():
    def __init__(self):
        self.price_info = []
        self.twtr_ = []
        self.models = []
        self.predict_ = {}
        self.spark = SparkSession.builder.master("local[4]").appName("crack_twtr").getOrCreate()
        self.path_list = None
        self.plot_y = []
        self.plot_x = []

    def enter_price_csv(self, price_csv):
        self.price_info = pd.read_csv(price_csv, parse_dates=['Date'], \
                                      date_parser=lambda dates: pd.datetime.strptime(dates, '%m/%d/%Y'))

    def get_twtr_path(self, price_info):
        twtr_path = []
        date_list = price_info['Date']
        for i in date_list:
            twtr_path.append("{:02d}/{:02d}/*/*.json.bz2".format(i.month, i.day))
        return twtr_path

    def twtr_analyze(self):

        self.path_list = self.get_twtr_path(self.price_info)

        def extract_features(twtr_line):
            twtr_line = str(twtr_line)
            split_line = twtr_line.split(", ")
            text = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(text=u)", " ", split_line[1])

            info_set = {}
            for s in stock_set:
                info_set.update({s: {"followers_count": 0, "p_count": 0, "n_count": 0, "mentioned_count": 0}})

            for s in stock_set:
                if (s in text) or (s.lower() in text):
                    info_set[s]['followers_count'] = filter(str.isdigit, split_line[0])
                    info_set[s]['mentioned_count'] = 1

                    split_text = text.split()

                    for st in split_text:
                        st = st.upper()
                        if st in positive_words:
                            info_set[s]['p_count'] += 1
                        elif st in negative_words:
                            info_set[s]['n_count'] += 1
                        else:
                            pass
            return info_set

        def aggragete_result(r1, r2):

            for s in stock_set:
                r1[s]["followers_count"] = int(r1[s]["followers_count"]) + int(r2[s]["followers_count"])
                r1[s]["mentioned_count"] = int(r1[s]["mentioned_count"]) + int(r2[s]["mentioned_count"])
                r1[s]["n_count"] = int(r1[s]["n_count"]) + int(r2[s]["n_count"])
                r1[s]["p_count"] = int(r1[s]["p_count"]) + int(r2[s]["p_count"])
            return r1

        current_file, total_files = 1, len(self.path_list) # tracker

        for i in self.path_list:  # the first feature is the params
            twtr = self.spark.read.json(i)
            twtr_en = twtr.filter(twtr['lang'] == 'en')
            twtr_target = twtr_en.select(twtr_en['user']['followers_count'], twtr_en['text'])
            self.twtr_.append(twtr_target.rdd.map(extract_features).reduce(aggragete_result))

            logging.info("processing %s / %s file" % (current_file, total_files))
            current_file += 1

        # regression
        for s in stock_set:
            X = []
            for f in self.twtr_[1:]:
                X.append(
                    [1, f[s]['followers_count'] / 1000., f[s]['mentioned_count'], f[s]['p_count'], f[s]['n_count']])
            pp = self.twtr_[0]
            predicting_param = [1, pp[s]['followers_count'] / 1000., pp[s]['mentioned_count'], pp[s]['p_count'],
                                pp[s]['n_count']]
            pricetmp = self.price_info[['Date', s]]
            pricetmp1 = pricetmp[s].diff() / pricetmp[s]
            returns = list(pricetmp1[~pricetmp1.isnull()])
            model = sm.OLS(returns, X).fit()
            self.models.append(model)
            self.plot_y = returns
            self.plot_x = X
            predicted_returns = model.predict(predicting_param)
            predicted_price = (predicted_returns + 1) * self.price_info[s][0]
            self.predict_.update({s: {"predict_return": predicted_returns, "predict_price": predicted_price}})

        print "According to twtr info, prediction is as follows:\n %s" % self.predict_

    def show_plot(self, n):
        index = range(1, len(self.plot_y) + 1)
        plot_y_fit = [float(self.models[n].predict(self.plot_x[i])) for i in xrange(0, len(self.plot_y))]
        plt.plot(index, self.plot_y, 'r-.', label="real_value")
        plt.plot(index, plot_y_fit, 'b--', label="fitted_value")
        plt.xlabel('Time')
        plt.ylabel('Returns')
        plt.legend()
        plt.savefig("regression_effect.png")


if __name__ == "__main__":

    # passing the parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="Enter the price_csv", required=True)
    parser.add_argument("-w", help="Enter the words_csv", required=True)
    args = parser.parse_args()

    # adding log file
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='crack_twtr.log',
                        filemode='w')
    logging.info("crack_twtr begins...")

    time1_begin = time.time() # begin
    global stock_set
    global positive_words, negative_words
    price_csv = args.p
    words_csv = args.w
    stock_set = ['IBM', 'MSFT', 'TSLA', "AMZN", "VZ"]
    lmDic = pd.read_csv(words_csv)[['Word', 'Negative', 'Positive']]
    positive_words = list(lmDic[lmDic['Negative'] != 0]['Word'])
    negative_words = list(lmDic[lmDic['Positive'] != 0]['Word'])
    task = crack_twtr()
    time1_end = time.time() # end
    logging.info("class established...")


    time2_begin = time.time() # begin
    task.enter_price_csv(price_csv)
    task.twtr_analyze()
    time2_end = time.time() # end
    logging.info("analyzer established...")


    time3_begin = time.time() # begin
    task.show_plot(0)
    time3_end = time.time() # end
    logging.info("plot established...")

    logging.info("prediction result:\n %s" % task.predict_)
    logging.info("establishing class takes: %s seconds" % str(time1_end - time1_begin))
    logging.info("analysis takes: %s seconds" % str(time2_end - time2_begin))
    logging.info("plotting takes: %s seconds" % str(time3_end - time3_begin))
    logging.info("program end...")
