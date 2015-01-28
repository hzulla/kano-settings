#!/usr/bin/env python

# set_mouse.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from gi.repository import Gdk
from kano_settings.templates import RadioButtonTemplate
from .config_file import get_setting, set_setting
from kano_settings.system.mouse import change_mouse_speed


modes = ["Slow", "Normal", "Fast"]


class SetMouse(RadioButtonTemplate):
    selected_button = 0
    initial_button = 0

    def __init__(self, win):
        title = _("Mouse")
        description = _("Pick your speed")
        kano_label = _("Apply changes").upper()
        option1 = _("Slow")
        option2 = _("Normal")
        option3 = _("Fast")
        desc1 = _("(Requires less move precision)")
        desc2 = _("(Default)")
        desc3 = _("(Better for wide screens)")

        RadioButtonTemplate.__init__(self, title, description, kano_label,
                                     [[option1, desc1],
                                      [option2, desc2],
                                      [option3, desc3]])
        self.win = win
        self.win.set_main_widget(self)

        # Show the current setting by electing the appropriate radio button
        self.current_setting()
        self.selected_button = self.initial_button
        self.get_button(self.initial_button).set_active(True)

        self.win.top_bar.enable_prev()
        self.win.change_prev_callback(self.reset_and_go_home)

        self.kano_button.connect("button-release-event", self.set_mouse)
        self.kano_button.connect("key-release-event", self.set_mouse)

        self.win.show_all()

    def reset_and_go_home(self, widget=None, event=None):
        self.selected_button = self.initial_button
        self.get_button(self.initial_button).set_active(True)
        self.win.go_to_home()

    def set_mouse(self, button, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:

            #  Mode   speed
            # Slow     1
            # Normal  default
            # High     10

            # Mode has no changed
            if self.initial_button == self.selected_button:
                self.win.go_to_home()
                return

            try:
                config = modes[self.selected_button]
            except IndexError:
                config = "Slow"

            # Update config
            set_setting("Mouse", config)
            self.win.go_to_home()

    def current_setting(self):
        mouse = get_setting("Mouse")
        try:
            self.initial_button = modes.index(mouse)
        except ValueError:
            pass

    def on_button_toggled(self, button, selected):

        if button.get_active():
            self.selected_button = selected
            # Apply changes so speed can be tested
            change_mouse_speed(self.selected_button)

