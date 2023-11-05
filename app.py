from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from src.facereconstrcut.pipeline.FaceFitPipeline import FaceFitter
from src.facereconstrcut import logger
import json
app = Flask(__name__)
import cv2
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Function to check if the uploaded file is an allowed image format
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if a file is provided in the POST request
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']

        # Check if the file is empty
        if file.filename == '':
            return redirect(request.url)

        # Check if the file is allowed
        if file and allowed_file(file.filename):
            # Save the file to the uploads directory
            filename = secure_filename(file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filename)
            return redirect(url_for('show_image', filename=file.filename))

    return render_template('upload.html')

@app.route('/uploads/<filename>')
def show_image(filename):
    return render_template('upload.html', filename=filename)


@app.route('/results/<filename>')
def show_res(filename):
    savename = os.path.basename(filename).split('.')[0] + '-crop.png'
    return render_template('upload.html', resultname=savename, filename=filename)

@app.route('/process_image/<filename>', methods=['POST'])
def processImage(filename):
    if request.method=='POST':
        #Read the image from static upload folder
        inputname = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        #process it
        ff = FaceFitter(inputname)
        save_dir = app.config['RESULT_FOLDER']
        os.makedirs(save_dir, exist_ok=True)
        obj_list, crop_list = ff.fitface(save_dir)
        print('######$$$$$$$#####\n',crop_list)
        
        obj_list = [url_for('static', filename=f'results/{x}') for x in obj_list]
        print('######$$$$$$$#####\n',obj_list)

        return render_template('upload.html', image_list=crop_list, obj_list=obj_list, filename=filename)
    else:
        return redirect(request.url)


if __name__ == '__main__':
    app.run(debug=True)