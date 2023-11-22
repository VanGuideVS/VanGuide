
import numpy as np
import cv2
import re
import pytesseract
from pytesseract import Output
from pytesseract import pytesseract
import pandas as pd


map_path = 'floorplannumsINVERTED_detecting.png'
room_count = 48


def represents_int(s):
        try: 
            int(s)
        except ValueError:
            return False
        else:
            return True

def text_detector(map_path):
    
    path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 
    pytesseract.tesseract_cmd = path_to_tesseract

    img = cv2.imread(map_path)

    def convert_grayscale(img):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return img

    def blur(img, param):
        img = cv2.medianBlur(img, param)
        return img

    def threshold(img):
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return img

    # h, w, c = img.shape
    # boxes = pytesseract.image_to_boxes(img)
    # for b in boxes.splitlines():
    #     b = b.split(' ')
    #     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    # print(b)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    d =pytesseract.image_to_data(img,output_type = Output.DICT)
    print(d['text'])

    n_boxes = len(d['conf'])
    print(n_boxes)
    room_pattern = r'.?\d{3}'
    position_x =[]
    position_y = []
    room =[]
    position = []
    for i in range (n_boxes):
        if int(float(d['conf'][i]))>5:
            if re.match(room_pattern,d['text'][i]):
                (x,y,w,h) = (d['left'][i],d['top'][i],d['width'][i],d['height'][i])
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                position_x.append(x)
                position_y.append(450-y)
                room.append(d['text'][i])
                position.append((x, 450-y, d['text'][i]))
            
    return position_x,position_y,room,img


x,y,room,img = text_detector(map_path)
room.append('00111')
print(room)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
leng=len(room)
for i in range (0,leng-1):
    
    if represents_int(room[i]):
        if int(room[i][0]) != 8 and len(room[i]) == 3:
            print(room[i],'not detected correctly please fix')
            val = input("enter the fixed value: ")
            room[i] = int(val)
        elif len(room[i]) != 3:
            print("the detected room number is: ", room[i])
            decision = input("should I pop? yes or no ")
            if decision == 'yes':
                room.pop(room.index(room[i]))
                x.pop(x.index(x[i]))
                y.pop(y.index(y[i]))
                leng = leng-1
            elif decision == 'no':
                val = input("enter the fixed value: ")
                val = input("enter the fixed value: ")
                room[i] = int(val)
                    
    else: 
        print(room[i],'not detected as an integer please fix')
        val = input("enter the fixed value: ")
        room[i] = int(val)

if len(room) < room_count: 
    print(room_count-len(room))
    # detect missing rooms manually before running 
    for i in range (0,room_count-len(room)):
        val_room = input('please enter the missing room number: ')
        val_x= input('please enter the missing room x_cord: ')
        val_y = input('please enter the missing room y_cord: ')
        
        
        if len(room) == len(x) and len(room) == len(y):
            room.append(val_room)
            x.append(val_x)
            y.append(val_y)
        else:
            raise Exception('data detection error, LENGTHS of x,y and room arrays not equal')
            
df = pd.DataFrame({"room_number":room,"x_coordinate":x,"y_coordinate":y})
df.to_csv("floorplan_test",index=False)
           



