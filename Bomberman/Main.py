import pygame
from keyboard import Keyboard
import game
import sprites

class App:
    
    class Cfg:
        img = "",
        game:game.Game.Cfg = {},

    def __init__(self, cfg:Cfg):
        self.exit = False
        self.m_Cfg = cfg
        pygame.init()
        self.m_Keyboard = keyboard.Keyboard()
        self.m_Clock = pygame.time.Clock()         
        self.m_Screen = pygame.display.set_mode((640, 480))  
        MainImg = pygame.image.load('player.png').convert_alpha()
        imgscfg = sprites.Sprites.Cfg();
        self.m_Images = sprites.Sprites(imgscfg, MainImg)
        self.m_Game = game.Game(self.m_Cfg.Game, self.m_Images, self.m_Keyboard)
        

    def Run(self):  
        while not self.exit: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    break            
            self.m_Screen.fill((0,0,0)) 
            self.m_Game.Update()
            game.DrawGame(self.m_Game, self.m_Screen)

            pygame.display.flip() 
            self.clock.tick(60) 
        pygame.quit() 
    
appcfg = 
{
    "img" : "Bomberman.png",
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
            data : [
            "WWWWWW",
            "W1 w W",
            "W  w W",
            "WwwwwW",
            "W   2W",
            "WWWWWW",
            ]

               
        }
    }
}
a = App(appcfg)
a.Run()

