# ssh

* No matching `hostkey` error

```
no matching host key type found. Their offer: ssh-rsa,ssh-dss #error message
```

* Edit your `/etc/ssh/ssh_config` file and append this line&#x20;

```
HostKeyAlgorithms +ssh-rsa,ssh-dss
```

* If the error is in regard to a different algorithm, make sure to sub out `ssh-rsa`&#x20;
