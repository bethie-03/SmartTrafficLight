from flask import Flask, render_template

app = Flask(__name__,static_folder="./static", template_folder="./templates")

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')

@app.route('/VD-template', methods=["GET"])
def Vehicle_Detection():
    return render_template('vehicle_detection.html')
    
if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)