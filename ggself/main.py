import discord 
from discord.ext import commands 
from discord import Game 
from discord.ext.commands import errors 

import discord.utils 
from discord.utils import find, get 

import aiohttp
import httpx
import asyncio 

import os 
import sys 
import platform 
import io

import random 
import string 

import requests 
import webbrowser 

import json 
import sqlite3

import time 
import datetime

import colorama 
from colorama import init, Fore 
if os.name == 'nt':
    init(convert=True) #Windows need to enable this to get their colors working

import base64
import subprocess

#################################################

def clear():
    if os.name == 'nt':
        return os.system('cls')
    return os.system('clear')

#################################################

class Config():
    def __init__(self):
        with open("Config/Bot.$", "r") as output:
            self._b = json.load(output)

    @property 
    def token(self):
        return self._b["Bot Token"]

    @property 
    def prefix(self):
        return self._b["Bot Prefix"]

c = Config()

#################################################

class Database():
    pass #TODO: Refresh this shit

d = Database()

#################################################

class Tracking():
    def __init__(self): #I didn't optimised this shit but it's working so "ok"
        self._delmsglog = "Logger/Sniper/Message/Deleted/Sniped.m"
        self._twlog = "Logger/Sniper/Message/Tracked/Tracked.t"
        self._rpdm = {}
        self._rp = {}

        with open("AutoReply/ReplyDM.dm", "r") as output:
            for line in output.read().splitlines():
                msg = line.split(" = ")[0]
                reply = line.split(" = ")[1]

                self._rpdm[msg] = reply

        self._rpdml = [*self._rpdm]
        self._rpdmr = []

        for value in self._rpdm.items():
            self._rpdmr.append(value[1])

        

        with open("AutoReply/ReplyServer.sv", "r") as output:
            for line in output.read().splitlines():
                msg = line.split(" = ")[0]
                reply = line.split(" = ")[1]

                self._rp[msg] = reply

        self._rpl = [*self._rp]
        self._rpr = []

        for value in self._rp.items():
            self._rpr.append(value[1])

        self._tw = []
        with open("Sniper/Word.s", "r") as out:
            for line in out.read().splitlines():
                self._tw.append(line)


    def append(self, filename, text: str):
        with open(filename, "a+") as out:
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
        with open("Logger/AutoReply/DM.dm", "a+") as out:
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
        with open("Logger/AutoReply/Server.sv", "a+") as out:
            out.write(f"AutoRep DM | {time} - {authname} - {authid} - {guildname} - {guildid} - {msgcontent} - {message}\n")

    ############################################### 

    def deleted_msg(self, msg, authname, guildname):
        t = time.strftime("%-m/%d/%y - %H:%M:%S")
        text = f"{t} - {msg} - {authname} - {guildname}\n"
        self.append(self._delmsglog, text)


    def is_trackedp(self, msg, authname, guildid):
        if any(msg in s for s in self._tw):
            t = time.strftime("%-m/%d/%y - %H:%M:%S")
            text = f"{t} - {msg} - {authname} - {guildid}\n"
            self.append(self._twlog, text)
            return
        return

t = Tracking()

#################################################

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
            self._c.execute("INSERT INTO whitelist VALUES (?, ?, ?)", (user_id, whitelisted, time.strftime("%-m/%d/%y - %H:%M:%S")))
            self._conn.commit()
            return 1
        return 0

    def add_whitelist(self, user_id: int):
        t = time.strftime("%-m/%d/%y - %H:%M:%S")
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

l = List()

#################################################

class Sniper():
    def __init__(self):
        self._n = ""

        with open("Sniper/Nitro.s", "r") as out:
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

s = Sniper()

#################################################

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
        with open(f, "a+") as out:
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

log = Log()

#################################################

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
        
g = Generator()

#################################################

bot = commands.Bot(command_prefix=c.prefix, self_bot=True)


@bot.event 
async def on_message(msg):  
    if msg.guild:
        if msg.author.id == self._bot.user.id:
            await self._bot.process_commands(msg)
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

            t.add_ar_dm(time.strftime("%-m/%d/%y - %H:%M:%S"), msg.author.name, msg.author.id, msg.guild.name, msg.guild.id, msg.content, message)

        if t.message_ar(msg.content) == 1:
            message = t.get_ans(msg.content)
            if message == 0:
                return
            await msg.channel.send(message)

            t.add_ar(time.strftime("%-m/%d/%y - %H:%M:%S"), msg.author.name, msg.author.id, msg.guild.name, msg.guild.id, msg.content, message)

        t.is_trackedp(msg.content, msg.author.name, msg.guild.name)

#################################################

@bot.command()
async def whitelist(ctx):
    prefix = c.prefix
    embed = discord.Embed()
    embed.add_field(name="Whitelist Commands", value=f"```{prefix}.add_whitelist <user> | Add someone to the whitelist\n{prefix}remove_whitelist <user> | Remove someone from the whitelist```")
    await ctx.send(embed=embed)

@bot.command()
async def add_whitelist(ctx, user: discord.User=None):
    if user is None:
        embed = discord.Embed(
            color = discord.Color.red(),
            title="Error",
            description = "You didn't specified any user to add"
        )
        await ctx.send(embed=embed)
        return

    if user.id == bot.user.id:
        embed = discord.Embed(
            color = discord.Color.red(),
            title = "Error",
            description = "You can't add yourself to the whitelist"
        )
        await ctx.send(embed=embed)
        return
    
    l.add_whitelist(user.id)

    embed = discord.Embed(
        title = "Succes",
        description = f"I added {user.mention} to the whitelist"
    )
    embed.set_footer(text=f"User ID: {user.id}", icon_url=user.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def remove_whitelist(ctx, user: discord.User=None):
    if user is None:
        embed = discord.Embed(
            color = discord.Color.red(),
            title="Error",
            description = "You didn't specified any user to remove"
        )
        await ctx.send(embed=embed)
        return

    if user.id == bot.user.id:
        embed = discord.Embed(
            color = discord.Color.red(),
            title = "Error",
            description = "You can't remove yourself from the whitelist"
        )
        await ctx.send(embed=embed)
        return
    
    if l.check_whitelisted(user.id) == 1:
        l.remove_whitelist(user.id)

        embed = discord.Embed(
            title = "Succes",
            description = f"I removed {user.mention} from the whitelist"
        )
        embed.set_footer(text=f"User ID: {user.id}", icon_url=user.avatar_url)
        await ctx.send(embed=embed)
        return

    if l.check_whitelisted(user.id) == 0:
        embed = discord.Embed(
            color = discord.Color.red(),
            title = "Error", 
            description = "This user is not on the whitelist"
        )

        await ctx.send(embed=embed)

################################################# FUN COMMANDS

@bot.command() #Credit: TOG6
async def gayrate(ctx, user: discord.User):
    num = random.randint(1, 99)
    embed = discord.Embed(
        title = f"{user.name}'s Gay %: ",
        description = f'{num}' #The F-String auto-convert int to str
    )
    await ctx.send(embed=embed)

@bot.command(name="8ball") #We need to use name because a func can't start with a number - Credit: TOG6
async def _8ball(ctx, *, question):
    responses = ['It is certain.', 'It is decidedly so', 'Without a Doubt', 'YES - Definitely', 'You may rely on it', 'As I see it, YES', 'Most Likely', 'Outlook good', 'Yes.', 'Signs Point To YES!', 'Reply Hazy, try again!', 'Ask Again Later', 'Better Not Tell You Now', 'Cannot Predict Now', 'Concentrate and ask again', 'Dont Count ON it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very Doubtful']
    saxena = random.choice(responses)
    await ctx.send(saxena)

@bot.command() #Credit: TOG6
async def car(ctx):
    message = await ctx.send("""```
_______
/|_||_\`.__
(   _    _ _|
=`-(_)--(_)-' 
    ```""")
    await message.edit(content="""```
    _______
    /|_||_\`.__
    (   _    _ _|
    =`-(_)--(_)-' 
    ```""")
    await message.edit(content="""```
        _______
        /|_||_\`.__
        (   _    _ _|
        =`-(_)--(_)-' 
    ```""")
    await message.edit(content="""```
            _______
            /|_||_\`.__
            (   _    _ _|
            =`-(_)--(_)-' 
    ```""")
    await message.edit(content="""```
                    _______
                    /|_||_\`.__
                    (   _    _ _|
                    =`-(_)--(_)-' 
    ```""")
    await message.edit(content="""```
                            _______
                            /|_||_\`.__
                            (   _    _ |
                            =`-(_)--(_)-' 
    ```""")
    await message.edit(content=f"""```
                            _______
                            /|_||_\`.__
                            (   _    _ |
                            =`-(_)--(_)-' 
    ```""")

@bot.command()
async def define(ctx, *, query):
    embed_error = discord.Embed(
        color = discord.Color.red(),
        title = "Error",
        description = f"Can't find a definition for `{query}`"
    )

    try:
        url = f"http://api.urbandictionary.com/v0/define?term={query}"
        r = requests.get(url).json()
        definition = r['list'][0]['definition']
        embed = discord.Embed(
            title = "Definition",
            description = f"{query} Definition: {definition}"
        )
        await ctx.send(embed=embed)
    except:
        await ctx.send(embed=embed_error)

@bot.command() #Credit: TOG6
async def minesweep(ctx):
    k = ["🍌", "🍌", "🍌", "💣"]

    await ctx.send(f"""||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||
||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||
||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||
||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||
||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||||{random.choice(k)}||
""")

@bot.command()
async def wife(ctx):
    wives = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '20 - But youre gayyyyyyyyyy!')
    await ctx.send(f'Answer: {random.choice(wives)}')

@bot.command() #Credit: TOG6
async def simprate(ctx):
    numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100']
    numran = random.choice(numeros)
    await ctx.send("Simp Rate = " + numran + "%")

@bot.command()
async def hack(ctx, user: discord.User=None): #It's only a fake hack, nothing's real
    if user is None:
        user = ctx.author 
    
    embed = discord.Embed(
        title = "Loading ...", 
        description = f"We're hacking {user.mention} ..."
    )
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(0.5)

    ip = g.get_ip

    user_id = str(user.id)
    ascx = user_id.encode('ascii')

    wbytes = base64.b64encode(ascx) 
    result = wbytes.decode("ascii") 

    username_lower = user.name.lower().replace(" ", "")
    ggmail = f"{username_lower}@gmail.com"


    embed = discord.Embed(
        title = f"Successfuly hacked {user.name}",
        description = f'Token: `{result}.***************************`\n Email: `{ggmail}`\n IP: `{ip}`'
    )

    await msg.edit(embed=embed)

@bot.command()
async def ip(ctx, user: discord.User=None):
    if user is None:
        user = ctx.author

    embed = discord.Embed(
        title = f"{user.name}'s IP",
        description = f"`{g.get_ip}`"
    )

    await ctx.send(embed=embed)

@bot.command()
async def pp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.author
    pps = ['=', '==', '===', '====', '=====', '======', '=======', '========', '=========', '==========', '===========', '============', '=============', '=================']
    ppx = random.choice(pps)
    await ctx.send("8" + ppx + "D")

@bot.command()
async def math(ctx, *, c):
    try:
        result = eval(c)
        embed = discord.Embed(
            title = "Math Calculator",
            description = f'```{result}```'
        )
        await ctx.send(embed=embed)

    except:
        embed = discord.Embed(
            color = discord.Color.red(),
            title = "Error",
            description = "Your context is invalid"
        )

        await ctx.send(embed=embed)

@bot.command()
async def python(ctx, *, c):
    try:
        old_stdout = sys.stdout 
        new_stdout = io.StringIO() 
        sys.stdout = new_stdout 
        local_variable = 2
        exec(c)
        r = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout 
        
        result = str(r)
        if result == "" or result == "  " or result == "  " or result is None:
            rr = "No result"
        rr = result 

        embed = discord.Embed(
            title = "Result",
            description = f'```{rr}```'
        )
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        embed = discord.Embed(
            color = discord.Color.red(),
            title = "Error",
            description = f"```{e}```"
        )

        await ctx.send(embed=embed)

#################################################

deletedcontent = []
deleteduser = []
 
@bot.event
async def on_message_delete(message): #Sniper Credit: TOG6
    if message.author.id == bot.user.id:
        return

    deletedcontent.append(message.content)
    deleteduser.append(message.author)

    t.deleted_msg(message.content, message.author.name, message.guild.name)
        
@bot.command()
async def snipe(ctx):
    
    k = deletedcontent[-1]
    v = deleteduser[-1]

    try:
        embed = discord.Embed(
            title = f"Sniper",
            description = f"```Message: {k} | Author: {v}```"
        )
        await ctx.message.edit(embed=embed)

    except KeyError:
        await ctx.message.edit("Nothing to snipe.")

#################################################

if __name__ == '__main__':
    bot.run(c.token, bot=False)