#!/usr/bin/env python3

import sys

# debug mode
debug_mode = False
# how many indentation levels to use for the current message
_debug_indent_c = 0

xtables_commands = {
    4: "iptables",
    6: "ip6tables",
}


def debug(message):
    global _debug_indent_c
    if debug_mode:
        print(("    " * _debug_indent_c) + message, file=sys.stderr)


def debug_indent(num):
    global _debug_indent_c
    _debug_indent_c += num
