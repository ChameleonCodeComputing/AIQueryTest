from flask import Flask, request, jsonify, send_file
from flask import send_file, make_response
import openpyxl
import requests
from bs4 import BeautifulSoup
import io
import os
import tempfile
from openpyxl.utils import get_column_letter
import random
from waitress import serve
from openpyxl.styles import Alignment
from flask_cors import CORS
import zipfile
import uuid
import boto3
import json
import textwrap
import re
import nltk
from nltk.tokenize import sent_tokenize
import csv
from openpyxl import load_workbook
import time
import pandas as pd





app = Flask(__name__)
CORS(app)

port = 5031
apiPath = f"/genAI_Sample_platform"
apiPathLarge = f"/genAI_Sample_platform_large"
apiTimeout = 120

# Record the start time
start_time = time.time()

# Add Your AWS credentials here
aws_access_key_id = 'exampleaccesskeyID'
aws_secret_access_key = 'exampleaccesskey'

#Enter query to be sent to ChatGPT here. Below is an example query.
gptPrompt = """

 Can you write a lymeric about a frog for me?

"""



light_html_temp="""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email</title>
</head>
<body>
    {{plaintext}}
    {{trackurl}}
    {{unsuburl}}
</html>


"""

system_prompt= gptPrompt



def write_to_s3(bucket_name, file_name, data):
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, file_name)
    object.put(Body=data)

# Function to send request to GPT model
def send_request(prompt, engine, temperature):
    #print("Calling our AI services")
    #print(f"full prompt is : {prompt}")




####################################################################################
####################################################################################
    #Enter your API key here
    #api_key = XXXXX
####################################################################################
####################################################################################







    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "messages": [{"role": "system", "content": prompt}],
        "model": engine,
        "temperature": temperature,
        "max_tokens": 1024,
        "top_p": 1,
	    "seed":37,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers, timeout=apiTimeout)
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return f"Error 999: {e}"
    else:
        if response.status_code == 200:
            try:
                return response.json()["choices"][0]["message"]["content"]
            except KeyError:
                return "Error: 'choices' or 'message' key not found in response."
        else:
            return f"Error {response.status_code}: {response.text}"



def getGPTResponse ():

    responseai = ""
    try:
        responseai = send_request(system_prompt, "gpt-3.5-turbo-16k", 0.7)
    except:
        return f"Error in call to GPT: {responseai}"
    else:
        return responseai



@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"}), 200



@app.route(apiPathLarge, methods=['POST'])
def gpt_Large():
    start_time = time.time()  # Start tracking the execution time
    #print("Uploading file...")

    # possibly pick up parameters
    response = getGPTResponse()

    return response




@app.route(apiPath, methods=['POST'])
def gpt():

    start_time = time.time()  # Start tracking the execution time
    #print("Uploading file...")

    # possibly pick up parameters
    response = getGPTResponse()

    return response


if __name__ == '__main__':
    print("Ready running : {0}: Gen AI {1} CSV file at {2} ".format(port, apiPathLarge))
    serve(app, host='0.0.0.0', port=port)
    print(f"All done: stopping : Gen AI Sample")
