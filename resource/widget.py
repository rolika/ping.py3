#############
### PING! ###
#############

# Widget classes

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

from tkinter import *

# placeholders
DISC_SIZE = 40 #diameter of a disc
MIN_FIELD_SIZE = 1
MAX_FIELD_SIZE = 12
RULES = """In Ping!, you have to turn around all discs to the opposit color.
When you left-click a disc, all surrounding discs are turned around, except the clicked one.
2x2 is simple, just click on each disc once. 4x4 is simple enough too. Others are very hard, and some configurations don't have a solution at all.
Have fun playing Ping!"""
LICENSE = """Ping!
Copyright (c) 2015 Weisz Roland\nweisz.roland@wevik.hu

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
(License: ISC)"""

class Slider(Scale):
    """ Defines a slider with mousehandling """
    def __init__(self, ro, co, root = None):
        """ Inits itself as a slider with it's grid coords """
        self.root = root
        super().__init__(self.root, length = 200,
                         from_ = float(MIN_FIELD_SIZE),
                         to = float(MAX_FIELD_SIZE),
                         command = self.root.redrawField) #reference to parent
        self.grid(row = ro, column = co, sticky = NW)

    def setHorizontal(self):
        """ Describes a horizontal slider """
        self["orient"], self["cursor"] = HORIZONTAL, "sb_h_double_arrow"
        self.bind("<MouseWheel>", self.mouseWheelH) #Windows, MacOS
        self.bind("<Button-4>", self.mouseWheelH) #Linux ,scroll down
        self.bind("<Button-5>", self.mouseWheelH) #Linux ,scroll up

    def setVertical(self):
        """ Describes a horizontal slider """
        self["orient"], self["cursor"] = VERTICAL, "sb_v_double_arrow"
        self.bind("<MouseWheel>", self.mouseWheelV) #Windows, MacOS
        self.bind("<Button-4>", self.mouseWheelV) #Linux ,scroll down
        self.bind("<Button-5>", self.mouseWheelV) #Linux ,scroll up

    def mouseWheelH(self, event):
        """ Handles scroll wheel over horizontal slider """
        self.set(self.get() + event.delta // 120) #Windows,MacOS
        if event.num == 4: self.set(self.get() + 1) #Linux
        elif event.num == 5: self.set(self.get() - 1)

    def mouseWheelV(self, event):
        """ Handles scroll wheel over vertical slider """
        self.set(self.get() - event.delta // 120) #Windows,MacOS
        if event.num == 4: self.set(self.get() - 1) #Linux
        elif event.num == 5: self.set(self.get() + 1)

class Table(Canvas):
    """ Draws game field """
    def __init__ (self, ro, co, root = None, columns = 4, rows = 4,
                  disc_size = DISC_SIZE):
        """ Game field is drawn upon: rows, columns, disc-size """
        self.root, self.columns, self.rows, self.disc_size =\
            root, columns, rows, disc_size
        self.offset = self.disc_size // 10 #offset from edge and grid
        self.raster = self.disc_size + self.offset * 2 #grid-distance
        self.canvas_width = self.columns * self.raster
        self.canvas_height = self.rows * self.raster
        super().__init__(self.root, width = self.canvas_width,
                         height = self.canvas_height, bg = "ivory")
        self.grid(row = ro, column = co, sticky = NW)

    def gridCoords(self):
        """ Calculates gridline coordinates - two listcomps concatenated """
        return \
        [(x, self.offset, x, self.canvas_height - self.offset) \
         for x in range(0, self.canvas_width, self.raster)] + \
        [(self.offset, y, self.canvas_width - self.offset, y) \
         for y in range(0, self.canvas_height, self.raster)]

    def discCoords(self):
        """ Calculates disc coordinates """
        coords = list()
        for row in range(0, self.canvas_height, self.raster):
            for column in range(0, self.canvas_width, self.raster):
                coords.append((column + self.offset, row + self.offset,
                              column + self.raster - self.offset,
                              row + self.raster - self.offset))
        return coords

    def discsToFlip(self, x, y):
        """ Calculates surrounding disc-indexes """
        indexes, col, row = list(), x // self.raster, y // self.raster
        for co in range(col - 1, col + 2):
            if co < 0: continue
            elif co > self.columns - 1: break
            for ro in range(row - 1, row + 2):
                if ro < 0: continue
                elif ro > self.rows - 1: break
                if ro == row and co == col: continue
                indexes.append(co + ro * self.columns)
        return indexes

class GameMenu(Frame):
    """ Creates the game-menu in an own frame """
    def __init__(self, ro, co, root):
        """ Arguments: grid coordinates & parent """
        self.root = root
        super().__init__(self.root)
        self.grid(row = ro, column = co, columnspan = 3, sticky = W)
        self.createGameMenu()
        self.createHelpMenu()

    def createGameMenu(self):
        """ Creates the game menu for new and restart """
        game = Menubutton(self, text = "Game", relief = RAISED, width = 6)
        game.grid(row = 0, column = 0)
        menu = Menu(game, tearoff = 0)
        menu.add_command(label = "New", command = self.root.newGame)
        menu.add_command(label = "Restart", command = self.root.restartGame)
        menu.add_command(label = "Quit",
                         command = self.root.winfo_toplevel().destroy)
        game["menu"] = menu

    def createHelpMenu(self):
        """ Creates the help menu for rules and about """
        hlp = Menubutton(self, text = "Help", relief = RAISED, width = 6)
        hlp.grid(row = 0, column = 1)
        menu = Menu(hlp, tearoff = 0)
        menu.add_command(label = "Rules", command = self.showRules)
        menu.add_command(label = "About", command = self.showCredit)
        hlp["menu"] = menu

    def showRules(self):
        """ Shows game rules """
        window = Toplevel(self)
        Message(window, width = 200, font = ("Liberation Mono", "10"),
                bg = "ivory", fg = "blue", text = RULES).grid()
        Button(window, text = "OK", command = window.destroy).grid()


    def showCredit(self):
        """ Shows author and license """
        window = Toplevel(self)
        Message(window, width = 300, font = ("Liberation Mono", "10"),
                bg = "ivory", fg = "blue", text = LICENSE).grid()
        Button(window, text = "OK", command = window.destroy).grid()
