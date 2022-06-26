# Welcome to the Empire
## Install
- Installing Empire
````
cd /opt
git clone https://github.com/BC-SECURITY/Empire/
cd /opt/Empire
./setup/install.sh
````
- Installing Starkiller
- Once Empire is installed we can install the GUI for Empire known as Starkiller.
````
cd /opt
````
- Download an up to date version of Starkiller from the BC-Security Github repo - https://github.com/BC-SECURITY/Starkiller/releases 
````
chmod +x starkiller-0.0.0.AppImage
````
### Starting Empire
- Once both Empire and Starkiller are installed we can start both servers. Being by starting Empire with the instructions below.
````
cd /opt/Empire
./empire --rest
````
- Starting Starkiller
- Once Empire is started follow the instructions below to start Starkiller.
````
cd /opt
./starkiller-0.0.0.AppImage
````
### Login to Starkiller

- Default Credentials
- Uri: `127.0.0.1:1337`
- User: `empireadmin`
- Pass: `password123`























































