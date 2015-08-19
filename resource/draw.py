#############
### PING! ###
#############

# Draw-element classes
# 2015 Weisz Roland

#from tkinter import *

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