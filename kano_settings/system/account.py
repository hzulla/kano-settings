#!/usr/bin/env python

# account.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Contains the account screen backend functions

import os
import pam
from kano.utils import get_user_unsudoed, run_cmd
from kano_world.functions import has_token


# Needs sudo permission
def add_user():
    os.system("kano-init newuser")


# Needs sudo permission
def delete_user():
    os.system('kano-init deleteuser {}'.format(get_user_unsudoed()))
    # back up profile
    if has_token():
        os.system("kano-sync --sync --backup")


# Returns True if password matches system password, else returns False
def verify_current_password(password):
    # Verify the current password in the first text box
    # Get current username
    username, e, num = run_cmd("echo $SUDO_USER")

    # Remove trailing newline character
    username = username.rstrip()

    if not pam.authenticate(username, password):
        # Could not verify password
        return False

    return True


# Successfully changed password is returns 0, else is successful
def change_password(new_password):
    out, e, cmdvalue = run_cmd("echo $SUDO_USER:{} | chpasswd".format(new_password))
    return cmdvalue
