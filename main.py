import pyscreenshot as ImageGrab
from os import listdir
from os.path import basename
import cv2
import numpy as np
from functools import reduce
import pyautogui
import time
import random


def filterFiles(file):
    return file != "tileTypeImages/.DS_Store"


tileTypeImages = filter(
    filterFiles, ["tileTypeImages/" + s for s in listdir("tileTypeImages")])


def initiliseTiles(imageFile):
    imageFileName = basename(imageFile).split(".", 1)[0]
    image = cv2.imread(imageFile)
    # # convert the images to grayscale
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return {"image": image, "type": imageFileName}


tileTypes = list(map(initiliseTiles, tileTypeImages))
baseWindowX = 100

baseX = 300
baseY = 200


def doClick(groupedTiles):
    for tile in groupedTiles:
        x = (tile['x'] + baseX)/2
        y = (tile['y'] + baseY)/2
        print(
            f"clicking tile at x{x} y{y}")
        pyautogui.click(x, y)
        pyautogui.click(x, y)


def doMerge(groupedTiles):
    firstTile = None

    random.shuffle(groupedTiles)
    for i, tile in enumerate(groupedTiles):
        x = (tile['x'] + baseX)/2
        y = (tile['y'] + baseY)/2
        if i == 0:
            firstTile = {"x": x, "y": y}
        else:
            toX = firstTile['x']
            toY = firstTile['y']
            print(
                f"moving tile at x{x} y{y} to x{toX} y{toY}")

            pyautogui.moveTo(x, y)
            pyautogui.dragTo(toX, toY, duration=3, button='left')


def removeDuplicates(list, item):
    unique = 1
    errorVariancePixels = 10
    for listItem in list:
        unique = unique and (
            abs(listItem["x"] - item["x"]) > errorVariancePixels or abs(listItem["y"] - item["y"]) > errorVariancePixels)
    if unique == 1:
        list.append(item)
    return list


def findTiles():
    # part of the screen
    screenshot = ImageGrab.grab(
        bbox=(baseX, baseY, baseX+1920, baseY + 1000))  # X1,Y1,X2,Y2
    screenshot.save("screenshot.png")
    img_rgb = cv2.imread('screenshot.png')
    # img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    groupedTiles = {}
    for tileType in tileTypes:
        typeImage = tileType["image"]
        type = tileType["type"]
        w, h = typeImage.shape[:-1]
        tiles = []
        res = cv2.matchTemplate(img_rgb, typeImage, cv2.TM_CCOEFF_NORMED)
        threshold = .65
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):  # Switch collmns and rows
            # xy of center point for moving
            x = pt[0] + (w/2)
            y = pt[1] + (h/2)
            tiles.append({"x": x, "y": y, "pt": pt})

        groupedTiles[type] = reduce(removeDuplicates, tiles, [])
        for tile in groupedTiles[type]:
            pt = tile["pt"]
            cv2.rectangle(img_rgb, pt,
                          (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            cv2.putText(img_rgb, type,
                        (pt[0] + w, pt[1] + h),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imwrite('result.png', img_rgb)

    return groupedTiles


def typeClickable(type):
    result = False
    if type in ["boneSeed"]:
        result = True

    return result


def handleTiles(tiles):
    if len(tiles):
        for type in tiles:
            groupedTiles = tiles[type]

            count = len(groupedTiles)
            if type != "unknown":
                if typeClickable(type) and count >= 0:
                    print(f"i can click {count} {type}!")
                   # doClick(groupedTiles)
                elif count >= 5:
                    print(f"i can merge {count} {type}!")
                    doMerge(groupedTiles)
                elif count >= 3:
                    print(f"i can merge 3 {type}!")
                    # doMerge(groupedTiles)


def start():
    tiles = findTiles()
    priorityTiles = {k: v for k, v in tiles.items() if k == "boneSeed"}
    # handleTiles(priorityTiles)
    tiles = {k: v for k, v in tiles.items() if k != "boneSeed"}
    handleTiles(tiles)


start()
