#MultipleBeStack

MultipleBeStack project contains 2 Built services using python and node.

## Quick start guide 🚀

This instructions allow you to build and deploy a stack for MultipleBe application.

Check **Deployment** to know how to deploy this project.
Check **Development** to know how to update this project.

### Pre-requisites  📋
  - _Node v12 or a later version_
  - _Python v3 or a later version_
  - An AWS account with described permisions in lambda-executor-policy.json file.
  - pyenv
```sh
$ brew install pyenv
$ pyenv install 3.8.2
$ pyenv install 3.8.6
$ pyenv global 3.8.2
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
$ python --version
```    
  - poetry
```sh
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
- Serverless:
```sh
$ npm install --silent --no-progress serverless@2.4.0
$ npm install
$ sls --version
```
#### Set your AWS credentials
Set your AWS credentials and set a profile name for $APP_PROFILE, in my case I called it as 'deploy'. You could use --overwrite to update an existing profile.
```sh
$ sls config credentials --provider aws --key $AWS_ACCESS_KEY --secret $AWS_SECRET_ACCESS_KEY --profile $APP_PROFILE
```

## Stack Services
Each service should be developed under ./services folder, e.g: 
- service-node
- service-python


#### Working in a service
Each service contains a defined structure: 
```sh
./service
    functions
        feature
            function.yml
            lambda_function.py
    resources
        resource.yml
    env.sh
    package.json
    serverless.yml    
```
In order to enable multiple-be-functions, use:
```sh
$ source env.sh
$ npm install
# enables: multiple-be-package, multiple-be-deploy, multiple-be-remove
```

#### Shared/Common code
- ./serverless.common.yml: Contains shared configuration 

### Deployment 🔧
```sh
$ cd ./service/multiple-be-service
$ source env.sh
$ multiple-be-package
$ multiple-be-deploy
```

### Testing

https://[URL_GENERATED]/dev/node
https://[URL_GENERATED]/dev/python

## Building with 🛠️

* [Serverless](https://www.serverless.com/) - Allows us to build and run applications and services without thinking about servers
* [Python](https://www.python.org/) - Just the easiest programming language
* [Node](https://www.nodejs.org/) - Programming language for dummies
* [AWS](https://aws.amazon.com/) -  Offers cloud computing web services.


## Authors ✒️
* **Pablo Atoche** - *Initial work* - [PalituxD](https://github.com/PalituxD)

## License 📄