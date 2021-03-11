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


class events(commands.Cog):
    def __init__(self, bot):
        self._bot = bot 
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Ready!')
        
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild:
            if msg.author.id == self._bot.user.id:
                # We made this check because without cogs we needed to add bot.process_commands(msg)
                return 

            if l.check_whitelisted(msg.author.id) == 1:
                return

            ############################ SNIPERS PARTS 
            #TODO: Continue sniper w/ Giveaway & More

            if 'gift/' in msg.content:
                if s.nitro_a == 1:
                    code = msg.content.split("gift/")[1]
                    if len(code) == 16 or len(code) == 24:
                        if s.get_nitro(code) == 0:
                            log.invalid_nitro(code, msg.author.name, msg.author.id, msg.guild.name, msg.guild.id)

                        if s.get_nitro(code) == 5:
                            log.invalid_nitro(code, msg.author.name, msg.author.id, msg.guild.name, msg.guild.id)

                        if s.get_nitro(code) == 4:
                            log.ratelimited_nitro(code, msg.author.name, msg.author.id, msg.guild.name, msg.guild.id)
                
                        if s.get_nitro(code) == 3:
                            log.alreadyclaimed_nitro(code, msg.author.name, msg.author.id, msg.guild.name, msg.guild.id)

                        if s.get_nitro(code) == 2:
                            log.claimed_nitro(code, msg.author.name, msg.author.id, msg.guild.name, msg.guild.id)

                        return

                    log.invalid_nitro(code, msg.author.name, msg.author.id, msg.guild.name, msg.guild.id) #If the len of the code isn't 16 or 24 it means that the code is invalid
                pass

            ############################ AUTO REPLY PART

            if t.message_ar_dm(msg.content) == 1:
                message = t.get_ans_dm(msg.content)
                if message == 0:
                    return
                await msg.author.send(message)

                t.add_ar_dm(time.strftime("%m/%d/%y %H:%M:%S"), msg.author.name, msg.author.id, msg.guild.name, msg.guild.id, msg.content, message)

            if t.message_ar(msg.content) == 1:
                message = t.get_ans(msg.content)
                if message == 0:
                    return
                await msg.channel.send(message)

                t.add_ar(time.strftime("%m/%d/%y %H:%M:%S"), msg.author.name, msg.author.id, msg.guild.name, msg.guild.id, msg.content, message)

            t.is_trackedp(msg.content, msg.author.name, msg.guild.name)
        