import random
import time
import threading
import pygame
import sys
import math
import subprocess
import joblib
import numpy as np
import cv2
from configs import POLY_REG_MODEL_PATH
import os
import warnings
warnings.filterwarnings("ignore")

model = joblib.load(POLY_REG_MODEL_PATH)
random.seed(42)
os.environ["SDL_VIDEODRIVER"] = "dummy"

#TEST SMART TRAFFIC LIGHT SYSTEM
# RIGHT-LEFT / DOWN / LEFT-RIGHT / UP
number_vehices_right_total = {'car':0, 'bus':0, 'truck':0, 'bike':0, 'container':0 , 'firetruck':0, 'van':0, 'bicycle':0, 'total':0}
number_vehices_down_total = {'car':0, 'bus':0, 'truck':0, 'bike':0, 'container':0 , 'firetruck':0, 'van':0, 'bicycle':0, 'total':0}
number_vehices_left_total = {'car':0, 'bus':0, 'truck':0, 'bike':0, 'container':0 , 'firetruck':0, 'van':0, 'bicycle':0, 'total':0}
number_vehices_up_total = {'car':0, 'bus':0, 'truck':0, 'bike':0, 'container':0 , 'firetruck':0, 'van':0, 'bicycle':0, 'total':0}
number_vehices_total = [number_vehices_right_total,number_vehices_down_total, number_vehices_left_total, number_vehices_up_total]

number_vehices_right_inZone = {'car':0, 'bus':0, 'truck':0, 'bike':0, 'container':0 , 'firetruck':0, 'van':0, 'bicycle':0, 'total':0}
number_vehices_down_inZone = {'car':0, 'bus':0, 'truck':0, 'bike':0, 'container':0 , 'firetruck':0, 'van':0, 'bicycle':0, 'total':0}
number_vehices_left_inZone = {'car':0, 'bus':0, 'truck':0, 'bike':0, 'container':0 , 'firetruck':0, 'van':0, 'bicycle':0, 'total':0}
number_vehices_up_inZone = {'car':0, 'bus':0, 'truck':0, 'bike':0, 'container':0 , 'firetruck':0, 'van':0, 'bicycle':0, 'total':0}
number_vehices_inZone = [number_vehices_right_inZone, number_vehices_down_inZone, number_vehices_left_inZone, number_vehices_up_inZone]


defaultGreen = {0:5, 1:5}
defaultRed = 150
defaultYellow = 5

signals = []
noOfSignals = 2
currentGreen = 0  
nextGreen = (currentGreen+1)%noOfSignals    
currentYellow = 0   # on / off


x = {'right':[0,0], 'down':[655,616], 'left':[1400,1400], 'up':[702,740]}    
y = {'right':[468,510], 'down':[10,10], 'left':[422,385], 'up':[920,920]}

x_motor = {'right':[0,0,0,0], 'down':[673,653,631,616], 'left':[1400,1400,1400,1400], 'up':[698,712,737,752]}    
y_motor = {'right':[465,480,502,517], 'down':[10,10,10,10], 'left':[435,420,397,382], 'up':[920,920,920,920]}


vehicles = {
    'right': {0: [], 1: [], 2: [], 3: [], 'crossed': 0}, 
    'down': {0: [], 1: [], 2: [], 3: [], 'crossed': 0}, 
    'left': {0: [], 1: [], 2: [], 3: [], 'crossed': 0}, 
    'up': {0: [], 1: [], 2: [], 3: [], 'crossed': 0}
        }
vehicles_notpassed = {
    'right': {0: [], 1: [], 2: [], 3: []}, 
    'down': {0: [], 1: [], 2: [], 3: []}, 
    'left': {0: [], 1: [], 2: [], 3: []}, 
    'up': {0: [], 1: [], 2: [], 3: []}
        }


ratio = {'right':0,'down':0,'left':0,'up':0}

vehicleSizes = {0:[62,25], 1:[88,30], 2:[81,33], 3:[28,8],4:[176,37],5:[115,35],6:[60,33],7:[23,13]}
vehicles_length = {'car': 62, 'bus':88, 'truck':81, 'bike':28, 'firetruck':115}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike',4:'container',5:'firetruck',6:'van',7:'bicycle'}
vehileArea = {'car': 1550, 'bus': 2640,'truck': 2673,'bike':112,'firetruck':4025}
speeds = {'car':4, 'bus':4, 'truck':4, 'bike':4, 'container':4, 'firetruck':4, 'van':4, 'bicycle':1}  
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

signalCoods = [(455,562),(560,152),(920,270),(786,673)]
signalTimerCoods = [(435,562),(540,152),(900,270),(816,673)]

stopLines = {'right': 500, 'down': 255, 'left': 895, 'up': 660}
defaultStop = {'right': 475, 'down': 235, 'left': 925, 'up': 690}


stoppingGap = 3   
movingGap = 6  

detect_length = 200 # pixels
detect_width = 77 # pixels

# Vehicle throughtput
vehicle_throughput = 0
vehicle_middle = 0


pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, angle, vehiclesize):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.queueMiddle = 0
        self.crossed = 0
        self.stopped = False 
        
        
        if vehicleClass != 'bike' and vehicleClass != 'bicycle':
            if lane == 0:
                self.lane_1 = 0
                self.lane_2 = 1
            elif lane == 1:
                self.lane_1 = 2
                self.lane_2 = 3
            if direction == 'right':
                self.x = min(x_motor[direction][self.lane_1], x_motor[direction][self.lane_2])
                self.y = y_motor[direction][self.lane_1]
            elif direction == 'down':
                self.x = x_motor[direction][self.lane_2]
                self.y = min(y_motor[direction][self.lane_1], y_motor[direction][self.lane_2])
            elif direction == 'left':
                self.x = max(x_motor[direction][self.lane_1], x_motor[direction][self.lane_2])
                self.y = y_motor[direction][self.lane_2]
            elif direction == 'up':
                self.x = x_motor[direction][self.lane_1]
                self.y = max(y_motor[direction][self.lane_1], y_motor[direction][self.lane_2])

            vehicles[direction][self.lane_1].append(self)
            vehicles[direction][self.lane_2].append(self)
            vehicles_notpassed[direction][self.lane_1].append(self.vehicleClass)
            vehicles_notpassed[direction][self.lane_2].append(self.vehicleClass)
            self.index_1 = len(vehicles[direction][self.lane_1]) - 1
            self.index_2 = len(vehicles[direction][self.lane_2]) - 1

            self.angle = angle
            path = "images/" + vehicleClass + ".png"

            self.image = pygame.transform.rotate(
                pygame.transform.scale(pygame.image.load(path), (vehiclesize[0], vehiclesize[1])),
                self.angle
            )

            if ((len(vehicles[direction][self.lane_1]) > 1 and  (vehicles[direction][self.lane_1][self.index_1 - 1].crossed == 0)) and (
                len(vehicles[direction][self.lane_2]) > 1 and  (vehicles[direction][self.lane_2][self.index_2 - 1].crossed == 0)
            )):
                if (direction == 'right'):
                    a = vehicles[direction][self.lane_1][self.index_1 - 1].stop - \
                                vehicles[direction][self.lane_1][self.index_1 - 1].image.get_rect().width - stoppingGap
                    b = vehicles[direction][self.lane_2][self.index_2 - 1].stop - \
                                vehicles[direction][self.lane_2][self.index_2 - 1].image.get_rect().width - stoppingGap
                    self.stop = min(a,b)
                elif (direction == 'left'):
                    a = vehicles[direction][self.lane_1][self.index_1 - 1].stop + \
                                vehicles[direction][self.lane_1][self.index_1 - 1].image.get_rect().width + stoppingGap
                    b = vehicles[direction][self.lane_2][self.index_2 - 1].stop + \
                                vehicles[direction][self.lane_2][self.index_2 - 1].image.get_rect().width + stoppingGap                
                    self.stop = max(a,b)
                elif (direction == 'down'):
                    a = vehicles[direction][self.lane_1][self.index_1 - 1].stop - \
                                vehicles[direction][self.lane_1][self.index_1 - 1].image.get_rect().height - stoppingGap
                    b = vehicles[direction][self.lane_2][self.index_2 - 1].stop - \
                                vehicles[direction][self.lane_2][self.index_2 - 1].image.get_rect().height - stoppingGap
                    self.stop = min(a,b)
                
                elif (direction == 'up'):
                    a = vehicles[direction][self.lane_1][self.index_1 - 1].stop + \
                                vehicles[direction][self.lane_1][self.index_1 - 1].image.get_rect().height + stoppingGap
                    b = vehicles[direction][self.lane_2][self.index_2 - 1].stop + \
                                vehicles[direction][self.lane_2][self.index_2 - 1].image.get_rect().height + stoppingGap
                    self.stop = max(a,b)
            else:
                self.stop = defaultStop[direction]

            if (direction == 'right'):
                temp = self.image.get_rect().width + stoppingGap
                x_motor[direction][self.lane_1] -= temp
                x_motor[direction][self.lane_2] -= temp

            elif (direction == 'left'):
                temp = self.image.get_rect().width + stoppingGap
                x_motor[direction][self.lane_1] += temp
                x_motor[direction][self.lane_2] += temp

            elif (direction == 'down'):
                temp = self.image.get_rect().height + stoppingGap
                y_motor[direction][self.lane_1] -= temp
                y_motor[direction][self.lane_2] -= temp

            elif (direction == 'up'):
                temp = self.image.get_rect().height + stoppingGap
                y_motor[direction][self.lane_1] += temp
                y_motor[direction][self.lane_2] += temp

            simulation.add(self)



        else:
            self.x = x_motor[direction][lane]
            self.y = y_motor[direction][lane]
            vehicles[direction][lane].append(self)
            self.index = len(vehicles[direction][lane]) - 1
            vehicles_notpassed[direction][self.lane].append(self.vehicleClass)
            self.angle = angle
            path = "images/" + vehicleClass + ".png"

            self.image = pygame.transform.rotate(
                pygame.transform.scale(pygame.image.load(path), (vehiclesize[0], vehiclesize[1])),
                self.angle
            )

            if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0):
                if (direction == 'right'):
                    self.stop = vehicles[direction][lane][self.index - 1].stop - \
                                vehicles[direction][lane][self.index - 1].image.get_rect().width - stoppingGap
                elif (direction == 'left'):
                    self.stop = vehicles[direction][lane][self.index - 1].stop + \
                                vehicles[direction][lane][self.index - 1].image.get_rect().width + stoppingGap
                elif (direction == 'down'):
                    self.stop = vehicles[direction][lane][self.index - 1].stop - \
                                vehicles[direction][lane][self.index - 1].image.get_rect().height - stoppingGap
                elif (direction == 'up'):
                    self.stop = vehicles[direction][lane][self.index - 1].stop + \
                                vehicles[direction][lane][self.index - 1].image.get_rect().height + stoppingGap
            else:
                self.stop = defaultStop[direction]

            if (direction == 'right'):
                temp = self.image.get_rect().width + stoppingGap
                x_motor[direction][lane] -= temp
            elif (direction == 'left'):
                temp = self.image.get_rect().width + stoppingGap
                x_motor[direction][lane] += temp
            elif (direction == 'down'):
                temp = self.image.get_rect().height + stoppingGap
                y_motor[direction][lane] -= temp
            elif (direction == 'up'):
                temp = self.image.get_rect().height + stoppingGap
                y_motor[direction][lane] += temp
            simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        global vehicle_throughput, vehicle_middle

        if currentYellow == 1 and not self.stopped:  
            self.stopped = True
            self.stop = defaultStop[self.direction] 


        if self.vehicleClass != 'bike' and self.vehicleClass != 'bicycle':

            if self.direction == 'right':
                if self.crossed == 0 and self.x + self.image.get_rect().width > stopLines[self.direction]:
                    self.crossed = 1
                    vehicle_middle += 1
                    vehicles_notpassed[self.direction][self.lane_1].pop(0)
                    vehicles_notpassed[self.direction][self.lane_2].pop(0)
                    self.speed = 3
                if self.crossed == 1 and self.x + self.image.get_rect().width > (stopLines[self.direction]+300) and self.queueMiddle == 0:
                        self.queueMiddle = 1
                        vehicle_middle -= 1
                        self.speed = speeds[self.vehicleClass] + 1.5
                        vehicle_throughput += 1
                if (self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (
                    currentGreen == 0 and currentYellow == 0)) and ((
                    self.index_1 == 0 or self.x + self.image.get_rect().width < (
                    vehicles[self.direction][self.lane_1][self.index_1 - 1].x - movingGap)) and ( 
                    self.index_2 == 0 or self.x + self.image.get_rect().width < (
                    vehicles[self.direction][self.lane_2][self.index_2 - 1].x - movingGap))):    
                    self.x += self.speed

            elif self.direction == 'down':
                if self.crossed == 0 and self.y + self.image.get_rect().height > stopLines[self.direction]:
                    self.crossed = 1
                    vehicle_middle += 1
                    vehicles_notpassed[self.direction][self.lane_1].pop(0)
                    vehicles_notpassed[self.direction][self.lane_2].pop(0)
                    self.speed = 3
                if self.crossed == 1 and self.y + self.image.get_rect().height > (stopLines[self.direction]+300) and self.queueMiddle == 0:
                        self.queueMiddle = 1
                        vehicle_middle -= 1
                        self.speed = speeds[self.vehicleClass] + 1.5
                        vehicle_throughput += 1
                if (self.y + self.image.get_rect().height <= self.stop or self.crossed == 1 or (
                    currentGreen == 1 and currentYellow == 0)) and ((
                    self.index_1 == 0 or self.y + self.image.get_rect().height < (
                    vehicles[self.direction][self.lane_1][self.index_1 - 1].y - movingGap)) and ( 
                    self.index_2 == 0 or self.y + self.image.get_rect().height < (
                    vehicles[self.direction][self.lane_2][self.index_2 - 1].y - movingGap)
                    )):    
                    self.y += self.speed

            elif self.direction == 'left':
                if self.crossed == 0 and self.x < stopLines[self.direction]:
                    self.crossed = 1
                    vehicle_middle += 1
                    vehicles_notpassed[self.direction][self.lane_1].pop(0)
                    vehicles_notpassed[self.direction][self.lane_2].pop(0)
                    self.speed = 3
                if self.crossed == 1 and self.x < (stopLines[self.direction]-300) and self.queueMiddle == 0:
                        vehicle_middle -= 1
                        self.queueMiddle = 1
                        self.speed = speeds[self.vehicleClass] + 1.5
                        vehicle_throughput += 1
                if (self.x >= self.stop or self.crossed == 1 or (
                        currentGreen == 0 and currentYellow == 0)) and ((
                        self.index_1 == 0 or self.x > (
                        vehicles[self.direction][self.lane_1][self.index_1 - 1].x +
                        vehicles[self.direction][self.lane_1][self.index_1 - 1].image.get_rect().width + movingGap)) and (
                        self.index_2 == 0 or self.x > (
                        vehicles[self.direction][self.lane_2][self.index_2 - 1].x +
                        vehicles[self.direction][self.lane_2][self.index_2 - 1].image.get_rect().width + movingGap)) ):
                    self.x -= self.speed

            elif self.direction == 'up':
                if self.crossed == 0 and self.y < stopLines[self.direction]:
                    self.crossed = 1
                    vehicle_middle += 1
                    vehicles_notpassed[self.direction][self.lane_1].pop(0)
                    vehicles_notpassed[self.direction][self.lane_2].pop(0)
                    self.speed = 3
                if self.crossed == 1 and self.y < (stopLines[self.direction]-300) and self.queueMiddle == 0:
                        vehicle_middle -= 1
                        self.queueMiddle = 1
                        self.speed = speeds[self.vehicleClass] + 1.5
                        vehicle_throughput += 1
                if (self.y >= self.stop or self.crossed == 1 or (
                        currentGreen == 1 and currentYellow == 0)) and ((
                        self.index_1 == 0 or self.y > (
                        vehicles[self.direction][self.lane_1][self.index_1 - 1].y +
                        vehicles[self.direction][self.lane_1][self.index_1 - 1].image.get_rect().height + movingGap)) and (
                        self.index_2 == 0 or self.y > (
                        vehicles[self.direction][self.lane_2][self.index_2 - 1].y +
                        vehicles[self.direction][self.lane_2][self.index_2 - 1].image.get_rect().height + movingGap))):
                    self.y -= self.speed

        else:
            if self.direction == 'right':
                if self.crossed == 0 and self.x + self.image.get_rect().width > stopLines[self.direction]:
                    self.crossed = 1
                    vehicle_middle += 1
                    vehicles_notpassed[self.direction][self.lane].pop(0)
                    self.speed = 3
                if self.crossed == 1 and self.x + self.image.get_rect().width > (stopLines[self.direction]+300) and self.queueMiddle == 0:
                        vehicle_middle -= 1
                        self.queueMiddle = 1
                        self.speed = speeds[self.vehicleClass] + 1.5
                        vehicle_throughput += 1
                if (self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (
                        currentGreen == 0 and currentYellow == 0)) and (
                        self.index == 0 or self.x + self.image.get_rect().width < (
                        vehicles[self.direction][self.lane][self.index - 1].x - movingGap)):
                    self.x += self.speed

            elif self.direction == 'down':
                if self.crossed == 0 and self.y + self.image.get_rect().height > stopLines[self.direction]:
                    self.crossed = 1
                    vehicle_middle += 1
                    vehicles_notpassed[self.direction][self.lane].pop(0)
                    self.speed = 3
                if self.crossed == 1 and self.y + self.image.get_rect().height > (stopLines[self.direction]+300) and self.queueMiddle == 0:
                        vehicle_middle -= 1
                        self.queueMiddle = 1
                        self.speed = speeds[self.vehicleClass] + 1.5
                        vehicle_throughput += 1
                if (self.y + self.image.get_rect().height <= self.stop or self.crossed == 1 or (
                        currentGreen == 1 and currentYellow == 0)) and (
                        self.index == 0 or self.y + self.image.get_rect().height < (
                        vehicles[self.direction][self.lane][self.index - 1].y - movingGap)):
                    self.y += self.speed

            elif self.direction == 'left':
                if self.crossed == 0 and self.x < stopLines[self.direction]:
                    self.crossed = 1
                    vehicle_middle += 1
                    vehicles_notpassed[self.direction][self.lane].pop(0)
                    self.speed = 3
                if self.crossed == 1 and self.x < (stopLines[self.direction]-300) and self.queueMiddle == 0:
                        vehicle_middle -= 1
                        self.queueMiddle = 1
                        self.speed = speeds[self.vehicleClass] + 1.5
                        vehicle_throughput += 1
                if (self.x >= self.stop or self.crossed == 1 or (
                        currentGreen == 0 and currentYellow == 0)) and (
                        self.index == 0 or self.x > (
                        vehicles[self.direction][self.lane][self.index - 1].x +
                        vehicles[self.direction][self.lane][self.index - 1].image.get_rect().width + movingGap)):
                    self.x -= self.speed

            elif self.direction == 'up':
                if self.crossed == 0 and self.y < stopLines[self.direction]:
                    self.crossed = 1
                    vehicle_middle += 1
                    vehicles_notpassed[self.direction][self.lane].pop(0)
                    self.speed = 3
                if self.crossed == 1 and self.y < (stopLines[self.direction]-300) and self.queueMiddle == 0:
                        vehicle_middle -= 1
                        self.queueMiddle = 1
                        self.speed = speeds[self.vehicleClass] + 1.5
                        vehicle_throughput += 1
                if (self.y >= self.stop or self.crossed == 1 or (
                        currentGreen == 1 and currentYellow == 0)) and (
                        self.index == 0 or self.y > (
                        vehicles[self.direction][self.lane][self.index - 1].y +
                        vehicles[self.direction][self.lane][self.index - 1].image.get_rect().height + movingGap)):
                    self.y -= self.speed


def initialize():
    
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, defaultYellow, defaultGreen[1])
    signals.append(ts2)


    repeat()
def get_vehicle_inZone():    
    vehicles_InDetectZone = {
    'right': {0: [], 1: [], 2: [], 3: []}, 
    'down': {0: [], 1: [], 2: [], 3: []}, 
    'left': {0: [], 1: [], 2: [], 3: []}, 
    'up': {0: [], 1: [], 2: [], 3: []}
        }
    for direction, lanes in vehicles_notpassed.items():
        for lane, vehicles in lanes.items():
            current_length = 0
            for vehicle in vehicles:
                if vehicle in vehicles_length:
                    vehicle_length = vehicles_length[vehicle]
                    if current_length + vehicle_length <= detect_length:
                        vehicles_InDetectZone[direction][lane].append(vehicle)
                        current_length += vehicle_length
                    else:
                        break  
    
    return vehicles_InDetectZone
def count_and_add_to_zone(vehicles_InDetectZone):
    vehicle_values = {'bike': 1, 'car': 0.5, 'bus': 0.5, 'truck': 0.5, 'firetruck':0.5}
    number_vehices_inZone = {
        'right': {'car': 0, 'bus': 0, 'truck': 0, 'bike': 0, 'firetruck': 0},
        'down': {'car': 0, 'bus': 0, 'truck': 0, 'bike': 0, 'firetruck': 0},
        'left': {'car': 0, 'bus': 0, 'truck': 0, 'bike': 0, 'firetruck': 0},
        'up': {'car': 0, 'bus': 0, 'truck': 0, 'bike': 0, 'firetruck': 0}
    }
    
    for direction, lanes in vehicles_InDetectZone.items():
        for vehicles in lanes.values():
            for vehicle in vehicles:
                if vehicle in vehicle_values:
                    number_vehices_inZone[direction][vehicle] += vehicle_values[vehicle]
    
    return number_vehices_inZone

def calculate_ratios(number_vehices_inZone):
    ratios = {}
    
    for direction, counts in number_vehices_inZone.items():
        total_area = sum(counts.get(vehicle, 0) * vehileArea.get(vehicle, 0) for vehicle in counts)
        area_direction = detect_width * detect_length
        ratios[direction] = total_area / area_direction
    
    return ratios
def prepare_input_data(ratios, number_vehices_inZone, direction):
    ratio_value = ratios[direction]
    vehicle_types = ['bike', 'car', 'bus', 'truck']
    
    vehicle_counts = [number_vehices_inZone[direction].get(vtype, 0) for vtype in vehicle_types]
    
    input_data = np.array([[ratio_value] + vehicle_counts])

    return input_data
def predict_traffic_light_time(input_data):
    predicted_time = model.predict(input_data)
    return predicted_time[0]

def check_for_firetruck(vehicles_InDetectZone):
    for direction, vehicles in vehicles_InDetectZone.items():
        if vehicles.get('firetruck', 0) > 0:
            return 1, direction
    return 0, None
def repeat():
    global currentGreen, currentYellow, nextGreen, vehicle_middle

    while signals[currentGreen].green > 0:   
        updateValues()
        time.sleep(1)

    currentYellow = 1  

    for vehicle in vehicles[directionNumbers[currentGreen]][0]:
        vehicle.stop = defaultStop[directionNumbers[currentGreen]]

    while signals[currentGreen].yellow > 0:
        updateValues()
        time.sleep(1)

    while vehicle_middle >= 5:
        time.sleep(1)

    currentYellow = 0   

    directions = ['down', 'up'] if currentGreen == 0 else ['right', 'left']

    detect_vehicle = count_and_add_to_zone(get_vehicle_inZone())
    ratios = calculate_ratios(detect_vehicle)

    if signals[currentGreen].green < 3:
        predicted_times = []
        
        for direct in directions:
            prepared_data = prepare_input_data(ratios, detect_vehicle, direct)
            traffic_light_time = predict_traffic_light_time(prepared_data)
            predicted_times.append(traffic_light_time)
        
        predict_green_time = round(max(predicted_times))
        print(f'Direct: {direct} - Green Time: {predict_green_time}')
        print("---------------------------------------------------")
        signals[currentGreen].green = predict_green_time
        signals[currentGreen].yellow = defaultYellow
        signals[currentGreen].red = defaultRed

    check_for_special_vehicle, vehicle_direct = check_for_firetruck(get_vehicle_inZone())
    if check_for_special_vehicle == 1:
        if (vehicle_direct in ['right', 'left']) and currentGreen == 1 and signals[currentGreen].red >= 0:
            nextGreen = 0
        elif (vehicle_direct in ['up', 'down']) and currentGreen == 0 and signals[currentGreen].red >= 0:
            nextGreen = 1

    currentGreen = nextGreen
    nextGreen = (currentGreen + 1) % noOfSignals
    signals[nextGreen].red = signals[currentGreen].yellow + signals[currentGreen].green

    repeat()

 

def updateValues():
    for i in range(0, noOfSignals):
        check_for_special_vehicle, _ = check_for_firetruck(get_vehicle_inZone())
        
        if check_for_special_vehicle == 1:
            break
        
        if i == currentGreen:
            signals[i].green -= 1 if currentYellow == 0 else 0
            signals[i].yellow -= 1 if currentYellow != 0 else 0
        else:
            signals[i].red -= 1

def generateVehicles():
    random.seed(42)

    dist_vehicle_car = 113
    dist_vehicle_bus = 20
    dist_vehicle_truck = 60
    dist_vehicle_motorbike = 793
    dist_vehicle_container = 0
    dist_vehicle_firetruck = 0
    dist_vehicle_van = 0
    dist_vehicle_bicycle = 0

    distance_increments = [
        dist_vehicle_car,
        dist_vehicle_bus,
        dist_vehicle_truck,
        dist_vehicle_motorbike,
        dist_vehicle_container,
        dist_vehicle_firetruck,            
        dist_vehicle_van,
        dist_vehicle_bicycle,        
    ]

    distributed_of_vehicle = [sum(distance_increments[:i+1]) for i in range(len(distance_increments))]

    while True:
        randNum_direction = random.randint(0, 99)
        randNum_vehicle = random.randint(0, distributed_of_vehicle[-1] - 1)

        if randNum_direction < 25:
            direction_number = 0
            angle = 0
        elif randNum_direction < 50:
            direction_number = 1
            angle = 270
        elif randNum_direction < 75:
            direction_number = 2
            angle = 180
        else:
            direction_number = 3
            angle = 90

        for i, dist in enumerate(distributed_of_vehicle):
            if randNum_vehicle < dist:
                vehicletype = vehicleTypes[i]
                vehiclesize = vehicleSizes[i]
                break

        lane_number = random.randint(0, 1) if i in [0, 1, 2, 4, 5, 6] else random.randint(0, 3)

        Vehicle(lane_number, vehicletype, direction_number, directionNumbers[direction_number], angle,vehiclesize)

        time.sleep(0.1)
        
class Main:
    def __init__(self):
        self.thread1 = threading.Thread(name="initialization", target=initialize, args=())  # initialization
        self.thread1.daemon = True
        self.thread1.start()

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.screenWidth = 1400
        self.screenHeight = 800
        self.screenSize = (self.screenWidth, self.screenHeight)

        self.background = pygame.image.load('images/best_cr.png')

        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("SIMULATION")

        self.redSignal = pygame.image.load('images/signals/red.png')
        self.yellowSignal = pygame.image.load('images/signals/yellow.png')
        self.greenSignal = pygame.image.load('images/signals/green.png')
        self.font = pygame.font.Font(None, 30)

        self.thread2 = threading.Thread(name="generateVehicles", target=generateVehicles, args=())  # Generating vehicles
        self.thread2.daemon = True
        self.thread2.start()

        # RUN TIME 
        self.run_time = 300
        self.start_time = time.time()

    def run(self):
        while True:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > self.run_time:
                print(f"Simulation has run for {self.run_time/60} minutes. Exiting...")
                print('Vehicle throughput:', vehicle_throughput)
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.blit(self.background, (0, 0)) 
            for i in range(0, noOfSignals):  
                if i == currentGreen:
                    if currentYellow == 1:
                        signals[i].signalText = signals[i].yellow
                        self.screen.blit(self.yellowSignal, signalCoods[i])
                        self.screen.blit(self.yellowSignal, signalCoods[i + 2])
                    else:
                        signals[i].signalText = signals[i].green
                        self.screen.blit(self.greenSignal, signalCoods[i])
                        self.screen.blit(self.greenSignal, signalCoods[i + 2])
                else:
                    if signals[i].red <= 10:
                        signals[i].signalText = signals[i].red
                    else:
                        signals[i].signalText = "---"
                    self.screen.blit(self.redSignal, signalCoods[i])
                    self.screen.blit(self.redSignal, signalCoods[i + 2])

            signalTexts = ["", "", "", ""]

            for i in range(0, noOfSignals):
                signalTexts[i] = self.font.render(str(signals[i].signalText), True, self.white, self.black)
                self.screen.blit(signalTexts[i], signalTimerCoods[i])
                self.screen.blit(signalTexts[i], signalTimerCoods[i + 2])

            for vehicle in simulation:
                self.screen.blit(vehicle.image, [vehicle.x, vehicle.y])
                vehicle.move()

            pygame.display.update()

            # Capture the frame
            frame = pygame.surfarray.array3d(self.screen)
            frame = np.rot90(frame)
            frame = np.flipud(frame)  
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

def get_pygame_frame():
    main = Main()
    return main.run()