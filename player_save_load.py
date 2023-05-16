"""
Player class for the game
Controling money, cars, upgrades, experience, etc.
useful for saving and loading
"""
from settings import *
# use json

class Player():
    def __init__(self):
        self.money = 0
        self.cars = []
        self.upgrades = []
        self.experience = 0