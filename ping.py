#!/usr/bin/env python3
# PING!
# Given is a table with discs in rows and columns.
# If player clicks on a disc, all surrounding discs are turned.
# Aim is to turn all discs. Not all configurations have a solution.
# 2015 Weisz Roland

from tkinter import *

class Disc():
    """ Defines a disc and it's handling methods """
    def __init__(self, x0, y0, x1, y1,
                 disc_front = "orange", disc_back = "gray",
                 table = None):
        """ Inits values for disc """
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1 #coords of disc
        self.disc_front, self.disc_back = disc_front, disc_back #colors
        self.color = self.disc_front #default color
        self.table = table #canvas
    
    def draw(self):
        """ Draws a disc with default color"""
        self.table.create_oval(self.x0, self.y0, self.x1, self.y1,
                               fill = self.color, width = 0)
    
    def flip(self):
        """ Flips a disc to opposit color """
        self.color = self.disc_front if self.color == self.disc_back\
            else self.disc_back
        self.table.itemconfigure(self, fill = self.color)
    
    def check(self):
        """ Checks if disc is turned over """
        if self.color == self.disc_front: return True
        return False

class Line:
    """ Defines a line for the grid """
    def __init__(self, x0, y0, x1, y1, grid_color = "gray", grid_line = 1,
                 table = None):
        """ Inits values  """
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1 #line coords
        self.grid_color, self.grid_line = grid_color, grid_line #color&width
        self.table = table #canvas
    
    def draw(self, canvas):
        """ Draws line on canvas """
        self.table.create_line(self.x0, self.y0, self.x1, self.y1,
                               width = self.grid_line, fill = self.grid_color)

class Message:
    """ Defines a message """
    def __init__(self, x, y, text = ""):
        """ Inits values """
        self.x, self.y, self.text = x, y, text #coords at text is displayed
        self.font_height, self.font_color, self.font_type =\
            32, "red", "monospace" #font properties
    
    def draw(self, canvas):
        """ Draws message on canvas, centered """
        self.table.create_text(self.x, self.y, text = self.text,\
            font = (self.font_type, self.font_height, self.font_color))
    
    def change(self, message):
        """ Changes text to message """
        self.table.itemconfigure(self, text = message)

class Table(Canvas):
    """ Draws game field """

    def __init__ (self, root = None, columns = 5, rows = 5, disc_size = 50):
        """ Game field is drawn upon: rows, columns, disc-size """
        self.root, self.columns, self.rows, self.disc_size = root, columns, rows, disc_size
        self.wid, self.hei = self.columns*disc_size, self.rows*disc_size
        super().__init__(self.root, width = self.wid, height = self.hei, bg = "ivory")
        self.grid()
        self.bind("<Button-1>", self.root.flipDisc)
        self.drawGrid()

    def drawGrid(self):
        """ Draws grid on game field """
        grid_color, self.offset = "light gray", self.disc_size//10
        for x in range(0, self.wid, self.disc_size): #vertical lines
            self.create_line(x, self.offset, x, self.hei-self.offset, fill = grid_color)
        for y in range(0, self.hei, self.disc_size): #horizontal lines
            self.create_line(self.offset, y, self.wid-self.offset, y, fill = grid_color)

    def surroundDiscs(self, row, col):
        """ Calculates surrounding disc-indexes """
        indexes = list()
        for co in range(col-1, col+2):
            if co < 0: continue
            elif co > self.columns-1: break
            for ro in range(row-1, row+2):
                if ro < 0: continue
                elif ro > self.rows-1: break
                if ro == row and co == col: continue
                indexes.append(co + ro*self.columns)
        return indexes

class ReverseIt(Frame):
    """ Main game application """

    def __init__ (self, root = None):
        """ Class initialiser """
        super().__init__(root)
        self.table = Table(self, 6, 6, 40) #setup game field
        self.setupDiscs()
        self.grid(row = 0, column = 0)

    def setupDiscs(self):
        """ Fills game grid with discs """
        self.discs = list()
        for row in range(self.table.rows):
            y0, y1 = row*self.table.disc_size + self.table.offset, (row + 1)*self.table.disc_size - self.table.offset
            for col in range(self.table.columns):
                x0, x1 = col*self.table.disc_size + self.table.offset, (col + 1)*self.table.disc_size - self.table.offset
                self.discs.append(Disc(x0, y0, x1, y1, self.table, 0))

    def flipDisc(self, event):
        """ Turns disc over """
        row, col = event.y // self.table.disc_size, event.x // self.table.disc_size
        disc_index = col + row*self.table.columns
        for disc in self.table.surroundDiscs(row, col):
            self.discs[disc].turnDisc()
        if self.checkStatus():
            quit("Good job!")

    def checkStatus(self):
        """ Checks if all discs are turned over """
        for disc in self.discs:
            if disc.status:
                return False
        return True #all discs were turned

if __name__ == "__main__":
    ReverseIt().mainloop()
