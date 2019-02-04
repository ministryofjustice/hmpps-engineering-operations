import json
import copy
import boto3
from dateutil import parser

from utils.config import Base_Config
from utils.helper_utils import HelperUtils


class DnsManager(Base_Config):
    def __init__(self, temp_creds):
        super().__init__()
        self.temp_creds = temp_creds
        self.client = boto3.client(
            'route53',
            aws_access_key_id=self.temp_creds['access_key'],
            aws_secret_access_key=self.temp_creds['secret_key'],
            aws_session_token=self.temp_creds['session_token'])

    def manage_cname_record(self, zone, record_name, target_record, action='UPSERT'):
        try:
            response = self.client.change_resource_record_sets(
                HostedZoneId=zone,
                ChangeBatch={
                    'Comment': 'asg cname record added by python',
                    'Changes': [
                        {
                            'Action': action,
                            'ResourceRecordSet': {
                                'Name': record_name,
                                'Type': 'CNAME',
                                'TTL': 300,
                                'ResourceRecords': [
                                    {
                                        'Value': target_record
                                    },
                                ],
                            },
                        }
                    ]
                }
            )
            response_code = response['ResponseMetadata']['HTTPStatusCode']
            if response_code <= 299:
                return True
            if response_code >= 400:
                return False
        except Exception as e:
            print(e)
            return False
