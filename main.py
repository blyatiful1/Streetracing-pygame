import pygame
import pygame.mixer
#Herr Adams ist eine toller Lehrer
from utils import *
from camera import *
from car import Car
from track import Track
from overlay import *
from settings import *
from player_save_load import Player
from menu import Menu

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Racing J")

        self.screen = pygame.display.set_mode(SCREENRECT.size)
        self.clock = CLOCK

        pygame.mixer.music.load("music/bg music.mp3")
        pygame.mixer.music.set_volume(0.1)

        self.player = Player()
        self.player.load()

        self.track = None

        self.car = None

        #self.camera_group = CameraGroup(self.screen, self.car, self.track)

        self.overlay = Overlay()
        self.speedometer = Speedometer(SCREENRECT.width - 100, SCREENRECT.height - 100, 50)

        self.menu = Menu(self.screen)
        for car in self.player.cars:
            self.menu.add_car(car)
        self.menu.init_menus()

        self.off_track_timer = Timer(5000)

        self.running = True
        self.menu_running = True
        self.game_running = False
        self.pause_running = False

    def main_loop(self):
        while self.running:
            while self.menu_running:
                self.menu.mainmenu()
                self.start_countdown()
                pygame.mixer.music.play(-1)
                self.game_running = True
                self.menu_running = False

                if self.menu.selected:
                    self.reset_race()

            while self.pause_running:
                self.menu.pause()

                if self.menu.selected:
                    self.reset_race()
                    self.pause_running = False
                    self.game_running = True
                
                if self.menu.restart_requested:
                    self.reset_race()
                    self.pause_running = False
                    self.game_running = True
                    self.menu.restart_requested = False

                self.pause_running = False
                self.game_running = True

            while self.game_running:
                self.events()
                self.update()
                self.draw()
                self.clock.tick(FPS)
                
        self.player.update_player()
        self.player.close()

        pygame.quit()
        sys.exit()

    def events(self):
        self.car.events()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.game_running = False
                self.pause_running = True
                #self.menu.pause()

    def update(self):
        self.moving = False

        self.camera_group.update()

        self.car.update(self.clock.get_time() / 100)

        if not self.track.is_on_track(self.car.rect):
            self.car.velocity *= 0.92
            self.car.angle_velocity *= 0.92
            if self.off_track_timer.check():
                self.reset_race()
        else:
            self.off_track_timer.reset()
            
        if self.car.hitbox.colliderect(self.track.finish_rect):
            self.overlay.win = True
            pygame.mixer.music.fadeout(3000)

            self.game_running = False

            end_time = time.time() - self.overlay.start_time
            self.player.add_money(round(10000 / end_time))
            self.player.add_experience(round(5000 / end_time))

            self.player.add_highscore("player", round(time.time() - self.overlay.start_time, 2), self.track.track_name, self.car.car_name)

            if self.player.get_experience() >= 250:
                if ("Donda TSX", 2) not in self.player.cars:
                    self.player.add_car(("Donda TSX", 2))
                    self.menu.add_car(("Donda TSX", 2))
                    self.menu.init_menus()
                    self.player.update_player()

            if self.player.get_experience() >= 500:
                if ("Yotota Yiras", 3) not in self.player.cars:
                    self.player.add_car(("Yotota Yiras", 3))
                    self.menu.add_car(("Yotota Yiras", 3))
                    self.menu.init_menus()
                    self.player.update_player()

            print(self.player)
            self.player.update_player()

            for row in self.player.get_highscore():
                print(row)

            self.menu.menu.enable()
            self.menu_running = True

        if self.car.hitbox.colliderect(self.track.border_rect):
            self.car.velocity *= -2

    def draw(self):
        #self.screen.fill((0, 0, 0))

        self.camera_group.custom_draw()

        self.overlay.run(self.car)

        #self.speedometer.draw(self.screen, self.car.speed * 1.5)

        #self.camera_group.temp_draw()

        pygame.display.flip()

    def start_countdown(self):
        self.overlay.start_countdown()

    def reset_race(self):
        self.file = open("selected_car.txt", "r")
        car = str(self.file.read())
        if car == "car_1.png":
            self.car = Car(car, self.screen, 100, 2.3, 1, 0.98, 0.4, 0.9, 50, 125, "Dazda RX7")
        elif car == "car_2.png":
            self.car = Car(car, self.screen, 110, 2.5, 1, 0.98, 0.27, 0.9, 50, 125, "Donda TSX")
        elif car == "car_3.png":
            self.car = Car(car, self.screen, 120, 2.7, 1, 0.98, 0.4, 0.9, 50, 110, "Yotota Yiras")
        else:
            print("error")
        self.file.close()

        self.file = open("selected_track.txt", "r")
        self.track = Track(str(self.file.read()))
            
        self.file.close()

        self.car.position = self.track.get_start_rect().center
        self.car.velocity = pygame.math.Vector2(0, 0)
        self.car.angle_velocity = 0
        self.car.angle = 0
        self.car.direction = pygame.math.Vector2(0, 1)

        self.camera_group = CameraGroup(self.screen, self.car, self.track)

        self.overlay.reset_start_time()

if __name__ == "__main__":
    game = Game()
    game.main_loop()