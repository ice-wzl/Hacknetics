# BaGet

BaGet is a lightweight NuGet and symbol server. It commonly appears on IIS/.NET targets and may expose package upload and NuGet service-index endpoints.

## Discovery

```bash
curl -I http://TARGET/
curl http://TARGET/v3/index.json
curl http://TARGET/upload
nuclei -u http://TARGET/ -rl 10 -c 10
```

Useful indicators:

```text
http-title: BaGet
Microsoft-IIS/10.0
HEAD GET POST PUT DELETE TRACE OPTIONS CONNECT PATCH
```

Documentation:

```text
https://loic-sharma.github.io/BaGet/
```

Nuclei template:

```text
https://github.com/projectdiscovery/nuclei-templates/blob/main/http/misconfiguration/baget-exposure.yaml
```
