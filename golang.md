# Golang

### Remove Debugging Information

```
go build -ldflags "-w -s"
```

* that will remove the debugging information and shrink the binary size by \~30%.

### Cross Compilation&#x20;

* `GOOS` -> Operating system
* `GOARCH` -> Architecture&#x20;

```
GOOS="linux" GOARCH="amd64" go build hello.go
```
