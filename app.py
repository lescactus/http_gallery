#!/usr/bin/env python3
 
# export FLASK_APP=app.py
# export FLASK_DEBUG=1
# flask run

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import flash
from werkzeug import secure_filename    # secure_filemane()
import imghdr                           # what()


app = Flask(__name__)
app.allowed_extensions = ('bmp', 'gif', 'png', 'jpg', 'jpeg')
app.upload_dir = './uploads/'
app.secret_key = '1RK+3588rZaM081C/c6fhTIvNOzb1L9K9nP0ojX3O7b7wJjAz5/I7EICH3m+/530/sW7iotaUK4R'

# Main page
@app.route("/index/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        
        # If file is uploaded
        if request.files['file']:

            # If the extension of the file is allowed
            if check_filetype(request.files['file'], request.files['file'].filename):
                
                filename = secure_filename(request.files['file'].filename)
                request.files['file'].save('./uploads/' + filename)
                return "OK"
            else:
                return "File extension not allowed"

        else:
            return "No file uploaded"


# Return true if the extension of filename is allowed
# and the type is truly an image, and not a random file 
# with an image extension
def check_filetype(file, filename):
    return  filename.rsplit('.')[-1].lower() in app.allowed_extensions and  imghdr.what(file)





if __name__ == "__main__":
    app.run()