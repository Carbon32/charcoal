# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			             Editor Class					    #
#			          Developer: Carbon				       	#
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from tkinter import Frame, Canvas, Text, Scrollbar
from variables import *

class Editor(Frame):
	def __init__(self, window, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
		self.editor = Text(window, font = ("Monaco", 13), bg = backgroundColor, fg = textColor, insertbackground = cursorColor, undo = True, padx = 20, pady = 10)
		self.scrollbar = Scrollbar(window, orient = "vertical", command = self.editor.yview)
		self.editor.configure(yscrollcommand = self.scrollbar.set, tabs = tabSize)
		self.lines = Numbering(window, width = 25, bg = backgroundColor)
		self.lines.attach(self.editor)
		self.scrollbar.pack(side= "right", fill = "y")
		self.lines.pack(side = "left", fill = "both", padx = 0, pady = 0)
		self.editor.pack(side = "top", fill = "both", expand = True, padx = 0, pady = 0)
		self.editor.bind("<Key>", self.onPressDelay)
		self.editor.bind("<Button-1>", self.lines.draw)
		self.scrollbar.bind("<Button-1>", self.onScrollPress)
		self.editor.bind("<MouseWheel>", self.onPressDelay)

	def onScrollPress(self, *args):
		self.scrollbar.bind("<B1-Motion>", self.lines.draw)

	def onScrollRelease(self, *args):
		self.scrollbar.unbind("<B1-Motion>", self.lines.draw)

	def onPressDelay(self, *args):
		self.after(2, self.lines.draw)

	def get(self, *args, **kwargs):
		return self.editor.get(*args, **kwargs)

	def insert(self, *args, **kwargs):
		return self.editor.insert(*args, **kwargs)

	def delete(self, *args, **kwargs):
		return self.editor.delete(*args, **kwargs)

	def index(self, *args, **kwargs):
		return self.editor.index(*args, **kwargs)

	def draw(self):
		self.lines.draw()


class Numbering(Canvas):
	def __init__(self, *args, **kwargs):
		Canvas.__init__(self, *args, **kwargs, highlightthickness = 0)
		self.widget = None

	def attach(self, widget):
		self.widget = widget

	def draw(self, *args):
		self.delete("all")

		i = self.widget.index("@0,0")
		while(True):
			line = self.widget.dlineinfo(i)
			if(line is None): break
			y = line[1]
			lineNumber = str(i).split(".")[0]
			self.create_text(10, y+2, anchor = "nw", text = lineNumber, fill = textColor)
			i = self.widget.index("%s+1line" % i)
