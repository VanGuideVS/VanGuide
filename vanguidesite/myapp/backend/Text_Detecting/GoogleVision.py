import numpy as np
import cv2
import re
import pandas as pd
from google.cloud import vision
import io
from google.oauth2 import service_account
map_path = ['atlas2_b.png','atlas2_t.png','atlas3_b.png','atlas3_t.png','atlas4_b.png','atlas4_t.png','atlas5_b.png','atlas5_t.png','atlas6_b.png','atlas6_t.png','atlas7_b.png','atlas7_t.png','atlas8_b.png','atlas8_t.png','atlas9_b.png','atlas9_t.png','atlas10_b.png','atlas10_t.png','atlas11_b.png','atlas11_t.png']
room_count = [33,33,28,28,48,35,28,28,50,41,24,35,49,45,39,27,46,49,39,38]
# map_path = ['atlas9_t.png','atlas10_b.png','atlas10_t.png','atlas11_b.png','atlas11_t.png']
# room_count = [27,46,49,39,38]
#int(input("How many rooms are there? \n"))
floor_num = [2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11]
#int(input("What floor is the map? \n"))
room_digits = [5,6]
#int(input("How many digits are the room numbers? \n"))

def represents_int(s):
        try: 
            int(s)
        except ValueError:
            return False
        else:
            return True
        
def get_image_height(image_path):
    image = cv2.imread(image_path)
    return image.shape[0]

print(get_image_height(r'Floor_Plans\\'+ map_path[0]))
        
def text_detection(map_path,count):

    # credentials = service_account.Credentials.from_service_account_file(r"C:\Users\ismail\Documents\GitHub\GIT-Projects\Text_Detecting\text-detector-from-png-70fcf67afe56.json")
    credentials = service_account.Credentials.from_service_account_file(r"C:\Users\20200866\OneDrive - TU Eindhoven\Desktop\Personal\VanGuide\Text_Detecting\text-detector-from-png-70fcf67afe56.json")
    client_options = {'api_endpoint': 'eu-vision.googleapis.com'}
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(map_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_text = []
    coordinates = []
    #room_pattern = r'.?\d{' + str(room_digits) + '}'

    room_pattern = r'^' + str(floor_num[count]) + r'\.[^T]\d+'

   

    for text in texts:
        print('Detected text: {}'.format(text.description))
        if re.match(room_pattern, text.description):
            detected_text.append(text.description)

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])
            
            coordinates.append(vertices)
            
    if len(detected_text)>1:
        detected_text.pop(0)
        coordinates.pop(0)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return detected_text, coordinates

def data_checks(detected_text, coordinates,index):
    if index < 16:
        length = len(detected_text)
        print(f"The number of detected rooms is: {length}")
        popped_num = 0
        for i in range(len(detected_text)-1, -1, -1):
            item = detected_text[i]
            #if represents_int(item):
            if item[0] != str(floor_num[index]) and len(item) == room_digits[0]:
                print(item, 'not detected correctly, please fix')
                val = input('enter the fixed value: ')
                detected_text[i] = int(val)
            elif len(item) != room_digits[0] and item[-1].isdigit():
                print("the detected room number is: ", item)
                decision = input("should I pop? (yes/no) ")
                if decision == 'yes':
                    coordinates.pop(i)
                    detected_text.pop(i)
                    popped_num += 1
                    length -= 1
                    print(f"popped_num = {popped_num}, length = {length}")
                else:
                    val = input("enter the fixed value: ")
                    # detected_text[i] = int(val)
    elif index >= 16:
        length = len(detected_text)
        print(f"The number of detected rooms is: {length}")
        popped_num = 0
        for i in range(len(detected_text)-1, -1, -1):
            item = detected_text[i]
            #if represents_int(item):
            print(item[0:2])
            if item[0:2] != str(floor_num[index]) and len(item) == room_digits[1]:
                print(item, 'not detected correctly, please fix')
                val = input('enter the fixed value: ')
                # detected_text[i] = int(val)
            elif len(item) != room_digits[1] and item[-1].isdigit():
                print("the detected room number is: ", item)
                decision = input("should I pop? (yes/no) ")
                if decision == 'yes':
                    coordinates.pop(i)
                    detected_text.pop(i)
                    popped_num += 1
                    length -= 1
                    print(f"popped_num = {popped_num}, length = {length}")
                else:
                    val = input("enter the fixed value: ")
                    # detected_text[i] = int(val)
        
            
    if len(detected_text) < room_count[index]:
        print(f"the number of rooms detected are less than the counted rooms: {room_count[index] - len(detected_text)}")

        print(f"The detected rooms are: {detected_text}")
        for i in range(0, room_count[index] - len(detected_text)):
            val_room = input('please enter the missing room number: ')
            top_left_x = input('please enter the missing rooms TOP LEFT X-coordinate: ')
            top_left_y = input('please enter the missing rooms TOP LEFT y-coordinate: ')

            bottom_right_x = input('please enter the missing rooms BOTTOM RIGHT x-coordinate: ')
            bottom_right_y = input('please enter the missing rooms BOTTOM RIGHT y-coordinate: ')

            top_right_x = bottom_right_x
            top_right_y = bottom_right_y

            bottom_left_x = top_left_x
            bottom_left_y = top_left_y

            added_coordinate = [f'({top_left_x},{top_left_y})', f'({top_right_x},{top_right_y})', f'({bottom_right_x},{bottom_right_y})', f'({bottom_left_x},{bottom_left_y})']
            

            if len(detected_text) == len(coordinates):
                detected_text.append(val_room)
                coordinates.append(added_coordinate)
            else:
                raise Exception('data detection error, LENGTHS of coordinates and detected_text arrays not equal')
            
            print(coordinates)
    rooms = [x for x in detected_text]
    room_coordinates = [[(int(x[0]), get_image_height(r'Floor_Plans\\'+ map_path[i])-int(x[1])) for x in map(lambda y: y.strip('()').split(','), sublist)] for sublist in coordinates]
    
    return rooms, room_coordinates


for i in range (len(map_path)+1):
    detected_text, coordinates = text_detection(r'Floor_Plans\\'+ map_path[i],i)
    rooms, room_coordinates = data_checks(detected_text, coordinates,i)

    print(detected_text)
    print(f"len of text = {len(rooms)}, len of coordinates = {len(room_coordinates)}")

    df = pd.DataFrame({"room_number":rooms, "coordinates": room_coordinates})
    df.to_csv(f"Text_Detecting\\CSV_FILES\\Atlas_{floor_num[i]}_{i}", index = False)