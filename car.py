import pygame, sys
from pygame.locals import *
from settings import *
from utils import *

class Car(pygame.sprite.Sprite):
    def __init__(self, image, screen, max_vel, accel, decel, friction, angle_accel, angle_friction, car_width, car_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(get_image_path(image)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (car_width, car_height))
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.mask = pygame.mask.from_surface(self.image)
        self.rotated_image = self.image
        self.rotated_rect = self.rect
        
        #---------------#
        # Car variables #
        #---------------#
        self.max_vel = max_vel
        self.accel = accel
        self.decel = decel
        self.friction = friction
        self.angle_accel = angle_accel
        self.angle_friction = angle_friction
        self.offset = (self.rect.centerx, self.rect.centery)

        #-------------#
        # Car physics #
        #-------------#
        self.position = pygame.math.Vector2(0, 0)
        self.direction = pygame.math.Vector2(0, 1)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.angle_velocity = 0
        self.angle_acceleration = 0

        #-------------#
        # other stuff #
        #-------------#
        self.screen = screen
        self.is_moving = False
        self.moving_forward = False
        self.speed = 0

    def events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.acceleration = -self.accel
            self.is_moving = True
            self.moving_forward = True
        elif keys[pygame.K_s]:
            self.acceleration = self.decel
            self.is_moving = True
            self.moving_forward = False
        else:
            self.acceleration = 0
            self.is_moving = False

        if self.is_moving or self.speed > 1.5:
            if keys[pygame.K_a]:
                self.turn(-1)
            elif keys[pygame.K_d]:
                self.turn(1)
            else:
                self.angle_acceleration = 0
        else:
            self.angle_acceleration = 0
        
        if keys[pygame.K_SPACE]:
            self.handbrake()

    def turn(self, direction):
        self.angle_acceleration = direction * self.angle_accel

    def update(self, dt):
        self.velocity += self.direction * self.acceleration
        self.velocity *= self.friction
        if self.velocity.length() > self.max_vel:
            self.velocity.scale_to_length(self.max_vel)

        displacement = self.velocity * dt

        self.position += displacement

        self.angle_velocity += self.angle_acceleration
        self.angle_velocity *= self.angle_friction
        self.angle -= self.angle_velocity

        self.direction.rotate_ip(self.angle_velocity)
        
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.rect = self.rotated_rect
        self.rect.center = self.position + self.offset

        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)

        self.speed = self.velocity.length()

    def handbrake(self):
        self.velocity *= 0.9

    def draw(self, screen, offset=(0, 0)):
        #self.rect.center = self.position + self.offset
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)
        screen.blit(self.rotated_image, self.rotated_rect.topleft + offset)

    def draw_debug(self, screen, offset=(0, 0)):
        pygame.draw.line(screen, (0, 255, 0), (SCREENRECT.centerx, SCREENRECT.centery), (SCREENRECT.centerx + self.velocity.x * 10, SCREENRECT.centery + self.velocity.y * 10), 2)
        pygame.draw.line(screen, (255, 0, 0), (SCREENRECT.centerx, SCREENRECT.centery), (SCREENRECT.centerx + self.direction.x * 10, SCREENRECT.centery + self.direction.y * 10), 2)

        pygame.draw.circle(screen, (255, 255, 255), (int(self.rect.centerx + offset[0]), int(self.rect.centery + offset[1])), 2)

        # draw mask outline
        olist = self.mask.outline()
        for i in range(len(olist)):
            p1 = olist[i]
            p2 = olist[(i + 1) % len(olist)]
            pygame.draw.line(screen, (255, 255, 255), (p1[0] + self.rect.x + offset[0], p1[1] + self.rect.y + offset[1]), (p2[0] + self.rect.x + offset[0], p2[1] + self.rect.y + offset[1]), 2)

        # draw rect x and y
        pygame.draw.line(screen, (255, 0, 0), (self.rect.x + offset[0], self.rect.y + offset[1]), (self.rect.x + offset[0] + self.rect.width, self.rect.y + offset[1]), 2)
        pygame.draw.line(screen, (0, 255, 0), (self.rect.x + offset[0], self.rect.y + offset[1]), (self.rect.x + offset[0], self.rect.y + offset[1] + self.rect.height), 2)

        # draw hitbox
        pygame.draw.rect(screen, (0, 0, 255), self.hitbox.move(offset[0], offset[1]), 2)
              

# test code
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
    clock = pygame.time.Clock()
    car = Car("car_1.png", screen, 10, 10, 0.5, 0.98, 0.5, 0.9, 420, 400)
    while True:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        car.events()
        car.update(dt)
        car.draw(screen)
        car.draw_debug(screen)
        pygame.display.flip()