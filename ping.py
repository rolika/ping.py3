#!/usr/bin/env python3

#############
### PING! ###
#############

# Given is a table with discs in rows and columns.
# If player clicks on a disc, all surrounding discs are turned.
# Aim is to turn all discs. Not all configurations have a solution.
# 2015 Weisz Roland

#global placeholders
DISC_SIZE = 40 #diameter of a disc
MIN_ROW = MIN_COLUMN = 1
MAX_ROW = MAX_COLUMN = 16

from tkinter import *

class Disc:
    """ Defines a disc and it's handling methods """
    def __init__(self, x0, y0, x1, y1, table = None,
                 disc_front = "orange", disc_back = "gray"):
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
    
    def draw(self):
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
        super().__init__(self.root, length = 200, from_ = 1.0, to = 16.0,
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
        self.set(self.get() + int(event.delta / 120)) #Windows,MacOS
        if event.num == 4: self.set(self.get() + 1) #Linux
        elif event.num == 5: self.set(self.get() - 1)
        
    def mouseWheelV(self, event):
        """ Handles scroll wheel over vertical slider """
        self.set(self.get() - int(event.delta / 120)) #Windows,MacOS
        if event.num == 4: self.set(self.get() - 1) #Linux
        elif event.num == 5: self.set(self.get() + 1)
        
class Table(Canvas):
    """ Draws game field """
    def __init__ (self, ro, co, root = None, columns = 4, rows = 4,
                  disc_size = 40):
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
        self.disc_size = 40 #diameter
        self.table = Label(self) #placeholder for first time run
        self.setSliders()
        self.redrawField(1) #argument because of event handling
    
    def setSliders(self):
        """ Sets horizontal and vertical sliders """
        Label(self, text = "1").grid(row = 1, column = 0, sticky = SE)
        # horizontal slider
        self.horizontal = Slider(1, 1, self)
        self.horizontal.setHorizontal()
        Label(self, text = "16").grid(row = 1, column = 2, sticky = SW)
        self.horizontal.set(4)
        # vertical slider
        self.vertical = Slider(2, 0, self)
        self.vertical.setVertical()
        Label(self, text = "16").grid(row = 3, column = 0, sticky = NE)
        self.vertical.set(4)

    def initGrid(self):
        """ Inits gridline objects """
        return [Line(*coords, table = self.table) \
                for coords in self.table.gridCoords()]  

    def initDiscs(self):
        """ Inits disc objects """
        return [Disc(*coords, table = self.table) \
                for coords in self.table.discCoords()]

    def redrawField(self, event):
        """ Redraws game field according to sliders """
        # table
        self.table.grid_forget()
        self.table = Table(2, 1, self,
                           self.horizontal.get(), self.vertical.get())
        # slider length
        self.horizontal["length"] = self.horizontal.get() * self.table.raster
        self.vertical["length"] = self.vertical.get() * self.table.raster
        # lines
        for line in self.initGrid(): line.draw()
        # discs
        self.discs = self.initDiscs()
        for disc in self.discs: disc.draw()
        
if __name__ == "__main__":
    Ping().mainloop()
