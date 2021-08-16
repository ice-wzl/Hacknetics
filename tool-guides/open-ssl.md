## Asymmetric File Encrypt and Decrypt
- Let’s generate some public/private keys and encrypt/decrypt a message! 

- To generate a private key we use the following command (8912 creates the key 8912 bits long):
````
openssl genrsa -aes256 -out private.key 8912
````
- To generate a public key we use our previously generated private key:
````
openssl rsa -in private.key -pubout -out public.key
````
- Lets now encrypt a file (plaintext.txt) using our public key:
````
openssl rsautl -encrypt -pubin -inkey public.key -in plaintext.txt -out encrypted.txt
````
- Now, if we use our private key, we can decrypt the file and get the original message:
````
openssl rsautl -decrypt -inkey private.key -in encrypted.txt -out plaintext.txt
````
