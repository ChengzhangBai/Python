#Author: Chengzhang Bai @AC
#Date: Nov. 27, 2020
import click
from PIL import Image, ImageFont, ImageDraw
#from gfxhat import lcd,  fonts

def generateDictionary():
    f = open('font3.txt','r')
    charList = []
    while True:
        line1 = f.readline()
        if line1 == "":#end of file
            break
        else:
            line1 = line1.replace("\n","").split(",")#delete the end of line symbol, and split the two items into list
        char = line1[1]#char
        value = hex2bin(line1[0])
        charList.append((char,value))
    charDict = dict(charList)#convert list to dict
    return charDict

def displayObject(obj, x, y):
    global pixel
    #lcd.clear()
    xp = x
    for y1 in obj:
        for x2 in y1:
            if x2 == 1:
                pixel = 1
            else:
                pixel = 0
            #lcd.set_pixel(xp, y, pixel)
            xp += 1
        y += 1
        #lcd.set_pixel(xp, y, pixel)

    #lcd.show()

def clearScreen(lcd):
    lcd.clear()
    lcd.show()

def displayText(text,lcd,x,y):
    lcd.clear()
    width, height = lcd.dimensions()
    image = Image.new('P', (width, height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fonts.AmaticSCBold, 24)
    w, h = font.getsize(text)
    draw.text((x,y), text, 1, font)
    for x1 in range(x,x+w):
        for y1 in range(y,y+h):
            pixel = image.getpixel((x1, y1))
            lcd.set_pixel(x1, y1, pixel)
            lcd.show()



def hex2bin(hexValue): #convert hex value to binary value, format of hexValue: 0x3C00000000000000
    hexValueList = list(hexValue[2:]) # delete 0x
    binValueList = [] #change hexvalue to list in order to loop
    for i in hexValueList:
        binValue = bin(int(i, 16))[2:].zfill(4) #delete ob, then convert each hex value to binary value with 4 digits
        binValueList.append(binValue)
    binValue = ''.join(binValueList)
    #print(hexValue,binValue)
    return binValue


def bitmapInHat():
    chars = generateDictionary() #put the dictionary to the variable chars
    print('Please press a key: ')
    c = click.getchar()
    print(c)
    n = 0
    for key in chars.keys():
        if key == c:
            clearScreen(lcd)
            displayText(chars[key], lcd, 2, 10)
            binValue = chars[key]
            list = []
            for i in range(0, 8):
                for j in range(0, 8):
                    list.append(int(binValue[i * 8 + j])) #change the binary value from str to list
            chunks = [list[x:x + 8] for x in range(0, len(list),8)]  # Split the 64 digits in the list into 8*8 chunks, thanks to: https://stackoverflow.com/questions/9671224/split-a-python-list-into-other-sublists-i-e-smaller-lists
            #print(chunks) #sample of chunks: [[1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
            displayObject(chunks, 16, 9)
            n = 1
            break
    if n == 0:
        msg = "The key you input isn't recorded in the dictionary."
        clearScreen(lcd)
        displayText(msg, lcd, 2, 10)
        print(msg)


bitmapInHat()



