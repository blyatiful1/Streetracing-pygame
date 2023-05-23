from settings import *
import time

class Overlay:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.font = FONT
        self.win = False

        self.time = time.time()
        self.start_time = 0

    def draw_fps(self, fps):
        fps = self.font.render("FPS: " + str(int(fps)), True, (255, 255, 255))
        self.display.blit(fps, (0, 0))

    def draw_pos(self, target):
        pos = self.font.render("Pos: " + str(target.rect.center), True, (0, 0, 0))
        self.display.blit(pos, (0, 20))

    def draw_speed(self, speed):
        speed = self.font.render("Speed: " + str(int(speed * 1.5)) + "km/h", True, (255, 255, 255))
        self.display.blit(speed, (0, SCREENRECT.height - speed.get_height()))

    def draw_now_playing(self):
        now_playing = self.font.render("Now playing: " + str(MUSIC), True, (255, 255, 255))
        self.display.blit(now_playing, (SCREENRECT.width / 2 - now_playing.get_width() / 2, 0))

    def run(self, target):
        if self.win:
            self.time = time.time() - self.start_time
            self.draw_win_screen()

            time.sleep(2)
            self.win = False
        else:
            #self.draw_fps(clock)
            #+self.draw_pos(target)
            self.draw_speed(target.speed)
            self.draw_now_playing()

    def start_countdown(self):
        self.display.fill((0, 0, 0))
        countdown = 3
        while countdown > 0:
            self.display.fill((0, 0, 0))
            text = self.font.render(str(countdown), True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREENRECT.width / 2, SCREENRECT.height / 2))
            self.display.blit(text, text_rect)
            pygame.display.flip()
            time.sleep(1)
            countdown -= 1

    def draw_win_screen(self):
        self.display.fill((0, 0, 0))
        win = self.font.render("Race finished!", True, (255, 255, 255))
        win_rect = win.get_rect(center=(SCREENRECT.width / 2, SCREENRECT.height / 2))

        time_text = self.font.render("Time: " + str(round(self.time, 2)) + " sec", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(SCREENRECT.width / 2, SCREENRECT.height / 2 + 50))

        self.display.blit(time_text, time_rect)
        self.display.blit(win, win_rect)
        pygame.display.flip()

    def reset_start_time(self):
        self.start_time = time.time()

#--------------#
# Experimental #
#--------------#
class Speedometer:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.font = FONT
        self.speed_text = self.font.render("0", True, (255, 255, 255))
        self.hand_length = self.radius - 10
        self.hand_thickness = 3

    def draw(self, screen, speed):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius, 2)

        speed_text = str(int(speed)) + " km/h"
        if speed != int(speed):
            speed_text = str(int(speed)) + " km/h"
        self.speed_text = self.font.render(speed_text, True, (255, 255, 255))
        text_rect = self.speed_text.get_rect(center=(self.x, self.y + self.radius + 20))
        screen.blit(self.speed_text, text_rect)

        angle = math.radians(225 - speed * 1.5)
        end_x = self.x + self.hand_length * math.cos(angle)
        end_y = self.y - self.hand_length * math.sin(angle)
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (end_x, end_y), self.hand_thickness)