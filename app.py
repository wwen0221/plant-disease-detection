from flask import Flask,render_template
import boto3, botocore
import configparser
import os
from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, request
import json
import numpy as np

app = Flask(__name__)

@app.route('/')
@app.route('/', methods=["POST","GET"])
def hello_world():
   return render_template('index.html')
   cls = ''
   prob = 0

   if request.method == 'POST':
      print('called')
      config = configparser.ConfigParser()
      config.read('config.ini')

      key = config['aws']['AWS_ACCESS_KEY']
      secret = config['aws']['AWS_SECRET_ACCESS_KEY']

      runtime = boto3.client(
         "sagemaker-runtime",
         aws_access_key_id=key,
         aws_secret_access_key=secret
      )

      endpoint = 'sagemaker-imageclassification-notebook-ep--2022-12-11-11-33-49'


      # Read image into memory
      payload = request.files['file']

      # Send image via InvokeEndpoint API
      response = runtime.invoke_endpoint(EndpointName=endpoint,
                                         ContentType='application/x-image',
                                         Body=payload)

      result = response["Body"].read()
      result = json.loads(result)
      index = np.argmax(result)

      object_categories = [
         "001.Apple___Apple_scab",
         "002.Apple___Black_rot",
         "003.Apple___Cedar_apple_rust",
         "004.Apple___healthy",
         "005.Blueberry___healthy",
         "006.Cherry_(including_sour)___healthy",
         "007.Cherry_(including_sour)___Powdery_mildew",
         "008.Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
         "009.Corn_(maize)___Common_rust_",
         "010.Corn_(maize)___healthy"
      ]

      cls = object_categories[index]
      prob = str(round(result[index],2))


   return render_template('index.html',cls=cls,prob=prob)



def upload_file_to_s3(file, acl="public-read"):
   print('called')

   config = configparser.ConfigParser()
   config.read('config.ini')

   BUCKET = config['aws']['AWS_BUCKET_NAME']
   key = config['aws']['AWS_ACCESS_KEY']
   secret = config['aws']['AWS_SECRET_ACCESS_KEY']
   domain = config['aws']['AWS_DOMAIN']
   print(key)
   print(secret)
   s3 = boto3.client(
       "s3",
       aws_access_key_id=key,
       aws_secret_access_key=secret
   )


   try:
      s3.upload_fileobj(
         file,
         BUCKET,
         'image',
         ExtraArgs={
            "ACL": acl,
            "ContentType": file.content_type
         }
      )

   except Exception as e:
      # This is a catch all exception, edit this part to fit your needs.
      print("Something Happened: ", e)
      return e

   # after upload file to s3 bucket, return filename of the uploaded file
   return 'image'

if __name__ == '__main__':
   app.run()
   app.run()

