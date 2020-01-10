#
# keyboard.py - keyboard backend data object
#
# Brent Fox <bfox@redhat.com>
# Mike Fulbright <msf@redhat.com>
# Jeremy Katz <katzj@redhat.com>
# Lubomir Rintel <lkundrak@v3.sk>
#
# Copyright 2002 Red Hat, Inc.
# Copyright 2009 Lubomir Rintel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import dbus
import string
import os
from subprocess import call
import keyboard_models

class Keyboard():
    def __init__(self):
        self._mods = keyboard_models.KeyboardModels()

        self.type = "PC"
        self.beenset = 0
        self.config = []

        # default to us
        self.set("us")

        try:
            bus = dbus.SystemBus()
            hal = dbus.Interface(bus.get_object("org.freedesktop.Hal","/org/freedesktop/Hal/Manager"),"org.freedesktop.Hal.Manager")
            kbs = hal.FindDeviceByCapability("input.keyboard")
            if len(kbs) == 0:
                self.type = "Serial"
            else:
                self._var ("KEYBOARDTYPE", "pc")
            kb = dbus.Interface(bus.get_object("org.freedesktop.Hal", kbs[0]), 'org.freedesktop.Hal.Device')
            if kb.GetPropertyString("info.product").startswith("Sun Type"):
                self.type == "Sun"
                self._var ("KEYBOARDTYPE", "sun")
        except:
            pass

    def _get_models(self):
        return self._mods.get_models()
    modelDict = property(_get_models)

    def _var (self, name, value = None):
        found = 0
        for line in self.config:
                if line[1] == name:
                        found = 1
                        break
        if not found:
                line = [None, None, None]
        # get or set?
        if not value:
            return line[2]
        line[1:3] = (name, value)
        line[0] = '{0}="{1}"\n'.format (name, value)
        if not found:
                self.config.append (line)

    def set(self, keytable):
        if self.type != "Serial":
            kb = self.modelDict[keytable]
            self._var ("KEYTABLE", keytable)
            self._var ("MODEL", kb[2])
            self._var ("LAYOUT", kb[1])
            self._var ("VARIANT", kb[3])
            self._var ("OPTIONS", kb[4])

    def get(self):
        return self._var ("KEYTABLE")

    def getKeymapName(self):
        kbd = self.modelDict[self.get()]
        if not kbd:
            return ""
        (name, layout, model, variant, options) = kbd
        return name
      
    def __getitem__(self, item):
        table = self._var ("KEYTABLE")
        if not self.modelDict.has_key(table):
            raise KeyError, "No such keyboard type %s" % (table,)

        kb = self.modelDict[table]
        if item == "rules":
            return "xorg"
        elif item == "model":
            return kb[2]
        elif item == "layout":
            return kb[1]
        elif item == "variant":
            return kb[3]
        elif item == "options":
            return kb[4]
        elif item == "name":
            return kb[0]
        elif item == "keytable":
            return table
        else:
            raise KeyError, item

    def read(self, instPath = "/"):
        try:
            file = open(instPath + "/etc/sysconfig/keyboard", "r")
        except:
            return
        self.config = []
        while 1:
                line = file.readline ()
                if not line:
                        break
                (name, value) = line.rstrip("\n").split ('=')
                self.config.append ([line, name, value.strip ('"'), 0])
        self.beenset = 1

    def write(self, instPath = "/"):
	file = open(instPath + "/etc/sysconfig/keyboard", "w")
	for line in self.config:
                file.write (line[0]);
        try:
            os.unlink(instPath + "/etc/sysconfig/console/default.kmap")
        except:
            pass

    def writeKS(self, f):
        f.write("keyboard %s\n" % (self.get(),))

    def activate(self):
        # XXX do isys.loadkeys
        console_kbd = self.get()
        if not console_kbd:
            return

        # Call loadkeys to change the console keymap
        if os.access("/bin/loadkeys", os.X_OK):
            command = "/bin/loadkeys"
        elif os.access("/usr/bin/loadkeys", os.X_OK):
            command = "/usr/bin/loadkeys"
        else:
            command = "/bin/loadkeys"
        argv = [ command, console_kbd ]

        if os.access(argv[0], os.X_OK) == 1:
            call (argv)

        try:
            kbd = self.modelDict[console_kbd]
        except KeyError:
            return

        if not kbd:
            return
        (name, layout, model, variant, options) = kbd

        # only set the X keyboard map if running X
        if not os.environ.has_key("DISPLAY"):
            return

        argv = [ "/usr/bin/setxkbmap", "-layout", layout ]

        # XXX setxkbmap(1) needs one -option flag for each option
        if options:
            argv = argv + [ "-option", options ]

        if variant:
            argv = argv + [ "-variant", variant ]

        if os.access(argv[0], os.X_OK) == 1:
            call (argv)

    def dracutSetupString(self):
        args = ""
        keyboardtype = self._var("KEYBOARDTYPE")
        keytable = self._var("KEYTABLE")

        if keyboardtype:
             args += " KEYBOARDTYPE=%s" % keyboardtype
        if keytable:
             args += " KEYTABLE=%s" % keytable

        return args
