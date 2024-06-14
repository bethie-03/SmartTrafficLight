from flask import Flask, render_template, request, Response
from inference import *
from road_analysis import *

app = Flask(__name__,static_folder="./static", template_folder="./templates")

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')

@app.route('/VD-template', methods=["GET"])
def vehicle_detect():
    return render_template('vehicle_detection.html')

@app.route('/RA-template', methods=["GET"])
def road_anal():
    return render_template('road_analysis.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' in request.form:
        file = request.form['image']
        vehicle_cfd = request.form['vehicle_cfd']
        VD = Vehicle_Detection(float(vehicle_cfd))
        result = VD.base64_image_inference(file)
        return {"result": result}
    
@app.route('/process-video', methods=['POST'])
def process_video():
    if 'video' in request.form:
        file = request.form['video']
        vehicle_cfd = request.form['vehicle_cfd']
        VD = Vehicle_Detection(float(vehicle_cfd))
        file_path = VD.base64_video_inference(file, 'sample_result/result.mp4')
        result = VD.video_to_base64(file_path)
        return {"result": result}

@app.route('/process_video_realtime', methods=['POST'])
def process_video_realtime():
    if 'video' in request.form:
        file = request.form['video']
        vehicle_cfd = request.form['vehicle_cfd']
        host_url = request.host_url
        VD = Vehicle_Detection(float(vehicle_cfd))
        return Response(VD.base64_video_realtime_inference(file, host_url), mimetype='text/event-stream')

@app.route('/analyse-image', methods=['POST'])
def road_analysis():
    if 'imagesrc' in request.form:
        imagesrc = request.form['imagesrc']
        points = request.form['points']
        roadLength = request.form['roadLength']
        motorcycle_speed = request.form['motorcycle_speed']
        car_speed = request.form['car_speed']
        motorcycle_speed_min, motorcycle_speed_average, motorcycle_speed_max = map(float, motorcycle_speed.split(','))
        car_speed_min, car_speed_average, car_speed_max = map(float, car_speed.split(','))
        RA = RoadAnalysis(imagesrc, points, roadLength, motorcycle_speed_min, motorcycle_speed_average, motorcycle_speed_max, car_speed_min, car_speed_average, car_speed_max)
        result = RA.road_analyse()
        return {"result": result}
        
if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)