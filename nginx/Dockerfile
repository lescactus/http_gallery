FROM nginx:stable

LABEL "Maintainer"="Alexandre Maldémé" \
        "version"="0.1"

# Add the Nginx app config in the image
ADD ./app.conf /etc/nginx/conf.d

# By default Nginx use port 80
EXPOSE 80


# Run Nginx
CMD ["nginx", "-g", "daemon off;"]
