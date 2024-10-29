Security conerns: Long secure password
======================================

## Task
Hi, TCC-CSIRT analyst,

a new colleague came up with a progressive way of creating a memorable password and would like to implement it as a new standard at TCC. Each user receives a TCC-CSIRT password card and determines the password by choosing the starting coordinate, direction, and number of characters. For skeptics about the security of such a solution, he published the card with a challenge to log in to his SSH server.

Verify if the card method has any weaknesses by logging into the given server.

- Download the password card (sha256 checksum: 9a35dc6284c8bde03118321b86476cf835a3b48a5fcf09ad6d64af22b9e555ca)
- The server has domain name password-card-rules.cypherfix.tcc and the colleagues's username is futurethinker.

## Solution

Hint in this task reveals two things: 1) that password of this administrator will be probably exactly 18 characters long. And 2) that with this method list of possible password will be probably short enough to brute force login with it. So, included quick dirty script generate list of all possible 18 characters long passwords. This is second version of this script after noticing, that the pictue in bottom right on the card isn't boat rudder as a reminder of The Catch 2023, but tells you that password can be created also in diagonal direction :-)

Script generate password dictionary with 518 items. Which really can be used for bruteforce attack. We can use metasploit. So run msfconsole, type use auxiliary/scanner/ssh/ssh_login and set these options (set OPTION value):
- PASS_FILE: dict_list.txt (generated list of possible passwords)
- RHOSTS: password-card-rules.cypherfix.tcc
- USERNAME: futurethinker
- STON_ON_SUCCESS: true
- VERBOSE: true

type run and wait: 

```
[+] 10.99.24.22:22 - Success: 'futurethinker:SAOPUNUKTPHCANEMFW' 'Nobody will ever read this message anyway, because the TCC password card is super secure. Even my lunch access-code is safe here: FLAG{uNZm-GGVK-JbxV-1DIx} Nobody will ever read this message anyway, because the TCC password card is super secure. Even my lunch access-code is safe here: FLAG{uNZm-GGVK-JbxV-1DIx} '
```
