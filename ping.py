#!/usr/bin/env python3

#############
### PING! ###
#############

# ISC License
#
# Copyright (c) 2015 Weisz Roland weisz.roland@wevik.hu
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

from resource.draw import * #import from sub-directory
from resource.widget import *

# placeholders
START = "READY?"
SOLVED = "GOOD!"

class Ping(Frame):
    """ Main game application """
    def __init__ (self, root = None):
        """ Class initialiser """
        super().__init__(root)
        self.grid(row = 0, column = 0)
        self.table = Label(self) #placeholder for first time run
        self.setWidgets()
        self.menubar.decorateWindow(self.winfo_toplevel())
        self.newGame()

    def newGame(self):
        """ Starts new game """
        self.horizontal.set(4)
        self.vertical.set(4)
        self.restartGame()

    def restartGame(self):
        """ Restarts actual configuration """
        self.redrawField(1) #argument because of event handling

    def setWidgets(self):
        """ Sets horizontal and vertical sliders """
        Label(self, text = str(MIN_FIELD_SIZE)). \
                    grid(row = 1, column = 0, sticky = SE)
        # horizontal slider
        self.horizontal = Slider(1, 1, self)
        self.horizontal.setHorizontal()
        Label(self, text = str(MAX_FIELD_SIZE)). \
                    grid(row = 1, column = 2, sticky = SW)
        # vertical slider
        self.vertical = Slider(2, 0, self)
        self.vertical.setVertical()
        Label(self, text = str(MAX_FIELD_SIZE)).\
                    grid(row = 3, column = 0, sticky = NE)
        # game menu
        self.menubar = GameMenu(0, 0, self)

    def initGrid(self):
        """ Inits gridline objects """
        return [Line(*coords, table = self.table) \
                for coords in self.table.gridCoords()] #argument-unpacking

    def initDiscs(self):
        """ Inits disc objects """
        return [Disc(*coords, table = self.table) \
                for coords in self.table.discCoords()] #argument-unpacking

    def redrawField(self, event):
        """ Redraws game field according to sliders """
        # table
        self.table.grid_forget() #placeholder in __init__ needed!
        self.table = Table(2, 1, self,
                           self.horizontal.get(), self.vertical.get())

        self.table.bind("<Button-1>", self.clickDisc)
        # slider length
        self.horizontal["length"] = self.horizontal.get() * self.table.raster
        self.vertical["length"] = self.vertical.get() * self.table.raster
        # lines
        for line in self.initGrid():
            line.draw()
        # discs
        self.discs = self.initDiscs() #discs needed for further process
        for disc in self.discs:
            disc.draw()
        # message
        self.message = Msg(self.table.canvas_width // 2,  self.table.canvas_height // 2, START, self.table)
        self.message.draw()

    def clickDisc(self, event):
        """ Handles mouseclicks on canvas """
        self.message.change("")
        for i in self.table.discsToFlip(event.x, event.y):
            self.discs[i].flip()
        for i in self.discs: #check disc colors
            if i.check(): return 0 #if front color, jump out
        self.message.change(SOLVED) #else solved

if __name__ == "__main__":
    Ping().mainloop()
