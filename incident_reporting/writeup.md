Miscellaneous: Incident reporting
======================================

## Task
Hi, TCC-CSIRT analyst,

our automatic incident recording system has captured about an hour of traffic originating from the IP range within the AI-CSIRT constituency. Analyze whether there are any incidents present and report all of them through the AI-CSIRT web interface.

- Download the pcap file (cca 53 MB) (sha256 checksum: e38550ba2cc32931d7c75856589a26e652f2f64e5be8cafaa34d5c191fc0fd1c)
- The web interface is at http://incident-report.csirt.ai.tcc.

## Solution

Entering data into incident report app reveals parts of flag. There are 4 attacks in dump, each reveal 1/4 of the flag when entered into the system. Entering data is a little bit anoying because every single typo, even in time, results in generic "nothing there" error. So what is in the dump:

- scanning from address 2001:db8:7cc::a1:42, scanning incident starts with IPv6 neighbor discovery packets (although that in filling incident you must specify scanned ports)
- web service enumeration from address 2001:db8:7cc::a1:210
- sucessful brute force attack (HTTP POST on /login.php) from 2001:db8:7cc::a1:210
- DoS attack from 2001:db8:7cc::a1:d055 (a lot of request on /check_status.php)