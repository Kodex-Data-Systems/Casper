#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, requests, os, json, sys
from argparse import RawTextHelpFormatter
from __init__ import JAnalyze

__version__ = "0.1.0-kodex"

globalAggregate = None
globalEpochBlocks = None
globalPools = None

api_url_base = None
api_url = None

def check_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def main():
    global api_url_base
    global api_url

    if args.restapi is not None:
        api_url_base = args.restapi
    else:
        api_url_base = os.environ.get("JORMUNGANDR_RESTAPI_URL", "http://localhost:3001/api")
    api_url = f"{api_url_base}/v0"

    analyze = JAnalyze({
        "node": api_url_base
    })

    # if args.stats == True:
    #     stats()
    #
    # if args.aggregateall is not None:
    #     aggregateall()

    if args.aggregate is not None:
        analyze.aggregate(
            aggregate=args.aggregate
        )

    if args.distribution:
        analyze.distribution(
            nozero=args.nozero,
            bigvaluesort=args.bigvaluesort
        )

    # if args.crossref == True:
    #     crossref()

    exit(0)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f'\nRun `{sys.argv[0]} -h` for helpi and usage information\n')
        exit(0)

    parser = argparse.ArgumentParser(description=(
        "Jormungandr analysis tools\n\n"),
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("-aa", "--aggregateall", nargs="?", metavar="X", type=check_int, const=1,
                        help="Calculate toal block creation per pool for all time starting with the tip")

    parser.add_argument("-a", "--aggregate", nargs="?", metavar="X", type=check_int, const=1,
                        help="Calculate aggregate block creation per pool for X epochs starting with the tip epoch (default = 1)")

    parser.add_argument("-b", "--bigvaluesort", action="store_true",
                        help="Show non <-j|--json> output sorted by big to small value rather than keys where possible")

    parser.add_argument("-d", "--distribution", action="store_true",
                        help="Calculate the stake distribution for the current epoch only")

    parser.add_argument("-f", "--full", action="store_true",
                        help="Calculate the full epoch history where possible")

    parser.add_argument("-j", "--json", action="store_true",
                        help="Output raw json only")

    parser.add_argument("-n", "--nozero", action="store_true",
                        help="Don't show zero value staking pools (blocks minted or stake valued)")

    parser.add_argument("-s", "--stats", action="store_true",
                        help="Show the current node stats")

    parser.add_argument("-v", "--version", action="store_true",
                        help="Show the program version and exit")

    parser.add_argument("-x", "--crossref", action="store_true",
                        help="Analyse the current epoch, cross referencing both block aggregate and stake distributions")

    parser.add_argument("-r", "--restapi", nargs="?", metavar="RESTAPI", type=str, const="http://127.0.0.1:3001/api",
                        help="Set the rest api to utilize; by default: \"http://127.0.0.1:3001/api\".  An env var of JORMUNGANDR_RESTAPI_URL can also be seperately set. ")

    args = parser.parse_args()

    if args.version:
        print(f'Version: {__version__}\n')
        exit(0)
    main()
