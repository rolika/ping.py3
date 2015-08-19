#!/usr/bin/env python3

#############
### PING! ###
#############

# Given is a table with discs in rows and columns.
# If player clicks on a disc, all surrounding discs are turned.
# Aim is to turn all discs. Not all configurations have a solution.
# 2015 Weisz Roland

from resource.draw import * #import from sub-directory
from resource.widget import *

class Ping(Frame):
    """ Main game application """
    def __init__ (self, root = None):
        """ Class initialiser """
        super().__init__(root)
        self.grid(row = 0, column = 0)
        #self.disc_size = 40 #diameter
        self.table = Label(self) #placeholder for first time run
        self.setSliders()
        self.redrawField(1) #argument because of event handling

    def setSliders(self):
        """ Sets horizontal and vertical sliders """
        Label(self, text = str(MIN_FIELD_SIZE)). \
                    grid(row = 1, column = 0, sticky = SE)
        # horizontal slider
        self.horizontal = Slider(1, 1, self)
        self.horizontal.setHorizontal()
        Label(self, text = str(MAX_FIELD_SIZE)). \
                    grid(row = 1, column = 2, sticky = SW)
        self.horizontal.set(4)
        # vertical slider
        self.vertical = Slider(2, 0, self)
        self.vertical.setVertical()
        Label(self, text = str(MAX_FIELD_SIZE)).\
                    grid(row = 3, column = 0, sticky = NE)
        self.vertical.set(4)

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
        for line in self.initGrid(): line.draw()
        # discs
        self.discs = self.initDiscs() #discs needed for further process
        for disc in self.discs: disc.draw()
        # message
        self.message = Msg(self.table.canvas_width // 2,  self.table.canvas_height // 2, "READY", self.table)
        self.message.draw()

    def clickDisc(self, event):
        """ Handles mouseclicks on canvas """
        self.message.change("")
        for i in self.table.discsToFlip(event.x, event.y):
            self.discs[i].flip()
        for i in self.discs:
            if i.check(): return 0
        self.message.change("GOOD!")

if __name__ == "__main__":
    Ping().mainloop()
