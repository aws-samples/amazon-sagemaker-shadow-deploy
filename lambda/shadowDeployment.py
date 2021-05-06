import os
import io
import boto3
import json
import csv
import sys
import uuid
from urllib.parse import unquote_plus

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['SHADOW_DEPLOYMENT_LOG'])
_lambda = boto3.client('lambda')

# grab environment variables
ENDPOINT_NAME_V1 = os.environ['ENDPOINT_NAME_V1']
ENDPOINT_NAME_V2 = os.environ['ENDPOINT_NAME_V2']

runtime = boto3.client('runtime.sagemaker')
s3 = boto3.client('s3')


def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    postData = json.loads(json.dumps(event))
    print("postData")
    print(postData)

    payloadIn = postData['body']
    print("payloadIn***")
    print(payloadIn)

    payloadJson = json.loads(payloadIn)

    payload = payloadJson['data']
    print("payload***")
    print(payload)

    response1 = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME_V1,
                                        ContentType='text/csv',
                                        Body=payload)
    print(response1)
    result = json.loads(response1['Body'].read().decode())
    print(result)
    pred = int(result['predictions'][0]['score'])
    predicted_label = 'M' if pred == 1 else 'B'
    print("Predicted result- from model version 1", predicted_label)

    strPayload = str(payload)
    strResult = str(result)

    dbResp1 = table.put_item(
        Item={
            'endpointName': ENDPOINT_NAME_V1,
            'request': strPayload,
            'response': strResult
        }
    )

    print('dbResp1:', dbResp1)

    response2 = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME_V2,
                                        ContentType='text/csv',
                                        Body=payload)
    print(response2)
    result1 = json.loads(response2['Body'].read().decode())
    print(result1)
    pred = int(result1['predictions'][0]['score'])
    predicted_label1 = 'M' if pred == 1 else 'B'
    print("Predicted result- from model version 2", predicted_label1)

    strResult1 = str(result1)

    dbResp2 = table.put_item(
        Item={
            'endpointName': ENDPOINT_NAME_V2,
            'request': strPayload,
            'response': strResult1
        }
    )

    print('dbResp2:', dbResp2)

    requestid = response1['ResponseMetadata']['RequestId']
    my_json_string = json.dumps(
        {'RequestID': requestid, 'Version1 Response': predicted_label, 'Version2 Response': predicted_label1})
    bodytext = predicted_label + predicted_label1
    filename = "shadowdeployment/" + requestid + ".json"

    print("compared prediction result: ", my_json_string)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "result ": result
        })
    }
