Miscellaneous: DNS madness
======================================

## Task
Hi, TCC-CSIRT analyst,

for infrastructure management, the Department of Operations must maintain a large number of DNS records in many zones. The DNS administrator has gone crazy from the sheer number of records, sitting in front of the monitor, swaying back and forth, and repeatedly saying "It came to me, my own, my love, my own, my precious infra.tcc". Your task is to examine the zones, resource records, and their counts so that we can hire a sufficiently resilient administrator next time.

## Solution

Hints in this task are saying something about DNS RFC standards. With the text, it will probably about zone transfers (AXFR) and DNS catalog zones. So, we need to start with something:

```
$ dig -t NS infra.tcc  
;; ANSWER SECTION:
infra.tcc.              74282   IN      NS      jamison.infra.tcc.
infra.tcc.              74282   IN      NS      jameson.infra.tcc.

;; ADDITIONAL SECTION:
jameson.infra.tcc.      55932   IN      A       10.99.24.29
jamison.infra.tcc.      55857   IN      A       10.99.24.28
jameson.infra.tcc.      55932   IN      AAAA    2001:db8:7cc::24:29
jamison.infra.tcc.      55857   IN      AAAA    2001:db8:7cc::24:28
```

```
$ dig -t SOA infra.tcc                                     
;; ANSWER SECTION:
infra.tcc.              86400   IN      SOA     jessiejames.infra.tcc. hostmaster.infra.tcc. 2024100701 604800 86400 2419200 86400
```

Now we know DNS slaves for this zone (jameson, jamision) and in SOA records is DNS master: jessiejames. Now we can try to do DNS zone transfer... and from the DNS master it's working:

```
$ dig AXFR infra.tcc @jessiejames.infra.tcc

; <<>> DiG 9.18.8-1-Debian <<>> AXFR infra.tcc @jessiejames.infra.tcc
;; global options: +cmd
infra.tcc.              86400   IN      SOA     jessiejames.infra.tcc. hostmaster.infra.tcc. 2024100701 604800 86400 2419200 86400
infra.tcc.              86400   IN      NS      jameson.infra.tcc.
infra.tcc.              86400   IN      NS      jamison.infra.tcc.
jameson.infra.tcc.      86400   IN      AAAA    2001:db8:7cc::24:29
jameson.infra.tcc.      86400   IN      A       10.99.24.29
jamison.infra.tcc.      86400   IN      AAAA    2001:db8:7cc::24:28
jamison.infra.tcc.      86400   IN      A       10.99.24.28
jessiejames.infra.tcc.  86400   IN      AAAA    2001:db8:7cc:0:6361:74:24:27
infra.tcc.              86400   IN      SOA     jessiejames.infra.tcc. hostmaster.infra.tcc. 2024100701 604800 86400 2419200 86400
```

But still nothing useful... so what about catalog zones? In quick, it's way how to tell slave DNS servers which zones the should be serving. These zones are then published... just like PTR records in another zone. So slaves are wathing this zone and when new record appears here they transfer this zone also. So let's try to transfer the catalog zone, how it can be named? Maybe, catalog? :-)

```
$ dig AXFR catalog.infra.tcc @jessiejames.infra.tcc

; <<>> DiG 9.18.8-1-Debian <<>> AXFR catalog.infra.tcc @jessiejames.infra.tcc
;; global options: +cmd
catalog.infra.tcc.      86400   IN      SOA     . . 2024100802 604800 86400 2419200 86400
catalog.infra.tcc.      86400   IN      NS      invalid.
version.catalog.infra.tcc. 86400 IN     TXT     "2"
aldoriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR aldoria.infra.tcc.
aldorninfratcc.zones.catalog.infra.tcc. 3600 IN PTR aldorn.infra.tcc.
arionisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR arionis.infra.tcc.
averoninfratcc.zones.catalog.infra.tcc. 3600 IN PTR averon.infra.tcc.
banneroninfratcc.zones.catalog.infra.tcc. 3600 IN PTR banneron.infra.tcc.
beloriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR beloria.infra.tcc.
blaveninfratcc.zones.catalog.infra.tcc. 3600 IN PTR blaven.infra.tcc.
branoxinfratcc.zones.catalog.infra.tcc. 3600 IN PTR branox.infra.tcc.
brinleyinfratcc.zones.catalog.infra.tcc. 3600 IN PTR brinley.infra.tcc.
brionisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR brionis.infra.tcc.
brystoninfratcc.zones.catalog.infra.tcc. 3600 IN PTR bryston.infra.tcc.
calianinfratcc.zones.catalog.infra.tcc. 3600 IN PTR calian.infra.tcc.
calindrainfratcc.zones.catalog.infra.tcc. 3600 IN PTR calindra.infra.tcc.
celoriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR celoria.infra.tcc.
corviniainfratcc.zones.catalog.infra.tcc. 3600 IN PTR corvinia.infra.tcc.
crystarinfratcc.zones.catalog.infra.tcc. 3600 IN PTR crystar.infra.tcc.
delwyninfratcc.zones.catalog.infra.tcc. 3600 IN PTR delwyn.infra.tcc.
draxorinfratcc.zones.catalog.infra.tcc. 3600 IN PTR draxor.infra.tcc.
draymoorinfratcc.zones.catalog.infra.tcc. 3600 IN PTR draymoor.infra.tcc.
drevininfratcc.zones.catalog.infra.tcc. 3600 IN PTR drevin.infra.tcc.
elarisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR elaris.infra.tcc.
eldarainfratcc.zones.catalog.infra.tcc. 3600 IN PTR eldara.infra.tcc.
eldoriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR eldoria.infra.tcc.
eldricinfratcc.zones.catalog.infra.tcc. 3600 IN PTR eldric.infra.tcc.
eldrininfratcc.zones.catalog.infra.tcc. 3600 IN PTR eldrin.infra.tcc.
elvoriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR elvoria.infra.tcc.
falwyninfratcc.zones.catalog.infra.tcc. 3600 IN PTR falwyn.infra.tcc.
fayleninfratcc.zones.catalog.infra.tcc. 3600 IN PTR faylen.infra.tcc.
fendarainfratcc.zones.catalog.infra.tcc. 3600 IN PTR fendara.infra.tcc.
finstarinfratcc.zones.catalog.infra.tcc. 3600 IN PTR finstar.infra.tcc.
galdoriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR galdoria.infra.tcc.
galdorinfratcc.zones.catalog.infra.tcc. 3600 IN PTR galdor.infra.tcc.
glenwoodiainfratcc.zones.catalog.infra.tcc. 3600 IN PTR glenwoodia.infra.tcc.
gorathinfratcc.zones.catalog.infra.tcc. 3600 IN PTR gorath.infra.tcc.
haldorainfratcc.zones.catalog.infra.tcc. 3600 IN PTR haldora.infra.tcc.
haldrixinfratcc.zones.catalog.infra.tcc. 3600 IN PTR haldrix.infra.tcc.
hesperainfratcc.zones.catalog.infra.tcc. 3600 IN PTR hespera.infra.tcc.
hexoriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR hexoria.infra.tcc.
illyriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR illyria.infra.tcc.
itharainfratcc.zones.catalog.infra.tcc. 3600 IN PTR ithara.infra.tcc.
jadroninfratcc.zones.catalog.infra.tcc. 3600 IN PTR jadron.infra.tcc.
jorathiainfratcc.zones.catalog.infra.tcc. 3600 IN PTR jorathia.infra.tcc.
jorathinfratcc.zones.catalog.infra.tcc. 3600 IN PTR jorath.infra.tcc.
kandorinfratcc.zones.catalog.infra.tcc. 3600 IN PTR kandor.infra.tcc.
karnisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR karnis.infra.tcc.
kylorainfratcc.zones.catalog.infra.tcc. 3600 IN PTR kylora.infra.tcc.
kynerainfratcc.zones.catalog.infra.tcc. 3600 IN PTR kynera.infra.tcc.
loriahinfratcc.zones.catalog.infra.tcc. 3600 IN PTR loriah.infra.tcc.
lunarainfratcc.zones.catalog.infra.tcc. 3600 IN PTR lunara.infra.tcc.
lyranthinfratcc.zones.catalog.infra.tcc. 3600 IN PTR lyranth.infra.tcc.
lyrisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR lyris.infra.tcc.
lytherainfratcc.zones.catalog.infra.tcc. 3600 IN PTR lythera.infra.tcc.
mardaleinfratcc.zones.catalog.infra.tcc. 3600 IN PTR mardale.infra.tcc.
mavrosinfratcc.zones.catalog.infra.tcc. 3600 IN PTR mavros.infra.tcc.
mirelandinfratcc.zones.catalog.infra.tcc. 3600 IN PTR mireland.infra.tcc.
mithrainfratcc.zones.catalog.infra.tcc. 3600 IN PTR mithra.infra.tcc.
mythrainfratcc.zones.catalog.infra.tcc. 3600 IN PTR mythra.infra.tcc.
nexorinfratcc.zones.catalog.infra.tcc. 3600 IN PTR nexor.infra.tcc.
nolarainfratcc.zones.catalog.infra.tcc. 3600 IN PTR nolara.infra.tcc.
nolviainfratcc.zones.catalog.infra.tcc. 3600 IN PTR nolvia.infra.tcc.
nyrosinfratcc.zones.catalog.infra.tcc. 3600 IN PTR nyros.infra.tcc.
odrisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR odris.infra.tcc.
orinthiainfratcc.zones.catalog.infra.tcc. 3600 IN PTR orinthia.infra.tcc.
ostarainfratcc.zones.catalog.infra.tcc. 3600 IN PTR ostara.infra.tcc.
phaelorinfratcc.zones.catalog.infra.tcc. 3600 IN PTR phaelor.infra.tcc.
prydiainfratcc.zones.catalog.infra.tcc. 3600 IN PTR prydia.infra.tcc.
quintisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR quintis.infra.tcc.
quorixinfratcc.zones.catalog.infra.tcc. 3600 IN PTR quorix.infra.tcc.
ravenorinfratcc.zones.catalog.infra.tcc. 3600 IN PTR ravenor.infra.tcc.
rivoriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR rivoria.infra.tcc.
rovilleinfratcc.zones.catalog.infra.tcc. 3600 IN PTR roville.infra.tcc.
rynisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR rynis.infra.tcc.
serethinfratcc.zones.catalog.infra.tcc. 3600 IN PTR sereth.infra.tcc.
silarisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR silaris.infra.tcc.
sylviainfratcc.zones.catalog.infra.tcc. 3600 IN PTR sylvia.infra.tcc.
talwyninfratcc.zones.catalog.infra.tcc. 3600 IN PTR talwyn.infra.tcc.
tarnixinfratcc.zones.catalog.infra.tcc. 3600 IN PTR tarnix.infra.tcc.
thalorinfratcc.zones.catalog.infra.tcc. 3600 IN PTR thalor.infra.tcc.
thyrainfratcc.zones.catalog.infra.tcc. 3600 IN PTR thyra.infra.tcc.
torvalinfratcc.zones.catalog.infra.tcc. 3600 IN PTR torval.infra.tcc.
triloreinfratcc.zones.catalog.infra.tcc. 3600 IN PTR trilore.infra.tcc.
uloriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR uloria.infra.tcc.
ulyriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR ulyria.infra.tcc.
valoriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR valoria.infra.tcc.
vandorinfratcc.zones.catalog.infra.tcc. 3600 IN PTR vandor.infra.tcc.
vandriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR vandria.infra.tcc.
vardisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR vardis.infra.tcc.
vermisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR vermis.infra.tcc.
vesperainfratcc.zones.catalog.infra.tcc. 3600 IN PTR vespera.infra.tcc.
vesperisinfratcc.zones.catalog.infra.tcc. 3600 IN PTR vesperis.infra.tcc.
vionixinfratcc.zones.catalog.infra.tcc. 3600 IN PTR vionix.infra.tcc.
wyncrestinfratcc.zones.catalog.infra.tcc. 3600 IN PTR wyncrest.infra.tcc.
wyrmarinfratcc.zones.catalog.infra.tcc. 3600 IN PTR wyrmar.infra.tcc.
xalithinfratcc.zones.catalog.infra.tcc. 3600 IN PTR xalith.infra.tcc.
xarioninfratcc.zones.catalog.infra.tcc. 3600 IN PTR xarion.infra.tcc.
yaraelinfratcc.zones.catalog.infra.tcc. 3600 IN PTR yarael.infra.tcc.
yloriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR yloria.infra.tcc.
zarvixinfratcc.zones.catalog.infra.tcc. 3600 IN PTR zarvix.infra.tcc.
zeloriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR zeloria.infra.tcc.
zephyriainfratcc.zones.catalog.infra.tcc. 3600 IN PTR zephyria.infra.tcc.
zylariainfratcc.zones.catalog.infra.tcc. 3600 IN PTR zylaria.infra.tcc.
catalog.infra.tcc.      86400   IN      SOA     . . 2024100802 604800 86400 2419200 86400
```

Yep. Now we have a lot of DNS zones. Probably we can retrieve every one with zone transfer. Most probably our flag will be as TXT record in one of these zones. So some easy quick dirty way how to get all TXT records? We can run dig on each of the zone and grep it with TXT:

```
$ for i in $(dig AXFR catalog.infra.tcc @jessiejames.infra.tcc|grep PTR | awk '{print $5}'); do dig AXFR $i @jessiejames.infra.tcc; done | grep TXT

40ae12928dbf450106d8097a7ec875ea.banneron.infra.tcc. 86400 IN TXT "RkxBR3tBdlhPLWlNazctM2JvSC1pWURwfQ=="
```

Decoding it with base64 returns flag: FLAG{AvXO-iMk7-3boH-iYDp}