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

def trans_paste(fg_img, bg_img, alpha=1.0, box=(0,0)):
    fg_img_trans = Image.new("RGBA",fg_img.size)
    fg_img_trans = Image.blend(fg_img_trans,fg_img,alpha)
    bg_img.paste(fg_img_trans,box,fg_img_trans)
    return bg_img

@app.route('/my/<image>/<int:width>/<int:height>')
def image_merge(image, width, height):
    filename = image.split('.')
    new_name = "{}_{}_{}.{}".format(filename[0],height,width,filename[1]);
    if not os.path.isfile(CURRENT_DIRECTORY+'/'+new_name):
        img = Image.open(CURRENT_DIRECTORY+'/'+image)
        img2 = Image.open(CURRENT_DIRECTORY+'/logo.png')

        img_resize = img.resize((width, height))
        img2_resize = img2.resize((100, 100))

        trans_paste(img2_resize,img_resize, 0.5, (100,100))

        img_resize.save(new_name, optimized=True) 

    return send_file(CURRENT_DIRECTORY+'/'+new_name, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()