# buffer-overflows

* For generating a bytearray

{% file src="../.gitbook/assets/bad-chars.py" %}

* Used to fuzz applicaitons remotely.  Will send increasingly large sequence of bytes in an attempt to crash the service

{% file src="../.gitbook/assets/fuzzer.py" %}

* Used to exploit the remote service with a buffer overflow

{% file src="../.gitbook/assets/exploit.py" %}
