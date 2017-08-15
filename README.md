HTTP Gallery
==================

A Flask web app that allow users to upload local images that are displayed in a html gallery and carousel.

**gallery**: [gallery.alexasr.tk][1]

It uses:

   * [Python v3][2]
   * [Flask v0.12][3]
   * [Bootstrap v3][4]
   * [JQuery v2.2.4][5]
   * [ludovicscribe/bootstrap-gallery][6]
   * [kartik-v/bootstrap-fileinput][7]

Use it now
----------

```sh
# Install requirements
$ pip install -r app/requirements.txt

# If you want the debug mode:
$ export FLASK_DEBUG=1

# Change settings in app/app.py (ex: SERVER_NAME)
$ vim app/app.py 
```
```python
> app.config['DEBUG'] = True
> app.config['SERVER_NAME'] = "www.myserver.com"

# 16Mb max per file upload
> app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024                       
# Allowed file extensions to be uploaded  
> app.config['ALLOWED_EXTENSIONS'] = ('bmp', 'gif', 'png', 'jpg', 'jpeg')
# Upload directory where images are stored
> app.config['UPLOAD_DIR'] = 'uploads/'
# Thumbnails directory where thumbnails are stored                                
> app.config['THUMBN_DIR'] = 'thumbnails/'
# Thumbnails size in px               
> app.config['THUMBN_SIZE'] = [300, 300]
# Secret key. Can be generated using head -1 /dev/urandom| base64                                 
> app.secret_key = '1RK+3588rZaM081C/c6fhTIvNOzb1L9K9nP0ojX3O7b7wJjAz5/I7EICH3m+/530/sW7iotaUK4R'
```
```sh
# Run it:
$ FLASK_APP=app/app.py python3 -m flask run
 * Serving Flask app "app"
 * Forcing debug mode on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 129-590-285
```

Now point your browser at http://127.0.0.1:5000

If you want to change the host and port Flask will bound to, just run:

```sh
$ FLASK_APP=app/app.py python3 -m flask run --host=0.0.0.0 --port=6000
 * Serving Flask app "app"
 * Forcing debug mode on
 * Running on http://0.0.0.0:6000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 129-590-285
```



### Docker
**gallery** can easily be dockerized and is shipped with a ``Dockerfile``.

By default, the container will expose port 5000, so change this within the ``Dockerfile`` if necessary. When ready, simply use the ``Dockerfile`` to build the image.

```sh
cd app
docker build -t gallery .
```
This will create the Docker image.

Once done, run the Docker image and map the port to whatever you wish on your host. In this example, we simply map port 80 of the host to port 5000 of the container:

```sh
docker run -d -p 80:5000 --restart="always" --name gallery gallery 
```

Now point your browser at http://127.0.0.1/ 

### Docker Compose
**gallery** comes docker-compose ready. It is shipped with a ``docker-compose.yml`` and an Nginx Dockerfile. Nginx will reverse-proxyfiying requests to the Flask container on port :5000


```yml
# docker-compose.yml
version: '2'

services:
  front:
    build:
      context: ./nginx/
      dockerfile: Dockerfile
    container_name: app-front
    depends_on:
      - back
    restart: always
    ports:
     - "80:80"
    links:
     - back:back

  back:
    build:
      context: ./app/
      dockerfile: Dockerfile
    container_name: app-back
    restart: always
    expose:
     - 5000
```


Modify the ``docker-compose.yml`` if needed and run:

```sh
$ docker-compose build
$ docker-compose up -d
```

This will map the port 80 of the host to the port 80 of Nginx's container. 


###Docker volumes
Since Docker is stateless, uploaded files are removed when the container is destroyed. You can make your data persistent by mounting the `uploads/` and `thumbnails/` folders in Docker volumes.
```sh
# docker run \
docker run -d \
-p 80:5000 \
-v $(pwd)/uploads:/var/www/uploads \
-v $(pwd)/thumbnails:/var/www/thumbnails \
--name app \
app
```

```yml
# With docker-compose
version: '2'

services:
  front:
    build:
      context: ./nginx/
      dockerfile: Dockerfile
    container_name: app-front
    depends_on:
      - back
    restart: always
    ports:
     - "80:80"
    links:
     - back:back

  back:
    build:
      context: ./app/
      dockerfile: Dockerfile
    container_name: app-back
    restart: always
    expose:
     - 5000
    volumes:
     - ./app/uploads:/var/www/uploads
     - ./app/thumbnails:/var/www/thumbnails
```
But be carefull with the folder permissions. Indeed, you must ensure to set ownership of the `uploads/` and `thumbnails/` folders to the user `www-data`, but it may not exists on the host. 

Screenshots
-----------
####Index
![Index](https://i.imgur.com/DIMzgU6.png "Index")
***
####Image upload form
![Upload an image](https://i.imgur.com/RGCiG8l.png "Upload an image")
***
####Gallery
![Gallery](https://i.imgur.com/eadFN3J.png "Gallery")
***
####Carousel
![Carousel](https://i.imgur.com/WaMuiv9.png "Carousel")
***
####Responsive gallery
![Responsive](https://i.imgur.com/fGxH2CH.png "Responsive")
***



[1]: http://gallery.alexasr.tk/
[2]: https://www.python.org/
[3]: http://flask.pocoo.org/
[4]: https://getbootstrap.com/
[5]: https://jquery.com/
[6]: https://github.com/ludovicscribe/bootstrap-gallery
[7]: https://github.com/kartik-v/bootstrap-fileinput