import pygame
import keyboard 
import game
import sprites
from Vec2d import Vector2D

class Screen:
    def __init__(self, scr:pygame.Surface):
        self.m_Screen = scr
        
    def DrawSprite(self, sprite, pos):
        self.m_Screen.blit(sprite.image, pos.to_tuple(), sprite.rect)  

class App:
   

    def __init__(self, cfg):
        self.exit = False
        displaysize = (640, 480)
        cfg["game"]["display_size"] = displaysize
        self.m_Cfg = cfg
        pygame.init()
        self.m_Keyboard = keyboard.Keyboard()
        self.m_Clock = pygame.time.Clock()         
        self.m_Screen = Screen(pygame.display.set_mode(displaysize))
        self.m_Images = sprites.Sprites(self.m_Cfg["images"])
        self.m_Game = game.Game(self.m_Cfg['game'], self.m_Images, self.m_Keyboard)
        

    def Run(self):  
        fps = self.m_Cfg["fps"]
        while not self.exit: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    return         
            self.m_Screen.m_Screen.fill('black')
            self.m_Game.Update()
            game.DrawGame(self.m_Game, self.m_Screen)
            pygame.display.flip() 
            
            self.m_Clock.tick(fps) 
        
    
appcfg = {
    "fps" : 20,
    "images" : {
        "name" :  "Bomberman.png",
        "fieldsize" : 16,
        "transparent_color" : (56, 135, 0),
        "fields" : {
            'W': (3,3, 1), 
            'w': (3,3, 6),
            'b': (0,3, 3),   
            'L': (0,0, 3),
            'D': (3,0, 3),
            'R': (0,1, 3),
            'U': (3,1, 3),
            ' ': (7,1, 1),
        },
    },
    "game" : {
        "step" : 0.25,
        "players" : [
            {
                "name" : "P1",
                "type" : "key",
                "keys" : ['w', 'a', 's', 'd', '1']
            },
            {
                "name" : "P2",
                "type" : "key",
                "keys" : ['up', 'left', 'down', 'right', 'p']
            },
        ],
        "map" : {
            "data" : [
            "WWWWWW",
            "W  w W",
            "W  w W",
            "WwwwwW",
            "W    W",
            "WWWWWW",
            ],
            "players" : [(1,1),(4,4)]               
        }
    }
}
a = App(appcfg)
a.Run()

