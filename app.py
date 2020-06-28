# entry point to the application
import os
from flask import Flask, request, render_template

# used to talk to comp vision service
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

# enter key
from msrest.authentication import CognitiveServicesCredentials

# Go get the values from .env files
from dotenv import load_dotenv
load_dotenv()

# Load the values of the env vars
COGSVCS_KEY = os.getenv('COGSVCS_KEY')
COGSVCS_CLIENTURL = os.getenv('COGSVCS_CLIENTURL')

# Create the core flask app
app = Flask(__name__)

# WANT to respond to two different methods/verbs (how the user asks for url they have specified)
# GET - user has requested the form
# POST - user has filled it out, submitted back
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # User is requesting form
        return render_template('form.html')
    elif request.method == 'POST':
        # User has sent us data
        # first need to read the data
        image = request.files['image']
        client = ComputerVisionClient(
            COGSVCS_CLIENTURL,
            CognitiveServicesCredentials(COGSVCS_KEY)
        )
        result = client.describe_image_in_stream(image)
        message = 'no dog found :('

        # check if there is a dog
        if 'dog' in result.tags: 
            message = 'There is a dog! Wonderful !!'
        return render_template('result.html', message=message)
