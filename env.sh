#! /bin/bash
export APP_STAGE=dev
export APP_REGION=us-east-1
export APP_PROFILE=deploy

function pl-package(){
	sls package --package ./target/$APP_STAGE --stage $APP_STAGE -v -r $APP_REGION --aws-profile $APP_PROFILE
}

function pl-deploy(){
	sls deploy --package ./target/$APP_STAGE --stage $APP_STAGE  -v -r $APP_REGION --aws-profile $APP_PROFILE
}

function pl-remove(){
	sls remove --package ./target/$APP_STAGE --stage $APP_STAGE  -v -r $APP_REGION --aws-profile $APP_PROFILE
}