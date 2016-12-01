#!/usr/bin/env python3

import os.path
import socket
import xtmlib

from xtmlib.types import Address

def ip_list(ip_version, path, filename):
    """
    Return a list of address strings with netmask (if supplied) which is read
    from a file. Only those addresses matching the IP version are returned.
    Parameters:
        ip_version The IP version (e.g. 4)
        filename The file to read adddresses from
    """
    listfile_path = os.path.join(path, filename)
    xtmlib.debug("Reading IPv{} addresses from '{}'".format(ip_version, listfile_path))
    addresses = []
    if ip_version == 4:
        ip_version = socket.AF_INET
    else:
        ip_version = socket.AF_INET6
    with open(listfile_path) as listfile:
        for line in listfile:
            # skip comments
            if line.startswith("#"):
                continue
            line = line.rstrip()
            # split the line into address and netmask
            address, _, netmask = line.partition("/")
            # try to parse the address
            try:
                socket.inet_pton(ip_version, address)
            except:
                continue
            addresses.append(line)
    return addresses
