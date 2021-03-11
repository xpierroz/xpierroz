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


class Sniper():
    def __init__(self):
        self._n = ""

        with open("Sniper/Nitro.s", "r", encoding="utf-8") as out:
            for line in out.read().splitlines():
                if "Activate" in line: #It should everytime be or the guys fucked the sys
                    o = line.split(" = ")[1]
                    if o.lower() == "on":
                        self._n = "ON"
                    elif o.lower() == "off":
                        self._n = "OFF"

    def get_nitro(self, code: str):
        """
        SNIPER CODE COLOR 
        -----------------
        0 = INVALID
        2 = VALID
        3 = ALREADY CLM
        4 = RATELIMITED
        5 = GLITCHED CODE
        """
        json = {
            'channel_id': None,
            'payment_source_id': None
        }

        h = {
            'Content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.13 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
            'Authorization': c.token
        }
        r = requests.post(f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', headers=h, json=json)
        rct = r.text
        
        if '{"message": "Unknown Gift Code", "code": 10038}' in rct:
            return 0 

        elif '{"message": "Page not Found.", "code": 404}' in rct:
            return 0 

        elif '{"message": "Payment source required to redeem gift.", "code": 50070}' in rct:
            return 5

        elif 'You are being rate limited' in rct:
            return 4
        
        elif '{"message": "This gift has been redeemed already.' in rct:
            return 3

        elif 'Access denied' in rct:
            return 0

        return 2

    @property 
    def nitro_a(self):
        if self._n == "ON":
            return 1
        return 0