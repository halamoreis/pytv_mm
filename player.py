#! /usr/bin/python

#
# gtk example/widget for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

"""VLC Gtk Widget classes + example application.

This module provides two helper classes, to ease the embedding of a
VLC component inside a pygtk application.

VLCWidget is a simple VLC widget.

DecoratedVLCWidget provides simple player controls.

When called as an application, it behaves as a video player.

$Id$
"""

import gtk
gtk.gdk.threads_init()

import sys
import os.path
import vlc
import time

from gettext import gettext as _

#To use Thread
from threading import Thread

#Import Server
import PyTVStreamClient

# Create a single vlc.Instance() to be shared by (possible) multiple players.
instance = vlc.Instance()

class VLCWidget(gtk.DrawingArea):
    """Simple VLC widget.

    Its player can be controlled through the 'player' attribute, which
    is a vlc.MediaPlayer() instance.
    """
    def __init__(self, *p):
        gtk.DrawingArea.__init__(self)
        self.player = instance.media_player_new()
        def handle_embed(*args):
            if sys.platform == 'win32':
                self.player.set_hwnd(self.window.handle)
            else:
                self.player.set_xwindow(self.window.xid)
            return True
        self.connect("map", handle_embed)
        self.set_size_request(320, 200)

class DecoratedVLCWidget(gtk.VBox):
    """Decorated VLC widget.

    VLC widget decorated with a player control toolbar.

    Its player can be controlled through the 'player' attribute, which
    is a Player instance.
    """
    def __init__(self, *p):
        gtk.VBox.__init__(self)
        self._vlc_widget = VLCWidget(*p)
        self.player = self._vlc_widget.player
        self.pack_start(self._vlc_widget, expand=True)
        self._toolbar = self.get_player_control_toolbar()
        self.pack_start(self._toolbar, expand=False)

    def get_player_control_toolbar(self):
        """Return a player control toolbar
        """
        tb = gtk.Toolbar()
        tb.set_style(gtk.TOOLBAR_ICONS)
        for text, tooltip, stock, callback in (
            (_("Play"), _("Play"), gtk.STOCK_MEDIA_PLAY, lambda b: self.player.play()),
            (_("Pause"), _("Pause"), gtk.STOCK_MEDIA_PAUSE, lambda b: self.player.pause()),
            (_("Stop"), _("Stop"), gtk.STOCK_MEDIA_STOP, lambda b: self.player.stop()),
            ):
            b=gtk.ToolButton(stock)
            b.set_tooltip_text(tooltip)
            b.connect("clicked", callback)
            tb.insert(b, -1)
        tb.show_all()
        return tb

class VideoPlayer:
    """Example simple video player.
    """
    def __init__(self):
        self.vlc = DecoratedVLCWidget()
    
    def open(self, fname):
        self.vlc.player.set_media(instance.media_new(fname))
	self.vlc.player.play()
       	

    def main(self):
        w = gtk.Window()
        w.add(self.vlc)
        w.show_all()
        w.connect("destroy", gtk.main_quit)

class player(Thread):
    def __init__ (self):
              Thread.__init__(self)
              self.player = VideoPlayer()

    def run(self):
              gtk.main()
    
    def start_player(self):
              print "Open the player "
              self.player.main();

    def open(self, fname):
              print "Open file %s" % fname
	      self.player.open(fname)
    
    def play(self):
              print "Play!"
	      self.player.vlc.player.play();


if __name__ == '__main__':
    client = PyTVStreamClient.Client();
    p = player()
    p.start_player();

    #p.open("videos/Nivarna-Poly.mp4");

    p.start();
    client.start();
    i = 0;
    videofile = "videosout/testfile"+str(i).zfill(3)+".webm"
    time.sleep(5) #sleep necessario para comecar a baixar o primeiro pkg
    print "Tocando..."
    while (os.path.exists(videofile) is True ):
      p.open("videosout/testfile"+str(i).zfill(3)+".webm")
      time.sleep(10) # sleep enquanto toca o video
      i = i + 1
      videofile = "videosout/testfile"+str(i).zfill(3)+".webm"


