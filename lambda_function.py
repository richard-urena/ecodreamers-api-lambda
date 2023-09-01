import json
from codecarbon import track_emissions
import requests
import logging
import sys
from codecarbon.output import LoggerOutput

logger = logging.getLogger(name="ecodreamers-api-lambda")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear


outputLogger = LoggerOutput(logger)

handler = logging.StreamHandler(sys.stdout)

logger.addHandler(handler)

import os

eco_dreamers_api_key = os.environ['API_KEY']
eco_dreamers_network_experiment_id = os.environ['NETWORK_EXPERIMENT_ID']
eco_dreamers_cpu_experiment_id = os.environ['CPU_EXPERIMENT_ID']

cpu_endpoint_name  = "ecodreamers-aws-cpu"
network_endpoint_name  = "ecodreamers-aws-network"

prometheus_push_gateway = os.environ['PROMETHEUS_PUSH_GATEWAY']

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
        '/cpu': cpu_route_handler
    }
    
    try:
        path = event['path']
        httpMethod = event['httpMethod']

        logger.info("processing method {} and path {} and sending to prometheus {}"
                    .format(httpMethod, path, prometheus_push_gateway))
        
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


@track_emissions(
                project_name=network_endpoint_name,
                save_to_prometheus=True,
                prometheus_url=prometheus_push_gateway,
                experiment_id=eco_dreamers_network_experiment_id, 
                api_key=eco_dreamers_api_key, 
                save_to_api=True, 
                cloud_provider="aws", 
                cloud_region="us-east-1", 
                save_to_logger=True,
                logging_logger=outputLogger, 
                save_to_file=False, 
                emissions_endpoint=False, 
                log_level="debug")
def network_route_handler(path):
    r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
        
    return {
        "result" : r.json(),
        "path" : path
    }
    

@track_emissions(
                project_name=cpu_endpoint_name,
                save_to_prometheus=True,
                prometheus_url=prometheus_push_gateway,
                experiment_id=eco_dreamers_cpu_experiment_id, 
                api_key=eco_dreamers_api_key, 
                save_to_api=True, 
                cloud_provider="aws", 
                cloud_region="us-east-1", 
                save_to_logger=True,
                logging_logger=outputLogger, 
                save_to_file=False, 
                emissions_endpoint=False, 
                log_level="debug")
def cpu_route_handler(path):

    num = 10
    r = factorial(num)

    return {
        "result" : "the factorial of num {} is {}".format(num, r),
        "path" : path
    }


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)