import os

def is_lambda():
    return os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None