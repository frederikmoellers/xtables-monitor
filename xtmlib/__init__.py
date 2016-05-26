#!/usr/bin/env python3

import sys

debug_mode = False
debug_indent_c = 0

def debug(message):
    global debug_indent_c
    if debug_mode:
        print(("    " * debug_indent_c) + message, file = sys.stderr)

def debug_indent(num):
    global debug_indent_c
    debug_indent_c += num
