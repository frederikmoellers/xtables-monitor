# xtables-monitor
Write firewall rules using templates!

## Dependencies
* Python >= 3.5
* [netifaces](https://pypi.python.org/pypi/netifaces)
* ip[6]tables-save and ip[6]tables-restore

## How to write rules
Check the examples directory. `xtables-monitor` is based on Jinja2 and uses its template mechanism. A more detailed documentation will follow.

## How to apply rules
Use the `-a` command line switch.

## How to install
For the moment, you can place the executable anywhere and the `xtmlib` directory either next to it or somewhere in your Python search path. Templates can either be given using paths (relative to CWD or absolute) on the command line or they can be placed in `/etc/xtables-monitor` and then be specified using their filename on the command line.

If you want to have `xtables-monitor` adapt to IP address changes, place a hook in the appropriate directory in `/etc/network/`. At some point `xtables-monitor` will be able to run as a daemon and detect IP address changes itself, but until then workarounds like this are necessary.

## Example
``` bash
$ ./xtables-monitor -i 4 examples/lan.xtm
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
