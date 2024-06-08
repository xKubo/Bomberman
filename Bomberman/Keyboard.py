import pygame

class Keyboard:
    class Handler:
        CharsPressed = "ULDRB"

        def __init__(self, keys, obj):
            self.m_Object = obj
            self.m_Keys = keys
            self.m_Codes = [pygame.key.key_code(k) for k in self.m_Keys ]            
            
        def Update(self, keymap):
            pressed = ""
            for i, c in enumerate(self.m_Codes):
                if keymap[c]:
                    pressed += self.CharsPressed[i]
            self.m_Object.OnCmd(pressed)

    def __init__(self):
        self.handlers = []
        
    def RegisterKeyHandler(self, keys, obj):        
        h = Keyboard.Handler(keys, obj)
        self.handlers.append(h)
            
    def Update(self):
        keymap = pygame.key.get_pressed()        
        for h in self.handlers:
            h.Update(keymap)
    

class KeyboardController:
    def __init__(self, keyboard, obj, keys):
        keyboard.RegisterKeyHandler(keys, obj)
               

        
    
        
        