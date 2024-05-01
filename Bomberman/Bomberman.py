import pygame, sys
import game
import player
import gamemap

pygame.init()
screen = pygame.display.set_mode((640, 480))
player.Init()



# GLOBAL VARIABLES 
COLOR = (255, 100, 98) 
SURFACE_COLOR = (80, 80, 80) 
WIDTH = 500
HEIGHT = 500

sprites = pygame.Surface([300, 400]) 
#sprites.fill(SURFACE_COLOR) 
sprites = pygame.image.load('bomberman.png').convert_alpha()
sprites.set_colorkey((56, 135, 0)) 
  
# Object class 
class Sprite(pygame.sprite.Sprite): 
    def __init__(self, color, height, width): 
        super().__init__() 
  
        self.image = pygame.Surface([width, height]) 
        self.image.fill(SURFACE_COLOR) 
        self.image.set_colorkey(COLOR) 
  
        pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height)) 
  
        self.rect = self.image.get_rect() 
  
  
 
RED = (255, 0, 0) 
  
all_sprites_list = pygame.sprite.Group() 
  
object_ = Sprite(RED, 20, 30) 
object_.rect.x = 200
object_.rect.y = 300

p = player.Player((50, 50))
  
all_sprites_list.add(object_) 
all_sprites_list.add(p) 
  
exit = True
clock = pygame.time.Clock() 
c = game.Game.Cfg()
g = game.Game(c)
mc = gamemap.Map.Cfg()
m = gamemap.Map(mc)
gamemap.Test()
print(g.GetCfg())
  
while exit: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = False
            
    all_sprites_list.update() 
    screen.fill(SURFACE_COLOR) 
    screen.blit(sprites, (250, 50))
    all_sprites_list.draw(screen) 
    pygame.display.flip() 
    clock.tick(60) 
  
pygame.quit() 