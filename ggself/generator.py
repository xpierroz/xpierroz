import os
import sys 

import colorama 
from colorama import init, Fore 
if os.name == 'nt':
    init(convert=True) #Windows users need this option

import requests
import httpx 

import asyncio 
import urllib3 

import json 
import sqlite3 

import random 
import string 

import time 
import datetime


class Generator():
    def __init__(self):
        self._l = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self._n = "0123456789"

    def generate_number(self):
        return random.choice(self._n)

    def generate_ip(self): #Yes it's definitly the hardest way I did but ok
        ip = ""
        for x in range(random.randint(2, 3)):
            ip += self.generate_number()
        ip += "."
        for x in range(random.randint(2, 3)):
            ip += self.generate_number()
        ip += "."
        ip += self.generate_number()
        ip += "."
        for x in range(random.randint(2, 3)):
            ip += self.generate_number()
        return ip

    @property
    def get_ip(self):
        return self.generate_ip()