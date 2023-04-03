# OpenVPN Server on Pfsense

* Article is a direct copy from here: [https://www.comparitech.com/blog/vpn-privacy/openvpn-server-pfsense/](https://www.comparitech.com/blog/vpn-privacy/openvpn-server-pfsense/)
* All credit to: [MARC DAHAN](https://www.comparitech.com/author/marcdahan/) SPECIALIST IN ONLINE PRIVACY

This guide assumes you’ve already got pfSense setup with working WAN and LAN interfaces.

<figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/1_WAN_LAN-923x1024.webp" alt=""><figcaption></figcaption></figure>

Settings that are ignored in the instructions should be left at their default values (i.e., untouched).

### Thinking about authentication

Before we configure our OpenVPN server, we need to choose an authentication method. Both OpenVPN and pfSense support password-based authentication, certificate-based authentication, or both. In this guide, we’ll be using both so that we cover all the bases. But you’re free to select one or the other. If you choose to use password-based authentication only, you can skip the steps of generating user certificates. But you still need to generate a Certificate Authority as well as a server certificate.

### Generating the Certificate Authority (CA)

The first thing we need to do is generate our Certificate Authority (CA), which will validate the OpenVPN server’s identity and authenticate user certificates (if enabled).

1.  From the menus at the top of the screen, select System > Cert. Manager.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/2_SelectCertManager.webp" alt=""><figcaption></figcaption></figure>
2.  Click the Add button at the bottom right.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/3_ClickAdd-1024x383.webp" alt=""><figcaption></figcaption></figure>
3. Enter a name for your CA.
4. Make sure Method is set to Create an internal Certificate Authority.
5. Select your Key type. I will be using RSA for this example, but you can also use ECDSA.
6. Set your Key length to at least 2048. I will be using 4096 for this example.
7. Set your Digest Algorithm to at least sha256. I will be using sha512 for this example.
8.  Choose a Common Name for your certificate or leave the default of internal-ca.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/4_ConfigureCA-997x1024.webp" alt=""><figcaption></figcaption></figure>
9.  Click Save at the bottom. You’ve created your Certificate Authority.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/5_Created_CA-1024x451.webp" alt=""><figcaption></figcaption></figure>

### Generating the server certificate

1. If you’re not already there, from the menus at the top of the screen, select System > Cert. Manager.
2.  Select the Certificates sub-menu.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/6_Select_Certificates-1024x451.webp" alt=""><figcaption></figcaption></figure>
3. From the Certificates sub-menu, click the Add/Sign button at the bottom right.
4. Make sure Method is set to Create an internal Certificate.
5. Enter a Descriptive name for your certificate.
6. Use the same values you set for the Certificate Authority for the Key type and length, as well as for the Digest Algorithm.
7. Set the Lifetime to 365 days.
8.  Select **Server Certificate** as the Certificate Type.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/7_ConfigureServerCert-864x1024.webp" alt=""><figcaption></figcaption></figure>
9. Click Save. You’ve created your server certificate.

### Create your OpenVPN user and your user certificate

We now need to create a user to access the OpenVPN server.

I will be creating a single user for this guide, but you can create as many users as you need. Simply repeat these steps.

1.  From the menus at the top of the screen, select System > User Manager. You are taken to the User Manager.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/14_UserManager-1024x264.webp" alt=""><figcaption></figcaption></figure>
2. Click the Add button at the bottom right.
3.  Enter a Username and Password for your user.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/15_ConfigureUser-1024x948.webp" alt=""><figcaption></figcaption></figure>
4.  Click Save. You’ve created your OpenVPN user and are taken back to the User Manager.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/16_UserCreated-1024x300.webp" alt=""><figcaption></figcaption></figure>
5. If you chose to set up your server for certificate-based authentication or for certificate and password-based authentication, click the pencil icon to the right of your new user. You’re taken back to the Edit User window.
6.  Click the Add button under User Certificates. You’re taken to the Certificate Manager, and you’re prompted to input the parameters for your user certificate.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/AddUserCertificate-1024x148.webp" alt=""><figcaption></figcaption></figure>
7. Make sure Method is set to Create an internal Certificate.
8. Enter a Descriptive name for your certificate.
9. Set the same values you set for the Certificate Authority for the Key type and length, as well as for the Digest Algorithm.
10. Set the Lifetime to 365 days.
11. Make sure Certificate Type is set to User Certificate.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/8_ConfigureUserCert-864x1024.webp" alt=""><figcaption></figcaption></figure>
12. Click Save. You’re taken back to the User Manager, and you can see that your newly created user certificate is now associated with your OpenVPN user.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/AddedUserCert-850x1024.webp" alt=""><figcaption></figcaption></figure>
13. Click Save.

### Creating the OpenVPN server

We’re now ready to create our OpenVPN server.

1.  From the menus at the top of the screen, select VPN > OpenVPN. You are taken to the OpenVPN Servers sub-menu.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/OVPNServersPage-1024x224.webp" alt=""><figcaption></figcaption></figure>
2. Click the Add button on the bottom right.

#### General Information

1. Set the Server mode to either Remote Access (SSL/TLS), Remote Access (User Auth), or Remote Access (SSL/TLS + User Auth). As mentioned above, I will be using Remote Access (SSL/TLS + User Auth) for this example.
2. Change the Local port to a different port if required by your network topology or leave it at the default (1194).
3.  Enter a name for your server in the Description field.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/10_ServerConf_GeneralInformation-1024x537.webp" alt=""><figcaption></figcaption></figure>

#### Cryptographic Settings

1. Make sure Use a TLS Key and Automatically generate a TLS Key are enabled.
2. Make sure your Peer Certificate Authority is set to the CA we created earlier.
3. Set the Server certificate field to the server certificate we created earlier.
4. Select 4096 for the DH Parameter Length setting.
5.  Set the Auth digest algorithm to RSA-SHA512 (512-bit).

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/11_ServerConf_CryptographicSettings-877x1024.webp" alt=""><figcaption></figcaption></figure>

#### Tunnel Settings

1. In the IPv4 Tunnel Network field, enter a subnet that is not present on your network to be used as the OpenVPN network’s internal subnet. In my case, I’m using 192.168.2.0/24.
2. If your network also supports IPv6 and you want your OpenVPN tunnel to support IPv6 as well, enter an unused IPv6 subnet in the IPv6 Tunnel Network field. In this example, I am configuring my server for IPv4 only.
3. Enable Redirect IPv4 Gateway in order to route all IPv4 traffic over the VPN tunnel.
4.  Enable Redirect IPv6 Gateway in order to route all IPv6 traffic over the VPN tunnel, if needed.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/12_ServerConf_TunnelSettings-1024x824.webp" alt=""><figcaption></figcaption></figure>

#### Advanced Configuration

1. Enable UDP Fast I/O.
2.  If you’re only using IPv4, select IPv4 only in the Gateway creation field. If you’re using both IPv4 and IPv6, leave it set to Both.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/14_ServerConf_AdvancedConfiguration-1024x854.webp" alt=""><figcaption></figcaption></figure>
3.  Click Save. You’ve created your OpenVPN server.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/ServerCreated-1024x306.webp" alt=""><figcaption></figcaption></figure>

#### Verifying the OpenVPN server configuration

1. To make sure our server is set up correctly, select Status > System Logs from the top menus.
2. Select the OpenVPN sub-menu. The OpenVPN logs are displayed.
3.  If everything is set up correctly, you should see Initialization Sequence Completed in the logs.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/InitializationSequenceComplete-1024x601.webp" alt=""><figcaption></figcaption></figure>

### Create firewall rules

Now that our OpenVPN server is configured, we need to create a firewall rule to allow traffic to and from our server.

#### OpenVPN rule

This rule will allow traffic from the OpenVPN subnet out to the internet.

1. From the menus at the top of the screen, select Firewall > Rules.
2. Select the OpenVPN sub-menu.
3.  Click the Add button to create a new rule at the top of the list.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/FirewallRules_ClickAdd-1024x322.webp" alt=""><figcaption></figcaption></figure>
4. Set the Address Family to IPv4 + IPv6 if your system is using both IPv4 and IPv6. If not, leave it at the default value of IPv4.
5. Set the Protocol field to Any.
6. Set the Source to Network.
7. Enter the OpenVPN subnet you specified earlier in the Source Address field but without the /24. For example: 192.168.2.0.
8. Select 24 from the drop-down menu to the right of the Source Address field.
9.  Enter a description for this rule in the Description field.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/Firewall_CreateRule-1024x882.webp" alt=""><figcaption></figcaption></figure>
10. Click Save. And click Apply Changes. Traffic will now be allowed out the firewall from the OpenVPN subnet.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/FirewallRules_Apply-1024x361.webp" alt=""><figcaption></figcaption></figure>

#### WAN rule

In order to connect to your OpenVPN server from the outside world (i.e., the internet), you’re going to need to open the port your server runs on (1194, in this example) on your WAN interface. This rule will allow your client to connect to your OpenVPN server from the internet.

1. From the menus at the top of the screen, select Firewall > Rules.
2. Select the WAN sub-menu (the default).
3. Click the Add button to create a new rule at the top of the list.
4. Set the Address Family to IPv4 + IPv6 if your system is using both IPv4 and IPv6. If not, leave it at the default value of IPv4.
5. Make sure Source is set to Any.
6. Set the Protocol field to UDP.
7. Set the Destination Port Range to 1194.
8.  Enter a description for this rule in the Description field.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/Firewall_CreateWANRule-999x1024.webp" alt=""><figcaption></figcaption></figure>
9.  Click Save. And click Apply Changes. Traffic will now be allowed from the internet to the OpenVPN server.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/Firewall_WANRuleCreated-1024x315.webp" alt=""><figcaption></figcaption></figure>

### Install the OpenVPN Client Export Utility

In order to easily configure our OpenVPN client, pfSense provides an automated configuration generator for OpenVPN. However, it’s not installed by default. We need to install the package from the pfSense Package Manager manually.

1. From the menus at the top of the screen, select System > Package Manager. You are taken to the Package Manager.
2.  Select the Available Packages sub-menu.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/17_AvailablePackages-1024x477.webp" alt=""><figcaption></figcaption></figure>
3.  Scroll down until you see openvpn-client-export and click the Install button to its right. You’re taken to the Package Installer page.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/18_InstallClienExport-1024x428.webp" alt=""><figcaption></figcaption></figure>
4.  Click Confirm. The installation begins.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/19_PackageInstaller-1024x215.webp" alt=""><figcaption></figcaption></figure>
5.  Once the installation is finished, the progress bar turns green, and you should see Success displayed in the Package Installation window.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/21_Installed-1024x547.webp" alt=""><figcaption></figcaption></figure>

### Export the OpenVPN client configuration

1. From the menus at the top of the screen, select VPN > OpenVPN.
2. Select the Client Export sub-menu.
3. Make sure the correct OpenVPN server is selected next to Remote Access Server.
4.  If you’re using [Dynamic DNS](https://www.comparitech.com/net-admin/dynamic-dns-providers/) to access your pfSense WAN, select Other from the Host Name Resolution drop-down menu. Then enter the hostname in the Host Name box that appears below. This allows you to access your pfSense WAN by hostname rather than IP address, which means that you won’t lose access to your OpenVPN server if your ISP changes your WAN IP address. If you’re not using Dynamic DNS, leave Host Name Resolution set to Interface IP Address.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/ClientExportPage-963x1024.webp" alt=""><figcaption></figcaption></figure>
5.  Scroll down to the bottom of the page, and you’ll find generated configurations for various systems and apps. Click on the appropriate configuration for your device(s) to download it to your computer.

    <figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/ExportBundles-1024x309.webp" alt=""><figcaption></figcaption></figure>

I’m going to be connecting a Linux laptop, so I downloaded the Most Clients inline configuration.

Upon importing my configuration in Linux’s Network Manager, I simply need to input my username and password (they’re not included in the configuration file), and I can connect to my OpenVPN server.

<figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/LinuxConnected-1024x866.webp" alt=""><figcaption></figcaption></figure>

I can then check to make sure that my public IP address has been changed to the WAN address of my home internet, using [Comparitech’s IP Address Check tool](https://www.comparitech.com/privacy-security-tools/my-ip-address/).

<figure><img src="https://cdn.comparitech.com/wp-content/uploads/2021/03/IPAddressChecker-1024x610.webp" alt=""><figcaption></figcaption></figure>

### Wrap-Up

So that’s how you set up a basic OpenVPN server in pfSense for remote access. There are a lot of places to go from here to accommodate more complex setups. You could also configure content filtering on your pfSense box to block ads and malicious sites. Your OpenVPN clients would benefit from this as well. But for now, you have a fully functional OpenVPN server configured on your home router (pfSense), enabling you to use your home internet connection from any device, wherever you are.

VPN on, friends.
