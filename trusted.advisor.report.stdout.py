#!/usr/bin/python
'''
Gets data from AWS Trusted Advisor and prints non-ok checks.
'''
import boto3
conn = boto3.client('support', region_name='us-east-1')


class bcolors:
    UNK = '\033[94m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDCOLOR = '\033[0m'


checks = conn.describe_trusted_advisor_checks(language='en')

checksCount = 1
for check in checks['checks']:
    status = conn.describe_trusted_advisor_check_summaries(checkIds=[check['id']])['summaries'][0]['status']
    if status != 'ok':
        color = bcolors.WARNING if status == 'warning' else bcolors.ERROR if status == 'error' else bcolors.UNK
        print(checksCount, '\tName: ' + check['name'])
        print('\tCategory: ' + check['category'])
        print('\tID : ' + check['id'])
        print('\tStatus: ', color + conn.describe_trusted_advisor_check_summaries(checkIds=[check['id']])['summaries'][0]['status'] + bcolors.ENDCOLOR)
        print()
        print('\tFlagged Resources: ')
        print('\t\tSlNo.\tStatus', '\t\t' if status == 'warning' else '\t', [str(md) for md in check['metadata']])
        print('\t\t---------------------------------------------------------')
        try:
            flaggedResources = conn.describe_trusted_advisor_check_result(checkId=check['id'], language='en')['result']['flaggedResources']
        except KeyError:
            print('\t\tNo flagged resources')
            flaggedResources = {}
        flaggedResourcesCount = 1
        for resource in flaggedResources:
            if resource['status'] != 'ok':
                color = bcolors.WARNING if status == 'warning' else bcolors.ERROR if status == 'error' else bcolors.UNK
                try:
                    print('\t\t', str(flaggedResourcesCount), '\t', color + str(resource['status']), '\t', [str(item) for item in resource['metadata']], bcolors.ENDCOLOR)
                except:
                    print('\t\t', str(flaggedResourcesCount), '\t', color + str(resource['status']), '\t')
                flaggedResourcesCount += 1
        print
    checksCount += 1
