import json
from codecarbon import track_emissions
import requests
import logging
import sys

logger = logging.getLogger(name="ecodreamers-api-lambda")
logger.setLevel(logging.INFO)


handler = logging.StreamHandler(sys.stdout)

logger.addHandler(handler)

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

        logger.info("processing method {} and path {}".format(httpMethod, path))
        
        if 'GET' == httpMethod and path in routes:
            logger.info("supported")
            return respond(200, None, routes[path](path))
        else:
            logger.error('Throw Unsupported method "{}"'.format(path))
            raise ValueError('Unsupported path in request')
        
    except ValueError as e:
        logger.error(e)
        return respond(400, e, None)
    except Exception as e:
        logger.error(e)
        return respond(500, e, None)    


@track_emissions(cloud_provider="aws", cloud_region="us-east-1", save_to_logger=True,
                  logging_logger=logger, save_to_file=False, 
                  emissions_endpoint=False, save_to_api=False, log_level="debug")
def network_route_handler(path):
    r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
        
    return {
        "result" : r.json(),
        "path" : path
    }
    

@track_emissions(cloud_provider="aws", cloud_region="us-east-1", save_to_logger=True,
                  logging_logger=logger, save_to_file=False, 
                  emissions_endpoint=False, save_to_api=False, log_level="debug")
def memory_route_handler(path):
    return {
        "result" : "some_memory_data",
        "path" : path
    }