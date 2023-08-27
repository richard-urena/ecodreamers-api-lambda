
# STEPS TO BUILD upload-lambda.zip

#### Execute:

```pip3 install --platform manylinux2014_x86_64 --only-binary=:all: --implementation cp -r requirements.txt -t ./package-exploded```

```cp ./lambda_function.py ./package-exploded && cd package-exploded && zip -x "*__pycache__*" -x "dist-info" -r ../upload-lambda.zip * && cd ..```

#### Finally upload upload-lambda.zip to AWS console Lambda