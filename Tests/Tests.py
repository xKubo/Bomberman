import utils
import pygame
from gameplayer import *

pygame.init()

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


def CanGo(CanGoValues):
    def _CanGo(v):
        return v in CanGoValues
    return _CanGo

# LastDir + pressed keys + 
Check(ComputeNewDir('L', EmptyDir, True) == EmptyDir, 'Stop moving')
Check(ComputeNewDir('L', 'L', True) == 'L', 'Same dir')
Check(ComputeNewDir('L', 'R', True) == 'R', 'Opposite dir')
Check(ComputeNewDir('L', 'LU', CanGo('D')) == 'L', 'Can''t go up, have to go left')

Check(ComputeNewDir('L', 'LU', CanGo('UL')) == 'U', 'Go up, because you came from right')
Check(ComputeNewDir('U', 'LU', CanGo('UL')) == 'L', 'Go left, because you came from down')
# Player will not move to the left, just the animation will play
Check(ComputeNewDir('L', 'LU', CanGo('')) == 'L', 'Still try to go left')

# for other directions
Check(ComputeNewDir('D', 'DR', CanGo('DR')) == 'R', 'Go right, because you came from up')
Check(ComputeNewDir('R', 'RD', CanGo('RD')) == 'D', 'Go down, because you came from left')








print('OK')