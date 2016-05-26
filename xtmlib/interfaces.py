#!/usr/bin/env python3

import netifaces
import socket
import xtmlib

from xtmlib.types import Address, Interface, InterfaceSet

def get_interfaces(ip_version = 4):
    """
    Retrieve network interface information and return a list of Interface
    instances.
    """
    interfaces = InterfaceSet()
    xtmlib.debug("Getting interface information")
    xtmlib.debug_indent(1)
    ifaces = netifaces.interfaces()
    for iface in netifaces.interfaces():
        interface = Interface(iface)
        # skip localhost
        if iface == "lo":
            continue
        # get addresses of given family
        if ip_version == 4:
            family = netifaces.AF_INET
        else:
            family = netifaces.AF_INET6
        ifaddresses = netifaces.ifaddresses(iface)
        if not family in ifaddresses:
            continue
        # print interface name
        xtmlib.debug("Interface %s" % str(interface))
        xtmlib.debug_indent(1)
        ifaddresses = ifaddresses[family]
        # process each address
        for ifaddress in ifaddresses:
            # strip trailing "%ifname" for IPv6
            addr = ifaddress["addr"]
            # for IPv4, the netmask might be invisible
            if ip_version == 4:
                # convert address to byte sequence to check the first byte
                addr = socket.inet_pton(socket.AF_INET, addr)
                # from https://en.wikipedia.org/wiki/IPv4_subnetting_reference
                if "netmask" in ifaddress:
                    netmask = ifaddress["netmask"]
                elif addr[0] < 128:
                    netmask = "255.0.0.0"
                elif addr[0] < 192:
                    netmask = "255.255.0.0"
                elif addr[0] < 224:
                    netmask = "255.255.255.0"
                else:
                    netmask = "255.255.255.255"
                addr = socket.inet_ntop(socket.AF_INET, addr)
            else:
                addr = addr.partition("%")[0]
                netmask = ifaddress["netmask"]
            # create Address instance
            address = Address(addr, netmask, 0, ip_version)
            xtmlib.debug("Address %d: %s/%s" % (address.num, str(address), address.netmask))
            # add address to interface instance
            interface.addresses.append(address)
        xtmlib.debug_indent(-1)
        # sort and enumerate addresses for interface
        # we do this here so the numbering is persistent for a given set of addresses (regardless of their order)
        interface.addresses.sort()
        num = 1
        for addr in interface.addresses:
            addr.num = num
            num += 1
        interfaces.add(interface)
    xtmlib.debug_indent(-1)
    xtmlib.debug("Done.")
    return interfaces
