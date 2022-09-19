# Recon and Enumeration

##

## NFS

* If there is a nfs port open on the attack machine try to find the name of the share

```
showmount -e [target ip]
```

* This should return a path like seen below

```
/srv/hermes*
```

* Make a directory on your box to mount to the target share

```
mkdir hack
```

* Mount to the target

```
sudo mount -t nfs [target ip]:/srv/hermes ~/hack
```

##



##

##

## Stuck

* https://book.hacktricks.xyz/
* https://guide.offsecnewbie.com/
