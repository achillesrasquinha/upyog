import os

import httpx

from upyog.util.environ import getenv
from upyog.util.string  import get_random_str
from upyog.util.eject   import ejectable
from upyog.api.base     import AsyncBaseClient, BaseClient

AWS_DEFAULT = {
    "service": "execute-api",
     "region": "us-west-2"
}

def is_lambda():
    return os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None

@ejectable(deps = ["getenv"])
def awsgetenv(*args, **kwargs):
    """
        Get AWS environment variables.

        Example
            >>> getenv("PROFILE")
            "default"
    """
    kwargs["prefix"] = "AWS"
    return getenv(*args, **kwargs)

@ejectable(deps = ["get_random_str"])
def get_aws_credentials(role = None, profile = None):
    import os.path as osp
    from configparser import ConfigParser
    import boto3

    if role:
        session = boto3.Session()
        sts     = session.client("sts")

        session_name = f"RoleSession-{get_random_str()}"

        assume_role  = sts.assume_role(
            RoleArn  = role,
            RoleSessionName = session_name,
        )

        assume_role_creds = assume_role["Credentials"]
        creds = {
            "aws_access_key_id": assume_role_creds["AccessKeyId"],
            "aws_secret_access_key": assume_role_creds["SecretAccessKey"],
            "aws_session_token": assume_role_creds["SessionToken"]
        }

        return { role: creds }
    else:
        path   = osp.join(osp.expanduser("~"), ".aws", "credentials")
        parser = ConfigParser()
        parser.read(path)

        creds  = { section: dict(parser[section])
            for section in parser.sections() }

        if "default" not in creds:
            kwargs = { "default": None }
            aws_access_key_id     = awsgetenv("ACCESS_KEY_ID", **kwargs)
            aws_secret_access_key = awsgetenv("SECRET_ACCESS_KEY", **kwargs)

            if aws_access_key_id and aws_secret_access_key:
                creds["default"] = {
                    "aws_access_key_id": aws_access_key_id,
                    "aws_secret_access_key": aws_secret_access_key,
                }

                aws_session_token = awsgetenv("SESSION_TOKEN", **kwargs)

                if aws_session_token:
                    creds["default"]["aws_session_token"] = aws_session_token
            else:
                session     = boto3.Session()
                credentials = session.get_credentials()

                creds["default"] = {
                    "aws_access_key_id": credentials.access_key,
                    "aws_secret_access_key": credentials.secret_key,
                    "aws_session_token": credentials.token,
                }

        if profile:
            assert profile in creds
            creds = creds[profile]

    return creds

@ejectable(imports = ["httpx"], globals_ = { "AWS_DEFAULT": AWS_DEFAULT })
class AWSSigV4Auth(httpx.Auth):
    requires_request_body = True

    def __init__(self,
        access_key,
        secret_key,
        token   = None,
        service = None,
        region  = None
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token      = token

        self.service    = service or AWS_DEFAULT["service"]
        self.region     = region  or AWS_DEFAULT["region"]

    def auth_flow(self, r):
        from botocore.awsrequest  import AWSRequest
        from botocore.auth        import SigV4Auth
        from botocore.credentials import Credentials

        method  = r.method
        
        headers = { "Content-Type": "application/json" }

        aws_request = AWSRequest(
            method  = method,
            url     = str(r.url),
            headers = dict(headers),
            data    = r.content
        )
        credentials = Credentials(
            access_key = self.access_key,
            secret_key = self.secret_key,
            token      = self.token
        )
        aws_sigv4_auth = SigV4Auth(credentials, self.service, self.region)
        aws_sigv4_auth.add_auth(aws_request)

        r.headers.update(dict(aws_request.headers))

        yield r

@ejectable(deps = ["AsyncBaseClient", "AWSSigV4Auth", "awsgetenv", "get_aws_credentials"], globals_ = { "AWS_DEFAULT": AWS_DEFAULT })
class AWSClient(AsyncBaseClient):
    """
        AWSClient: AWS Client.

        Args:
            profile: AWS Profile.
            role: AWS Role.
            region: AWS Region.
            service: AWS Service.
    """
    def __init__(self,
        profile = None,
        role    = None,
        region  = None,
        service = None,
        *args, **kwargs
    ):
        super_   = super(AWSClient, self)
        super_.__init__(*args, **kwargs)

        role     = getenv("AWS_CLIENT_ROLE", default = role)

        if not self.auth:
            profile = str(profile or awsgetenv("PROFILE", default = "default"))
            aws_credentials = get_aws_credentials(role = role)

            if role:
                profile = role

            if profile not in aws_credentials:
                raise ValueError(f"Profile '{profile}' not found in AWS credentials.")
            
            region  = region or getattr(self, "region", AWS_DEFAULT["region"])
            assert region, "region is required."

            service = getattr(self, "service", service or AWS_DEFAULT["service"])
            assert service, "service is required."

            credentials = aws_credentials[profile]

            self.auth   = AWSSigV4Auth(
                access_key = credentials["aws_access_key_id"],
                secret_key = credentials["aws_secret_access_key"],
                token      = credentials.get("aws_session_token", None),
                service    = service,
                region     = region
            )