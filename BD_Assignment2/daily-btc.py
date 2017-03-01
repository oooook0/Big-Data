from blockchain import blockexplorer
import datetime, time, logging, argparse

def daily_btc(date):
    total_num, total_val = 0, 0
    dt = datetime.datetime.strptime(date,'%Y%m%d')
    dt_utc = int(dt.strftime("%s"))
    blocks = blockexplorer.get_blocks(dt_utc*1000) # unix time in milliseconds
    for block in blocks:
        try:
            transaction = blockexplorer.get_block(block.hash).transactions
            total_num += len(transaction)
            for t in transaction:
                out = t.outputs
                for o in out:
                    total_val += o.value
        except:
            total_num += 0
            total_val += 0

    total_val /= 1e8
    return total_num, total_val

if __name__ == "__main__":
    # time tracker
    start_time = time.time()

    # passing the parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="enter the date in format 'YYYYMMDD'", required=True)
    args = parser.parse_args()

    # adding log file
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	    datefmt='%a, %d %b %Y %H:%M:%S',
	    filename='daily_btc.log',
	    filemode='w')

    logging.info("start daily_btc function")
    num, val = daily_btc(args.d)
    logging.info("end daily_btc function")

    end_time = time.time()
    print "Date: %s: num of transactions: %s, total value: %s" % (args.d, num, val)
    logging.info("Date: %s: num of transactions: %s, total value: %s" % (args.d, num, val))
    logging.info("Running time: %s" % (end_time-start_time))
    logging.info("End")
