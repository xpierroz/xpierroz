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


class List():
    def __init__(self):
        self._conn = sqlite3.connect("Database/Whitelist.db", check_same_thread=False)
        self._c = self._conn.cursor()

    def check_user(self, user_id: int):
        self._c.execute(f"SELECT user_id FROM whitelist WHERE user_id={int(user_id)}") #Yes, we shouldn't get the user_id object if it's what we're looking for bruh
        r = self._c.fetchone()
        if r is None:
            return 0 
        return 1

    def check_whitelisted(self, user_id: int):
        if self.check_user(user_id) == 0:
            self.add_user(user_id)
        
        self._c.execute(f"SELECT whitelisted FROM whitelist WHERE user_id={int(user_id)}") #It's already an int but f-string is fucked up
        r = self._c.fetchone()
        if r is None: #If it's none it should tell that the system is fucked too 
            self.add_user(user_id)
            return 0 
        return r[0]

    def add_user(self, user_id: int, whitelisted = 0):
        if self.check_user(user_id) == 0:
            self._c.execute("INSERT INTO whitelist VALUES (?, ?, ?)", (user_id, whitelisted, time.strftime("%m/%d/%y - %H:%M:%S")))
            self._conn.commit()
            return 1
        return 0

    def add_whitelist(self, user_id: int):
        t = time.strftime("%m/%d/%y - %H:%M:%S")
        if self.check_user(user_id) == 1:
            if self.check_whitelisted(user_id) == 0:
                self._c.execute(f'UPDATE whitelist SET whitelisted=1, time="{t}" WHERE user_id={int(user_id)}')
                self._conn.commit()
                return 1 
            if self.check_whitelisted(user_id) == 1:
                return
        self.add_user(user_id, whitelisted=1) #Anyways if we pass 1 into our add_user object it'll make it as whitelisted
        return 1 

    def remove_whitelist(self, user_id: int):
        if self.check_user(user_id) == 0:
            self.add_user(user_id)

        if self.check_whitelisted(user_id) == 0:
            return 

        self._c.execute(f'UPDATE whitelist SET whitelisted=0, time="." WHERE user_id={int(user_id)}')
        self._conn.commit()
        return