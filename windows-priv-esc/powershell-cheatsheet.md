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














