import json
from codecarbon import track_emissions
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


def lambda_handler(event, context):
    
    routes = {
        '/network': network_route_handler,
        '/memory': memory_route_handler,
    }
    
    try:
        path = event['path']
        httpMethod = event['httpMethod']

        print("processing method {} and path {}".format(httpMethod, path))
        
        if 'GET' == httpMethod and path in routes:
            print("supported")
            return respond(200, None, routes[path](path))
        else:
            print('Throw Unsupported method "{}"'.format(path))
            raise ValueError('Unsupported path in request')
        
    except ValueError as e:
        return respond(400, e, None)
    except Exception as e:
        return respond(500, e, None)    



@track_emissions(cloud_region="us-east-1")
def network_route_handler(path):
    
    r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
        
    return {
        "result" : r.json(),
        "path" : path
    }
    

@track_emissions(cloud_region="us-east-1")   
def memory_route_handler(path):
    return {
        "result" : "some_memory_data",
        "path" : path
    }