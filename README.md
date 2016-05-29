# xtables-monitor
Write firewall rules using templates!

## Installation
Run `setup.py install`. It should automatically check for (Python) dependencies and will install the package.
Copy the examples to or create your own templates in `/etc/xtables-monitor`.

## Dependencies
* Python >= 3.5
* ip[6]tables-save and ip[6]tables-restore
* [Jinja2](http://jinja.pocoo.org/)
* [netifaces](https://pypi.python.org/pypi/netifaces)

## How to write rules
Check the examples directory. `xtables-monitor` is based on Jinja2 and uses its template mechanism. A more detailed documentation will follow.

## How to apply rules
Use the `-a` command line switch.

## How to react to IP address changes
For the moment, you have to install hooks in `/etc/network/if-*.d` or call the execuable yourself.

## Example
``` bash
$ xtables-monitor -i 4 examples/lan.xtm
```

```
*raw
:PREROUTING ACCEPT [1248:1225640]
:OUTPUT ACCEPT [1204:175650]
COMMIT
*nat
:PREROUTING ACCEPT [83:20726]
:POSTROUTING ACCEPT [142:14494]
:OUTPUT ACCEPT [142:14494]
COMMIT
*mangle
:PREROUTING ACCEPT [1248:1225640]
:INPUT ACCEPT [1246:1225576]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [1204:175650]
:POSTROUTING ACCEPT [1211:176396]
COMMIT
*filter
:INPUT DROP [844:1171925]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [788:111247]
[0:0] -A INPUT -i wlan0 -s 192.168.0.2/255.255.255.0 -m comment --comment "XTM:allow-local-wlan0-1" -j ACCEPT
[0:0] -A INPUT -m comment --comment "XTM:reject" -j REJECT
COMMIT
```
