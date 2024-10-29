CSIRT training center: Request of cooperation
=============================================

## Task
Hi, CSIRT trainee,

we have received a request for cooperation issued by law enforcement authorities to locate a device on our network 2001:db8:7cc::/64. Please try to accommodate the requester as much as possible.

## Solution
In details in PDF document is several interesting information: we have IPv6 prefix used, we have MAC address, we know that device uses IPv6 stateless configuration and there are some web page on TCP port 1701. In IPv6 stateless configuration is IPv6 address of device determined by prefix and used MAC address. So combining these information (we can use some EUI-64 calculator) we know IPv6 address of device: 2001:db8:7cc::2ca:7aff:fed0:ea71. After several fails with typing IPv6 address in Firefox and curl I've tried my second most favourite web browser: telnet:

```
$ telnet 2001:db8:7cc::2CA:7AFF:FED0:EA71 1701
Trying 2001:db8:7cc:0:2ca:7aff:fed0:ea71...
Connected to 2001:db8:7cc::2CA:7AFF:FED0:EA71.
Escape character is '^]'.
GET / HTTP/1.0
```

And flag is somewhere in returned page: FLAG{Sxwr-slvA-pBuT-CzyD}
