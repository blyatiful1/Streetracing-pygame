import pygame
#Herr Adams ist eine toller Lehrer
from utils import *
from camera import *
from car import Car
from track import Track
from overlay import *
from settings import *
from menu import Menu
from timer import Timer

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENRECT.size)
        self.clock = CLOCK
        pygame.display.set_caption("Streetracing Japan")

        self.track = Track("track_1")

        self.car = Car("car_1.png", self.screen, 120, 2.5, 1, 0.98, 0.4, 0.9, 170, 150)
        self.car.position = self.track.get_start_rect().topleft

        self.camera_group = CameraGroup(self.car, self.track)

        self.overlay = Overlay()
        self.speedometer = Speedometer(SCREENRECT.width - 100, SCREENRECT.height - 100, 50)

        self.menu = Menu(self.screen)

        self.off_track_timer = Timer(5000)

        self.running = True
        self.menu_running = True
        self.game_running = False

    def main_loop(self):
        while self.running:
            while self.menu_running:
                self.menu.menu.mainloop(self.screen)
                self.start_countdown()
                self.game_running = True
                self.menu_running = False

                if self.menu.selected:
                    self.reset_race()

            while self.game_running:
                self.events()
                self.update()
                self.draw()
                self.clock.tick(FPS)

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
                self.menu.pause()

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
            self.game_running = False
            self.menu.menu.enable()
            self.menu_running = True

        if self.car.hitbox.colliderect(self.track.border_rect):
            self.car.velocity -= 2 * self.car.velocity

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.camera_group.custom_draw()

        self.overlay.run(self.clock.get_fps(), self.car)

        self.speedometer.draw(self.screen, self.car.speed * 1.5)

        self.camera_group.temp_draw()

        pygame.display.flip()

    def start_countdown(self):
        self.overlay.start_countdown()

    def reset_race(self):
        self.file = open("selected_car.txt", "r")
        car = str(self.file.read())
        if car == "car_1.png":
            self.car = Car(car, self.screen, 90, 2, 1, 0.98, 0.4, 0.9, 50, 125)
        elif car == "car_2.png":
            self.car = Car(car, self.screen, 110, 2.5, 1, 0.98, 0.27, 0.9, 50, 125)
        else:
            print("error")
        self.file.close()

        self.file = open("selected_track.txt", "r")
        track = str(self.file.read())
        if track == "track_3":
            self.track = Track(track, 3)
        else:
            self.track = Track(track)
            
        self.file.close()

        self.car.position = self.track.get_start_rect().center
        self.car.velocity = pygame.math.Vector2(0, 0)
        self.car.angle_velocity = 0
        self.car.angle = 0
        self.car.direction = pygame.math.Vector2(0, 1)

        self.camera_group = CameraGroup(self.car, self.track)

        self.overlay.reset_start_time()

if __name__ == "__main__":
    game = Game()
    game.main_loop()