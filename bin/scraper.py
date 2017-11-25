import argparse
from API import *


def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()


    adj = EtherScanScraper2(currency='OmiseGo', test=False)
    adj.run()


if __name__ == "__main__":
    main()