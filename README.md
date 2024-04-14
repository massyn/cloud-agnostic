# cloud-agnostic
Generic library to abstract common cloud API calls

## Overview

### What is Cloud Agnostic?

Everything was fine when I purely developed on AWS, but then my clients started asking to move code to other platforms.  Many of my Python scripts had hard-coded `boto3` references, making the code impossible to run on another platform.  The use of `docker` containers however makes the transporting of software in a container much easier.  The challenge however is that the business logic part of the code still needed to interact with the cloud backend in some shape or form.  That's where CloudAgnostic comes in.

CloudAgnostic creates an abstraction layer between the Cloud SDK tools, and your software, thus negating the need for you to write code for AWS, GCP and Azure.  You simply make the call, and provided the parameters have been provided, CloudAgnostic will make the call for you.

## But there's hardly anything in it?!!

This is a brand new project.  As I need things, I add them in.

* Found a bug?  Raise an [issue](https://github.com/massyn/cloud-agnostic/issues/new)
* Want to add a new feature?  Submit a PR!

## Keeping it simple

Each cloud platform has their own nuances in how they operate.  Not every possible scenario could always be accounted for, but we'll try.  The goal will be to "keep it simple".  Instead of building a function that can do everything, we'll build a function that does just one thing.  For example, you want to write a blob to a storage account, use the `write` function.  It takes just two parameters, the `target`, and the `body`.  Your software need to keep some variable somewhere to say what the target should be (ie `s3://bucket/key.txt`).  If you port your software to another platform, you just have to account for this variable.  Anywhere in your code where you call `CA.write(target,body)`, it will write to that storage account, regardless of what the platform is.

## This is too complicated.  Just use boto3!

I believe there will be use-cases where you may have to use the vendor SDK instead of CloudAgnostic simply because your own requirements may be more complex than what CloudAgnostic can offer you.

If however you do find an opportunity to expand the usage of CloudAgnostic to support your particular use case, you can always create a Pull Request and include your code to the project, or head on over to the [discussion](https://github.com/massyn/cloud-agnostic/discussions/categories/ideas) forum to share your ideas.

## Functions

|**Function**|**What it does**|**Local**|**AWS**|**Azure**|**GCP**|
|--|--|--|--|--|--|
|`alert`|Sends a message|![slack](https://img.shields.io/badge/slack-00B050)|![SNS](https://img.shields.io/badge/sns-00B050)|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|
|`list`|List the contents of a storage account|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|
|`read`|Reads a blob to storage|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|
|`write`|Writes a blob to storage|![local disk](https://img.shields.io/badge/local%20disk-00B050)|![s3 bucket](https://img.shields.io/badge/s3-00B050)|![no](https://img.shields.io/badge/no-C00000)|![gs](https://img.shields.io/badge/gs-00B050)|
|`secret`|Retrieves a secret|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|![no](https://img.shields.io/badge/no-C00000)|


## Installation

```bash
$ git clone https://github.com/massyn/cloud-agnostic
$ pip install -r cloud-agnostic/requirements.txt
```


## Examples

### Write a file

**AWS S3**

```python
from cloudagnostic import CloudAgnostic
CA = CloudAgnostic()

CA.write('s3://bucket/key.txt','hello world')
```

**Google storage**

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


