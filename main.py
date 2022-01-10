# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   				      #
#			          Python Code Editor					   		#
#			          Developer: Carbon				       		#
#													   				      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from tkinter import Tk, PhotoImage, Text, Button, Scrollbar, Menu
from tkinter.filedialog import askopenfilename, asksaveasfilename
from idlelib.colorizer import ColorDelegator, make_pat
from idlelib.percolator import Percolator
from os import system, path
from re import compile, S, match

# Editor class & Variables: #

from editor import *

# Editor Window: #

window = Tk()
window.title("Python Editor: Untitled")
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
window.geometry(f'{screenWidth // 2}x{screenHeight // 2}')
window.call('tcl_wordBreakAfter', '', 0) 
window.call('set', 'tcl_wordchars', '[a-zA-Z0-9_]')
window.call('set', 'tcl_nonwordchars', '[^a-zA-Z0-9_]')

# Editor Icon: #

icon = PhotoImage(file = 'logo.png')
window.iconphoto(False, icon)

# Text Editor: #

editor = Editor(window)
editor.insert("end", "" + 0*'\n')
editor.pack()
editor.editor.focus()
window.after(200, editor.draw())

# Text Highlighting: 

highlight = ColorDelegator()
highlight.prog = compile(r'\b(P<M"y"GROUP>tkinter)\b|' + make_pat(), S)
highlight.idprog = compile(r'\s+(\w+)', S)

highlight.tagdefs['COMMENT'] = {'foreground': cmntColor, 'background': backgroundColor}
highlight.tagdefs['KEYWORD'] = {'foreground': keyWordColor, 'background': backgroundColor}
highlight.tagdefs['BUILTIN'] = {'foreground': builtInColor, 'background': backgroundColor}
highlight.tagdefs['STRING'] = {'foreground': stringColor, 'background': backgroundColor}
Percolator(editor.editor).insertfilter(highlight)

# Editor Variables: #

globalPath = ''

# Editor Functions: #

def runCode(*event):
	global globalPath
	if(globalPath == ''):
		if(saveAsFile()):
			command = f'start cmd.exe /k python {globalPath}'
			system(command)
	else:
		saveFile()
		command = f'start cmd.exe /k python {globalPath}'
		system(command)

def newFile(*event):
	global globalPath
	editor.editor.delete('1.0', "end")
	globalPath = ''
	window.title("Python Editor: Untitled")

def openFile(*event):
	global globalPath
	filePath = askopenfilename(filetypes = [('Python Files', '*.py')])
	if(filePath == ''):
			if(globalPath == ''):
				window.title("Python Editor: Untitled")
			else:
				window.title(f"Python Editor: {path.basename(globalPath)}")
			return
	with open(filePath, 'r') as file:
		text = file.read()
		editor.editor.delete('1.0', "end")
		editor.editor.insert('1.0', text)
		file.close()
	globalPath = filePath
	window.title(f"Python Editor: {path.basename(filePath)}")

def saveFile(*event):
	global globalPath
	if(globalPath == ''):
		filePath = asksaveasfilename(filetypes = [('Python Files', '*.py')])
	else:
		filePath = globalPath
		with open(filePath, 'w') as file:
			text = editor.editor.get('1.0', "end")
			file.write(text)
	globalPath = filePath
	window.title(f"Python Editor: {path.basename(filePath)}")

def saveAsFile(*event):
	global globalPath
	filePath = asksaveasfilename(filetypes = [('Python Files', '*.py')])
	if(filePath == ''):
		return
	with open(filePath, 'w') as file:
		text = editor.editor.get('1.0', "end")
		file.write(text)
	globalPath = filePath
	window.title(f"Python Editor: {path.basename(filePath)}")

def copyText(*event): # Auto-bind
   editor.editor.event_generate("<<Copy>>")

def cutText(*event): # Auto-bind
   editor.editor.event_generate("<<Cut>>")

def pasteText(*event): # Auto-bind
   editor.editor.event_generate("<<Paste>>")

def selectAll(*event): # Auto-bind
  	editor.editor.tag_add('sel', '1.0', "end")

# Keybinds: #

window.bind("<Control-s>", saveFile)
window.bind("<Control-f>", saveAsFile)
window.bind("<Control-l>", openFile)
window.bind("<Control-n>", newFile)
window.bind("<Control-b>", runCode)

# Menu & Buttons: #

# Menu:
menu = Menu(window)

filesBar = Menu(menu, tearoff = 0)
editBar = Menu(menu, tearoff = 0)

# New File:
filesBar.add_command(label = "New File", accelerator="Ctrl+N", command = newFile)

# Open:
filesBar.add_command(label = 'Open File', accelerator="Ctrl+L", command = openFile)

# Save:
filesBar.add_command(label = 'Save', accelerator="Ctrl+S", command = saveFile)

# Save As:
filesBar.add_command(label = 'Save As', accelerator="Ctrl+F", command = saveAsFile)

# Copy: 
editBar.add_command(label = 'Copy', accelerator="Ctrl+C", command = copyText)

# Cut: 
editBar.add_command(label = 'Cut', accelerator="Ctrl+X", command = cutText)

# Paste: 
editBar.add_command(label = 'Paste', accelerator="Ctrl+V", command = pasteText)

# Select All: 
editBar.add_command(label = 'Select All', accelerator="Ctrl+A", command = selectAll)

menu.add_command(label = 'Run', accelerator="Ctrl+B", command = runCode)

# Add buttons to the their sections:
menu.add_cascade(label = 'Files', menu = filesBar)
menu.add_cascade(label = 'Edit', menu = editBar)

# Config: #

window.config(menu = menu)

# Window Loop: #

window.mainloop()