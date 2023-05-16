import time, pygame

class Timer:
    def __init__(self, duration, with_start=True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + duration

    def check(self):
        if pygame.time.get_ticks() >= self.next:
            self.next += self.duration
            return True
        return False
    
    def reset(self):
        self.next = pygame.time.get_ticks() + self.duration