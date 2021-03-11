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


class Log():
    def __init__(self):
        """
        PATH CODE
        ---------
        N = NITRO
        ---------
        I = INVALID
        A = ALREADY CLAIMED
        R = RATLIMITED
        """
        self._nipath = "Logger/Sniper/Nitro/Invalid.s"
        self._napath = "Logger/Sniper/Nitro/AlreadyClaimed.s"
        self._nrpath = "Logger/Sniper/Nitro/Ratelimited.s"

    def append(self, f, i):
        with open(f, "a+", encoding="utf-8") as out:
            out.write(i)

    def invalid_nitro(self, code, msgauthname, msgauthid, msgguildname, msgguildid):
        print(f'    {Fore.YELLOW}.$ Sniper :: {Fore.LIGHTRED_EX}Invalid Code {Fore.YELLOW}- {Fore.LIGHTYELLOW_EX}{self._nipath}')
        output = f"discord.gift/{code} - {msgauthname} - {msgauthid} - {msgguildname} - {msgguildid}\n"
        self.append(self._nipath, output) #We're using the output var because putting everything like that would be so cool

    def alreadyclaimed_nitro(self, code, msgauthname, msgauthid, msgguildname, msgguildid):
        print(f'    {Fore.YELLOW}.$ Sniper :: {Fore.LIGHTYELLOW_EX}Invalid Code {Fore.YELLOW}- {Fore.LIGHTYELLOW_EX}{self._napath}')
        output = f"discord.gift/{code} - {msgauthname} - {msgauthid} - {msgguildname} - {msgguildid}\n"
        self.append(self._napath, output)

    def ratelimited_nitro(self, code, msgauthname, msgauthid, msgguildname, msgguildid):
        print(f'    {Fore.YELLOW}.$ Sniper :: {Fore.LIGHTYELLOW_EX}Invalid Code {Fore.YELLOW}- {Fore.LIGHTYELLOW_EX}{self._nrpath}')
        output = f"discord.gift/{code} - {msgauthname} - {msgauthid} - {msgguildname} - {msgguildid}\n"
        self.append(self._nrpath, output)