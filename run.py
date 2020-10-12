import os 
from flask import Flask, Response, send_file, render_template, request, redirect, jsonify
from utils import fileutils
from PIL import Image
from datetime import datetime
from decouple import config
import pytesseract


CURRENT_DIRECTORY = os.getcwd()
app = Flask(__name__)

def trans_paste(fg_img, bg_img, alpha=1.0, box=(0,0)):
    fg_img_trans = Image.new("RGBA",fg_img.size)
    fg_img_trans = Image.blend(fg_img_trans,fg_img,alpha)
    bg_img.paste(fg_img_trans,box,fg_img_trans)
    return bg_img

@app.route("/")
def index():
    return render_template('docs/index.html')

@app.route("/upload-image/", methods=['GET', 'POST'])
def upload_image():
    context = dict()
    if (request.method=='POST'):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        context['msg'] = "imagem Enviada!"
        file = request.files['image']
        names = file.filename.split('.')
        file.save(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens',  '{}.{}'.format(int(timestamp), names[1])))
    return render_template('docs/upload-image.html', **context)

@app.route("/upload-logo/", methods=['GET', 'POST'])
def upload_logo():
    context = dict()
    if (request.method=='POST'):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        context['msg'] = "marca Enviada!"
        context['class'] = "success"
        file = request.files['image']
        names = file.filename.split('.')
        if names[1] in ['png', 'PNG']:
            file.save(os.path.join(CURRENT_DIRECTORY, 'uploads', 'marcas',  '{}.{}'.format(int(timestamp), names[1])))
        else:
            context['msg'] = "A imagem deve permitir transparecencia [PNG]"
            context['class'] = "danger"

    return render_template('docs/upload-logo.html', **context)

@app.route("/get-images/")
def get_form_images():
    images = os.listdir(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens'))
    marcas = os.listdir(os.path.join(CURRENT_DIRECTORY, 'uploads', 'marcas'))

    images = filter( lambda a: 're' not in a, images)
    marcas = filter( lambda a: 're' not in a, marcas)

    return render_template('docs/get-images.html', imagens=images, magua=marcas)

@app.route("/py-tesseract/")
def get_form_tesseract():
    images = os.listdir(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens'))
    images = filter( lambda a: 're' not in a, images)

    return render_template('docs/get-ocr.html', imagens=images)

@app.route("/tesseract/")
def tesseract():
    image = request.args.get('image')
    text = ""
    if os.path.isfile(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', image)):
        img = Image.open(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', image))
        text = pytesseract.image_to_string(img).strip()
        
    return jsonify({
        "text": text
    })

@app.route("/boto3/")
def textextract_aws():

    import boto3

    image = request.args.get('image')
    text = ""
    if os.path.isfile(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', image)):
        document_name = os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', image)
        with open(document_name, 'rb') as document:
            imageBytes = bytearray(document.read())

    textract = boto3.client('textract', 
            region_name='us-west-2', 
            aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key= config("AWS_SECRET_ACCESS_KEY"))
    response = textract.detect_document_text(Document={'Bytes': imageBytes})

    texts = []
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            texts.append({'text': item["Text"]})

    return jsonify(texts)

@app.route("/image/", methods=['GET', ])
def image():
    image = request.args.get('image')
    width = request.args.get('width', default=0, type=int)
    height = request.args.get('height', default=0, type=int)
    marca = request.args.get('marca')
    filename = image.split('.')

    if width or height:
        new_name = fileutils.new_image_name_factory(filename[0],filename[1],width,height)
    else:
        new_name = image

    if not os.path.isfile(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name)):
        img = Image.open(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', image))
        img_resize = fileutils.resize_image(img, width=width, height=height)
        img_resize.save(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name), optimized=True) 
    
    if marca:
        new_image = Image.open(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name))
        marca_image = Image.open(os.path.join(CURRENT_DIRECTORY, 'uploads', 'marcas', marca))
        width_of_marca = int(new_image.width*(25/100))
        marca_new_image = fileutils.resize_image(marca_image, width=width_of_marca)
        new_image = trans_paste(marca_new_image, new_image, 0.5, (100,100))
        new_image = new_image.convert("RGB")
        new_image.save(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name), optimized=True) 

    return send_file(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name), mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True)