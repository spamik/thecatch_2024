Miscellaneous: Old service
======================================

## Task
Hi, TCC-CSIRT analyst,

rumors are spreading in the ticketing system that an old, unmaintained service is running somewhere in the network, which could be a security risk (even though it's called 3S - Super Secure Service). Old-timers claim that it had the domain name supersecureservice.cypherfix.tcc. This name does not exist in the current DNS, but some information might still be available on the DNS server ns6-old.tcc, which will be shut down soon.

Explore the service and gather as much information as possible about 3S.

## Solution
First we need to determine IP address on which the service is running. In DNS provided in VPN it couldn't be resolved but we can ask the mentioned server:

```
$ dig supersecureservice.cypherfix.tcc @ns6-old.tcc                                    
supersecureservice.cypherfix.tcc. 86400 IN A    10.99.24.21

```

TCP port 80 is closed so we can scan all ports with nmap:

```
# nmap -p- 10.99.24.21

PORT     STATE SERVICE
8020/tcp open  intu-ec-svcdisc

```

Open that IP with port in web browser and there is meme with Yoda and text "default page this is, acquire the correct hostname, you must." It probably tells that we are missing Host header, since we opened this page using IP address. So you can use some extension to modify Host header, add this record to /etc/hosts or just use my favourite curl with parameter -H "Host: supersecureservice.cypherfix.tcc".

Which returns anotherpage with another meme where guy is looking on another almost same girl labeled by "SVCB" while his girlfriend labeled with "A" looks jealous. So back to the dig, A record wasn't the good was to go:

```
$ dig -t SVCB supersecureservice.cypherfix.tcc @ns6-old.tcc                
;; ANSWER SECTION:
supersecureservice.cypherfix.tcc. 86400 IN SVCB 1 web3s-746865636174636832303234.cypherfix.tcc. alpn="h2,h3,mandatory=alpn" port=8020
supersecureservice.cypherfix.tcc. 86400 IN SVCB 4 web3s-7468656361746368323032343.cypherfix.tcc. alpn="h2,h3,mandatory=alpn" port=8020
supersecureservice.cypherfix.tcc. 86400 IN SVCB 2 web3s-7468656361746368323032342.cypherfix.tcc. alpn="h2,h3,mandatory=alpn" port=8020

```

This give us another 3 DNS names which we can try to send with Host header. And getting page with header "web3s-746865636174636832303234.cypherfix.tcc" returns some login page with flag included: FLAG{yNx6-tH9y-hKtB-20k6}