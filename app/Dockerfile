FROM registry.access.redhat.com/ubi9/python-311

LABEL "Maintainer"="Alexandre Maldémé" \
        "version"="0.1"

# Add the app
COPY --chown=1001:1001 . .

# Set Flask env variables
ENV FLASK_APP=app.py \
    FLASK_DEBUG=0

# Flask will use port 8080
EXPOSE 8080

# Install Flask via pip,
# Change ownership of app to www-data
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
