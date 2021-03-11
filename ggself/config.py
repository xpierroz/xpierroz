import os
import sys 

import json 



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