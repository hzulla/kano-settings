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


MODES = ['Slow', 'Normal', 'Fast']
LABELS = {
    'Slow': _("Slow"),
    'Normal': _("Normal"),
    'Fast': _("Fast")
}


class SetMouse(RadioButtonTemplate):
    selected_button = 0
    initial_button = 0

    def __init__(self, win):
        RadioButtonTemplate.__init__(
            self,
            _("Mouse"),
            _("Pick your speed:"),
            _("Apply changes").upper(),
            [
                [LABELS['Slow'], _("(requires less move precision)")],
                [LABELS['Normal'], _("(Default)")],
                [LABELS['Fast'], _("(better for wide screens)")]
            ]
        )
        self.win = win
        self.win.set_main_widget(self)

        # Show the current setting by electing the appropriate radio button
        try:
            self.initial_button = MODES.index(get_setting('Mouse'))
        except ValueError:
            self.initial_button = 0

        self.selected_button = self.initial_button
        self.get_button(self.initial_button).set_active(True)

        self.win.top_bar.enable_prev()
        self.win.change_prev_callback(self.reset_and_go_home)

        self.kano_button.connect('clicked', self.set_mouse)
        self.win.show_all()

    def reset_and_go_home(self, widget=None, event=None):
        change_mouse_speed(self.initial_button)
        self.win.go_to_home()

    def set_mouse(self, button):
        try:
            config = MODES[self.selected_button]
        except IndexError:
            config = 'Normal'

        if not config == get_setting('Mouse'):
            set_setting('Mouse', config)
        self.win.go_to_home()

    def on_button_toggled(self, button, selected):
        if button.get_active():
            self.selected_button = selected
            # Apply changes so speed can be tested
            change_mouse_speed(selected)

