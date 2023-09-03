
# STEPS TO BUILD upload-lambda.zip

#### Execute:

```pip3 install --platform manylinux2014_x86_64 --only-binary=:all: --implementation cp -r requirements.txt -t ./package-exploded```

```cp ./lambda_function.py ./package-exploded && cd package-exploded && zip -x "*__pycache__*" -x "dist-info" -r ../upload-lambda.zip * && cd ..```

#### Finally upload upload-lambda.zip to AWS console Lambda



# INFO

Using an LED light bulb for 1 hour per day results in 0.07 kilowatt-hours (kWh) of electricity per week, 0.30 kWh per month, and 3.65 kWh per year.

Our lambda's /memory endpoint consumes 0.000001 kWh for 1 execution. At this energy consumption, how many lambda executions does it take to match the consumption of 1 ED light bulb for 1 hour. 


- [codecarbon INFO @ 22:59:46] Energy consumed for RAM : 0.000000 kWh. RAM Power : 0.06868028640747072 W
- [codecarbon INFO @ 22:59:46] Energy consumed for all CPUs : 0.000001 kWh. Total CPU Power : 42.5 W
- [codecarbon INFO @ 22:59:46] 0.000001 kWh of electricity used since the beginning.


70K lambda executions == 0.07 kWh / 0.000001 kWh

It would take 70K lambda executions on the /memory endpoint to consume the same as 1 ED light bulb for 1 hour. 


import boto3
from boto3.dynamodb.types import TypeSerializer


dynamo = boto3.client('dynamodb')



output.py L: 289

class LoggerOutput(BaseOutput):
    """
    Send emissions data to a logger
    """

    def __init__(self, logger, severity=logging.INFO):
        self.logger = logger
        self.logging_severity = severity

    def out(self, data: EmissionsData):
        try:
            logger.info("DynamoTest Configuring Dynamo .data: {}.".format(data))
            data_dict = data.__dict__
            logger.info("DynamoTest Configuring Dynamo data.__dict__: {}.".format(data_dict))

            data_loaded_obj = json.loads(json.dumps(data_dict), parse_float=Decimal)

            data_loaded_obj['cloud_provider'] = 'aws'
            data_loaded_obj['cloud_region'] = 'us-east-1'
            data_loaded_obj['on_cloud'] = 'Y'

            serialized_item = python_obj_to_dynamo_obj(data_loaded_obj)

            logger.info("DynamoTest serialized_data {} .".format(serialized_item))

            dynamo.put_item(TableName="emissions", Item=serialized_item)

            payload = dataclasses.asdict(data)
            self.logger.log(self.logging_severity, msg=json.dumps(payload))
        except Exception as e:
            logger.error(e, exc_info=True)

def python_obj_to_dynamo_obj(python_obj: dict) -> dict:
    logger.info("DynamoTest python_obj_to_dynamo_obj with: {}.".format(python_obj))

    serializer = TypeSerializer()
    return {
        k: serializer.serialize(v)
        for k, v in python_obj.items()
    }