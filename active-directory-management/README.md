# Active Directory Management

### **Prerequisite Required** <a href="#viewer-b6rie" id="viewer-b6rie"></a>

* &#x20;VM or Physical Server with Windows Server 2019 installed (w_e are using Server with Desktop Experience installation option_)
* Assign a static IP address to the server that we promote as Domain Controller.
* As we'll configure Active Directory-integrated DNS, therefore change the DNS settings in the network interface and set the same server IP address as the primary DNS server.

### **Step 1: Install Active Directory Domain Services (ADDS)** <a href="#viewer-7f5cp" id="viewer-7f5cp"></a>

* Log into your Windows Server 2019 with administrative credentials. Open **Server Manager** → click on **Dashboard** → click on **Add roles and features**.

<figure><img src="https://static.wixstatic.com/media/115dee_fabba8d7e01c443fb1981cffe99cb6b4~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_fabba8d7e01c443fb1981cffe99cb6b4~mv2.png" alt=""><figcaption></figcaption></figure>

* The "**Before you begin**" tab contains some important information. Please go through it and click "**Next**".

<figure><img src="https://static.wixstatic.com/media/115dee_eeecc83de06d43e093cf401d8aa31d40~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_eeecc83de06d43e093cf401d8aa31d40~mv2.png" alt=""><figcaption></figcaption></figure>

* In the "**Installation Type**" tab choose **Role-based or Feature-based installation** and click on the **Next** button.

<figure><img src="https://static.wixstatic.com/media/115dee_f48e7119d845411eb10f67e247ff8c94~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_f48e7119d845411eb10f67e247ff8c94~mv2.png" alt=""><figcaption></figcaption></figure>

* In the **Server Selection** tab, please select the destination server on which the role will be installed. Please verify the hostname and the IP address points of the selected server. Click **Next** to continue.

<figure><img src="https://static.wixstatic.com/media/115dee_a939b030e9314cacb4435bcac32ac394~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_a939b030e9314cacb4435bcac32ac394~mv2.png" alt=""><figcaption></figcaption></figure>

* In the **Server Roles** tab, put a tickmark for **"Active Directory Domain Services"** _(you can select the **DNS Server** role as well, as we will configure AD integrated DNS server. If not selected, during installation it will automatically select and install the DNS Role)_.
* Then, it will prompt to show you the associated features for the role. Click on **Add Features** to add those. Then click **Next** to continue.\


<figure><img src="https://static.wixstatic.com/media/115dee_b7046ff12a2547ee84be8bea533ffb2f~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_b7046ff12a2547ee84be8bea533ffb2f~mv2.png" alt=""><figcaption></figcaption></figure>

<figure><img src="https://static.wixstatic.com/media/115dee_36f89be0dcc447ad9dca9cb5059ed8a5~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_36f89be0dcc447ad9dca9cb5059ed8a5~mv2.png" alt=""><figcaption></figcaption></figure>

* In the **Features** tab, the basic features for this required role are already selected by default. Click **Next** to install continue.

<figure><img src="https://static.wixstatic.com/media/115dee_519735a2cadf4229a5a2e6334d35d960~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_519735a2cadf4229a5a2e6334d35d960~mv2.png" alt=""><figcaption></figcaption></figure>

* In the next window, it gives brief information about the "**Active Directory Domain Services"** service. Click **next** to proceed.

<figure><img src="https://static.wixstatic.com/media/115dee_83d80e18cef54cb5a0896dab4c128370~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_83d80e18cef54cb5a0896dab4c128370~mv2.png" alt=""><figcaption></figcaption></figure>

* In the **Confirmation** tab, verify the selections and click on the **Install** button. You may or may not select the option **"Restart the destination server automatically if required"**. It is always a best practice to restart the server post-installation.

<figure><img src="https://static.wixstatic.com/media/115dee_483fdb64004c42c0a1d2d746637dd999~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_483fdb64004c42c0a1d2d746637dd999~mv2.png" alt=""><figcaption></figcaption></figure>

* Once done, it will start the installation process and you can check the same in the **Results** tab.

<figure><img src="https://static.wixstatic.com/media/115dee_b7e2ed0bd84743c4a4b55ffad6324e47~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_b7e2ed0bd84743c4a4b55ffad6324e47~mv2.png" alt=""><figcaption></figcaption></figure>

### **Step 2: Promote the server into a Domain Controller** <a href="#viewer-3l9nd" id="viewer-3l9nd"></a>

* Once the **ADDS** role installation completes, click on the option **"Promote this server to a Domain Controller"** _(highlighted in the below image)_**.** Alternately, you will see a notification flag next to the Manage menu. From there also you can select "Promote this server into a domain controller", this will start the configuration process.

<figure><img src="https://static.wixstatic.com/media/115dee_af0d26c5765b4132a58d7b06561279e6~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_af0d26c5765b4132a58d7b06561279e6~mv2.png" alt=""><figcaption></figcaption></figure>

* It will open the **"Active Directory Configuration Wizard"**. Now, from the Deployment Configuration tab, select **"Add a new forest"** (as I am configuring a new Forest and it is my first domain controller). Provide a **Root Domain name**, mine is **"VirtualGyanis.Com"** (you have to put your domain name here). Then, click on **Next** to continue.
* Note: If you are adding this domain controller into an existing domain/forest you can choose the relevant option accordingly.

<figure><img src="https://static.wixstatic.com/media/115dee_c3610edbc3aa4c25bc736e1f21bb5fb4~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_c3610edbc3aa4c25bc736e1f21bb5fb4~mv2.png" alt=""><figcaption></figcaption></figure>

* In the `Domain Controller Option` tab, select a `Forest functional level` and a `Domain functional level` as per your environment. Since this is the first domain controller in the forest, please select the `DNS Server (as we are configuring AD integrated DNS)` and the `Global Catalog (GC)` checkboxes. Then, enter the `Active Directory Restore Mode (DSRM)` password, this is used to retrieve/restore Active Directory data. Then, click `Next` to continue

<figure><img src="https://static.wixstatic.com/media/115dee_c7048e1ea7884c5bb92fc6c9f6a3f4ff~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_c7048e1ea7884c5bb92fc6c9f6a3f4ff~mv2.png" alt=""><figcaption></figcaption></figure>

* Since we have configured an AD-integrated DNS server, you can ignore the DNS Delegation warning as shown in the below screen. Then, click **Next** to continue.

<figure><img src="https://static.wixstatic.com/media/115dee_709de13858f746bf94b8a0507138b835~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_709de13858f746bf94b8a0507138b835~mv2.png" alt=""><figcaption></figcaption></figure>

* In the `Additional Options` tab, enter a `NetBIOS` name for your domain. It is suggested to keep the NetBIOS name the same as the root domain name _(by default, it will fetch the domain name only)_. Then, click **Next** to continue.

<figure><img src="https://static.wixstatic.com/media/115dee_849e5531b4d748b18393ce8d1e2b5f43~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_849e5531b4d748b18393ce8d1e2b5f43~mv2.png" alt=""><figcaption></figcaption></figure>

* In the **Path** tab, you have to mention the **Database (NTDS Database), LOG** **files and SYSVOL** folders path. You can change the default path as per your organization security policies. I have kept them default. Now, click **Next** to continue.

<figure><img src="https://static.wixstatic.com/media/115dee_0bc2901019ff45b1a98a3f2ebb2b9784~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_0bc2901019ff45b1a98a3f2ebb2b9784~mv2.png" alt=""><figcaption></figcaption></figure>

* In the **Review Options** tab, you will review the configuration. If everything is as per your need, you can click **Next** to proceed or otherwise you can go back and change the required setting as per your need and then proceed further.
* You can also view the powershell script for future deployment. The below-mentioned script is from my environment.
* Note: Always test your PowerShell scripts in a test environment, before running in a production environment.

```
Import-Module ADDSDeployment
Install-ADDSForest `
-CreateDnsDelegation:$false `
-DatabasePath "C:\Windows\NTDS" `
-DomainMode "WinThreshold" `
-DomainName "VirtualGyanis.Com" `
-DomainNetbiosName "VIRTUALGYANIS" `
-ForestMode "WinThreshold" `
-InstallDns:$true `
-LogPath "C:\Windows\NTDS" `
-NoRebootOnCompletion:$false `
-SysvolPath "C:\Windows\SYSVOL" `
-Force:$true
```

<figure><img src="https://static.wixstatic.com/media/115dee_019661c159f54f6fa27b8e1c274c00c0~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_019661c159f54f6fa27b8e1c274c00c0~mv2.png" alt=""><figcaption></figcaption></figure>

In the **Prerequisites Check** tab, it will do prerequisite check.

<figure><img src="https://static.wixstatic.com/media/115dee_42a3227178fb4488be4fc4f214e6a0bf~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_42a3227178fb4488be4fc4f214e6a0bf~mv2.png" alt=""><figcaption></figcaption></figure>

* Once prerequisite checks completed successfully, it will enable/highlight the Install option. Then, click on I**nstall** button to start the installation process.

![](https://static.wixstatic.com/media/115dee\_fe76f0ba8f1e4a538e5662bac7556ded\~mv2.png/v1/fill/w\_740,h\_416,al\_c,q\_85,usm\_0.66\_1.00\_0.01,enc\_auto/115dee\_fe76f0ba8f1e4a538e5662bac7556ded\~mv2.png)

* Once installation completed successfully, you will get the below confirmation message. Close this window and restart the Server.

<figure><img src="https://static.wixstatic.com/media/115dee_b191d547c71d49e58e439ed9b36da2ad~mv2.png/v1/fill/w_722,h_535,al_c,lg_1,q_90,enc_auto/115dee_b191d547c71d49e58e439ed9b36da2ad~mv2.png" alt=""><figcaption></figcaption></figure>

* Once server rebooted, you have to login with your domain Admin credentials. By default, the local admin account will promoted as a Domain Admin account. Login and verify the health of the Domain controller. You can run **DCDIAG** command to check the health.
* You can also verify the settings/configurations from the Active Directory tools like _**Active Directory Users and Computers or Active Directory Domains and Trusts**_ etc. You will get all the Active Directory tools in the folder named _**Administrative Tools**_ on the Start menu. Go and explore the tools.

\


<figure><img src="https://static.wixstatic.com/media/115dee_d802a7f674d24fcb8fccc4832b66933f~mv2.png/v1/fill/w_740,h_416,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/115dee_d802a7f674d24fcb8fccc4832b66933f~mv2.png" alt=""><figcaption></figcaption></figure>

Credit: [https://www.virtualgyanis.com/post/step-by-step-how-to-install-and-configure-domain-controller-on-windows-server-2019](https://www.virtualgyanis.com/post/step-by-step-how-to-install-and-configure-domain-controller-on-windows-server-2019)
