# Impacket-install

### Installing Impacket:

* Whether you're on the Kali 2019.3 or Kali 2021.1, Impacket can be a pain to install correctly. Here's some instructions that may help you install it correctly!
* First, you will need to clone the Impacket Github repo onto your box. The following command will clone Impacket into `/opt/impacket`:

```
git clone https://github.com/SecureAuthCorp/impacket.git /opt/impacket
```

After the repo is cloned, you will notice several install related files, `requirements.txt`, and `setup.py`. A commonly skipped file during the installation is `setup.py`

* This actually installs Impacket onto your system so you can use it and not have to worry about any dependencies.
* To install the Python requirements for Impacket:

```
pip3 install -r /opt/impacket/requirements.txt
```

* Once the requirements have finished installing, we can then run the python setup install script:

```
cd /opt/impacket/ && python3 ./setup.py install
```

* After that, Impacket should be correctly installed now and it should be ready to use!
* If you are still having issues, you can try the following script and see if this works:

```
sudo git clone https://github.com/SecureAuthCorp/impacket.git /opt/impacket
sudo pip3 install -r /opt/impacket/requirements.txt
cd /opt/impacket/ 
sudo pip3 install .
sudo python3 setup.py install
```

* Credit for proper Impacket install instructions goes to Dragonar#0923 in the THM Discord
