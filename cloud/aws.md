# AWS

### Data Collection with Storage

* External block storage basically acts as a Cloud USB drive allowing the addition of storage to the cloud system.
* If you provision more block storage, it will appear automatically in Windows
* In Linux we can create a mount point&#x20;

```
sudo fdisk -l 
sudo mkdir /mnt/sdh1 && mount /dev/sdh1 /mnt/sdh1
#replace sdh1 with the actual device 
```

### Collection of AWS Storage

```
aws ec2 describe-volume | jq -r '.Volumes[] | select (.AvailabilityZone | contains("us-east-1") ) | .VolumeId'
#output will return a volume id
aws ec2 attatch-volume --volume-id vol-VOLUME_NUMBER --instance-id INSTANCE_ID --device /dev/sdh
```

### Cloud Logging&#x20;

* When in possession of Cloud logs, manual analysis is extremely difficult, use automated tools

```
s3logparse.py useragent USER_AGENT_HERE
#search for a specific user-agent
```

* Examine the logs in a web server like view&#x20;

```
zcat /path/to/logs/* > log_flow.txt
export LOG_TEXT=/home/logs/log_flow.txt
npm run build-graph 
npm run client
#will start on localhost:8080
```

### Revoking Cloud Keys

* Most compromises have to do with an unauthorized user gaining access to a cloud key&#x20;
* AWS IAM search by username or Key ID by clicking IAM --> Users

```
Set-ADAccountPassword -Identity jack -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "My_Password" -Force)
Set-ADAccountPassword -Identity jack -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "My_Password" -Force)
```

* For Azure AD make sure to reset the password twice!!!
