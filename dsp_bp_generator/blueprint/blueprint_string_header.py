from .packet import Packet
import random

class BlueprintStringHeader:
    SIZE = 10

    def __init__(self):
        self.fixed0_1 = 0
        self.layout = 10
        self.icon0 = 0
        self.icon1 = 0
        self.icon2 = 0
        self.icon3 = 0
        self.icon4 = 0
        self.fixed0_2 = 0
        self.timestamp = 0
        self.game_version = "0.10.29.22015"
        self.short_desc = "New%20Blueprint"

    def parse(self, string):
        component = string[BlueprintStringHeader.SIZE:].split(",")
        self.fixed0_1 = component[0]
        self.layout = component[1]
        self.icon0 = component[2]
        self.icon1 = component[3]
        self.icon2 = component[4]
        self.icon3 = component[5]
        self.icon4 = component[6]
        self.fixed0_2 = component[7]
        self.timestamp = component[8]
        self.game_version = component[9]
        self.short_desc = component[10]

    def serialize(self):
        return f"BLUEPRINT:{str(self.fixed0_1)},{str(self.layout)},{str(self.icon0)},{str(self.icon1)},{str(self.icon2)},{str(self.icon3)},{str(self.icon4)},{str(self.fixed0_2)},{str(self.timestamp)},{str(self.game_version)},{str(self.short_desc)},"

    def __str__(self):
        return f"""
Blueprint string header:
========================
Binary data: {self.serialize()}
========================
Fixed 1: {self.fixed0_1}
Layout: {self.layout}
Icon0: {self.icon0}
Icon1: {self.icon1}
Icon2: {self.icon2}
Icon3: {self.icon3}
Icon4: {self.icon4}
Fixed 2: {self.fixed0_2}
Timestamp: {self.timestamp}
Game version: {self.game_version}
Description: {self.short_desc}
"""