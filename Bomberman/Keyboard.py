import pygame

class Keyboard:
    def __init__(self):
        self.handlers = {}
        
    def RegisterKeyHandler(self, keys, obj):
        for k in keys:
            self.handlers[k] = obj
            
    def Update(self):
        keymap = pygame.key.get_pressed()
        keys = []
        for k in self.handlers:
            if keymap[k]:
                keys.append(k)
        if keys:
            self.handlers[k].OnCmd(keys)
    

class KeyboardController:
    def __init__(self, keys, obj, keyboard):
        keyboard.RegisterKeyHandler(keys, obj)
               

        
    
        
        