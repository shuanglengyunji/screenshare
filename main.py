from flask import Flask, render_template, Response
from camera import VideoCamera
import flask
from PIL import ImageGrab
from PIL import Image
from io import BytesIO
import socket
import win32gui
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

imCursor = Image.open('cursor.png')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Grab & Feed Screen Shot
@app.route('/screen.png')
def serve_pil_image():
    # Grab Screen 
    imScreen=ImageGrab.grab()
    # Get Cursor
    curX,curY=win32gui.GetCursorPos()
    # Add Cursor
    imScreen.paste(imCursor,box=(curX,curY),mask=imCursor)
    # Save to BytesIO
    img_buffer = BytesIO()
    imScreen.save(img_buffer,'PNG',quality=10)
    img_buffer.seek(0)
    return flask.send_file(img_buffer, mimetype='image/png')

@app.route('/js/<path:path>')
def send_js(path):
    return flask.send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return flask.send_from_directory('css', path)

if __name__ == '__main__':
	app.run('0.0.0.0', debug=False)

'''
ImageGrab.grab().save(img_buffer, 'PNG', quality=10)

# app.run(host=get_ip(), debug=False)
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
'''
