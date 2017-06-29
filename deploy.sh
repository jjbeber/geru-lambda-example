#!/bin/bash

sudo docker run \
    -v $(pwd)/function:/app/ \
    python:3.6 \
    	pip install \
            -r /app/requirements.txt \
            -t /app/

aws cloudformation package \
    --template-file geru-lambda-example.yaml \
    --s3-bucket geru-lambda-example-code \
    --output-template-file packaged-template.yaml

ams_version=vrs$(date "+%s")

aws cloudformation create-change-set \
    --change-set-name $ams_version \
    --stack-name geru-lambda-example \
    --template-body file://packaged-template.yaml

aws cloudformation wait change-set-create-complete \
    --change-set-name $ams_version \
    --stack-name geru-lambda-example

aws cloudformation execute-change-set \
    --change-set-name $ams_version \
    --stack-name geru-lambda-example
