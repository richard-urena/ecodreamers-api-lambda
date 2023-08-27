#import boto3
import json

#dynamo = boto3.client('dynamodb')

from codecarbon import track_emissions


# pip3 install -r requirements.txt -t ./

import requests



def respond(status_code, err, res=None):
    response = {
        'statusCode': status_code,
        'body': 'unsupported' if err else res,
        'headers': {
            'Content-Type': 'application/json',
        }
    }
    
    return response


#@track_emissions(cloud_region="us-east-1")
def lambda_handler(event, context):
    
    routes = {
        '/network': network_route_handler,
        '/memory': memory_route_handler,
    }
    
    path = event['path']
    #path = '/network'
    httpMethod = event['httpMethod']
    # httpMethod = 'GET'

    print("process method {} and path {}".format(httpMethod, path))
    
    if 'GET' == httpMethod and path in routes:
        print("supported")
        return respond(200, None, routes[path](path))
    else:
        print('Unsupported method "{}"'.format(path))
        return respond(400, ValueError('Unsupported path in request'), None)


@track_emissions(cloud_region="us-east-1")
def network_route_handler(path):
    
    # how to downd with pip and package for upload to lambda 
    # https://medium.com/@cziegler_99189/using-the-requests-library-in-aws-lambda-with-screenshots-fa36c4630d82
    
    # TODO: set up .zip and download codecarbo and requests library
    
    try:
        print("UPDATED VIA BUILD SCRIPTS")
        r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))

        
        return {
            "result" : r.json(),
            "path" : path
        }
        
    except Exception as e:
        respond(500, ValueError('Error processing handler: {e}'.format(e=e)), None)
    
    
def memory_route_handler(path):
    return {
        "result" : "some_memory_data",
        "path" : path
    }