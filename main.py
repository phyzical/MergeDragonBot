import image_slicer as ImageSlicer
import pyscreenshot as ImageGrab
from skimage.metrics import structural_similarity as ssim
from os import remove, listdir
from os.path import basename
from itertools import groupby
import pyautogui
import cv2


tileTypeImages = ["tileTypeImages/" + s for s in listdir("tileTypeImages")]


def initiliseTiles(imageFile):
    f = open(imageFile, "rb")
    imageFileName = basename(imageFile).split(".", 1)[0]
    image = cv2.imread(imageFile)
    # convert the images to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return {"image": image, "type": imageFileName}


tileTypes = map(initiliseTiles, tileTypeImages)
baseWindowX = 100


def doMerge(tiles):
    firstTile = tiles[0]
    for i, tile in tiles:
        if i != 0:
            pyautogui.dragTo(baseWindowX+1, baseWindowX)


def calculateType(slice):
    types = {}
    for tileType in tileTypes:
        (score, diff) = ssim(slice, tileType["image"], full=True)
        print(score)
        print(diff)
        types[tileType] = ssim(slice, tileType["image"])
    return max(types, key=types.get)


def getScreenShotSlices():
    scanTileSize = 14
    # part of the screen
    screenshot = ImageGrab.grab(bbox=(10, 10, 510, 510))  # X1,Y1,X2,Y2
    screenshotFilePath = "temp/screenshot.png"
    screenshot.save(screenshotFilePath)
    ImageSlicer.slice(screenshotFilePath, scanTileSize)
    remove(screenshotFilePath)
    return map(initiliseTiles, ["temp/" + s for s in listdir("temp")])


def start():
    tiles = []
    x = 0
    y = 0
    # todo add the ability to pan to cover whole map
    ## pyautogui.dragTo(100, 150)
    screenshotSlices = getScreenShotSlices()
    for index, slice in enumerate(screenshotSlices):
        print(calculateType(slice))
        tiles[index] = {"type": calculateType(slice).type, "x": x, "y": y}

    for groupedTiles in groupby(tiles, key=lambda x: x['type']):
        if groupedTiles.count == 5:
            print(f"i can merge 5 {groupedTiles[0]['type']}!")
            doMerge(groupedTiles)
        elif (groupedTiles.count == 3):
            print(f"i can merge 3 {groupedTiles[0]['type']}!")


start()
