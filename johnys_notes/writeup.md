Security conerns: Johny's notes
======================================

## Task

Hi, TCC-CSIRT analyst,

admin Johny is testing a new notebook to take notes, as any good administrator would. He thinks he has correctly secured the application so that only he can access it and no one else. Your task is to check if he made any security lapses.

- Admin Johny uses workstation johny-station.cypherfix.tcc.
- Application for notes runs on notes.cypherfix.tcc.

## Solution

We can try open the notes application. Let's start with curl to see what's happening. Web page on port 80 return some weird javascript, which redirect to port 8080. On port 8080 we receive empty reply. If we try it with telnet, we can see that connection is opened and immediately closed before we send anything. Task description is saying that only admin Johny can access notes. I have seen some similar behaviour with using /etc/hosts.allow. So this probably means that our connection is closed before we can send any request to webserver and only Johny's workstation can communicate with it.

So now we focus on workstation and start with nmap. On WS is open port 22 (SSH) and 80 on which is running apache, with default page. Web enumeration on apache doesn't find anything useful but we can try another thing. Somewhere in past was popular web home directory. Our admin is johny. So, let's try /~johny URL. Bingo, there is directory listing with flatnotes dir. Inside is a lot of files, another directories... if we google it, we find out that it probably will be regular flatnotes application which we can find on github. So there is question if and where we find something useful... it was on github, it's git repository? Let's findout and open johny-station.cypherfix.tcc/~johny/flatnotes/.git/ url. Yes, something is here. If we know it, we can mirror this directory with this command: wget --mirror -np http://johny-station.cypherfix.tcc/~johny/flatnotes/.git/

cd into .git dir and run git log. This is the last commit:

```
commit 47dab1229b328b6ec01c69c02c1a77d2651a2bf5 (HEAD -> develop)
Author: johny <johny@cypherfix.tcc>
Date:   Thu Oct 24 07:50:44 2024 +0000

    User password for http://notes.cypherfix.tcc:8080
```

It's not from the upstream, probably :-) So we can diff it:

```
# git diff 43f1b8d3e5aeb7c4a2ee7d74da66aeb4fbe1c5b1..
diff --git a/README.md b/README.md
index 15ea2e5..edc31a0 100644
--- a/README.md
+++ b/README.md
@@ -68,7 +68,7 @@ docker run -d \
   -e "PGID=1000" \
   -e "FLATNOTES_AUTH_TYPE=password" \
   -e "FLATNOTES_USERNAME=user" \
-  -e "FLATNOTES_PASSWORD=changeMe!" \
+  -e "FLATNOTES_PASSWORD=gojohnygo" \^M
   -e "FLATNOTES_SECRET_KEY=aLongRandomSeriesOfCharacters" \
   -v "$(pwd)/data:/data" \
   -p "8080:8080" \
```

Good, we have password to the notes application which we can't access... But previously we have seen that admins won't do their work very good... and we have opened SSH. So, maybe SSH user has same password? Login with user johny, password gojohnygo on johny-station.cypherfix.tcc works. But the user has shell set to nologin so connection is immediately closed. But do we need shell? We only have to access notes application from this workstation. For this, port forwarding is sufficient. Can we use port forwarding without shell? Maybe:

```
# ssh -N -L 8080:10.99.24.33:8080 johny@johny-station.cypherfix.tcc
johny@johny-station.cypherfix.tcc's password:
```

And in browser open URL http://localhost:8080. You should see flatnotes login. With credentials user:gojohnygo is possible to login and you will se note named flag with content: FLAG{VfCK-Hlp4-cQl8-p0UM}