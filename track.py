from settings import *
from utils import *
import pytmx

class Track():
    def __init__(self, track_name, laps=0):
        self.track_name = track_name
        self.tmxData = pytmx.load_pygame(os.path.join(PATHTMX, self.track_name + ".tmx"))
        self.width = self.tmxData.width * self.tmxData.tilewidth
        self.height = self.tmxData.height * self.tmxData.tileheight
        self.laps = laps

        self.finish_rect = self.get_finish_rect()
        self.start_rect = self.get_start_rect()
        self.checkpoint_rect = self.get_checkpoint_rect()
        self.border_rect = self.get_border_rect()

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey(black)
        self.create_surface()

        self.rect = self.get_rect()

        self.road_surface = self.get_road_layer_rect()

        self.mask = None

    def draw(self, screen):
        layers = self.tmxData.visible_layers
        for layer in layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxData.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * self.tmxData.tilewidth,
                                           y * self.tmxData.tileheight))
                        
    def create_surface(self):
        layers = self.tmxData.visible_layers
        for layer in layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxData.get_tile_image_by_gid(gid)
                    if tile:
                        self.surface.blit(tile, (x * self.tmxData.tilewidth,
                                           y * self.tmxData.tileheight))
                        
    def get_rect(self):
        return self.surface.get_rect()
    
    def get_finish_rect(self):
        for obj in self.tmxData.objects:
            if obj.name == "finish":
                return pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            
    def get_start_rect(self):
        for obj in self.tmxData.objects:
            if obj.name == "start":
                return pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            
    def get_checkpoint_rect(self):
        for obj in self.tmxData.objects:
            if obj.name == "checkpoint":
                return pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            
    def get_border_rect(self):
        for obj in self.tmxData.objects:
            if obj.name == "border":
                return pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    def draw_border(self, screen, offset):
        pygame.draw.rect(screen, white, self.border_rect.move(offset))
            
    def get_road_layer_rect(self):
        road = self.tmxData.get_layer_by_name("road")
        surface = pygame.Surface((self.width, self.height))
        surface.set_colorkey(black)
        for x, y, gid in road:
            tile = self.tmxData.get_tile_image_by_gid(gid)
            if tile:
                surface.blit(tile, (x * self.tmxData.tilewidth,
                                    y * self.tmxData.tileheight))
        return surface
    
    def is_on_track(self, rect):
        if self.road_surface.get_at((int(rect.centerx), int(rect.centery))) == (166,201,203,255):
            return True
        else:
            return False