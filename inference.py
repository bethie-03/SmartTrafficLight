from ultralytics import YOLO
from configs import *
import cv2
import numpy as np
import tempfile
import base64

class Vehicle_Detection:
    def __init__(self, vehicle_conf):
        self.model = YOLO(MODEL_PATH)
        self.vehicle_conf = vehicle_conf
        self.__fourcc = cv2.VideoWriter_fourcc(*'H264')
        
    def image_inference(self, image):
        results = self.model(image)[0]
        
        if len(results.boxes.data) > 0:
            for result in results.boxes.data:
                confidence = result[4]
                if confidence > self.vehicle_conf:
                    x1, y1, x2, y2 = list(map(int, result[:4])) 
                    confidence = result[4]
                    class_id = int(result[5])
                    cv2.putText(image, f'{self.model.names[class_id]}', (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.rectangle(image, (x1,y1), (x2,y2), (255,255,255), 2)
                else:
                    continue
        return image
        
    def base64_image_inference(self, base64_image_data):
        encoded_data = str(base64_image_data).split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        result_image = self.image_inference(image)
        
        _, buffer = cv2.imencode('.jpg', result_image)
        jpg_as_text = base64.b64encode(buffer)

        return f"data:image/jpeg;base64,{jpg_as_text.decode('utf-8')}"
    
    def base64_video_inference(self, base64_video_data, output_video_path):
        encoded_data = str(base64_video_data).split(',')[1]
        decoded = base64.b64decode(encoded_data)
        
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(decoded)
            cap = cv2.VideoCapture(temp.name)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
        out = cv2.VideoWriter(filename=output_video_path, fourcc=self.__fourcc, fps=fps, frameSize=(width, height))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            

            result_frame = self.image_inference(frame)
            out.write(result_frame)

        cap.release()
        out.release()
        return output_video_path
    
    def video_to_base64(self, file_path):
        with open(file_path, "rb") as video_file:
            video_bytes = video_file.read()
            base64_encoded = base64.b64encode(video_bytes)
        
        return f"data:video/mp4;base64,{base64_encoded.decode('utf-8')}"
    
    def base64_video_realtime_inference(self, base64_video_data, host_url):
        encoded_data = str(base64_video_data).split(',')[1]
        decoded = base64.b64decode(encoded_data)
        
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(decoded)
            cap = cv2.VideoCapture(temp.name)
                    
        id = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            result_frame = self.image_inference(frame)
            cv2.imwrite(f'./static/images/frame_{id}.jpg', result_frame)
            image_url = host_url + f'static/images/frame_{id}.jpg'
            yield f'{image_url}'
            id += 1
        cap.release()
