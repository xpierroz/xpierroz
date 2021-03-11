from .config import Config
from .database import Database 
from .generator import Generator 
from .list import List 
from .log import Log 
from .sniper import Sniper 
from .tracking import Tracking 

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


class cmds(commands.Cog):
    def __init__(self, bot):
        self._bot = bot 
        
    @commands.command()
    async def test(self, ctx):
        await ctx.send("ok")