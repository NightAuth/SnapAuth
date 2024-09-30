from flask import Flask, jsonify, render_template, Response
from eyetracking import *


app = Flask(__name__)

@app.route('/')
def root():
    pass

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary-frame')

@app.route()

if __name__ == '__main__':
    app.run(debug=True)

