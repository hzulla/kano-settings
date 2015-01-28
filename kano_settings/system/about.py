#!/usr/bin/env python

# about.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Contains the about screen backend functions

import subprocess


def get_current_version():
    version_number = "?"
    with open('/etc/kanux_version', 'r') as f:
        output = f.read().strip()
        version_number = output.split("-")[-1]
    return _("Kano OS v.{version}").format(version = version_number)


def get_space_available():
    output = subprocess.check_output("LANG=C df -h | grep rootfs", shell=True)
    items = output.strip().split(" ")
    items = filter(None, items)
    total_space = items[1]
    space_used = items[2]
    return _("Disk space used: {used}B / {total}B").format(used = space_used, total = total_space)


def get_temperature():
    temperature = 0
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        output = f.read().strip()
        temperature = int(output) / 1000.0
    return _(u"Temperature: {celsius:.1f}\N{DEGREE SIGN}C").format(celsius = temperature)
