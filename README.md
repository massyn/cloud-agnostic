# cloud-agnostic
Generic library to abstract common cloud API calls

## Functions

|**Function**|**What it does**|**Local**|**AWS**|**Azure**|**GCP**|
|--|--|--|--|--|--|
|`alert`|Sends a message|![slack](https://img.shields.io/badge/slack-00B050)|![SNS](https://img.shields.io/badge/sns-00B050)|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|
|`list`|List the contents of a storage account|local disk|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|
|`read`|Reads a blob to storage|local disk|S3 bucket / key|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|
|`write`|Writes a blob to storage|![local disk](https://img.shields.io/badge/local%20disk-00B050)|![s3 bucket](https://img.shields.io/badge/s3-00B050)|![no](https://img.shields.io/badge/no-C00000)|![gs](https://img.shields.io/badge/gs-00B050)|
|`secret`|Retrieves a secret|![no](https://img.shields.io/badge/no-C00000)|Secrets Manager|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|


## Installation

```bash
$ git clone https://github.com/massyn/cloud-agnostic
$ pip install -r cloud-agnostic/requirements.txt
```


## Examples

### Write a file

***AWS S3**

```python
from cloudagnostic import CloudAgnostic
CA = CloudAgnostic()

CA.write('s3://bucket/key.txt','hello world')
```

***Google storage**

```python
from cloudagnostic import CloudAgnostic
CA = CloudAgnostic()

CA.write('gs://bucket/key.txt','hello world')
```

**Local file**

```python
from cloudagnostic import CloudAgnostic
CA = CloudAgnostic()

CA.write('/tmp/key.txt','hello world')
```

### Send an alert

**Slack**

```python
from cloudagnostic import CloudAgnostic
CA = CloudAgnostic(alert = 'https://hooks.slack.com/services/.....')
CA.alert('INFO','hello world')
```

**AWS SNS**

```python
from cloudagnostic import CloudAgnostic
CA = CloudAgnostic(alert = 'arn:aws:sns:ap-southeast-2:000000000000:mytopic')
CA.alert('INFO','hello world')
```


