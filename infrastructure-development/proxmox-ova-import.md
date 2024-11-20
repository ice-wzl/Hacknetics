# Proxmox OVA Import

* scp ova to proxmox&#x20;
* untar the ova

```
qmimport <vmid> <ovf> local-lvm 
qmimport ovf 101 centos.ovf local-lvm 
```
