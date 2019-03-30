from flask import Flask, Response, send_file
from PIL import Image
import os 
CURRENT_DIRECTORY = os.getcwd()

app = Flask(__name__)

@app.route("/")
def hello():
    return "coloque o nome da imagem na url"

@app.route('/<image>')
def image(image):
    return send_file(CURRENT_DIRECTORY+'/'+image, mimetype='image/jpeg')

@app.route('/<image>/<int:width>/<int:height>')
def image_resize(image, width, height):
    filename = image.split('.')
    new_name = "{}_{}_{}.{}".format(filename[0],height,width,filename[1]);
    if not os.path.isfile(CURRENT_DIRECTORY+'/'+new_name):
        img = Image.open(CURRENT_DIRECTORY+'/'+image)
        img_resize = img.resize((width, height))
        img_resize.save(new_name, optimized=True) 
    return send_file(CURRENT_DIRECTORY+'/'+new_name, mimetype='image/jpeg')

