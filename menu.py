import pygame_menu
from settings import *
from car import Car 

class Menu:
    def __init__(self, screen):
        self.selected = False
        self.screen = screen

        self.menu = pygame_menu.Menu("Wheels of ice", SCREENRECT.width, SCREENRECT.height, theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.button("Play", self.start_the_game)
        self.menu.add.dropselect("Cars", [("Dazda RD7 FD", 1), ("Donda TSX", 2)], onchange=self.car)
        self.menu.add.dropselect("Tracks", [("Mount Akagi", 1), ("Usui Pass", 2), ("Mount Haruna", 3)], onchange=self.track)
        self.menu.add.button("Quit", pygame_menu.events.EXIT)

        self.pause_menu = pygame_menu.Menu("Pause", SCREENRECT.width, SCREENRECT.height, theme=pygame_menu.themes.THEME_DARK)
        self.pause_menu.add.button("Resume", self.resume)
        self.pause_menu.add.button("reset", self.reset)
        self.pause_menu.add.button("Back to menu", self.back_to_menu)
        self.pause_menu.add.button("Quit", pygame_menu.events.EXIT)

        self.auto = Car("car_1.png", self.screen, 120, 2.5, 1, 0.98, 0.4, 0.9, 170, 150)

    def car(self, value, car):
        print(car)
        self.file = open("selected_car.txt", "w")
        self.file.write("car_" + str(car) + ".png")
        self.file.close()
        self.selected = True

    def track(self, value, track):
        print(track)
        self.file = open("selected_track.txt", "w")
        self.file.write("track_" + str(track))
        self.file.close()
        self.selected = True

    def start_the_game(self):
        self.menu.disable()
        self.selected = True

    def resume(self):
        if self.resume == True:
            self.pause_menu.disable()
            self.auto.velocity = 0
            return self.start_the_game()
        else:
            self.auto.velocity = self.auto.velocity

    def reset(self):
        self.pause_menu.disable()
        return self.start_the_game()

    def back_to_menu(self):
        self.pause_menu.disable()
        self.menu.enable()

    def pause(self):
        self.pause_menu.enable()
        self.pause_menu.mainloop(self.screen)

    def back(self):
        self.pause_menu.disable()
        self.menu.enable()

    def run(self):
        self.menu.mainloop(self.screen)

# test menu
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
    menu = Menu(screen)
    while True:

        menu.run()


    pygame.quit()
