from argparse import ArgumentParser

from utils.credentials import Credentials
from utils.dns_manager import DnsManager

""" Parses arguments provided
Attributes:
    :runTime: which environment script is running CI or LOCAL: If local is set mfa_token to true
    :tokenCode: mfa token code when running locally
"""
parser = ArgumentParser(description='Config Renderer')
parser.add_argument('--runTime', choices=['local', 'ci'], default=None)
parser.add_argument('--tokenCode', type=str, default=None)
parser.add_argument('--awsRegion', type=str, default='eu-west-2')

args = parser.parse_args()

run_time = args.runTime
token_code = args.tokenCode
region = args.awsRegion

if run_time is not None:
    if run_time == 'local':
        assumed_role = Credentials(mfa_auth=True, token_code=token_code)
        assumed_role.get_temp_credentials_mfa()
    elif run_time == 'ci':
        assumed_role = Credentials()
        assumed_role.get_temp_credentials()
else:
    print('Please provide a valid runtime argument -> ci or local')
    exit()

# Manage Records
dns_record = DnsManager(assumed_role.temp_creds)

dns_record.manage_cname_record(
    'Z2QF2SEPISTMNB',
    'mis-ldap.dev.delius-core.probation.hmpps.dsd.io',
    'ip-10-161-20-224.eu-west-2.compute.internal'
)
