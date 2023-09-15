import json
from codecarbon import track_emissions
import requests
import logging
import sys
from codecarbon.output import LoggerOutput
import random

from time import sleep

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
mem_hog_endpoint_name  = "ecodreamers-aws-mem-hog"
mem_endpoint_name = "ecodreamers-aws-mem"

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
        '/cpu': cpu_route_handler,
        '/mem' : mem_route_handler,
        '/mem-hog': mem_hog_route_handler
    }
    
    try:
        path = event['path']
        httpMethod = event['httpMethod']
        queryStringParameters: dict = event['queryStringParameters']

        logger.info("processing method {} and path {} and sending to prometheus {}"
                    .format(httpMethod, path, prometheus_push_gateway))
        
        if 'GET' == httpMethod and path in routes:
            logger.info("supported")
            return respond(200, None, routes[path](path, queryStringParameters))
        else:
            logger.error('Throw Unsupported method "{}"'.format(path))
            raise ValueError('Unsupported path in request')
        
    except ValueError as e:
        logger.error(e)
        return respond(400, e, None)
    except Exception as e:
        logger.error(e)
        return respond(500, e, None)    


def network_route_handler(path, queryStringParameters):
    counter = queryStringParameters.get('counter')
    responses = []

    for index in range(counter):
        response = network_call(index)
        responses.append(response)

    return {
        "path" : path,
        "responses" : responses
    }


@track_emissions(
                project_name=network_endpoint_name,
                save_to_prometheus=False,
                prometheus_url=prometheus_push_gateway,
                experiment_id=eco_dreamers_network_experiment_id, 
                api_key=eco_dreamers_api_key, 
                save_to_api=False, 
                cloud_provider="aws", 
                cloud_region="us-east-1", 
                save_to_logger=True,
                logging_logger=outputLogger, 
                save_to_file=False, 
                emissions_endpoint=False, 
                log_level="info")
def network_call(index):
    r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))

    return {
        "index"  : index,
        "result" : r.json()
    }
    


def cpu_route_handler(path, queryStringParameters):
    counter = queryStringParameters.get('counter')
    factorial_n = queryStringParameters.get('factorial_n')
    responses = []

    for index in range(counter):
        response = cpu_call(index, factorial_n)
        responses.append(response)

    return {
        "path" : path,
        "responses" : responses
    }

@track_emissions(
                project_name=cpu_endpoint_name,
                save_to_prometheus=False,
                prometheus_url=prometheus_push_gateway,
                experiment_id=eco_dreamers_cpu_experiment_id, 
                api_key=eco_dreamers_api_key, 
                save_to_api=False, 
                cloud_provider="aws", 
                cloud_region="us-east-1", 
                save_to_logger=True,
                logging_logger=outputLogger, 
                save_to_file=False, 
                emissions_endpoint=False, 
                log_level="info")
def cpu_call(index, factorial_n):

    
    r = factorial(factorial_n)

    return {
        "index" : index,
        "result" : "the factorial of num {} is {}".format(factorial_n, r)
    }


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    

def mem_route_handler(path, queryStringParameters):
    counter = queryStringParameters.get('counter')
    list_size = queryStringParameters.get('list_size')
    responses = []

    for index in range(counter):
        response = mem_call(index, list_size)
        responses.append(response)

    return {
        "path" : path,
        "responses" : responses
    }


@track_emissions(
                project_name=mem_endpoint_name,
                save_to_prometheus=False,
                prometheus_url=prometheus_push_gateway,
                experiment_id=eco_dreamers_cpu_experiment_id, 
                api_key=eco_dreamers_api_key, 
                save_to_api=False, 
                cloud_provider="aws", 
                cloud_region="us-east-1", 
                save_to_logger=True,
                logging_logger=outputLogger, 
                save_to_file=False, 
                emissions_endpoint=False, 
                log_level="info")
def mem_call(index, list_size):

    memory_intensive_list = [random.randint(1, 100) for _ in range(int(list_size))]

    return {
        "index" : index,
        "result" : "generated a list of {} random numbers".format(len(memory_intensive_list))
    }



def mem_hog_route_handler(path, queryStringParameters):
    counter = queryStringParameters.get('counter')
    mem_in_mb = queryStringParameters.get('mem_in_mb')

    responses = []

    for index in range(counter):
        response = mem_hog_call(index, mem_in_mb)
        responses.append(response)

    return {
        "path" : path,
        "responses" : responses
    }


@track_emissions(
                project_name=mem_hog_endpoint_name,
                save_to_prometheus=False,
                prometheus_url=prometheus_push_gateway,
                experiment_id=eco_dreamers_cpu_experiment_id, 
                api_key=eco_dreamers_api_key, 
                save_to_api=False, 
                cloud_provider="aws", 
                cloud_region="us-east-1", 
                save_to_logger=True,
                logging_logger=outputLogger, 
                save_to_file=False, 
                emissions_endpoint=False, 
                log_level="info")
def mem_hog_call(index, mem_in_mb):
    
    result = memory_hog(int(mem_in_mb))

    return {
        "index" : index,
        "result" : "Memory Hog size is {}".format(result)
    }


def memory_hog(mem_in_mb):
    
    try:
        result: bytearray = bytearray(mem_in_mb * 1024 * 1024)
        return f"size of bytearray is {len(result)}"
    except MemoryError as e:
        return str(e)