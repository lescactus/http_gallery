#!/usr/bin/env python3
 
# export FLASK_APP=app.py
# export FLASK_DEBUG=1
# flask run

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import flash
from flask import redirect
from flask import send_from_directory
from werkzeug import secure_filename    # secure_filemane()
import imghdr                           # what()
import os                               # join()


app = Flask(__name__)

# App config
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024                         # 16Mb max per upload
app.config['ALLOWED_EXTENSIONS'] = ('bmp', 'gif', 'png', 'jpg', 'jpeg')     # Allowed file extensions to be uploaded
app.config['UPLOAD_DIR'] = 'uploads/'                                       # Upload directory
app.secret_key = '1RK+3588rZaM081C/c6fhTIvNOzb1L9K9nP0ojX3O7b7wJjAz5/I7EICH3m+/530/sW7iotaUK4R'


# Main page
@app.route("/index/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def main():
    #if request.method == 'GET':
    #    return render_template('index.html')
    if request.method == 'POST':
        
        # If file is uploaded
        if request.files['file'] and request.files['file'].filename:
            
            # If the extension of the file is allowed
            if check_filetype(request.files['file']):
                
                filename = secure_filename(request.files['file'].filename)

                # Save the file in app.config['UPLOAD_DIR']
                request.files['file'].save(
                    os.path.join(
                        app.config['UPLOAD_DIR'], 
                        filename))

                flash(u'OK', 'status_ok')
                return redirect(request.url)
                
            else:
                flash(u'File extension not allowed !', 'error')

        else:
            flash(u'No file uploaded !', 'error')

    # List if images in the upload folder
    images = [ img for img in os.listdir(app.config['UPLOAD_DIR']) 
        if (
            check_filetype(
                os.path.join(app.config['UPLOAD_DIR'], img)
            ) and 
            img.rsplit('.')[-1].lower() 
                in app.config['ALLOWED_EXTENSIONS']
        )
    ]

    # Display the index for GET or POST requests
    return render_template('index.html', 
        upload_dir=app.config['UPLOAD_DIR'], 
        images=images)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_DIR'],
                               filename)


# Return true if the type is truly an image, 
# and not a random file # with an image 
# extension
def check_filetype(file):
    return imghdr.what(file) in app.config['ALLOWED_EXTENSIONS']



if __name__ == "__main__":
    app.run()