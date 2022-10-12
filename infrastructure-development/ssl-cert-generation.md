# SSL Cert Generation

* One of the easiest ways to generate SSL certs is with `certbot` which leverages `letsencrypt`

### Generate your Certs

* `certbot certonly --manual -d mydomain.com`

### SSL Overview&#x20;

* This command will generate four files in:

```
/etc/letsencrypt/live/mydomain.com
```

#### privkey,pem

* This is the key file, a.k.a. your private key&#x20;
* Sometimes also named as `cert.key` or `mydomain.com.key`

#### fullchain.pem

* This is your `crt` file
* Also sometimes named `mydomain.crt`

#### bundle.pem

* Contains all the certificates&#x20;
* Would be created with&#x20;

`cat fullchain.pem privkey.pem > bundle.pem`

#### cert.pem

* This file contains only your certificate
* Can only be used by itself if the browser already has the certificate which signed it
* May work in testing, don't use in production

#### chain.pem

* Intermediary signed authority, signed by the root authority&#x20;
* All browsers are guaranteed to have in their pre-built cache.

### Checking Certs&#x20;

* You can inspect the cert like this:

```
openssl x509 -in cert.pem -text -noout
```

*   **Check a Certificate Signing Request (CSR)**

    ```
    openssl req -text -noout -verify -in CSR.csr
    ```
*   **Check a private key**

    ```
    openssl rsa -in privateKey.key -check
    ```
*   **Check a certificate**

    ```
    openssl x509 -in certificate.crt -text -noout
    ```
*   **Check a PKCS#12 file (.pfx or .p12)**

    ```
    openssl pkcs12 -info -in keyStore.p12
    ```
