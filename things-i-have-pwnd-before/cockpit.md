# Cockpit

Cockpit is a Linux web administration console. It usually authenticates against local system accounts, so web app credentials are worth trying here after SQLi, LFI, config leaks, or password dashboard access.

## Discovery

```bash
nmap -sC -sV TARGET -p 9090
# 9090/tcp open  http  Cockpit web service
# http-title: Did not follow redirect to https://TARGET:9090/
```

Browse to:

```bash
https://TARGET:9090/
```

The login page may disclose the OS version after loading, e.g. Ubuntu 20.04.x.

## Credential Reuse

Try credentials recovered from the web app against Cockpit. Do not only test the web application's admin user; test named users too because Cockpit wants valid Linux accounts.

```text
root:root
USER:WEB_APP_PASSWORD
```

If a user logs in successfully, check whether the terminal is enabled:

```text
https://TARGET:9090/system/terminal
```

## Post Login

From the Cockpit terminal, treat it like a normal local shell:

```bash
id
hostname
cat /etc/os-release
sudo -l
```
