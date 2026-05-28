# SSH

- TCP 22, OpenSSH is the most common implementation
- Six authentication methods: password, public-key, host-based, keyboard, challenge-response, GSSAPI

## Config

- Default config: `/etc/ssh/sshd_config`

```
cat /etc/ssh/sshd_config | grep -v "#" | sed -r '/^\s*$/d'
```

## Dangerous Settings

| Setting | Description |
|---|---|
| PasswordAuthentication yes | Password auth enabled |
| PermitEmptyPasswords yes | Empty passwords allowed |
| PermitRootLogin yes | Root login allowed |
| Protocol 1 | Outdated encryption standard |
| X11Forwarding yes | GUI forwarding |
| AllowTcpForwarding yes | Port forwarding |
| PermitTunnel | Tunneling |
| DebianBanner yes | Shows specific OS banner |

## SSH-Audit

```
git clone https://github.com/jtesta/ssh-audit.git && cd ssh-audit
./ssh-audit.py 10.129.14.132
```

## Change Auth Method

```
ssh -v cry0l1t3@10.129.14.132
ssh -v cry0l1t3@10.129.14.132 -o PreferredAuthentications=password
```

## Hostkey Algorithm Fix

- No matching `hostkey` error:

```
no matching host key type found. Their offer: ssh-rsa,ssh-dss
```

- Append to `/etc/ssh/ssh_config`:

```
HostKeyAlgorithms +ssh-rsa,ssh-dss
```

- If the error references a different algorithm, substitute accordingly

## Forced Command Keys and Legacy SCP

If a recovered private key authenticates but the server closes the shell with a forced command, inspect the matching `authorized_keys` entry. A restricted key may look like:

```text
no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty,command="/home/USER/scp_wrapper.sh" ssh-rsa ...
```
scp error message too long
```text
scp: Received message too long
scp: Ensure the remote shell produces no output for non-interactive sessions.
```
Fix this error with scp legacy mode `-O`
```bash
scp -O -i id_rsa ~/.ssh/id_rsa.pub USER@TARGET:/home/USER/.ssh/authorized_keys
ssh USER@TARGET -i ~/.ssh/id_rsa
```

The `-O` flag forces the legacy SCP protocol instead of SFTP, which can be needed when the remote wrapper expects `scp` and otherwise returns:


