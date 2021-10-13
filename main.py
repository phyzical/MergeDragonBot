import image_slicer as ImageSlicer
import pyscreenshot as ImageGrab
import logging
from skimage import ssim
from os import listdir
from os.path import isfile, join
from itertools import groupby
import pyautogui

tileTypeImagePath = "./tileTypeImages"
tileTypeImages = [f for f in listdir(tileTypeImagePath) if isfile(join(tileTypeImagePath, f))]

tileTypes = map(initiliseTypeTiles, tileTypeImages)

def initiliseTypeTiles(imageFile)
  f = open(imageFile, "r")
  imageFileName =  os.path.basename(imageFile).split(".", 1)[0
  return {image: f.read(), type: imageFileName}

baseWindowX = 100
def start
  tiles = []
  x  = 0
  y = 0
  // todo add the ability to pan to cover whole map
  //pyautogui.dragTo(100, 150)
  screenshotSlices = getScreenShotSlices()
  for index, slice in screenshotSlices:
      print(slice)
      tiles[index] = { type: calculateType(slice), x: x, y: y }
      
  for groupedTiles in groupby(lst,key=lambda x:x['type']):
    if groupedTiles.count == 5
      print(f"i can merge 5 {groupedTiles[0]["type"]}!")
      doMerge(groupedTiles)
    else if  groupedTiles.count == 3
      print(f"i can merge 3 {groupedTiles[0]["type"]}!")

def doMerge(tiles)
  firstTile = tiles[0]
  for i, tile in tiles:
    if i != 0
      #pyautogui.dragTo(baseWindowX+1, baseWindowX)
      


def calculateType(slice)
  // todo find an image regognition pacakge that matches images
  types = {}
  for tileType in tileTypes:
    types[tileType] = ssim(slice, tileType.image)
  return max(types, key=stats.get)

def getScreenShotSlices
  scanTileSize = 14
  # part of the screen
  screenshot = ImageGrab.grab(bbox=(10, 10, 510, 510))  # X1,Y1,X2,Y2

  return ImageSlicer.slice(screenshot, scanTileSize)

start()
