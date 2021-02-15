#! /bin/bash

function my-app-create-service() {
  sls create --template-path ./template/ --path ./services/$1 --name $1
}

function my-app-dynamodb-admin() {
  DYNAMO_ENDPOINT=http://localhost:8000
  ./node_modules/.bin/dynamodb-admin --port 8081 -o
}

export DIR_WORK_PATH=$(pwd)