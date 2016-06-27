#!/usr/bin/env python3

import re
import shlex
import subprocess
import xtmlib

from xtmlib import xtables_commands
from xtmlib.types import Counter, CounterSet

COMMENT_TAG = "XTM:"

re_chain = re.compile(
    r':(?P<name>[^ ]+) '
    r'(?P<policy>[^ ]+) '
    r'\[(?P<packets_in>\d+):(?P<bytes_in>\d+)\]'
)
re_rule = re.compile(
    r'\[(?P<packets_in>\d+):(?P<bytes_in>\d+)\] (?P<arguments>.*)'
)


def get_counters(ip_version=4):
    xtmlib.debug("Getting counters from current setup.")
    xtmlib.debug_indent(1)
    counters = CounterSet()
    try:
        ipt_output = subprocess.check_output(
            [xtables_commands[ip_version] + "-save", "-c"]
        ).decode()
    except subprocess.CalledProcessError:
        xtmlib.debug(
            "Failed to call %s!" % (xtables_commands[ip_version] + "-save")
        )
        return counters
    table = None

    for line in ipt_output.splitlines():
        line = line.strip()
        counter = None
        if line.startswith("*"):
            # table
            table = line[1:]
            xtmlib.debug("Table '%s'" % table)
            xtmlib.debug_indent(1)
        elif line.startswith(":"):
            # chain
            match = re_chain.match(line)
            chain = match.group("name")
            counter = Counter(
                "%s.%s" % (table, chain),
                int(match.group("packets_in")),
                int(match.group("bytes_in"))
            )
        elif line.startswith("["):
            # rule
            rule = re_rule.match(line)
            args = shlex.split(rule.group("arguments"))
            comment = False
            chain = None
            for arg in args:
                if comment is True:
                    comment = arg
                elif chain is True:
                    chain = arg
                elif arg == "--comment":
                    comment = True
                elif arg in {"-A", "-I", "-R"}:
                    chain = True
            if type(comment) is str and comment.startswith(COMMENT_TAG):
                counter = Counter(
                    "%s.%s.%s" % (table, chain, comment[len(COMMENT_TAG):]),
                    int(rule.group("packets_in")),
                    int(rule.group("bytes_in"))
                )
        elif line == "COMMIT":
            table = None
            xtmlib.debug_indent(-1)
        if counter:
            xtmlib.debug("Counter '%s': %s" % (counter.name, str(counter)))
            counters.add(counter)

    xtmlib.debug_indent(-1)
    xtmlib.debug("Done.")
    return counters
