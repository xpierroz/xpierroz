from .config import Config
from .database import Database 
from .generator import Generator 
from .list import List 
from .log import Log 
from .sniper import Sniper 
from .tracking import Tracking 

from .events import events
from .commands import cmds

import discord 
from discord.ext import commands

import os
import sys 
import platform

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

c = Config()
d = Database()
g = Generator()
l = List()
log = Log()
s = Sniper()
t = Tracking()


bot = commands.Bot(command_prefix=c.prefix, self_bot=True)

def load_cogs():
    bot.add_cog(events(bot))
    bot.add_cog(cmds(bot))
    return

def run():
    load_cogs()
    bot.run(c.token, bot=False)
