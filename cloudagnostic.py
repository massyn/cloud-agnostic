import json
import requests
import boto3
from google.cloud import storage

class CloudAgnostic:
    def __init__(self,**KW):
        self.log('INFO','Initializing...')
        self.parameters = {}

        self.debug = KW.get('debug',False)

        # -- define alert parameters
        self.parameters['alert'] = KW.get('alert')
    
    def log(self,sev,msg):
        if sev == 'DEBUG' and not self.debug:
            return
        print(f"[CloudAgnostic] {sev} : {msg}")
        if sev == 'FATAL':
            exit(1)

    def alert(self,sev,message,subject = None):
        self.log("INFO",f"alert ({sev}) {message}")
        if subject is None:
            subject = f"{sev} alert"
        # == determine what the platform type is
        if self.parameters['alert'].startswith('https://hooks.slack.com'):
            self.log("INFO","Alert target = slack")
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
                self.log("ERROR","Unable to send a slack message")
        elif self.parameters['alert'].startswith('arn:aws:sns:'):
            self.log("INFO","Alert target = aws sns")
            try:
                boto3.client('sns').publish(TopicArn=self.parameters['alert'],Message = message, Subject = subject)
            except Exception as err:
                self.log("ERROR",f"sns.publish - {err}")
        else:
            self.log("ERROR","Unable to determine what alert type this is")

    def write(self,target,body):
        self.log("DEBUG","- function = write")
        self.log("DEBUG",f"- target   = {target}")

        if target.lower().startswith('s3://'):
            self.log("INFO",f"Writing to s3 {target}")
            bucket = target.split('/')[2]
            key = '/'.join(target.split('/')[3:])
            self.log("DEBUG",f"- S3 bucket = {bucket}")
            self.log("DEBUG",f"- S3 key    = {key}")
            try:
                boto3.resource('s3').Bucket(bucket).put_object(
                    ACL         = 'bucket-owner-full-control',
                    ContentType = 'application/json',
                    Key         = key,
                    Body        = body
                )
                self.log("SUCCESS",f"Wrote a total of {len(body)} bytes.")
            except Exception as err:
                self.log("ERROR",f"s3.put_object - {err}")
        elif target.lower().startswith('gs://'):
            self.log("INFO",f"Writing to gs {target}")
            bucket = target.split('/')[2]
            key = '/'.join(target.split('/')[3:])
            self.log("DEBUG",f"- GS bucket = {bucket}")
            self.log("DEBUG",f"- GS key    = {key}")
            try:
                client = storage.Client()
                bucket = client.get_bucket(bucket)
                blob = bucket.blob(key)
                blob.upload_from_string(body)
                self.log("SUCCESS",f"Wrote a total of {len(body)} bytes.")
            except Exception as err:
                self.log("ERROR",f"storage.upload_from_string - {err}")
        else:
            # -- defaults to disk
            self.log("INFO",f"Writing to local path {target}")
            try:
                with open(target,'wt',encoding='UTF-8') as w:
                    w.write(body)
                self.log("SUCCESS",f"Wrote a total of {len(body)} bytes.")
            except Exception as err:
                self.log("ERROR",f"Unable to write to local path {target} - {err}")

    def read(self,target):
        self.log("DEBUG","- function = read")
        self.log("DEBUG",f"- target   = {target}")

        if target.lower().startswith('s3://'):
            self.log("INFO",f"Reading from s3 {target}")
            bucket = target.split('/')[2]
            key = '/'.join(target.split('/')[3:])
            self.log("DEBUG",f"- S3 bucket = {bucket}")
            self.log("DEBUG",f"- S3 key    = {key}")
            try:
                body = boto3.client('s3').get_object(bucket, Key=key)['Body'].read().decode('utf-8')

                self.log("SUCCESS",f"Read a total of {len(body)} bytes.")
                return body
            except Exception as err:
                self.log("ERROR",f"Unable to read from s3 {target} - {err}")
                return False
        else:
            # -- defaults to disk
            self.log("INFO",f"Reading from local path {target}")
            try:
                with open(target,'rt') as q:
                    body = q.read()
                    self.log("SUCCESS",f"Read a total of {len(body)} bytes.")
                    return body
            except Exception as err:
                self.log("ERROR",f"Unable to read from local file {target} - {err}")
                return False

        
