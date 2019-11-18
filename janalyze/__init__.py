#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://raw.githubusercontent.com/input-output-hk/jormungandr-nix/master/scripts/janalyze.py
Jormungandr Analysis Tools
forked by kodex
"""

__version__ = "0.1.0-kodex"

import argparse, requests, os, json, sys
from argparse import RawTextHelpFormatter
from requests.exceptions import HTTPError
from operator import itemgetter
from tabulate import tabulate

class JAnalyze():
    globalAggregate = None
    globalEpochBlocks = None
    globalPools = None
    api_url_base = None
    api_url = None

    def __init__(self, settings):
        n = settings["node"]
        self.api_url_base = f"{n}/api"
        self.api_url = f"{self.api_url_base}/v0"

    def endpoint(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except HTTPError as http_err:
            print("\nWeb API unavailable.\nError Details:\n")
            print(f"HTTP error occurred: {http_err}")
            exit(1)
        except Exception as err:
            print("\nWeb API unavailable.\nError Details:\n")
            print(f"Other error occurred: {err}")
            exit(1)
        else:
            return(r)

    def get_api(self, path):
        r = self.endpoint(f'{self.api_url}/{path}')
        return r.text


    def get_tip(self):
        return self.get_api("tip")


    def get_block(self, block_id):
        r = self.endpoint(f'{self.api_url}/block/{block_id}')
        hex_block = r.content.hex()
        return hex_block

    def parse_block(self, block):
        return {
          "epoch": int(block[16:24], 16),
          "slot": int(block[24:32], 16),
          "parent": block[104:168],
          "pool": block[168:232],
        }

    def check_int(self, value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
        return ivalue

    def lostblocks(self):
        thisblockhex = self.get_tip()
        opportunities = 0
        wins = 0
        lostlogs = []
        thisblock = self.parse_block(self.get_block(thisblockhex))
        r = self.endpoint(f'{self.api_url}/leaders/logs')
        y = json.loads(r.content)
        completed = [x for x in y if x['finished_at_time'] != None]
        for result in sorted(completed, key=itemgetter('finished_at_time'), reverse=True):
            epoch, slot=result['scheduled_at_date'].split(".")
            if(int(epoch) < int(thisblock['epoch'])):
                break
            opportunities += 1
            while(int(slot) < int(thisblock['slot'])):
                thisblockhex = thisblock['parent']
                thisblock = self.parse_block(self.get_block(thisblock['parent']))

            if(int(thisblock['epoch']) == int(epoch) and int(thisblock['slot']) == int(slot)):
                if(thisblockhex == result['status']['Block']['block']):
                    wins += 1
                else:
                    lostlogs.append({
                        "epoch": epoch,
                        "slot": slot,
                        "lost_to": thisblock['pool']
                        })

        if(opportunities - wins):
            header = lostlogs[0].keys()
            rows = [x.values() for x in lostlogs]
            table = tabulate(rows, header, tablefmt="psql")
            print(table)

        print(f'{"Blocks Created:":<21}{opportunities:,d}')
        print(f'{"Lost Blocks:":<21}{opportunities-wins:,d}')
        if(opportunities):
            print(f'{"Percent Lost:":<21}{(opportunities-wins)*100/opportunities:,.0f}%')

    def aggregate(self, silent=False, aggregate=1):

        #global globalAggregate
        #global globalEpochBlocks
        tip = self.get_tip()
        block = self.parse_block(self.get_block(tip))
        epochBlockTotal = {}
        currentEpoch = block['epoch']
        epochs = {}
        pools = {}

        while block["parent"] != ("0" * 64):
            # if args.full == False:
            if (currentEpoch - aggregate + 1) > block['epoch']:
                break
            epoch = block['epoch']
            parent = block['parent']
            pool = block['pool']
            if epoch not in epochs:
                epochs[epoch] = {}
                epochBlockTotal[epoch] = 0

            if pool not in epochs[epoch]:
                epochs[epoch][pool] = {}
                epochs[epoch][pool]['blocks'] = 1
                epochBlockTotal[epoch] = epochBlockTotal[epoch] + 1
            else:
                epochs[epoch][pool]['blocks'] = epochs[epoch][pool]['blocks'] + 1
                epochBlockTotal[epoch] = epochBlockTotal[epoch] + 1
            block = self.parse_block(self.get_block(block['parent']))
            # if pool == '0b32cee60ff511665ec6f0b362f7273b4f0c2c3cc7f1f77ad976ceda71785088':
            #    print(f'block found {epoch} {parent} {block}')


        for epoch, epochData in epochs.items():
            epochs[epoch]['stats'] = {}
            epochs[epoch]['stats']['blocksum'] = epochBlockTotal[epoch]
            for pool, poolData in epochData.items():
                if pool != 'stats':
                    epochs[epoch][pool]['percent'] = poolData['blocks'] / epochBlockTotal[epoch] * 100

        if silent == False:
            print('\nJormungandr Epoch Block Aggregate:\n')
            for epoch, epochData in epochs.items():
                headers = [f'EPOCH {epoch}, Pool (Node ID)', "Blocks (#)", "Block Percent (%)"]
                table = []
                for pool, data in epochData.items():
                    if pool != 'stats':
                        record = [ pool, data['blocks'], data['percent'] ]
                        table.append(record)
                # if args.bigvaluesort == True:
                #     print(f'{tabulate(sorted(table, key=lambda x: x[1], reverse=True), headers, tablefmt="psql")}')
                # else:
                ### Big Value Sort by Default ###
                print(f'{tabulate(sorted(table, key=lambda x: x[1], reverse=True), headers, tablefmt="psql")}')
                print(f'{"Totalblocks:":<21}{epochData["stats"]["blocksum"]}\n\n')
        self.globalAggregate = epochs

    def distribution(self, silent=False, bigvaluesort=True, nozero=True):
        epoch = 0
        unassigned = 0
        dangling = 0
        stakeSum = 0
        totalPercentStaked = 0
        total = 0
        pools = {}

        r = self.endpoint(f'{self.api_url}/stake')
        raw = r.json()

        epoch = raw['epoch']
        dangling = raw['stake']['dangling']
        unassigned = raw['stake']['unassigned']

        if bigvaluesort == True:
            sortedRaw = sorted(raw['stake']['pools'], key = lambda x: x[1], reverse=True)
        else:
            sortedRaw = sorted(raw['stake']['pools'])
        for [pool, stake] in sortedRaw:
            pools[pool] = {}
            pools[pool]['stake'] = stake
            pools[pool]['percent'] = 0
            stakeSum = stakeSum + stake

        total = stakeSum + unassigned + dangling
        totalPercentStaked = stakeSum / total

        # Calculate percentage stake delegation of total staked ADA
        for pool in pools.keys():
            pools[pool]['percent'] = pools[pool]['stake'] / stakeSum * 100

        pools['stats'] = {}
        pools['stats']['epoch'] = epoch
        pools['stats']['dangling'] = dangling
        pools['stats']['unassigned'] = unassigned
        pools['stats']['total'] = total
        pools['stats']['stakesum'] = stakeSum
        pools['stats']['totalpercentstaked'] = totalPercentStaked

        if silent == False:
            print('\nJormungandr Stake Pool Distribution:\n')
            print(f'{"Epoch:":<21}{epoch}')
            print(f'{"Dangling:":<21}{dangling / 1e6:,.6f} ADA')
            print(f'{"Unassigned:":<21}{unassigned / 1e6:,.6f} ADA')
            print(f'{"Total:":<21}{total / 1e6:,.6f} ADA')
            print(f'{"TotalStaked:":<21}{stakeSum / 1e6:,.6f} ADA')
            print(f'{"TotalPercentStaked:":<21}{totalPercentStaked * 100:.2f}%\n')
            headers = [f'EPOCH {epoch}, Pool (Node ID)', "Stake (ADA)", "Percent (%)"]
            table = []
            for pool, poolData in pools.items():
                if pool != 'stats':
                    if nozero == False or poolData['stake'] != 0:
                        record = [ pool, poolData['stake'] / 1e6, poolData['percent'] ]
                        table.append(record)
            if bigvaluesort == True:
                print(f'{tabulate(sorted(table, key=lambda x: x[1], reverse=True), headers, tablefmt="psql", floatfmt=("%s", "0.6f"))}\n\n')
            else:
                print(f'{tabulate(sorted(table, key=lambda x: x[0]), headers, tablefmt="psql", floatfmt=("%s", "0.6f"))}\n\n')
        self.globalPools = pools
