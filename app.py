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
from werkzeug import secure_filename            # secure_filemane()
from flask_wtf import FlaskForm                 # FlaskForm
from flask_wtf.file import FileField            # FileField()
from flask_wtf.file import FileRequired         # FileRequired()
from wtforms.validators import ValidationError  # ValidationError()
import imghdr                                   # what()
import os                                       # join()


app = Flask(__name__)

# App config
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024                         # 16Mb max per upload
app.config['ALLOWED_EXTENSIONS'] = ('bmp', 'gif', 'png', 'jpg', 'jpeg')     # Allowed file extensions to be uploaded
app.config['UPLOAD_DIR'] = 'uploads/'                                       # Upload directory
app.secret_key = '1RK+3588rZaM081C/c6fhTIvNOzb1L9K9nP0ojX3O7b7wJjAz5/I7EICH3m+/530/sW7iotaUK4R'





def validate_file(alwd_ext):

    def _validate_file(form, field):

        # Raise a ValidationError if the image is not
        # a real image. Ex: random file with image extension
        if not imghdr.what(field.data) in alwd_ext:
            message = "File must be an image !"
            raise ValidationError(message)
            return _validate_file

        # Raise a ValidationError if the image extension is not
        # listed in app.config['ALLOWED_EXTENSIONS']
        if not field.data.filename.rsplit('.')[-1].lower() in app.config['ALLOWED_EXTENSIONS']:
            message = "File must have a valid image extension !"
            raise ValidationError(message)
            return _validate_file
        
        
    return _validate_file


# Image form declaration
class ImageForm(FlaskForm):

    image = FileField('image', validators=[
        FileRequired(),
        validate_file(app.config['ALLOWED_EXTENSIONS'])
    ])



# Main page
@app.route("/index/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def main():

    form = ImageForm()
    if request.method == 'POST':

        # Form is submitted
        if form.validate_on_submit():
            f = form.image.data
            filename = secure_filename(f.filename)

            print("f: " + str(f))
            print("filename: " + str(filename))
            print("save path: " + os.path.join(app.config['UPLOAD_DIR'],  filename))

            f.save(os.path.join(
                app.config['UPLOAD_DIR'], 
                filename
            ))

            flash(u'File successfully uploaded', 'status_ok')
            return redirect(request.url)

    # List if images in the upload folder
    images = [ img for img in os.listdir(app.config['UPLOAD_DIR']) 
        if 
        (
            check_filetype(os.path.join(app.config['UPLOAD_DIR'], 
                img)) 
            and img.rsplit('.')[-1].lower() 
                in app.config['ALLOWED_EXTENSIONS']
        )
    ]

    # Display the index for GET or POST requests
    return render_template('index.html', 
        upload_dir=app.config['UPLOAD_DIR'], 
        images=images,
        form=form)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_DIR'],
                               filename)


if __name__ == "__main__":
    app.run()



# Raise a ValidationError if the image is not
# a real image. Ex: random file with image extension
def check_filetype(alwd_ext):
    message = "File must be an image !"

    def _check_filetype(form, field):    
        if not imghdr.what(field.data) in alwd_ext:
            raise ValidationError(message)
  
    return _check_filetype
