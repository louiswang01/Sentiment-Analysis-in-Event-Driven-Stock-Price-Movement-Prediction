#!/usr/bin/env python3
"""
Download the ticker list from NASDAQ and save as csv.
Output filename: ./input/tickerList.csv
"""
import sys
import numpy as np
from urllib.request import urlopen


def get_tickers(percent):
    """Keep the top percent market-cap companies."""
    assert isinstance(percent, int)

    output = []
    for exchange in ["NASDAQ", "NYSE", "AMEX"]:
        url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange="
        repeat_times = 10 # repeat downloading in case of http error
        for i in range(repeat_times):
            try:
                print("Downloading tickers from %s (%d/%d try)..." % (exchange, i+1, repeat_times))
                response = urlopen(url + exchange + '&render=download')
                content = response.read().decode('utf-8').split('\n')
                for num, line in enumerate(content):
                    line = line.strip().strip('"').split('","')
                    if num == 0 or len(line) != 9:
                        continue # filter unmatched format
                    
                    # Header: Symbol, Name, LastSale, MarketCap, ADR TSO, IPOyear, Sector, 
                    #         Industry, Summary Quote
                    ticker      = line[0]
                    name        = line[1].replace(',', '').replace('.', '')
                    market_cap  = float(line[3])
                    output.append([ticker, name, exchange, market_cap])
                break
            except:
                continue
    
    cap_stat = [row[3] for row in output]
    threshold = np.percentile(cap_stat, 100 - percent)
    top_companies = [record for record in output if record[3] > threshold]
    with open('./input/tickerList.csv', 'w') as f:
        for data in sorted(top_companies):
            data[3] = str(data[3])  # market cap float
            f.write(','.join(data) + '\n')


def main():
    if len(sys.argv) < 2:
        print('Usage: ./all_tickers.py <int_percent>')
        return
    top_n = sys.argv[1]
    get_tickers(int(top_n)) # keep the top N% market-cap companies


if __name__ == "__main__":
    main()
