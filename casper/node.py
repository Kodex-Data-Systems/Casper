#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, requests, sys
import urllib.request
from .utils import get_exec_sh
from requests.exceptions import HTTPError

class Node(object):
    def __init__(self, settings):
        self.executable = get_exec_sh()

        self.url = settings["node"]
        # Checkin an ApiRoute to ensure node is up
        try:
            response_code = urllib.request.urlopen(f"{self.url}/api/v0/network/stats").getcode()
        except:
            # Here we can determine response_code.
            print(f"ERROR NODE IS NOT RESPONDING")
            sys.exit(2)

    def show_peers(self):
        try:
            peers = subprocess.check_output('netstat -anl | egrep "ESTABLISHED+.*jormungandr" | cut -c 45-68 | cut -d ":" -f 1 | sort | uniq -c | sort -nr',
            shell=True,
            executable=self.executable
            ).decode().replace("\n", "")
            return peers


        except subprocess.CalledProcessError:
            print('Only Linux supported\n')

#  REQUESTS
#  API DOCS:
#  https://editor.swagger.io/?url=https://raw.githubusercontent.com/input-output-hk/jormungandr/master/doc/openapi.yaml
    def _get_api(self, path):
        r = self._endpoint(f'{self.url}/api/v0/{path}')
        return r.text


    def get_tip(self):
        return self._get_api("tip")


    def get_block(self, block_id = False):
        if block_id is False:
            block_id = self.get_tip()
        r = self._endpoint(f'{self.url}/api/v0/block/{block_id}')
        hex_block = r.content.hex()
        return self._parse_block(hex_block)

    def _parse_block(self, block):
        return {
          "epoch": int(block[16:24], 16),
          "slot": int(block[24:32], 16),
          "parent": block[104:168],
          "pool": block[168:232],
        }

    def _get(self, url):
        try:
            data = requests.get(url)
        except:
            raise Exception(f"ERROR GET URL: {url}")
        finally:
            return data.json()

    def _endpoint(self, url):
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
    def show_stats(self):
        return self._get(f"{self.url}/api/v0/network/stats")

    def show_settings(self):
        return self._get(f"{self.url}/api/v0/settings")

    def show_node_stats(self):
        return self._get(f"{self.url}/api/v0/node/stats")

    def show_stake(self):
        return self._get(f"{self.url}/api/v0/stake")

    def show_stake_pools(self):
        return self._get(f"{self.url}/api/v0/stake_pools")

    def show_leader_logs(self):
        return self._get(f"{self.url}/api/v0/leaders/logs")

    def show_utxo(self, fragment_id, output_index=255):
        return self._get(f"{self.url}/api/v0/utxo/{fragment_id}/{output_index}")

    def show_balance(self, _acct_id):
        # BUGS!!!
        url = f"{self.url}/api/v0/account/{_acct_id}"
        try:
            data = requests.get(url)
        except:
            raise Exception(f"ERROR GET URL: {url}")
        finally:
            try:
                return data.json()
            except:
                print(f"ACCOUNT {_acct_id} NOT FOUND")
                return
