#!/usr/bin/env python

# set_overclock.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from gi.repository import Gdk
from kano_settings.templates import RadioButtonTemplate
import kano_settings.common as common
from kano_settings.boot_config import get_config_value
from kano_settings.system.overclock import change_overclock_value

# 0 = None
# 1 = Modest
# 2 = Medium
# 3 = High
# 4 = Turbo
modes = ["None", "Modest", "Medium", "High", "Turbo"]


class SetOverclock(RadioButtonTemplate):
    selected_button = 0
    initial_button = 0
    boot_config_file = "/boot/config.txt"

    def __init__(self, win):

        title = _("Overclock your processor")
        description = _("Make your computer's brain think faster, but run hotter.")
        kano_label = _("Apply changes").upper()
        option1 = _("None")
        option2 = _("Modest")
        option3 = _("Medium")
        option4 = _("High")
        option5 = _("Turbo")
        desc1 = _("( 700MHz ARM, 250MHz core, 400MHz SDRAM, 0 overvolt)")
        desc2 = _("( 800MHz ARM, 250MHz core, 400MHz SDRAM, 0 overvolt)")
        desc3 = _("( 900MHz ARM, 250MHz core, 450MHz SDRAM, 2 overvolt)")
        desc4 = _("( 950MHz ARM, 250MHz core, 450MHz SDRAM, 6 overvolt)")
        desc5 = _("(1000MHz ARM, 500MHz core, 600MHz SDRAM, 6 overvolt)")

        RadioButtonTemplate.__init__(self, title, description, kano_label,
                                     [[option1, desc1],
                                      [option2, desc2],
                                      [option3, desc3],
                                      [option4, desc4],
                                      [option5, desc5]])
        self.win = win
        self.win.set_main_widget(self)

        # Show the current setting by electing the appropriate radio button
        self.current_setting()
        self.selected_button = self.initial_button
        self.get_button(self.initial_button).set_active(True)

        self.win.top_bar.enable_prev()
        self.win.change_prev_callback(self.win.go_to_home)

        self.kano_button.connect("button-release-event", self.set_overclock)
        self.kano_button.connect("key-release-event", self.set_overclock)

        self.win.show_all()

    def set_overclock(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:

            #  Mode      arm_freq       core_freq      sdram_freq     over_voltage
            #  None;      700 MHz ARM,  250 MHz core,  400 MHz SDRAM, 0 overvolt
            #  Modest;    800 MHz ARM,  250 MHz core,  400 MHz SDRAM, 0 overvolt
            #  Medium;    900 MHz ARM,  250 MHz core,  450 MHz SDRAM, 2 overvolt
            #  High;      950 MHz ARM,  250 MHz core,  450 MHz SDRAM, 6 overvolt
            #  Turbo;    1000 MHz ARM,  500 MHz core,  600 MHz SDRAM, 6 overvolt

            # Mode has no changed
            if self.initial_button == self.selected_button:
                self.win.go_to_home()
                return

            change_overclock_value(modes[self.selected_button])

            # Tell user to reboot to see changes
            common.need_reboot = True

            self.win.go_to_home()

    def current_setting(self):
        freq = get_config_value('arm_freq')

        if freq == 700:
            self.initial_button = 0
        elif freq == 800:
            self.initial_button = 1
        elif freq == 900:
            self.initial_button = 2
        elif freq == 950:
            self.initial_button = 3
        elif freq == 1000:
            self.initial_button = 4

    def on_button_toggled(self, button, selected):

        if button.get_active():
            self.selected_button = selected
