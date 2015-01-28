#!/usr/bin/env python

# set_about.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import os
from gi.repository import Gtk
from kano.gtk3.kano_dialog import KanoDialog
from kano.gtk3.buttons import OrangeButton, KanoButton
from kano_profile.paths import legal_dir
from kano_settings.common import media
from kano_settings.system.about import (get_current_version, get_space_available, get_temperature)


class SetAbout(Gtk.Box):
    selected_button = 0
    initial_button = 0

    def __init__(self, win):

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.win = win
        self.win.set_main_widget(self)
        self.win.top_bar.enable_prev()
        self.win.change_prev_callback(self.win.go_to_home)

        image = Gtk.Image.new_from_file(media + "/Graphics/about-screen.png")

        version_align = self.create_version_align()
        space_available = get_space_available()
        temperature = get_temperature()

        space_align = self.create_other_align(space_available)
        temperature_align = self.create_other_align(temperature)

        terms_and_conditions = OrangeButton(_("Terms and conditions"))
        terms_and_conditions.connect("button_release_event", self.show_terms_and_conditions)

        self.kano_button = KanoButton(_("Go back").upper())
        self.kano_button.pack_and_align()

        image.set_margin_top(30)
        self.pack_start(image, False, False, 10)
        self.pack_start(version_align, False, False, 2)
        self.pack_start(space_align, False, False, 2)
        self.pack_start(temperature_align, False, False, 2)
        self.pack_start(terms_and_conditions, False, False, 3)
        self.pack_start(self.kano_button.align, False, False, 10)

        self.kano_button.connect("button-release-event", self.win.go_to_home)
        self.kano_button.connect("key-release-event", self.win.go_to_home)

        # Refresh window
        self.win.show_all()

    def create_version_align(self):
        text = get_current_version()
        label = Gtk.Label(text)
        label.get_style_context().add_class("about_version")

        align = Gtk.Alignment(xalign=0.5, xscale=0, yalign=0, yscale=0)
        align.add(label)

        return align

    def create_other_align(self, text):
        label = Gtk.Label(text)
        label.get_style_context().add_class("about_label")

        align = Gtk.Alignment(xalign=0.5, xscale=0, yalign=0, yscale=0)
        align.add(label)

        return align

    def show_terms_and_conditions(self, widget, event):

        legal_text = ''
        for file in os.listdir(legal_dir):
            with open(legal_dir + file, 'r') as f:
                legal_text = legal_text + f.read() + '\n\n\n'

        kdialog = KanoDialog(_("Terms and conditions"), "",
                             scrolled_text=legal_text,
                             parent_window=self.win)
        kdialog.run()
