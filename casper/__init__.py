#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, subprocess, json, platform, pprint
from requests import get
from .node import Node
from .database import Database
from .cli import Cli
from .utils import get_exec_sh, Yaml, runcli
yaml = Yaml()

# os.environ["PYTHONIOENCODING"] = "utf-8"

with open('package.json', 'r') as json_file:
    package = json.load(json_file)
    version = package["version"]

class CasperCore(object):
    def __init__(self, settings, USER_PWD=None, CRYPTO_MOD="Fernet", USER_NAME=None):
        if sys.platform == 'win32':
            print("Windows not supported")
            sys.exit(2)

        self.executable = get_exec_sh()
        self.settings = settings

        if "version" in self.settings:
            self.version = self.settings["version"]
        elif self.version != version:
            self.version = version
            self.settings["version"] = version
            yaml.save_file(self.settings, location="config/settings.yaml")
        else:
            self.version = version


        if USER_PWD is None:
            USER_PWD = input("Enter your Password\n")


        self.versions()

        self.db = Database(self.settings, USER_PWD, CRYPTO_MOD)
        self.node = Node(self.settings)
        self.cli = Cli(self.settings, self.db)


        if USER_NAME is None:
            self.db._verify_user(USER_PWD)
        else:
            self.db._verify_user(USER_NAME)

        self.verifiy_versions()


    def versions(self):
        print("STARTING CASPER CORE v" + self.version)
        print("OS", platform.platform())
        jcli_version = runcli("jcli --full-version")
        jormungandr_version = runcli("jormungandr --full-version")
        python_version = runcli("python3 --version")

        if jormungandr_version is None:
            self.settings["NO_JORMUNGANDR"] = True
            print("ERROR JORMUNGANDR NOT INSTALLED")
            #  sys.exit(2) # JORMUNGANDR is not required

        if jcli_version is None:
            print("ERROR JCLI NOT INSTALLED")
            sys.exit(2)

        if python_version is None:
            print("ERROR PYTHON3 NOT INSTALLED")
            sys.exit(2)

        print(jcli_version)
        print(jormungandr_version)
        print(python_version)

    def download_raw_git(self, url, file_name):
        # open in binary mode
        return self.cli._run(
            f"curl -H 'Accept: application/vnd.github.v3.raw' -O -L {url}"
        )


    def update_binaries(self):
        releases = self.node._get("https://api.github.com/repos/input-output-hk/jormungandr/releases")
        last = releases[0]
        key = None
        url = None
        _platform = platform.platform().lower()

        if "darwin" in _platform:
            key = "darwin"
        ## elifs for other platforms needed


        for item in last["assets"]:
            if url is not None:
                continue
            name = None
            if "name" in item:
                if "name" in item:
                    _name = item["name"]
                    if "darwin.tar.gz" in _name:
                        url = item["browser_download_url"]
                        d = input(f"Download file: {_name}? (y/n) ")
                        if os.path.isfile(_name) is False and d is "y":
                            self.download_raw_git(url, _name)
                            #  MOVE FILES TO INSTALLTION FOLDER ?
                            print("DOWNLOAD DONE")
                        return url


    def verifiy_versions(self):
        version = self.node._get("https://api.github.com/repos/input-output-hk/jormungandr/tags")
        current_version = version[0]["name"]
        installed_version = self.cli._run("jormungandr --version").replace("jormungandr ", "v")
        if current_version != installed_version:
            print(f'\n\nJORMUNGANDR IS OUTDATED! \n\nRELEASED VERSION: {current_version} - YOUR VERSION: {installed_version}')
            c = input("DO YOU WANT TO CONTINUE / EXIT? (c/e): ")
            if c == "e":
                sys.exit(2)
            elif c == "u":
                self.update_binaries()
                sys.exit(2)
            else:
                print("CONTINUE WITH OLDER VERSION")
