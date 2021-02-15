import os


def dynamodb():
    if os.environ.get('IS_OFFLINE'):
        return {
            'region': 'localhost',
            'host': 'http://localhost:8000'
        }
    else:
        return {
            'region': os.environ.get('DYNAMODB_REGION'),
            'host': f"https://dynamodb.{os.environ.get('DYNAMODB_REGION')}.amazonaws.com"
        }
