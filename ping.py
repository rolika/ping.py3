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

class Slider(Scale):
    """ Defines a slider with mousehandling """
    def __init__(self, ro, co, root = None):
        """ Inits itself as a slider with it's grid coords """        
        self.root = root
        super().__init__(self.root, length = 200, from_ = 1.0, to = 20.0,
                         command = None)
        self.grid(row = ro, column = co)

    def setHorizontal(self):
        """ Describes a horizontal slider """
        self.["orient"], self.["cursor"] = HORIZONTAL, "sb_h_double_arrow"

    def setVertical(self):
        """ Describes a horizontal slider """
        self.["orient"], self.["cursor"] = VERTICAL, "sb_v_double_arrow"
        
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

class Ping(Frame):
    """ Main game application """
    def __init__ (self, root = None):
        """ Class initialiser """
        super().__init__(root)
        self.grid(row = 0, column = 0)
        self.setSliders()
    
    def setSliders(self):
        """ Sets horizontal and vertical sliders """
        Label(self, text = "1").grid(row = 1, column = 0) #common start value
        # horizontal slider
        self.horizontal = Scale(self, orient = HORIZONTAL, length = 200,
            cursor = "sb_h_double_arrow", showvalue = 1,
            from_ = 1.0, to = 20.0, command = None)
        self.horizontal.grid(row = 1, column = 1)
        Label(self, text = "20").grid(row = 1, column = 2)
        self.horizontal.set(4)
        self.horizontal.bind("<MouseWheel>", self.mouseWheelH)
        # vertical slider
        self.vertical = Scale(self, orient = VERTICAL, length = 200,
            cursor = "sb_v_double_arrow", showvalue = 1,
            from_ = 1.0, to = 20.0, command = None)
        self.vertical.grid(row = 2, column = 0)
        Label(self, text = "20").grid(row = 3, column = 0)
        self.vertical.set(4)
        self.vertical.bind("<MouseWheel>", self.mouseWheelV)

    def mouseWheelH(self, event):
        """ Handles scroll wheel over horizontal slider """
        self.horizontal.set(self.horizontal.get() + int(event.delta / 120))
        
    def mouseWheelV(self, event):
        """ Handles scroll wheel over vertical slider """
        self.vertical.set(self.vertical.get() - int(event.delta / 120))
        
if __name__ == "__main__":
    Ping().mainloop()
