from configs import *
import cv2
import numpy as np
import tempfile
import base64
import os

class Vehicle_Detection:
    def __init__(self):
        self.model = MODEL
        self.__fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
    def image_inference(self, image, vehicle_conf):
        self.model.conf = vehicle_conf
        results = self.model(image)
        dataframe = results.pandas().xyxy[0]
        if len(dataframe) > 0:
            for index in range(len(dataframe)):
                row = dataframe.iloc[index]
                x1 = int(row.iloc[0])
                y1 = int(row.iloc[1])
                x2 = int(row.iloc[2])
                y2 = int(row.iloc[3])
                confidence = round(row.iloc[4],2)
                name = row.iloc[6]
                cv2.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
                cv2.putText(image, f'{name}-{confidence}', (x1,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 5)
                cv2.putText(image, f'{name}-{confidence}', (x1,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return image
        
    def base64_image_inference(self, base64_image_data, vehicle_conf):
        encoded_data = str(base64_image_data).split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        result_image = self.image_inference(image, vehicle_conf)
        
        _, buffer = cv2.imencode('.jpg', result_image)
        jpg_as_text = base64.b64encode(buffer)

        return f"data:image/jpeg;base64,{jpg_as_text.decode('utf-8')}"
    
    def base64_video_inference(self, base64_video_data, output_folder, vehicle_conf):
        encoded_data = str(base64_video_data).split(',')[1]
        decoded = base64.b64decode(encoded_data)
        output_video_path = output_folder + '/result.mp4'
        output_video_path_temp = output_folder + '/result_temp.mp4'
        
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
            
            result_frame = self.image_inference(frame, vehicle_conf)
            out.write(result_frame)

        cap.release()
        out.release()
        
        os.system(f'ffmpeg -i {output_video_path} -vcodec libx264 -movflags faststart -acodec aac -strict experimental {output_video_path_temp}')
        os.rename(output_video_path_temp, output_video_path)

        return output_video_path
    
    def video_to_base64(self, file_path):
        with open(file_path, "rb") as video_file:
            video_bytes = video_file.read()
            base64_encoded = base64.b64encode(video_bytes)
        
        return f"data:video/mp4;base64,{base64_encoded.decode('utf-8')}"
    
    def base64_video_to_path(self, base64_video_data):
        encoded_data = base64_video_data.split(',')[1]
        decoded_data = base64.b64decode(encoded_data)

        with open('sample_result/base64_video.mp4', 'wb') as video_file:
            video_file.write(decoded_data)
    
    def base64_video_realtime_inference(self, vehicle_conf):
        file_path = 'sample_result/base64_video.mp4'
        cap = cv2.VideoCapture(file_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            result_frame = self.image_inference(frame, vehicle_conf)
            _, buffer = cv2.imencode('.jpg', result_frame)
            byte_image = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + byte_image + b'\r\n')
            
        cap.release()
        if os.path.exists(file_path):
            os.remove(file_path)

    