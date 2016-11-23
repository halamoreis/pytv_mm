#! /usr/bin/python
# coding=utf-8
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
        self.mediaList = instance.media_list_new()
        # Agora o player deve ser um tocador de playlist(media_list)!
        self.player = instance.media_list_player_new()
        # Seta a lista para o player
        self.player.set_media_list(self.mediaList)
        # seta o player para o media_list_player
        self.player.set_media_player(self._vlc_widget.player)
        # self.player = self._vlc_widget.player
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
    def __init__(self, numberVideosOnPlaylist, client, nextFragment):
        self.vlc = DecoratedVLCWidget()
        self.numberVideosOnPlaylist = numberVideosOnPlaylist
        self.client = client
        self.nextFragment = nextFragment
        self.resolucao = resolucaoInicial

        evm = self.vlc.player.event_manager()
        evm.event_attach(vlc.EventType().MediaListPlayerNextItemSet, self.event_handler_nextMedia)


    # Invocado para tratar o evento quando uma mídia (fragmento) é tocado.
    def event_handler_nextMedia(self, event):
        print "****   ***"
        print "* Rolou um evento agora!"
        print "****   %s " % (event)
        print "****   ***"
        # Um vídeo já foi tocado.
        self.numberVideosOnPlaylist -= 1
        # Adicionar novas mídias baixadas à playlist.
        videoPath = client.getVideo(codigoVideo, self.resolucao, self.nextFragment)
        if(videoPath != False):
            self.addMedia(videoPath)
            self.nextFragment += 1
        else:
            time.sleep(2)
        # Solicita novas mídias
        client.requestVideo(codigoVideo, self.resolucao, self.nextFragment)
        self.nextFragment += 1



    # Utilizado apenas para o primeiro play.
    def open(self, fname):
        self.vlc.mediaList.add_media(instance.media_new(fname))
        # self.vlc.player.set_media(instance.media_new(fname))
        self.vlc.player.play()

    def addMedia(self, fname):
        print "Adicionando à playlist '%s'" % (fname)
        self.vlc.mediaList.add_media(instance.media_new(fname))
        # Um vídeo foi adicionado.
        self.numberVideosOnPlaylist += 1

    def main(self):
        w = gtk.Window()
        w.add(self.vlc)
        w.show_all()
        w.connect("destroy", gtk.main_quit)


# Thread do Player VLC
class PlayerThread(Thread):
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
    # Representa a quantidade de fragmentos que o buffer comporta
    tamBuffer = 4
    # Representa o código do vídeo a ser tocado (correspondente à tabela de vídeos)
    codigoVideo = 1
    # Representa a resolução inicial
    resolucaoInicial = 1

    client = PyTVStreamClient.Client();
    p = PlayerThread()
    p.start_player();

    #p.open("videos/Nivarna-Poly.mp4");

    p.start();
    # client.start();
    # i = 0;
    # videofile = "videosout/v1res3_"+str(i).zfill(3)+".mp4"
    print "rodando a playlist..."

    # TODO Inicialmente baixar fragmentos para encher o buffer (1 = resolução mais baixa)
    # Iterando entre número de fragmentos a serem baixados
    for fragNumber in range(0, tamBuffer):
        client.requestVideo(codigoVideo, resolucaoInicial, fragNumber)

    # Adiciona à playlist os fragmentos iniciais que foram baixados.
    fragNumber = 0
    while(True):
        if( -1 != client.wasReceivedVideo(codigoVideo, resolucaoInicial, fragNumber)):
            # Se conseguiu receber o vídeo, então adicionao à media list do player.
            p.player.addMedia(client.getVideo(codigoVideo, resolucaoInicial, fragNumber))
            fragNumber += 1
        else:
            time.sleep(0.2)

    # Ao conseguir adicionar todos os fragmentos, começa a tocar a playlist.
    """ A partir desse momento a adição de novos fragmentos é tratada assincronamente
    >>> pela função event_handler_next_media.
    """
    p.play()



    # i = 1
    # videofile = "videosout/v1res3_" + str(i).zfill(3) + ".mp4"
    # while ( True):
    #     if(os.path.exists(videofile)):
    #         print "Arquivo '%s' encontrado!" % (videofile)
    #         videofile = "videosout/v1res3_" + str(i).zfill(3) + ".mp4"
    #         p.open(videofile)
    #         i += 1
    #     else:
    #         print "Não encontrei o arquivo. Vou dormir..."
    #     time.sleep(2)  # sleep enquanto toca o video


    print "fializando..."

