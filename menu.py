import pygame_menu
from settings import *
from player_save_load import Player

class Menu:
    def __init__(self, screen):
        self.selected = False
        self.restart_requested = False
        self.screen = screen
        self.player = Player()
        self.player.load()

        self.cars = []

        self.theme = pygame_menu.themes.THEME_DARK.copy()
        self.theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        self.theme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        self.theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        self.theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        self.theme.widget_font_size = 26

    def init_menus(self):
        self.menu = pygame_menu.Menu("Racing J", SCREENRECT.width, SCREENRECT.height, theme=self.theme)
        self.menu.add.button("Play", self.start_the_game)
        self.menu.add.dropselect("Cars", self.cars, onchange=self.car, 
                                        placeholder="Select a car", 
                                        selection_box_height=100)
        self.menu.add.dropselect("Tracks", [("Mount Akagi", 1), ("Usui Pass", 2), ("Mount Haruna", 3)],
                                        onchange=self.track,
                                        placeholder="Select a track",
                                        selection_box_height=100)
        self.menu.add.button("Highscores", self.highscores)
        self.menu.add.button("Settings", self.settings)
        self.menu.add.button("Quit", pygame_menu.events.EXIT)

        self.settings_menu = pygame_menu.Menu("Settings", SCREENRECT.width, SCREENRECT.height, theme=self.theme)
        self.settings_menu.add.dropselect("Resolution", [("Fullscreen", 1), ("1280x720", 2), ("800x600", 3)], onchange=self.resolution)
        self.settings_menu.add.button("Back to menu", self.back_to_menu)


        self.pause_menu = pygame_menu.Menu("Pause", SCREENRECT.width, SCREENRECT.height, theme=self.theme)
        self.pause_menu.add.button("Resume", self.pause_menu.disable)
        self.pause_menu.add.button("reset", self.reset)
        self.pause_menu.add.button("Back to menu", self.back_to_menu)
        self.pause_menu.add.button("Quit", pygame_menu.events.EXIT)

        highscores = self.player.get_highscore()
        self.highscore_menu = pygame_menu.Menu("Highscores", SCREENRECT.width, SCREENRECT.height, theme=self.theme)
        for highscore in highscores:
            self.highscore_menu.add.label(" Time: " + str(highscore[1]) + "| Track: " + highscore[2] + "| Car: " + highscore[3] + "| Date: " + str(highscore[4]))
        self.highscore_menu.add.button("Back to menu", self.back_to_menu)
        self.highscore_menu.add.button("Quit", pygame_menu.events.EXIT)

        #--------------#
        # experimental #
        #--------------#

        #self.win_menu = pygame_menu.Menu("You win!", SCREENRECT.width, SCREENRECT.height, theme=self.theme)
        #self.win_menu.add.label("Time: ")
        #self.win_menu.add.text_input("Player name: ")
        #self.win_menu.add.button("Back to menu", self.back_to_menu)
        #self.win_menu.add.button("Quit", pygame_menu.events.EXIT)

    def car(self, value, car):
        print(car)
        self.file = open("selected_car.txt", "w")
        self.file.write("car_" + str(car) + ".png")
        self.file.close()
        self.selected = True

    def add_car(self, car):
        self.cars.append(car)

    def track(self, value, track):
        print(track)
        self.file = open("selected_track.txt", "w")
        self.file.write("track_" + str(track))
        self.file.close()
        self.selected = True

    def resolution(self, value, resolution):
        if resolution == 1:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif resolution == 2:
            self.screen = pygame.display.set_mode((1280, 720))
        elif resolution == 3:
            self.screen = pygame.display.set_mode((800, 600))
        SCREENRECT.width = self.screen.get_width()
        SCREENRECT.height = self.screen.get_height()
        self.settings_menu.disable()

    def start_the_game(self):
        self.menu.disable()
        self.selected = True

    def resume(self):
        self.pause_menu.disable()

    def reset(self):
        self.pause_menu.disable()
        self.restart_requested = True

    def back_to_menu(self):
        #self.win_menu.disable()
        self.highscore_menu.disable()
        self.settings_menu.disable()
        self.pause_menu.disable()
        self.selected = True
        self.menu.enable()
        self.menu.mainloop(self.screen)

    def mainmenu(self):
        self.menu.enable()
        self.menu.mainloop(self.screen)

    def pause(self):
        self.pause_menu.enable()
        self.pause_menu.mainloop(self.screen)

    def highscores(self):
        self.highscore_menu.enable()
        self.highscore_menu.mainloop(self.screen)

    def settings(self):
        self.settings_menu.enable()
        self.settings_menu.mainloop(self.screen)

    def back(self):
        self.pause_menu.disable()
        self.menu.enable()

    def run(self):
        self.menu.mainloop(self.screen)

# test menu
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("RacingJ")
    screen = pygame.display.set_mode(SCREENRECT.size)
    menu = Menu(screen)
    menu.init_menus()
    menu.run()