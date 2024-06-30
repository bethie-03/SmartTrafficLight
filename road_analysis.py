import cv2
from ultralytics import YOLO
import numpy as np
from configs import *
import base64
import pickle

class RoadAnalysis:
    def __init__(self, base64_image_data, ratio_points: list, road_length: float, motorcycle_speed_min, motorcycle_speed_average, motorcycle_speed_max, car_speed_min, car_speed_average, car_speed_max):
        self.model = YOLO(MODEL_PATH)
        self.image = self.base64_image_inference(base64_image_data)
        self.mask = None
        self.mask_image = None
        self.total_bounding_box_area = 0
        self.road_length = road_length
        
        self.bboxes = []
        self.points = self.actual_point(ratio_points) #top_left, top_right, bottom_right, bottom_left
        self.points_array_list = None

        self.motorcycle_speed_min = motorcycle_speed_min #km/h
        self.motorcycle_speed_average = motorcycle_speed_average
        self.motorcycle_speed_max = motorcycle_speed_max

        self.car_speed_min = car_speed_min
        self.car_speed_average = car_speed_average
        self.car_speed_max = car_speed_max
        
        self.polynomial_reg_model = POLYNOMIAL_REG_MODEL
        
    def base64_image_inference(self, base64_image_data):
        encoded_data = str(base64_image_data).split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image
    
    def actual_point(self, ratio_points):
        actual_points = []
        height, width, _ = self.image.shape
        for i in range(len(ratio_points)):
            x_ratio, y_ratio = ratio_points[i]
            actual_x = int(width * x_ratio)
            actual_y = int(height * y_ratio)
            actual_points.append([actual_x, actual_y])
        return actual_points
    
    def convert_array_list(self):
        self.points_array_list = np.array(self.points, np.int32)
        self.points_array_list = self.points_array_list.reshape((-1, 1, 2))
    
    def create_mask_image(self) -> int:
        height, width, _ = self.image.shape
        self.convert_array_list()
        self.mask = np.zeros((height, width), dtype=np.uint8)
        cv2.fillPoly(self.mask, [self.points_array_list], color=255)
        self.mask_image = cv2.bitwise_and(self.image,self.image, mask=self.mask)
    
    def calculate_total_zone_pixels(self) -> int:
        total_zone_area = cv2.countNonZero(self.mask)
        return total_zone_area
        
    def calculate_intersection_area(self, box1, box2):
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2
        
        x1_i = max(x1_1, x1_2)
        y1_i = max(y1_1, y1_2)
        x2_i = min(x2_1, x2_2)
        y2_i = min(y2_1, y2_2)
        
        intersection_area = max(0, x2_i - x1_i + 1) * max(0, y2_i - y1_i + 1)
        return intersection_area
    
    '''def count_total_overlap_area(self):
        total_overlap_area = 0
        bboxes = self.bboxes.copy()
        while len(bboxes) > 1:
            for i in range(1, len(bboxes)):
                intersection_area = self.calculate_intersection_area(bboxes[0][:4], bboxes[i][:4])
                total_overlap_area += intersection_area
            bboxes.pop(0)
            
        self.total_bounding_box_area -= total_overlap_area'''
        
    def calculate_total_bounding_box_area(self, image):
        image = cv2.bitwise_and(image,image, mask=self.mask)
        height, width, _ = image.shape
        for y in range(height):
            for x in range(width):
                pixel_value = image[y, x]
                if np.all(pixel_value == [255, 0, 0]):
                    self.total_bounding_box_area += 1

    def calculate_ratio(self, image):
        self.calculate_total_bounding_box_area(image) 
        total_zone_area = self.calculate_total_zone_pixels()
        ratio = self.total_bounding_box_area/total_zone_area
        return ratio
        
    def find_indices_of_min_value(self, distances: list):
        min_value = min(distances)
        return [index for index, value in enumerate(distances) if value == min_value]
    
    def find_indices_of_max_value(self, distances: list):
        max_value = max(distances)
        return [index for index, value in enumerate(distances) if value == max_value]

    def find_furthest_vehicle_position(self):
        top_left, top_right, bottom_right, bottom_left = self.points

        height = abs(max(top_left[1], top_right[1]) - max(bottom_left[1], bottom_right[1]))
        width = abs(max(top_left[0], bottom_left[0]) - max(top_right[0], bottom_right[0]))

        road_height = max(bottom_right[1], bottom_left[1]) - max(top_left[1], top_right[1]) + 1
        
        nearest_to_the_top_distances = []
        furthest_to_the_bottom_distances = []
        
        if height > width:
            for box in self.bboxes:
                distance = max(0, box[1] - max(top_left[1], top_right[1]) + 1)
                nearest_to_the_top_distances.append(distance)
        else:
            for box in self.bboxes:
                distance = max(0, box[0] - max(top_left[0], bottom_left[0]) + 1)
                nearest_to_the_top_distances.append(distance)
            
        indices_of_min_value = self.find_indices_of_min_value(nearest_to_the_top_distances)
                
        if len(indices_of_min_value) > 1:
            if height > width:
                for index in indices_of_min_value:
                    distance = max(bottom_right[1], bottom_left[1]) - self.bboxes[index][3] + 1
                    furthest_to_the_bottom_distances.append(distance)
            else:
                for index in indices_of_min_value:
                    distance = max(top_right[0], bottom_right[0]) - self.bboxes[index][2] + 1
                    furthest_to_the_bottom_distances.append(distance)
            indices_of_max_value = self.find_indices_of_max_value(furthest_to_the_bottom_distances)
            return furthest_to_the_bottom_distances[indices_of_max_value[0]], indices_of_min_value[indices_of_max_value[0]]
        else:
            if height > width:
                furthest_to_the_bottom_distance = max(bottom_right[1], bottom_left[1]) - self.bboxes[indices_of_min_value[0]][3] + 1
            else:
                furthest_to_the_bottom_distance = max(top_right[0], bottom_right[0]) - self.bboxes[indices_of_min_value[0]][2] + 1
            return road_height, furthest_to_the_bottom_distance , indices_of_min_value[0]
    
    def create_front_vehicle_zone(self):
        top_left, top_right, bottom_right, bottom_left = self.points

        height = abs(max(top_left[1], top_right[1]) - max(bottom_left[1], bottom_right[1]))
        width = abs(max(top_left[0], bottom_left[0]) - max(top_right[0], bottom_right[0]))

        _, _ , furthest_index = self.find_furthest_vehicle_position()
        x1, y1, x2, y2, _ = self.bboxes[furthest_index]
        if height > width:
            front_zone_box = (x1 - (x2 - x1), y2, x2 + (x2 - x1), max(bottom_right[1], bottom_left[1]))
            front_zone_height = front_zone_box[3] - front_zone_box[1]
        else:
            front_zone_box = (x2, y1, max(top_right[0], bottom_left[0]), y2)
            front_zone_height = front_zone_box[3] - front_zone_box[1]
        cv2.rectangle(self.image, (front_zone_box[0], front_zone_box[1]), (front_zone_box[2], front_zone_box[3]), (255,0,0), 2)
        return front_zone_box, front_zone_height
    
    def check_front_vehicle_appearance(self, furthest_vehicle_y2):
        check = False
        front_zone_box, front_zone_height = self.create_front_vehicle_zone()
        for box in self.bboxes:
            intersection_area = self.calculate_intersection_area(box[:4], front_zone_box)
            if intersection_area != 0:
                '''distance_between_vehicles = abs(box[3] - furthest_vehicle_y2)
                ratio_of_distance_to_road_height = distance_between_vehicles / front_zone_height
                if ratio_of_distance_to_road_height >= 0.5:
                    continue
                else:'''
                cv2.rectangle(self.image, (box[0], box[1]), (box[2], box[3]), (255,0,0), 2)
                check = True
        return check 

    def calculate_actual_speed(self, v_min, v_average, v_max, ratio):
        ratio_deviation = 0.5 - ratio
        if ratio_deviation < 0:
            ratio_deviation_percentage = (abs(ratio_deviation) / (0.8 - 0.5)) 
            actual_speed = v_average - ((v_average - v_min) * ratio_deviation_percentage)
        elif ratio_deviation > 0:
            ratio_deviation_percentage = (abs(ratio_deviation) / 0.5) 
            actual_speed = v_average + ((v_max - v_average) * ratio_deviation_percentage)
        else:
            return v_average
        return actual_speed   

    def calculate_time_for_furthest_vehicle_to_light(self, ratio):
        road_height, furthest_vehicle_to_light_height , index = self.find_furthest_vehicle_position()
        furthest_vehicle_to_light_distance = (furthest_vehicle_to_light_height / road_height) * self.road_length
        if self.check_front_vehicle_appearance(self.bboxes[index][3]) == True:
            if self.bboxes[index][4] == 5:
                vehicle_speed = self.calculate_actual_speed(self.motorcycle_speed_min, 
                                                            self.motorcycle_speed_average, 
                                                            self.motorcycle_speed_max, 
                                                            ratio)
            else:
                vehicle_speed = self.calculate_actual_speed(self.car_speed_min, 
                                                            self.car_speed_average, 
                                                            self.car_speed_max, 
                                                            ratio)
        else:
            if self.bboxes[index][4] == 5:
                vehicle_speed = self.motorcycle_speed_max
            else:
                vehicle_speed = self.car_speed_max
        time = furthest_vehicle_to_light_distance/vehicle_speed
        time=round(time*3600,2)
        cv2.rectangle(self.image, (self.bboxes[index][0], self.bboxes[index][1]), (self.bboxes[index][2], self.bboxes[index][3]), (0,255,), 2)
        return time
        
    def count_label(self, ratio):
        input_value = [round(ratio,2),0,0,0,0] #Ratio	Motorcycle count	Car count	Bus count	Truck count	
        for box in self.bboxes:
            if box[4] == 0:
                input_value[3] += 1
            elif box[4] == 3:
                input_value[1] += 1
            elif box[4] == 4:
                input_value[2] += 1
            else:
                input_value[4] += 1
        return input_value
    
    def predict_green_light_time(self, ratio):
        input_value = self.count_label(ratio)
        input_value_array = np.array([input_value])
        green_light_time = np.round(self.polynomial_reg_model.predict(input_value_array),2)
        return input_value, green_light_time
            
    def road_analyse(self):
        self.convert_array_list() 
        image = self.image.copy()
        cv2.polylines(self.image, [self.points_array_list], isClosed=True, color=(0, 0, 255), thickness=2)        
        self.create_mask_image()
        results = self.model(self.mask_image)[0]
        
        if len(results.boxes.data) > 0:
            for result in results.boxes.data:
                x1, y1, x2, y2 = list(map(int, result[:4])) 
                class_id = int(result[5])
                self.bboxes.append([x1,y1,x2,y2, class_id])
                
                cv2.rectangle(image, (x1,y1), (x2,y2), (255,0,0), -1)
                
                #cv2.putText(self.image, f'{self.model.names[class_id]}', (x1,y1), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(self.image, (x1,y1), (x2,y2), (0,0,255),2)
                cv2.putText(self.image, f'{class_id}-{round(float(result[4]),2)}', (x1 ,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 5)
                cv2.putText(self.image, f'{class_id}-{round(float(result[4]),2)}', (x1 ,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                
            ratio = self.calculate_ratio(image)
            input_value, green_light_time = self.predict_green_light_time(ratio)
            if ratio <= 0.8:
                time = self.calculate_time_for_furthest_vehicle_to_light(ratio)
                            
        else:
            cv2.putText(self.image, f'NO DETECTION', (10,50), cv2.FONT_HERSHEY_DUPLEX, 1, color=(255,255,255), thickness=3) 
            
        _, buffer = cv2.imencode('.jpg', self.image)
        jpg_as_text = base64.b64encode(buffer)
        return f"data:image/jpeg;base64,{jpg_as_text.decode('utf-8')}", input_value, green_light_time, time
