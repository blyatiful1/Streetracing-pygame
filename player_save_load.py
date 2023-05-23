from settings import *
import sqlite3, datetime

class Player():
    def __init__(self):
        self.conn = sqlite3.connect("player.db")
        self.c = self.conn.cursor()
        self.money = 0
        self.cars = []
        self.upgrades = []
        self.experience = 0

        self.create_player()
        self.create_highscore()

    def create_player(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS player
            (money INTEGER, cars TEXT, upgrades TEXT, experience INTEGER)''')
        self.conn.commit()

    def create_highscore(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS highscore
            (name TEXT, time FLOAT, track TEXT, car TEXT, date TEXT)''')
        self.conn.commit()

    def drop_player(self):
        self.c.execute("DROP TABLE player")
        self.conn.commit()

    def drop_highscore(self):
        self.c.execute("DROP TABLE highscore")
        self.conn.commit()

    def close(self):
        self.conn.close()

    def load(self):
        self.c.execute("SELECT * FROM player")
        player = self.c.fetchone()
        if player:
            self.money = player[0]
            self.cars = eval(player[1])
            self.upgrades = eval(player[2])
            self.experience = player[3]

    def save(self):
        self.c.execute("INSERT INTO player VALUES (?, ?, ?, ?)", (self.money, str(self.cars), str(self.upgrades), self.experience))
        self.conn.commit()

    def update_player(self):
        self.c.execute("UPDATE player SET money = ?, cars = ?, upgrades = ?, experience = ?", (self.money, str(self.cars), str(self.upgrades), self.experience))
        self.conn.commit()

    def add_highscore(self, name, time, track, car):
        self.c.execute("INSERT INTO highscore VALUES (?, ?, ?, ?, ?)", (name, time, track, car, datetime.datetime.now()))
        self.conn.commit()

    def get_highscore(self):
        self.c.execute("SELECT * FROM highscore")
        return self.c.fetchall()

    def add_money(self, amount):
        self.money += amount

    def remove_money(self, amount):
        self.money -= amount

    def add_car(self, car):
        self.cars.append(car)

    def remove_car(self, car):
        self.cars.remove(car)

    def add_upgrade(self, upgrade):
        self.upgrades.append(upgrade)

    def remove_upgrade(self, upgrade):
        self.upgrades.remove(upgrade)

    def add_experience(self, amount):
        self.experience += amount

    def remove_experience(self, amount):
        self.experience -= amount

    def get_money(self):
        return self.money

    def get_cars(self):
        return self.cars

    def get_upgrades(self):
        return self.upgrades

    def get_experience(self):
        return self.experience

    def set_money(self, amount):
        self.money = amount

    def set_upgrades(self, upgrades):
        self.upgrades = upgrades

    def set_experience(self, amount):
        self.experience = amount

    def reset(self):
        self.drop_player()
        self.drop_highscore()
        self.create_player()
        self.create_highscore()

    def __str__(self):
        return f"Player: {self.money} {self.cars} {self.upgrades} {self.experience}"
    
if __name__ == "__main__":
    player = Player()
    player.reset()
    player.set_money(1000)
    player.add_car(("Dazda RX 7", 1))

    player.save()
    print(player)
    player.close()