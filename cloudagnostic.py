import requests
import json
import boto3
import botocore

class CloudAgnostic:
    def __init__(self,**KW):
        print('CloudAgnostic')
        self.parameters = {}

        # -- define alert parameters
        self.parameters['alert'] = KW.get('alert')
    
    def alert(self,sev,message,subject = None):
        print(f"Sending {sev} alert : {message}")
        if subject is None:
            subject = f"{sev} alert"
        # == determine what the platform type is
        if self.parameters['alert'].startswith('https://hooks.slack.com'):
            print(" - slack")
            icons = {
                'INFO' : ':information_source:',
                'WARNING' : ':warning:',
                'ERROR' : ':x:',
                'SUCCESS' : ':white_check_mark:',
                'FATAL' : ':skull_and_crossbones:'
            }

            i = icons.get(sev,icons['INFO'])

            req = requests.post(self.parameters['alert'],data=json.dumps({ 'text' : f"{i} {message}" }).encode('utf-8'),headers = {   
                'Content-Type': 'application/json',
                'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
            }, timeout=30)
            if req.status_code != 200:
                print("ERROR - Unable to send a slack message")
        elif self.parameters['alert'].startswith('arn:aws:sns:'):
            print('- AWS SNS')
            try:
                boto3.client('sns').publish(TopicArn=self.parameters['alert'],Message = message, Subject = subject)
            except botocore.exceptions.ClientError as error:
                print(f"ERROR - sns.publish - {error.response['Error']['Code']}")

        else:
            print('ERROR - Unable to determine what alert type this is')

        if sev == 'FATAL':
            exit(1)