# ---------------------------------------------------- #
#													   #
#			     Python Code Editor					   #
#			     Developer: Carbon				       #
#													   #
# ---------------------------------------------------- #

# Imports: #

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
import subprocess

# Editor Window: #

window = Tk()
window.title("Py Editor:")
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
window.geometry(f'{screenWidth // 2}x{screenHeight // 2}')

# Text Editor: #

textEditor = Text()
textEditor.pack(side = "top", fill = "both", expand = True, padx = 0, pady = 0)

# Output:

outPut = Text(height = 7)
outPut.pack(side = "bottom", fill = "both", expand = True, padx = 0, pady = 0)

Percolator(textEditor).insertfilter(ColorDelegator()) # Placeholder

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
			outPut.insert('1.0', error)
		else:
			outPut.insert('1.0', result)

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

