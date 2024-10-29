CSIRT training center: Personal portal
=============================================

## Task
Hi, CSIRT trainee,

check if there is a leak of non-public data on the personal portal.

The portal is accesible at http://perso.cypherfix.tcc.


## Solution

On link is some web application with login form. Except input fields and loggin button there is help link. Opening this links shows something similar to webserver directory listing with some files: info.txt, meeting2024-09-05.md, index.html and help.html. Meeting file looks interesting but clicking on it returns 404 not found. But look on the URL of help page: /files?file=help.html. It looks that content of file is server with some script and file is determined by GET parameter. So I changed URL to this one: /files?file=meeting2024-09-05.md and this download markdown file. At the end of this file is signature code: RkxBR3tZemZOLVo5UlAtb2MxUC1hdURvfQo=. It looks like base64 and decoding it returns flag: FLAG{YzfN-Z9RP-oc1P-auDo}.