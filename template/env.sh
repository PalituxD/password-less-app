#! /bin/bash
export APP_STAGE=dev
export APP_REGION=us-east-1
export APP_PROFILE=deploy

function my-app-package() {
  echo "PARENT DIR_WORK_PATH-> $DIR_WORK_PATH"
  "$DIR_WORK_PATH"/node_modules/.bin/sls package --package ./target/$APP_STAGE --stage $APP_STAGE -v -r $APP_REGION --aws-profile $APP_PROFILE
}

function my-app-deploy() {
  echo "PARENT DIR_WORK_PATH-> $DIR_WORK_PATH"
  "$DIR_WORK_PATH"/node_modules/.bin/sls deploy --package ./target/$APP_STAGE --stage $APP_STAGE -v -r $APP_REGION --aws-profile $APP_PROFILE
}

function my-app-remove() {
  echo "PARENT DIR_WORK_PATH-> $DIR_WORK_PATH"
  "$DIR_WORK_PATH"/node_modules/.bin/sls remove --package ./target/$APP_STAGE --stage $APP_STAGE -v -r $APP_REGION --aws-profile $APP_PROFILE
}

function my-app-offline() {
  echo "PARENT DIR_WORK_PATH-> $DIR_WORK_PATH"
  python -m venv .env
  source .env/bin/activate
  pip install -r target/$APP_STAGE/requirements.txt
  "$DIR_WORK_PATH"/node_modules/.bin/sls offline start
  deactivate
  rm -r .env
}

function my-app-unittest() {
  pyenv versions
  poetry env info
  poetry install
  poetry show --tree
  ln -s ../../common common
  poetry run pytest tests
  rm common
}
