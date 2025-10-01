# torsocks

* On modern kali the shared object is often in a non default location&#x20;

```
sudo ln -sf /usr/lib/x86_64-linux-gnu/torsocks/libtorsocks.so \                                                     
            /usr/lib/x86_64-linux-gnu/libtorsocks.so
sudo ldconfig
```

* spawn a shell

```
torsocks --shell
curl http://ipinfo.io
```
