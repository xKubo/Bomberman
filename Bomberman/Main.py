import diag 

import pygame
import keyboard 
import game
import sprites
import utils
import configuration
from Vec2d import Vector2D
from screen import Screen




class App:
   
    def CreateController(self, cfg, obj):
        t = cfg["type"]
        if t != 'key':
            raise utils.Error("Invalid player type: " + t)
        return keyboard.KeyboardController(self.m_Keyboard, obj, cfg["keys"])

    def __init__(self, cfg):

        displaysize = (1024, 768)
        cfg["game"]["display_size"] = displaysize
        self.m_Cfg = cfg
        pygame.init()
        self.m_Keyboard = keyboard.Keyboard()
        self.m_Clock = pygame.time.Clock()         
        self.m_Screen = Screen(pygame.display.set_mode(displaysize))
        self.m_Images = sprites.Sprites(self.m_Cfg["images"], cfg["fps"], self.m_Cfg["text"])
        self.m_Game = game.Game(self.m_Cfg['game'], self.m_Images, self.CreateController, self.m_Screen)
        

    def Run(self):  
        fps = self.m_Cfg["fps"]
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    return         
            self.m_Screen.m_Screen.fill('black')
            self.m_Keyboard.Update()
            self.m_Game.Update()
            self.m_Game.Draw()
            pygame.display.flip()             
            self.m_Clock.tick(fps) 
        
    
appcfg = {
    
    "fps" : 20,
    "images" : configuration.Images,
    "text" : configuration.Text,
    "game" : {
        "diag" : True,
        "player_defaults" : {
            "step" : 0.25,   # quarter of field
            "bomb_time" : "2s",
            "flame_size" : 3,
        },
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
        "field_tolerance" : 0.10,   
        "map" : {
            "data" : [
            "WWWWWW",
            "W    W",
            "W    W",
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

