import pygame
import utils
import sprites
import screen
from Vec2d import Vector2D

class Text:
    def __init__(self, cfg): 
         self.m_Image = pygame.image.load(cfg["name"]).convert()
         invchar = cfg["invalid_char"]
         self.m_Table = cfg["chars_table"]
         self.m_Table = cfg["chars_table"]
         self.m_Dims = cfg["dims"]
         self.m_LetterSize = cfg["letter_size"]
         self.m_Position = Vector2D(0, 0)
         self.m_LetterWidth = self.m_LetterSize*3//4
         self.m_InitialX = 0
         
         self.m_InvalidCharNum = self._AsciiToSpriteNum(ord(invchar))
         self.m_InvalidCharSprite = self._SpriteNumToSprite(self.m_InvalidCharNum)
         
         self.m_CharSprites = []
         for a in range(32, 128):
             num = self._AsciiToSpriteNum(a)
             self.m_CharSprites.append(self._SpriteNumToSprite(num))
    
    def _AsciiToSpriteNum(self, a):
        for i in range(len(self.m_Table)):
            if self.m_Table[i][0] > a:
                if i == 0:
                    return self.m_InvalidCharNum
                prev = self.m_Table[i-1]
                return a - prev[0] + prev[1]   
        return 
        
    def _SpriteNumToSprite(self, num):
        linesize = self.m_Dims[0]        
        w = num % linesize
        h = num // linesize
        rect = pygame.Rect(w*self.m_LetterSize, h*self.m_LetterSize, self.m_LetterSize, self.m_LetterSize)
        return sprites.StaticSprite(rect, self.m_Image)
        
    def GetSpriteForChar(self, ch):
        a = ord(ch)
        if a < 32:
            return self.m_InvalidCharSprite
        a -= 32
        if a > len(self.m_CharSprites):
            return self.m_InvalidCharSprite
        return self.m_CharSprites[a]
    
    def SetPos(self, pos:Vector2D):
        self.m_Position = pos
        self.m_InitialX = pos.x

    def Print(self, scr, *textargs):
        s = ''.join(*textargs) 
        for ch in s:
            spr = self.GetSpriteForChar(ch)
            scr.DrawSpritePix(spr, self.m_Position)
            self.m_Position.x += self.m_LetterWidth

    def PrintLn(self, scr, *textargs):
        self.Print(scr, *textargs)
        self.m_Position.x = self.m_InitialX
        self.m_Position.y += self.m_LetterSize
            