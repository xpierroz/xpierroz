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


class Tracking():
    def __init__(self): #I didn't optimised this shit but it's working so "ok"
        self._delmsglog = "Logger/Sniper/Message/Deleted/Sniped.m"
        self._twlog = "Logger/Sniper/Message/Tracked/Tracked.t"
        self._rpdm = {}
        self._rp = {}

        with open("AutoReply/ReplyDM.dm", "r", encoding="utf-8") as output:
            for line in output.read().splitlines():
                msg = line.split(" = ")[0]
                reply = line.split(" = ")[1]

                self._rpdm[msg] = reply

        self._rpdml = [*self._rpdm]
        self._rpdmr = []

        for value in self._rpdm.items():
            self._rpdmr.append(value[1])

        

        with open("AutoReply/ReplyServer.sv", "r", encoding="utf-8") as output:
            for line in output.read().splitlines():
                msg = line.split(" = ")[0]
                reply = line.split(" = ")[1]

                self._rp[msg] = reply

        self._rpl = [*self._rp]
        self._rpr = []

        for value in self._rp.items():
            self._rpr.append(value[1])

        self._tw = []
        with open("Sniper/Word.s", "r", encoding="utf-8") as out:
            for line in out.read().splitlines():
                self._tw.append(line)


    def append(self, filename, text: str):
        with open(filename, "a+", encoding="utf-8") as out:
            out.write(text)

    def message_ar_dm(self, word: str):
        if any(word in s for s in self._rpdml):
            return 1
        return 0

    def get_ans_dm(self, word: str):
        try:
            r = self._rpdm[word]
            return r
        except:
            return 0

    @property
    def check_reply_dm(self):
        return self._rpdm

    @property 
    def rpdm_msg(self):
        return self._rpdml 

    @property 
    def rpdm_ans(self):
        return self._rpdmr

    def add_ar_dm(self, time, authname, authid, guildname, guildid, msgcontent, message):
        with open("Logger/AutoReply/DM.dm", "a+", encoding="utf-8") as out:
            out.write(f"AutoRep DM | {time} - {authname} - {authid} - {guildname} - {guildid} - {msgcontent} - {message}\n")

    ############################ TODO: Refresh this Syntax

    def message_ar(self, word: str):
        if any(word in s for s in self._rpl):
            return 1
        return 0

    def get_ans(self, word: str):
        try:
            r = self._rp[word]
            return r
        except:
            return 0

    @property
    def check_reply(self):
        return self._rp

    @property 
    def rp_msg(self):
        return self._rpl 

    @property 
    def rp_ans(self):
        return self._rpr

    def add_ar(self, time, authname, authid, guildname, guildid, msgcontent, message):
        with open("Logger/AutoReply/Server.sv", "a+", encoding="utf-8") as out:
            out.write(f"AutoRep DM | {time} - {authname} - {authid} - {guildname} - {guildid} - {msgcontent} - {message}\n")

    ############################################### 

    def deleted_msg(self, msg, authname, guildname):
        t = time.strftime("%m/%d/%y - %H:%M:%S")
        text = f"{t} - {msg} - {authname} - {guildname}\n"
        self.append(self._delmsglog, text)


    def is_trackedp(self, msg, authname, guildid):
        if any(msg in s for s in self._tw):
            t = time.strftime("%m/%d/%y - %H:%M:%S")
            text = f"{t} - {msg} - {authname} - {guildid}\n"
            self.append(self._twlog, text)
            return
        return