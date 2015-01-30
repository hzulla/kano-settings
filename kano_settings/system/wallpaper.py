#!/usr/bin/env python

# wallpaper.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Backend wallpaper functions
#


from kano.logging import logger
import os

kdeskrc_home = "/home/{user}/.kdeskrc"


def change_wallpaper(path, name):
    logger.info('set_wallpaper / change_wallpaper image_name:{}'.format(name))

    # home directory
    USER = os.environ['SUDO_USER']
    deskrc_path = kdeskrc_home.format(user = USER)

    # Wallpaper selected
    image_169 = "{}{}-16-9.png".format(path, name)
    image_43 = "{}{}-4-3.png".format(path, name)
    image_1024 = "{}{}-1024.png".format(path, name)

    # Look for the strings
    found = False
    if os.path.isfile(deskrc_path):
        f = open(deskrc_path, 'r')
        newlines = []
        for line in f:
            if "Background.File-medium:" in line:
                line = "  Background.File-medium: {}\n".format(image_1024)
                found = True
            elif "Background.File-4-3:" in line:
                line = "  Background.File-4-3: {}\n".format(image_43)
            elif "Background.File-16-9:" in line:
                line = "  Background.File-16-9: {}\n".format(image_169)
            newlines.append(line)
        f.close()
    if found:

        # Overwrite config file with new lines
        outfile = open(deskrc_path, 'w')
        outfile.writelines(newlines)
        outfile.close()

    # If not found add it
    else:
        with open(deskrc_path, "a") as outfile:
            outfile.write("  Background.File-medium: {}\n".format(image_1024))
            outfile.write("  Background.File-4-3: {}\n".format(image_43))
            outfile.write("  Background.File-16-9: {}\n".format(image_169))

    # Refresh the wallpaper
    cmd = 'sudo -u %s kdesk -w' % USER
    os.system(cmd)
    return 0
