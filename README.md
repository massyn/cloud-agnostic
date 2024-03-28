# cloud-agnostic
Generic library to abstract common cloud API calls

## Installation

```bash
$ git clone https://github.com/massyn/cloud-agnostic
$ pip install -r cloud-agnostic/requirements.txt
```

## Examples

### Send an alert

**Slack**

```python
CA = CloudAgnostic(alert = 'https://hooks.slack.com/services/.....')
CA.alert('INFO','hello world')
```

**AWS SNS**

```python
CA = CloudAgnostic(alert = 'arn:aws:sns:ap-southeast-2:000000000000:mytopic')
CA.alert('INFO','hello world')
```

## On the todo list

* Read a file from storage (local, AWS S3, Azure Storage, etc)
* Read a secret (AWS Secrets Manager, Azure Key Vault)

## Functions

|**Function**|**What it does**|**Local**|**AWS**|
|--|--|--|--|
|`alert`|Sends a message|Slack Webhook|SNS Topic|
