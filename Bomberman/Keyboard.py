import pygame

class Keyboard:
    def __init__(self):
        self.handlers = {}
        
    def RegisterKeyHandler(self, keys, OnKey):
        for k in keys:
            self.handlers[k] = OnKey
            
    def Update(self):
        keymap = pygame.key.get_pressed()
        keys = []
        for k in self.handlers:
            if keymap[k]:
                keys.append(k)
        if keys:
            self.handlers[k](keys)
    

class KeyboardController:
    def __init__(self, obj, keyboard):
        self.m_Keyboard = keyboard
        
    
        
        