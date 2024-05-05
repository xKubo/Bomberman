import pygame
import keyboard 
import game
import sprites

class App:
   

    def __init__(self, cfg):
        self.exit = False
        displaysize = (640, 480)
        cfg["game"]["display_size"] = displaysize
        self.m_Cfg = cfg
        pygame.init()
        self.m_Keyboard = keyboard.Keyboard()
        self.m_Clock = pygame.time.Clock()         
        self.m_Screen = pygame.display.set_mode(displaysize)  
        self.m_Images = sprites.Sprites(self.m_Cfg["images"])
        self.m_Game = game.Game(self.m_Cfg['game'], self.m_Images, self.m_Keyboard)
        

    def Run(self):  
        while not self.exit: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    return         
            self.m_Screen.fill('black')
            self.m_Game.Update()
            game.DrawGame(self.m_Game, self.m_Screen)

            pygame.display.flip() 
            self.m_Clock.tick(self.m_Cfg["tick"]) 
        
    
appcfg = {
    "tick" : 60,
    "images" : {
        "name" :  "Bomberman.png",
        "fieldsize" : 16,
        "fields" : {
            'W': (3,3, 1), 
            'w': (3,3, 6),
            'b': (3,3, 3),   
            'L': (0,0, 3),
            'D': (0,3, 3),
            'R': (1,0, 3),
            'U': (1,3, 3),
            ' ': (4,0, 1),
        },
    },
    "game" : {
        "players" : [
            {
                "name" : "P1",
                "type" : "key",
                "keys" : "wasd"
            },
            {
                "name" : "P2",
                "type" : "key",
                "keys" : "8456"
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

