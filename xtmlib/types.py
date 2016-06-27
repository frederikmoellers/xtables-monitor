#!/usr/bin/env python3

import socket


class _Item:
    """
    General item class.
    Supports sorting and converting to a string.
    """
    def __init__(self, name=None):
        if name is None:
            name = hex(id(self))
        self.name = name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name


class _ItemSet:
    """
    A set of items.
    Supports element access using ["name"] and get("name")
    Supports iteration and access to a list of members via all() and reversed()
    """
    def __init__(self, item_type):
        self._items = {}
        self._item_type = item_type

    def add(self, item):
        self._items[item.name] = item

    def all(self):
        for item in self:
            yield item

    def get(self, name):
        return self[name]

    def __contains__(self, item):
        return item in self._items

    def __delitem__(self, key):
        del self._items[key]

    def __getitem__(self, key):
        if key not in self._items:
            self._items[key] = self._item_type()
        return self._items[key]

    def __iter__(self):
        for item in self._items.values():
            yield item

    def __len__(self):
        return len(self._items)

    def __reversed__(self):
        return reversed(self._items)

    def __setitem__(self, key, value):
        self._items[key] = value


class Counter(_Item):
    """
    A packet/byte counter from iptables-save for iptables-restore
    """
    def __init__(self, name=None, packets_in=0, bytes_in=0):
        super(Counter, self).__init__(name=name)
        self.packets_in = packets_in
        self.bytes_in = bytes_in

    def __str__(self):
        return "[%d:%d]" % (self.packets_in, self.bytes_in)


class CounterSet(_ItemSet):
    """
    A set of Counter instances
    """
    def __init__(self):
        super(CounterSet, self).__init__(Counter)


class Address(_Item):
    """
    An IPv4/6 address
    Also saves the subnet mask and a number for uniqueness among all addresses
    of a given interface
    """
    def __init__(self, addr, netmask, num, ip_version):
        super().__init__()
        self.addr = addr
        self.netmask = netmask
        self.num = num
        self.ip_version = ip_version

    def __lt__(self, other):
        if self.ip_version != other.ip_version:
            return self.ip_version < other.ip_version
        if self.addr == other.addr:
            return self.num < other.num
        if self.ip_version == 4:
            ip_family = socket.AF_INET
        else:
            ip_family = socket.AF_INET6
        return (
            socket.inet_pton(ip_family, self.addr) <
            socket.inet_pton(ip_family, other.addr)
        )

    def __str__(self):
        return self.addr


class Interface(_Item):
    """
    A network interface
    """
    def __init__(self, name=None):
        super(Interface, self).__init__(name)
        self.addresses = []


class InterfaceSet(_ItemSet):
    """
    A set of network interfaces
    """
    def __init__(self):
        super(InterfaceSet, self).__init__(Interface)
