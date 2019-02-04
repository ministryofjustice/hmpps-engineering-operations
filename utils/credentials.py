import boto3
import os


class Credentials:
    """ Class provides Credentials for AWS role assume"""

    def __init__(self, mfa_auth=False, token_code=None):
        """ This methods sets initial values
        :Arguments:
            mfa_auth: controls which method is used to get temp credentials. default = False
            token_code: mfa token code. default = None
        """
        self.temp_creds = {}
        self.parameters = {}
        self.iam_role = os.getenv('TERRAGRUNT_IAM_ROLE')
        self.mfa_auth = mfa_auth
        self.mfa_arn = os.getenv('AWS_MFA_ARN', '')
        self.token_code = token_code

    def get_temp_credentials_mfa(self):
        """ This methods get temp creds from AWS using sts when using mfa"""
        client = boto3.client('sts')
        duration_seconds = 3600
        try:
            response = client.assume_role(
                RoleArn=self.iam_role,
                RoleSessionName='render',
                SerialNumber=self.mfa_arn,
                DurationSeconds=duration_seconds,
                TokenCode=self.token_code
            )
            temp_creds = dict(
                access_key=response['Credentials']['AccessKeyId'],
                secret_key=response['Credentials']['SecretAccessKey'],
                session_token=response['Credentials']['SessionToken']
            )
            self.temp_creds = temp_creds
            return True
        except Exception as e:
            print(e)
            return False

    def get_temp_credentials(self):
        """ This methods get temp creds from AWS using sts non mfa approach for CI"""
        client = boto3.client('sts')
        duration_seconds = 900
        try:
            response = client.assume_role(
                RoleArn=self.iam_role,
                RoleSessionName='render',
                DurationSeconds=duration_seconds
            )
            temp_creds = dict(
                access_key=response['Credentials']['AccessKeyId'],
                secret_key=response['Credentials']['SecretAccessKey'],
                session_token=response['Credentials']['SessionToken']
            )
            self.temp_creds = temp_creds
            return True
        except Exception as e:
            print(e)
            return False

    def get_auth(self):
        """ This methods get calls local methods depending on if the mfa_auth flag is set true or false"""
        if self.mfa_auth:
            get_creds = self.get_temp_credentials_mfa()
        else:
            get_creds = self.get_temp_credentials()

        if get_creds:
            return True
        else:
            return False
