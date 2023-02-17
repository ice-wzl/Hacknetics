# RID Hijacking

#### Overview

* When a user is created, an identifier called Relative ID (RID) is assigned to them.
* The `RID` is simply a numeric identifier representing the user across the system. When a user logs on, the `LSASS` process gets its `RID` from the `SAM` registry hive and creates an access token associated with that `RID`.
* If we can tamper with the registry value, we can make windows assign an Administrator access token to an unprivileged user by associating the same RID to both accounts.
* In any Windows system, the default Administrator account is assigned the `RID = 500`, and regular users usually have `RID >= 1000`.

```
wmic useraccount get name,sid

Name                SID
Administrator       S-1-5-21-1966530601-3185510712-10604624-500
DefaultAccount      S-1-5-21-1966530601-3185510712-10604624-503
--snip--
```

* Now we only have to assign the `RID=500` to `jack`. To do so, we need to access the `SAM` using `Regedit`. The `SAM` is restricted to the `SYSTEM` account only, so even the `Administrator` won't be able to edit it. To run `Regedit` as `SYSTEM`, we will use `psexec`.
* `PsExec64.exe -i -s regedit` From Regedit, we will go to:
* `HKLM\SAM\SAM\Domains\Account\Users\`
* We need to search for a key with its `RID` in hex `(1010 = 0x3F2)`. Under the corresponding key, there will be a value called `F`, which holds the user's effective `RID` at position `0x30`:

![](https://user-images.githubusercontent.com/75596877/180829367-5257c90e-37bc-4773-9ae2-d1a9bbb0fdc5.png)

* Notice the RID is stored using little-endian notation, so its bytes appear reversed.
* We will now replace those two bytes with the RID of Administrator in hex (500 = 0x01F4), switching around the bytes (F401):

![](https://user-images.githubusercontent.com/75596877/180829481-acd6a81c-fb14-480b-92c8-aa41539dc9f3.png)
