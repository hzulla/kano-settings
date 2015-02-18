#!/usr/bin/env python
#
# account.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Controls the UI of the account setting

from gi.repository import Gtk, Gdk, GObject
import threading
import os

from kano.gtk3.heading import Heading
import kano.gtk3.kano_dialog as kano_dialog
from kano.gtk3.buttons import KanoButton
from kano.gtk3.labelled_entries import LabelledEntries

from kano.utils import ensure_dir
import kano_settings.common as common
from kano_settings.templates import Template

from kano_settings.system.account import add_user, delete_user, verify_current_password, change_password


ADD_REMOVE_USER_PATH = '/tmp/kano-init/add-remove'


class SetAccount(Gtk.Box):

    def __init__(self, win):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.win = win
        self.win.set_main_widget(self)

        self.win.top_bar.enable_prev()
        self.win.change_prev_callback(self.win.go_to_home)

        self.added_or_removed_account = False

        main_title = _("System account settings")
        main_description = _("Set your account")
        accounts_title = _("Accounts")
        accounts_description = _("Add or remove accounts")
        add_text = _("Add account").upper()
        remove_text = _("Remove account").upper()
        pass_text = _("Change password").upper()

        main_heading = Heading(main_title, main_description)

        self.pass_button = KanoButton(pass_text)
        self.pass_button.pack_and_align()
        self.pass_button.connect("button-release-event", self.go_to_password_screen)
        self.pass_button.connect("key-release-event", self.go_to_password_screen)

        self.add_button = KanoButton(add_text)
        self.add_button.set_size_request(200, 44)
        self.add_button.connect("button-release-event", self.add_account)
        self.add_button.connect("key-release-event", self.add_account)

        self.remove_button = KanoButton(remove_text, color="red")
        self.remove_button.set_size_request(200, 44)
        self.remove_button.connect("button-release-event", self.remove_account_dialog)
        self.remove_button.connect("key-release-event", self.remove_account_dialog)

        button_container = Gtk.Box()
        button_container.pack_start(self.add_button, False, False, 10)
        button_container.pack_start(self.remove_button, False, False, 10)

        button_align = Gtk.Alignment(xscale=0, xalign=0.5)
        button_align.add(button_container)

        accounts_heading = Heading(accounts_title, accounts_description)

        # Check if we already scheduled an account add or remove by checking the file
        added_or_removed_account = os.path.exists(ADD_REMOVE_USER_PATH)
        # Disable buttons if we already scheduled
        if added_or_removed_account:
            self.disable_buttons()

        self.pack_start(main_heading.container, False, False, 0)
        self.pack_start(self.pass_button.align, False, False, 0)
        self.pack_start(accounts_heading.container, False, False, 0)
        self.pack_start(button_align, False, False, 0)

        self.win.show_all()

    def go_to_password_screen(self, widget, event):

        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            self.win.clear_win()
            SetPassword(self.win)

    # Gets executed when ADD button is clicked
    def add_account(self, widget=None, event=None):

        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            # Bring in message dialog box
            dialog_title = _("Reboot the system.")
            dialog_description = _("A new account will be created next time you reboot.")

            kdialog = kano_dialog.KanoDialog(
                dialog_title,
                dialog_description,
                parent_window=self.win
            )
            kdialog.run()
            #
            self.disable_buttons()
            # add new user command
            add_user()
            # Tell user to reboot to see changes
            common.need_reboot = True

    # Gets executed when REMOVE button is clicked
    def remove_account_dialog(self, widget=None, event=None):

        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            dialog_title = _("Are you sure you want to delete the current user?")
            dialog_description = _("You will lose all the data on this account")
            # Bring in message dialog box
            kdialog = kano_dialog.KanoDialog(
                dialog_title,
                dialog_description,
                [
                    {
                        'label': _("Cancel").upper(),
                        'color': 'red',
                        "return_value": 0
                    },
                    {
                        'label': _("OK").upper(),
                        'color': 'green',
                        "return_value": -1
                    }
                ],
                parent_window=self.win
            )
            response = kdialog.run()
            if response == -1:
                self.disable_buttons()
                # Delete current user
                delete_user()

                kdialog = kano_dialog.KanoDialog(
                    _("To finish removing this account, you need to reboot"),
                    _("Do you want to reboot?"),
                    [
                        {
                            'label': _("No").upper(),
                            'color': 'red',
                            "return_value": 0
                        },
                        {
                            'label': _("Yes").upper(),
                            'color': 'green',
                            "return_value": -1
                        }
                    ],
                    parent_window=self.win
                )
                response = kdialog.run()
                if response == -1:
                    os.system("sudo reboot")

    # Disables both buttons and makes the temp 'flag' folder
    def disable_buttons(self):

        self.add_button.set_sensitive(False)
        self.remove_button.set_sensitive(False)
        self.added_or_removed_account = True

        ensure_dir(ADD_REMOVE_USER_PATH)


class SetPassword(Template):

    def __init__(self, win):
        main_title = _("Change your password")
        main_description = ""
        entry_heading_1 = _("Old password")
        entry_heading_2 = _("New password")
        entry_heading_3 = _("Repeat new password")
        description_1 = _("\"kano\" is default")
        description_2 = ""
        description_3 = ""

        kano_text = _("Change password").upper()
        Template.__init__(self, main_title, main_description, kano_text)

        self.labelled_entries = LabelledEntries(
            [{"heading": entry_heading_1, "subheading": description_1},
             {"heading": entry_heading_2, "subheading": description_2},
             {"heading": entry_heading_3, "subheading": description_3}]
        )

        self.entry1 = self.labelled_entries.get_entry(0)
        self.entry1.set_size_request(300, 44)
        self.entry1.set_visibility(False)
        self.entry1.props.placeholder_text = entry_heading_1

        self.entry2 = self.labelled_entries.get_entry(1)
        self.entry2.set_size_request(300, 44)
        self.entry2.set_visibility(False)
        self.entry2.props.placeholder_text = entry_heading_2

        self.entry3 = self.labelled_entries.get_entry(2)
        self.entry3.set_size_request(300, 44)
        self.entry3.set_visibility(False)
        self.entry3.props.placeholder_text = entry_heading_3

        self.entry1.connect("key_release_event", self.enable_button)
        self.entry2.connect("key_release_event", self.enable_button)
        self.entry3.connect("key_release_event", self.enable_button)

        self.entry1.grab_focus()

        self.win = win
        self.win.set_main_widget(self)

        self.box.pack_start(self.labelled_entries, False, False, 0)

        self.win.top_bar.enable_prev()
        self.win.change_prev_callback(self.go_to_accounts)

        self.kano_button.set_sensitive(False)
        self.kano_button.connect("button-release-event", self.apply_changes)
        self.kano_button.connect("key-release-event", self.apply_changes)

        self.win.show_all()

    def apply_changes(self, button, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:

            # This is a callback called by the main loop, so it's safe to
            # manipulate GTK objects:
            watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
            self.win.get_window().set_cursor(watch_cursor)
            self.kano_button.start_spinner()
            self.kano_button.set_sensitive(False)

            def lengthy_process():
                old_password = self.entry1.get_text()
                new_password1 = self.entry2.get_text()
                new_password2 = self.entry3.get_text()

                success = False
                password_verified = verify_current_password(old_password)

                if not password_verified:
                    title = _("Could not change password")
                    description = _("Your old password is incorrect!")
                elif new_password1 == new_password2:
                    title, description, success = self.try_change_password(new_password1)
                else:
                    title = _("Could not change password")
                    description = _("The new passwords don't match! Try again!")

                def done(title, description, success):
                    if success:
                        response = create_success_dialog(title, description, self.win)
                    else:
                        response = create_error_dialog(title, description, self.win)

                    self.win.get_window().set_cursor(None)
                    self.kano_button.stop_spinner()
                    self.clear_text()

                    if response == 0:
                        self.go_to_accounts()

                GObject.idle_add(done, title, description, success)

            thread = threading.Thread(target=lengthy_process)
            thread.start()

    # Returns a title, description and whether the process was successful or not
    def try_change_password(self, new_password):
        success = False

        cmdvalue = change_password(new_password)

        # if password is not changed
        if cmdvalue != 0:
            title = _("Could not change password")
            description = _("Your new password is not long enough or contains special characters.")
        else:
            title = _("Password changed!")
            description = ""
            success = True

        return (title, description, success)

    def go_to_accounts(self, widget=None, event=None):
        self.win.clear_win()
        SetAccount(self.win)

    def clear_text(self):
        self.entry1.set_text("")
        self.entry2.set_text("")
        self.entry3.set_text("")
        self.entry1.grab_focus()

    def enable_button(self, widget, event):
        text1 = self.entry1.get_text()
        text2 = self.entry2.get_text()
        text3 = self.entry3.get_text()
        self.kano_button.set_sensitive(text1 != "" and text2 != "" and text3 != "")


def create_error_dialog(message1=_("Could not change password"), message2="", win=None):
    kdialog = kano_dialog.KanoDialog(
        message1,
        message2,
        [
            {
                'label': _("Go back").upper(),
                'color': 'red',
                'return_value': 0
            },
            {
                'label': _("Try again").upper(),
                'color': 'green',
                'return_value': -1
            }
        ],
        parent_window=win
    )

    response = kdialog.run()
    return response


def create_success_dialog(message1, message2, win):
    kdialog = kano_dialog.KanoDialog(message1, message2,
                                     parent_window=win)
    response = kdialog.run()
    return response
