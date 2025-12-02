# How to Join a Windows 11 PC to a Domain

### Things You Need to Join a Windows 11 PC to a Domain

If you want to join a domain, the following is needed:

* A Windows 11 PC running **Windows 11 Professional, Enterprise,** or **Education**.
* A suitable account on an **Active Directory** domain (with a username and password).
* The device is on the same network (it works [over a VPN connection](https://go.gplink.io/nordvpn)) as the domain with access to the **domain controller**.

Joining a Windows 11 PC to a domain isn’t an easy step for beginners, and we’ll be using industry-specific terms in this article. If you’re unsure, make sure to consult with a network administrator before you begin.

### How to Join a Windows 11 PC to a Domain

If you think you’re ready to join your Windows 11 PC to a domain, and you’re on the same network, you can start now.

**To join a Windows 11 PC to a domain:**

1. Open the **Start** menu and press **Settings**.
2. In Settings, press **Accounts > Access work or school** and click on the **Connect** button.
3.  Select the **Join this device to a local Active Directory domain** option.

    <figure><img src="https://www.groovypost.com/wp-content/uploads/2022/04/gp-SettingsAccountsConnectJoinDomain.png" alt=""><figcaption></figcaption></figure>
4.  Type in the **domain name** when instructed.

    * There are two different types of domain name we can use here. We use the **single legacy name** or the more **extended name** separated with dots, similar to a web address. In our image below, the legacy domain name is ‘bryntze’, and the longer so-called [DNS](https://www.groovypost.com/howto/what-is-dns-and-why-does-it-matter/) (also called FQDN) domain name is ‘ad.bryntze.cloud’. You can use either name given by your network administrator.

    <figure><img src="https://www.groovypost.com/wp-content/uploads/2022/04/gp-SettingsAccountsConnectJoinDomain-2.png" alt=""><figcaption></figcaption></figure>
5.  Joining the device to the domain requires the correct permissions. If your network administrator has given your account access, you can enter your credentials. If not, ask your network administrator to enter their admin credentials to join the device for you.

    <figure><img src="https://www.groovypost.com/wp-content/uploads/2022/04/gp-SettingsAccountsConnectJoinDomain-3.png" alt=""><figcaption></figcaption></figure>
6.  We might see an extra dialog to **Add an account.** However, this isn’t necessary to join the device to the domain, so press the **Skip** button.

    <figure><img src="https://www.groovypost.com/wp-content/uploads/2022/04/gp-SettingsAccountsConnectJoinDomain-4.png" alt=""><figcaption></figcaption></figure>
7.  At this point, your account should be set up in Active Directory. You’ll need to [restart your PC](https://www.groovypost.com/howto/shut-down-or-restart-windows-11/) when prompted to do so.

    <figure><img src="https://www.groovypost.com/wp-content/uploads/2022/04/gp-SettingsAccountsConnectJoinDomain-5.png" alt=""><figcaption></figcaption></figure>
8.  After restarting the Windows 11 device, we can now log in with our domain user. To do this, type in **DOMAIN\username** or the **User Principle Name** (often the same as our email address).

    <figure><img src="https://www.groovypost.com/wp-content/uploads/2022/04/gp-SettingsAccountsConnectJoinDomain-6.png" alt=""><figcaption></figcaption></figure>
9.  Once you’ve logged in, we can go to **Settings > Accounts > Access work or school** again and verify that our domain shows up.

    <figure><img src="https://www.groovypost.com/wp-content/uploads/2022/04/gp-SettingsAccountsConnectJoinDomain-7.png" alt=""><figcaption></figcaption></figure>

![](https://www.groovypost.com/wp-content/uploads/2022/04/gp-SettingsAccountsConnectJoinDomain-8.png)

Credit: [https://www.groovypost.com/howto/join-a-windows-11-pc-to-a-domain/](https://www.groovypost.com/howto/join-a-windows-11-pc-to-a-domain/)

<br>
