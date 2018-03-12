#!/usr/bin/env python3

import netifaces
import socket
import xtmlib

from xtmlib.types import Address, Interface, InterfaceSet


def get_interfaces(ip_version=4):
    """
    Retrieve network interface information and return a list of Interface
    instances.
    """
    interfaces = InterfaceSet()
    xtmlib.debug("Getting interface information")
    xtmlib.debug_indent(1)
    for interface in netifaces.interfaces():
        interface = Interface(interface)
        # skip localhost
        if str(interface) == "lo":
            continue
        # get addresses of given family
        if ip_version == 4:
            family = netifaces.AF_INET
        else:
            family = netifaces.AF_INET6
        interface_addresses = netifaces.ifaddresses(interface.name)
        if family not in interface_addresses:
            continue
        # print interface name
        xtmlib.debug("Interface %s" % str(interface))
        xtmlib.debug_indent(1)
        interface_addresses = interface_addresses[family]
        # process each address
        for interface_address in interface_addresses:
            # strip trailing "%ifname" for IPv6
            addr = interface_address["addr"]
            # for IPv4, the netmask might be invisible
            if ip_version == 4:
                # convert address to byte sequence to check the first byte
                addr = socket.inet_pton(socket.AF_INET, addr)
                # from https://en.wikipedia.org/wiki/IPv4_subnetting_reference
                if "netmask" in interface_address:
                    netmask = interface_address["netmask"].partition("/")[0]
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
                netmask = interface_address["netmask"].partition("/")[0]
            # create Address instance
            address = Address(addr, netmask, 0, ip_version)
            xtmlib.debug(
                "Address %d: %s/%s" % (
                    address.num, str(address), address.netmask)
            )
            # add address to interface instance
            interface.addresses.append(address)
        xtmlib.debug_indent(-1)
        # sort and enumerate addresses for interface
        """
        we do this here so the numbering is persistent for a given set of
        addresses (regardless of their order)
        """
        interface.addresses.sort()
        num = 1
        for addr in interface.addresses:
            addr.num = num
            num += 1
        interfaces.add(interface)
    xtmlib.debug_indent(-1)
    xtmlib.debug("Done.")
    return interfaces
