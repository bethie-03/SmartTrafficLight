from flask import Flask, render_template, request, Response
from inference import *
from road_analysis import *
from pygame_demo import get_pygame_frame

app = Flask(__name__,static_folder="./static", template_folder="./templates")
RA = RoadAnalysis()
VD = Vehicle_Detection()

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')

@app.route('/VD-template', methods=["GET"])
def vehicle_detect():
    return render_template('vehicle_detection.html')

@app.route('/RA-template', methods=["GET"])
def road_anal():
    return render_template('road_analysis.html')

@app.route('/Pygame-template', methods=["GET"])
def pygame_demo():
    return render_template('pygame.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' in request.form:
        file = request.form['image']
        vehicle_cfd = request.form['vehicle_cfd']
        result = VD.base64_image_inference(file, float(vehicle_cfd))
        return {"result": result}
    
@app.route('/process-video', methods=['POST'])
def process_video():
    if 'video' in request.form:
        file = request.form['video']
        vehicle_cfd = request.form['vehicle_cfd']
        file_path = VD.base64_video_inference(file, 'sample_result/result.mp4', float(vehicle_cfd))
        result = VD.video_to_base64(file_path)
        return {"result": result}
    
@app.route('/process_video_realtime', methods=['POST'])
def upload_video():
    if 'video' in request.form:
        file = request.form['video']
        global vehicle_cfd
        vehicle_cfd = request.form['vehicle_cfd']
        VD.base64_video_to_path(file)
    return "Video uploaded successfully", 200

@app.route('/stream_video', methods=['GET'])
def process_video_realtime():
    return Response(VD.base64_video_realtime_inference(float(vehicle_cfd)), mimetype='multipart/x-mixed-replace; boundary=frame')
    
def convert_to_int(points):
    int_points = []
    points = points.split(',')
    
    for i in range(len(points)):
        points[i] = float(points[i])
        int_points.append(points[i])
        
    return int_points

@app.route('/analyse-image', methods=['POST'])
def road_analysis():
    if 'imagesrc' in request.form:
        ratio_points=[]
        imagesrc = request.form['imagesrc']
        
        top_left = request.form['top_left']
        top_right = request.form['top_right']
        bottom_right = request.form['bottom_right']
        bottom_left = request.form['bottom_left']
        
        roadLength = request.form['roadLength']
        motorcycle_speed = request.form['motorcycle_speed']
        car_speed = request.form['car_speed']
        
        top_left_point = convert_to_int(top_left)
        top_right_point = convert_to_int(top_right)
        bottom_right_point = convert_to_int(bottom_right)
        bottom_left_point = convert_to_int(bottom_left)
        
        ratio_points.append(top_left_point)
        ratio_points.append(top_right_point)
        ratio_points.append(bottom_right_point)
        ratio_points.append(bottom_left_point)
        
        motorcycle_speed_min, motorcycle_speed_average, motorcycle_speed_max = map(float, motorcycle_speed.split(','))
        car_speed_min, car_speed_average, car_speed_max = map(float, car_speed.split(','))
        result, input_value, green_light_time, time = RA.road_analyse(imagesrc, ratio_points, float(roadLength), motorcycle_speed_min, motorcycle_speed_average, motorcycle_speed_max, car_speed_min, car_speed_average, car_speed_max)
        return {"result": result, 
                "Ratio" : input_value[0], 
                "Motorcycle_count": input_value[1], 
                "Car_count": input_value[2],
                "Bus_count": input_value[3], 
                "Truck_count": input_value[4],
                "Green_light_time": green_light_time[0],
                "Furthest_vehicle_to_light_time": time}
    
@app.route('/stream_pygame')
def stream_pygame():
    return Response(get_pygame_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)