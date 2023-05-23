import pygame, os, math, sys

pygame.init()

## Game settings
FONT = pygame.font.Font("fonts/m6x11.ttf", 30)
SCREENRECT = pygame.Rect(0, 0, 1280, 720)
CLOCK = pygame.time.Clock()
FPS = 60

## Paths
PATHFILE = os.path.dirname(os.path.abspath(__file__))
PATHIMG = os.path.join(PATHFILE, "images")
PATHJSON = os.path.join(PATHFILE, "json")
PATHTMX = os.path.join(PATHFILE, "tmx")

## Colors
black = (0, 0, 0)
white = (255, 255, 255)
light_grey = (200, 200, 200)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)

## Music
MUSIC = "Spooky scary skeletons (Eurobeat remix)"
