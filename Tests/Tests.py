import utils

try:
  raise utils.Error("test")
except utils.Error as e:
  print(e)