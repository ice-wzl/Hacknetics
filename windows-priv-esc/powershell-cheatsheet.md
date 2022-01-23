# Powershell
### Creating Objects From Previous cmdlets
![Zdxicjj](https://user-images.githubusercontent.com/75596877/150692716-9d937291-9a6b-4e29-84b0-6a812eb31460.png)
````
Get-ChildItem | Select-Object -Property Mode, Name
````
- You can also use the following flags to select particular information:

- `first` - gets the first x object
- `last` - gets the last x object
- `unique` - shows the unique objects
- `skip` - skips x objects
### Checking the Stopped Processes
````
Get-Service | Where-Object -Property Status -eq Stopped
````
### Sort Object
````
Get-ChildItem | Sort-Object
````
# Find File Recursive
````
Get-Childitem –Path C:\ -Recurse -Force -ErrorAction SilentlyContinue | findstr /i "interesting-file.txt"
Get-ChildItem -Path C:\ -Include *.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue
````
- ![image](https://user-images.githubusercontent.com/75596877/150693932-501b2d5c-3695-4a41-8662-27b121d7f5ac.png)
- Hash File
````
Get-FileHash -Algorithm md5 .\interesting-file.txt.txt
````
- Will default to `SHA-256`
## See all Cmdlets Installed
````
Get-Command | Where-Object -Property CommandType -eq Cmdlet | measure
````
## Users
- See users on the sytem
````
net users
Get-LocalUser
````
- See what user a SID belongs to
````
Get-LocalUser -SID "S-1-5-21-1394777289-3961777894-1791813945-501"
````
- Pull value from users
````
get-localuser * | select * #find parameter you want and then pass into second command value
get-localuser * | select * | findstr /i "Passwordrequired"
````
## Groups
- See Groups
````
Get-LocalGroup
````
## IP Address Information / TCP/UDP Connections
````
Get-NetIPAddress
Get-NetTCPConnections
Get-Net-UDPEndpoints
````
- ![image](https://user-images.githubusercontent.com/75596877/150695096-edaaf297-0394-4213-a415-7d46cedecee2.png)
# Base64 Powershell Decode
````
certutil -decode "C:\Users\Administrator\Desktop\b64.txt" decode.txt
Get-Content decode.txt
````










