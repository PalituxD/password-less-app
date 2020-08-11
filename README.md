# PasswordLessApp

PasswordLessApp project builds a passwordless stack api in AWS that allows you create your own secured services. The Authentication process is verified using the user's mobile number. A secret code is sent to the user inmeditly after invocation of /sign-up and validated it in /sign-in, the generated JWT could be refreshed using /refresh-token endpoint.

## Quick start guide 🚀

This instructions allow you to build and deploy a passwordless application.

Check **Deployment** to know how to deploy this project.
Check **Development** to know how to update this project.

### Pre-requisites  📋
  - _Node v12 or a later version_
  - _Python v3 or a later version_
  - An AWS account with described permisions in lambda-executor-policy.json file.

### Deployment 🔧

```sh
$ npm install --silent --no-progress -g serverless
# Test the serverless installation
$ sls --version
# Set your AWS credentials an set a profile name for $APP_PROFILE, in my case I called it as 'deploy'. You could use --overwrite to update an existing profile.
$ sls config credentials --provider aws --key $AWS_ACCESS_KEY --secret $AWS_SECRET_ACCESS_KEY --profile $APP_PROFILE
###
# You can run the command 'source ./env.sh' to load your own environment variables and enable pl-package/pl-deploy/pl-remove functions. If you had edit this file, then you should load the environment changes again.
# You also can replace them here directly:
###
# Build the stack for a custom stage/region/profile
$ sls package --package ./target/$APP_STAGE --stage $APP_STAGE -v -r $APP_REGION --aws-profile $APP_PROFILE
# Deploy the stack for a custom stage/region/profile
$ sls deploy --package ./target/$APP_STAGE --stage $APP_STAGE -v -r $APP_REGION --aws-profile $APP_PROFILE
# To remove the stack for a custom stage/region/profile
$ sls remove --package ./target/$APP_STAGE --stage $APP_STAGE -v -r $APP_REGION --aws-profile $APP_PROFILE
```
### Development ⌨️

Open your favorite Terminal and run these commands.

```sh
$ python3 -m venv .env
$ source .env/bin/activate
(.env)$ pip3 install boto3
# List source files
(.env)$ ls -la ./functions/otp
```

## Testing ⚙️

PasswordLessApp is built with python, we need to go to the virtual environment to have a local context in order to install current/future dependencies.

### Unit tests 🔩

File ./functions/otp/test/test_unit.py: constains all unit tests for sign-up/otp requests.

```
$ source .env/bin/activate
(.env)$ python3 -m unittest -v functions.otp.test.test_unit
```

### Manual / integration tests 🔩
Deploy the stack in an specific environment.
Use the file: 'openapi/schema.yml' to build an API client in postman.
Replace servers.url property with the generated url of API gateway.

```
$ source .env/bin/activate
(.env)$ python3 -m unittest -v functions.otp.test.test_unit
```

## Building with 🛠️

* [Serverless](https://www.serverless.com/) - Allows us to build and run applications and services without thinking about servers
* [Python](https://www.python.org/) - Just the easiest programming language
* [AWS](https://aws.amazon.com/) -  Offers cloud computing web services.


## Authors ✒️
* **Pablo Atoche** - *Initial work* - [PalituxD](https://github.com/PalituxD)

## License 📄

* Apache license 2.0