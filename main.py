# ---------------------------------------------------- #
#													   #
#			     Python Code Editor					   #
#			     Developer: Carbon				       #
#													   #
# ---------------------------------------------------- #

# Imports: #

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Editor Window: #

window = Tk()
window.title("Py Editor:")

# Text Editor: #

textEditor = Text()
textEditor.pack()

# Editor Variables: #

globalPath = ''

# Editor Functions: #

def runCode():
	code = textEditor.get('1.0', END)
	exec(code)

def newFile():
	global globalPath
	textEditor.delete('1.0', END)
	globalPath = ''

def openFile():
	global globalPath
	path = askopenfilename(filetypes = [('Python Files', '*.py')])
	with open(path, 'r') as file:
		text = file.read()
		textEditor.delete('1.0', END)
		textEditor.insert('1.0', text)
	globalPath = path

def saveFile():
	global globalPath
	if(globalPath == ''):
		path = asksaveasfilename(filetypes = [('Python Files', '*.py')])
	else:
		path = globalPath
		with open(path, 'w') as file:
			text = textEditor.get('1.0', END)
			file.write(text)


def saveAsFile():
	global globalPath
	path = asksaveasfilename(filetypes = [('Python Files', '*.py')])
	with open(path, 'w') as file:
		text = textEditor.get('1.0', END)
		file.write(text)
	globalPath = path

# Menu & Buttons: #

# Run:
menu = Menu(window)

filesBar = Menu(menu, tearoff = 0)
runBar = Menu(menu, tearoff = 0)

# New File:
filesBar.add_command(label = "New File", command = newFile)

# Open:
filesBar.add_command(label = 'Open File', command = openFile)

# Save:
filesBar.add_command(label = 'Save', command = saveFile)

# Save As:
filesBar.add_command(label = 'Save As...', command = saveAsFile)

# Run: 
runBar.add_command(label = "Run", command = runCode)

# Add buttons to the their sections:
menu.add_cascade(label = 'Files', menu = filesBar)
menu.add_cascade(label = 'Run', menu = runBar)

# Config: #

window.config(menu = menu)

# Window Loop: #

window.mainloop()

