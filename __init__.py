##
#   Project: gespeaker - A GTK frontend for espeak  
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2013 Fabio Castelli
#   License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
# 
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
# 
# On Debian GNU/Linux systems, the full text of the GNU General Public License
# can be found in the file /usr/share/common-licenses/GPL-2.
##

PLUGIN_NAME = 'Telepathy'
PLUGIN_VERSION = '0.1'
PLUGIN_DESCRIPTION = 'Interface for Telepathy received messages'
PLUGIN_AUTHOR = 'Fabio Castelli'
PLUGIN_ICON = '%s/icon.svg' % __path__[0]
PLUGIN_WEBSITE = ''

import dbus
import dbus.mainloop.glib
from plugins import GespeakerPlugin, register_plugin

class GespeakerPlugin_Telepathy(GespeakerPlugin):
  def __init__(self, name, version, description, author, icon, website):
    "Module initialization"
    GespeakerPlugin.__init__(self, name, version, description, author, icon, website)
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    bus.add_signal_receiver(self.message_received, 
      dbus_interface='org.freedesktop.Telepathy.Channel.Type.Text',
      signal_name = 'Received'
    )

  def on_uiready(self, ui):
    self.ui = ui

  def message_received(self, msgid, timestamp, sender, msgtype, flags, message):
    "New message received"
    self.logger('message_received(%d, %d, %d, %d, %d, %s)' % (
      msgid, timestamp, sender, msgtype, flags, message))
    self.ui.proxy['text.set'](message, 0)
    self.ui.proxy['espeak.play'](None, None)

plugin = GespeakerPlugin_Telepathy(
  PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, 
  PLUGIN_AUTHOR, PLUGIN_ICON, PLUGIN_WEBSITE)
register_plugin(PLUGIN_NAME, plugin)
