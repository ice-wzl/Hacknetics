# Golang

### Remove Debugging Information

```
go build -ldflags "-w -s"
```

* that will remove the debugging information and shrink the binary size by \~30%.
