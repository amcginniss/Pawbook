from __future__ import print_function

from __future__ import print_function

import boto3
import json
import requests

def lambda_handler(event, context):


    image_url = event['image']
    img_data = requests.get(image_url).content

    img_name = image_url.split('/')[-1]

    s3_client = boto3.client('s3')

    response = s3_client.put_object(
    Body=requests.get(image_url).content,
    Bucket='pawbook-images',
    Key=img_name
    )

    return response, img_name
