import utils
import pygame
from gameplayer import *
import diag

pygame.init()

diag.init()

diag.test('test');
diag.test('test2');

def Check(b, msg = ""):
  if not b:
        raise utils.Error("Check failed:" + msg)


# How throw an exception
try:
    raise utils.Error("test")
    Check(false, "You cannot get here")
except utils.Error as e:
    pass
  
# key code conversion
Check(pygame.key.key_code("a") == pygame.K_a) 
Check(pygame.key.name(pygame.K_a) == "a")











print('OK')