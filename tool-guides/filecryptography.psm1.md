# FileCryptography.psm1

### Unprotect files&#x20;

* File will be encrypted on Windows&#x20;
* The key will look like below

```
01000000d08c9ddf0115d1118c7a00c04fc297eb01000000615043d935095745afc9a3eeac1d3c250000000002000000000003660000c0000000100000005634044f9a507cbde0a83d50c9c447120000000004800000a0000000100000002dabe6e27356685d05a85fd0fd69b104600000003a6975c935a91b5503750cea11202a524740d3d52700d92038f5378e47a17b392f30f6ceb7d6553e8ef35271df92da21ca0d08aae9725fc93e74818f9d1b499491aba2892510a0ab7f69352364db2e4cea3035bae97ef9dc3d5d9255f41ec6b614000000a769f750b39ecabc8475eabca9d73ee63b3f24ec
```

### Unprotect the file&#x20;

```
$key = gc key.txt | convertto-securestring -force
import-module .\FileCryptography.psm1
unprotect-file '.\secret.txt.AES' -Algorithm AES -Key $key
type secret.txt
```
