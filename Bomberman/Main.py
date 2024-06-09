import pygame
import keyboard 
import game
import sprites
import utils
from Vec2d import Vector2D
from screen import Screen

class App:
   
    def CreateController(self, cfg, obj):
        t = cfg["type"]
        if t != 'key':
            raise utils.Error("Invalid player type: " + t)
        return keyboard.KeyboardController(self.m_Keyboard, obj, cfg["keys"])

    def __init__(self, cfg):
        displaysize = (640, 480)
        cfg["game"]["display_size"] = displaysize
        self.m_Cfg = cfg
        pygame.init()
        self.m_Keyboard = keyboard.Keyboard()
        self.m_Clock = pygame.time.Clock()         
        self.m_Screen = Screen(pygame.display.set_mode(displaysize))
        self.m_Images = sprites.Sprites(self.m_Cfg["images"])
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
    "images" : {
        "name" :  "Bomberman.png",
        "fieldsize" : 16, #pixels
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
            'X': (0,2, 6),
        },
        "cross" : [(2,6), (7,6), (2,11), (7,11)],
    },
    "game" : {
        "step" : 0.25,  # 1/4 of field, 100 == one field
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
        "field_tolerance" : 0.10,   #1/5 of field 
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

