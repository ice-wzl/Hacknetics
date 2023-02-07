# Rubeus to Ccache

### Method 1

* Normally Rubeus outputs the tickets in Base64-encoded .kirbi format, .kirbi being the type of file commonly used by [Mimikatz](https://github.com/gentilkiwi/mimikatz).
* Impacket tools use the .ccache file format to represent Kerberos tickets
* Convert tickets with the impacket built in converter (still need to convert Rubeus output from base64 to .kirbi before using `ticketConverter.py`

```
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($base64RubeusTGT))
```

* [https://github.com/fortra/impacket/blob/master/examples/ticketConverter.py](https://github.com/fortra/impacket/blob/master/examples/ticketConverter.py)

### Method 2

* **Rubeus to Ccache**
* Pass the script the base64 blob and you will get a ticket in both formats&#x20;
* Ensure you export the proper env variable before trying to convert&#x20;

```
export KRB5CCNAME=shiny_new_ticket.ccache
```

* Then you can use most Impacket tools like this:&#x20;
* `wmiexec.py domain/user@192.168.1.1 -k -no-pass`, where the `-k` flag indicates the use of Kerberos tickets for authentication.
* Tool: [https://github.com/SolomonSklash/RubeusToCcache](https://github.com/SolomonSklash/RubeusToCcache)
