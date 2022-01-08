# ---------------------------------------------------- #
#													   #
#			     Python Code Editor					   #
#			     Developer: Carbon				       #
#													   #
# ---------------------------------------------------- #

# Imports: #

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import idlelib.colorizer as colorizer
import idlelib.percolator as percolator
import subprocess
import os
import re

# Editor Window: #

window = Tk()
window.title("Python Editor: Untitled")
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
window.geometry(f'{screenWidth // 2}x{screenHeight // 2}')

# Editor Icon: #

icon = PhotoImage(file = 'logo.png')
window.iconphoto(False, icon)

# Text Editor: #

textEditor = Text(window, font=("Monaco", 15), bg = "#2D3132", fg = "#FFFFFF")
textEditor.pack(side = "top", fill = "both", expand = True, padx = 0, pady = 0)

# Output:

outPut = Text(height = 8)
outPut.pack(side = "bottom", fill = "both", expand = False, padx = 0, pady = 0)

# Text Highlighting: 

highlight = colorizer.ColorDelegator()
highlight.prog = re.compile(r'\b(P<MYGROUP>tkinter)\b|' + colorizer.make_pat(), re.S)
highlight.idprog = re.compile(r'\s+(\w+)', re.S)

highlight.tagdefs['COMMENT'] = {'foreground': '#BACBE7', 'background': '#2D3132'}
highlight.tagdefs['KEYWORD'] = {'foreground': '#5FD66B', 'background': '#2D3132'}
highlight.tagdefs['BUILTIN'] = {'foreground': '#F29020', 'background': '#2D3132'}
highlight.tagdefs['STRING'] = {'foreground': '#1E69EB', 'background': '#2D3132'}
percolator.Percolator(textEditor).insertfilter(highlight)

# Scroll Bar: 

scrollBarY = Scrollbar(textEditor, orient = VERTICAL)
scrollBarY.pack(side = RIGHT, fill = Y, padx = 0)
scrollBarY.config(command = textEditor.yview)
textEditor.config(yscrollcommand = scrollBarY.set)

# Editor Variables: #

globalPath = ''

# Editor Functions: #

def runCode():
	global globalPath
	if(globalPath == ''):
		saveAsFile()
	else:
		saveFile()
		outPut.delete('1.0', END)
		command = f'python {globalPath}'
		process = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
		result, error = process.communicate()
		if(error):
			outPut.config(background="white", foreground="red")
			outPut.insert('1.0', error)
		else:
			outPut.config(background="white", foreground="green")
			outPut.insert('1.0', result)

def newFile():
	global globalPath
	textEditor.delete('1.0', END)
	globalPath = ''
	window.title(f"Python Editor: Untitled")

def openFile():
	global globalPath
	path = askopenfilename(filetypes = [('Python Files', '*.py')])
	if(path == ''):
			return
	with open(path, 'r') as file:
		text = file.read()
		textEditor.delete('1.0', END)
		textEditor.insert('1.0', text)
	globalPath = path
	window.title(f"Python Editor: {os.path.basename(path)}")

def saveFile():
	global globalPath
	if(globalPath == ''):
		path = asksaveasfilename(filetypes = [('Python Files', '*.py')])
	else:
		path = globalPath
		with open(path, 'w') as file:
			text = textEditor.get('1.0', END)
			file.write(text)
	window.title(f"Python Editor: {os.path.basename(path)}")

def saveAsFile():
	global globalPath
	path = asksaveasfilename(filetypes = [('Python Files', '*.py')])
	if(path == ''):
		return
	with open(path, 'w') as file:
		text = textEditor.get('1.0', END)
		file.write(text)
	globalPath = path
	window.title(f"Python Editor: {os.path.basename(path)}")

def copyText():
   textEditor.event_generate("<<Copy>>")

def cutText():
   textEditor.event_generate("<<Cut>>")

def pasteText():
   textEditor.event_generate("<<Paste>>")

def selectAll():
  	textEditor.tag_add('sel', '1.0', END)

# Menu & Buttons: #

# Run:
menu = Menu(window)

filesBar = Menu(menu, tearoff = 0)
editBar = Menu(menu, tearoff = 0)

# New File:
filesBar.add_command(label = "New File", command = newFile)

# Open:
filesBar.add_command(label = 'Open File', command = openFile)

# Save:
filesBar.add_command(label = 'Save', command = saveFile)

# Save As:
filesBar.add_command(label = 'Save As...', command = saveAsFile)

# Copy: 
editBar.add_command(label = 'Copy (CTRL + C)', command = copyText)

# Cut: 
editBar.add_command(label = 'Cut (CTRL + X)', command = cutText)

# Paste: 
editBar.add_command(label = 'Paste (CTRL + V)', command = pasteText)

# Select All: 
editBar.add_command(label = 'Select All (CTRL + A)', command = selectAll)

# Run:
menu.add_command(label = "Run", command = runCode)

# Add buttons to the their sections:
menu.add_cascade(label = 'Files', menu = filesBar)
menu.add_cascade(label = 'Edit', menu = editBar)

# Config: #

window.config(menu = menu)

# Window Loop: #

window.mainloop()

