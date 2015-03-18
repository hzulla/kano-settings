#!/usr/bin/env python

# set_appearence.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# This page has the screensaver and wallpaper options on different tabs

import os
import shutil

from kano.utils import run_cmd

from gi.repository import Gtk, Gdk
from kano_settings.set_wallpaper import SetWallpaper
from kano_settings.set_screensaver import SetScreensaver


class SetAppearance(Gtk.Notebook):

    def __init__(self, win):

        Gtk.Notebook.__init__(self)

        background = Gtk.EventBox()
        background.get_style_context().add_class('set_appearance_window')
        background.add(self)

        self.win = win
        self.win.set_main_widget(background)
        self.win.top_bar.enable_prev()
        self.win.change_prev_callback(self.win.go_to_home)

        # Modify set_wallpaper so it doesn't add itself to the window
        wallpaper_widget = SetWallpaper(self.win)
        screensaver_widget = SetScreensaver(self.win)
        reset_widget = SetResetDesktop(self.win)

        wallpaper_label = Gtk.Label(_("Wallpaper").upper())
        screensaver_label = Gtk.Label(_("Screensaver").upper())
        general_label = Gtk.Label(_("General").upper())

        # Add the screensaver and wallpaper tabs
        self.append_page(wallpaper_widget, wallpaper_label)
        self.append_page(screensaver_widget, screensaver_label)
        self.append_page(reset_widget, general_label)

        self.win.show_all()


from kano.gtk3.buttons import KanoButton
from kano.gtk3.kano_dialog import KanoDialog


class SetResetDesktop(Gtk.Box):

    def __init__(self, win):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.win = win

        reset_button = KanoButton(text = _("Reset your desktop").upper(), color='orange')
        reset_button.connect('clicked', self.reset_button_cb)
        reset_button.pack_and_align()
        reset_button.align.set(0.5, 0.5, 0, 0)

        self.pack_start(reset_button.align, True, True, 0)

    def reset_button_cb(self, button):
        kdialog = KanoDialog(
            title_text = _("This will reset all of your desktop changes"),
            description_text = _("Do you want to continue?"),
            button_dict=[
                {
                    'label': _("No").upper(),
                    'color': 'red',
                    'return_value': False
                },
                {
                    'label': _("Yes").upper(),
                    'color': 'green',
                    'return_value': True
                }
            ],
            parent_window=self.win
        )

        do_reset_changes = kdialog.run()
        if do_reset_changes:
            self.reset_desktop()

    def restore_lxpanel_configuration(self):
        userid=os.getuid()
        groupid=os.getgid()
        original_lxpanel_path='/etc/skel/.config/lxpanel/'
        user_lxpanel_path=os.path.join('/home/' + os.getenv('SUDO_USER'), '.config/lxpanel')

        # remove the current local copy
        shutil.rmtree(user_lxpanel_path, ignore_errors=True)

        # re-create the copy from the skeleton
        shutil.copytree(original_lxpanel_path, user_lxpanel_path, symlinks=False, ignore=None)
        for root, dirs, files in os.walk(user_lxpanel_path):
            for name in files:
                os.chown(os.path.join(root, name), userid, groupid)
                
        _, _, _ = run_cmd('lxpanelctl restart')

    def reset_desktop(self):
        # Add functionality here
        self.restore_lxpanel_configuration()
