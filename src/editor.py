# # # # # # # # # # # # # # # # # # # # #
#                                       #
#           Charcoal Editor             #
#                                       #
# # # # # # # # # # # # # # # # # # # # #

# Imports: #

try: from src.lexer import *
except: from lexer import *

# Editor: #

class Editor(QsciScintilla):
	def __init__(self, parent: "None" = None, path: "Path" = None, is_python_file: "bool" = True):
		super(Editor, self).__init__(parent)
		self.cursorPositionChanged.connect(self._cursorPositionChanged)

		self.path = path.absolute()
		self.is_python_file = is_python_file

		self.setUtf8(True)
		self.editor_font = QFont("Ebrima")
		self.editor_font.setPointSize(12)
		self.setFont(self.editor_font)

		self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
		self.setIndentationGuides(True)
		self.setTabWidth(4)
		self.setIndentationsUseTabs(True)
		self.setAutoIndent(True)

		self.setAutoCompletionSource(QsciScintilla.AcsAll)
		self.setAutoCompletionThreshold(1)
		self.setAutoCompletionCaseSensitivity(False)
		self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

		self.setCaretForegroundColor(QColor("#d3d3d3"))
		self.setCaretLineVisible(True)
		self.setCaretWidth(2)
		self.setCaretLineBackgroundColor(QColor("#494646"))

		self.setEolMode(QsciScintilla.EolWindows)
		self.setEolVisibility(False)

		self.setMarginType(0, QsciScintilla.NumberMargin)
		self.setMarginWidth(0, "00000")
		self.setMarginsForegroundColor(QColor("#d3d3d3"))
		self.setMarginsBackgroundColor(QColor("#2E2E2E"))
		self.setMarginsFont(self.editor_font)

		self.init_lexer()

	def keyPressEvent(self, event: "QKeyEvent") -> None:
		if(event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Space): self.autoCompleteFromAll()
		else: return super().keyPressEvent(event)

	def _cursorPositionChanged(self, line: "int", index: "int"):
		if(self.is_python_file): self.auto_complete.get_completions(line + 1, index, self.text())

	def init_lexer(self):
		if(self.is_python_file):
			self.lexer = PythonLexer(self)
			self.lexer.setDefaultFont(self.editor_font)
			self.__api = QsciAPIs(self.lexer)
			self.auto_complete = AutoComplete(self.path, self.__api)
			self.setLexer(self.lexer)
		else:
			self.setPaper(QColor("#2E2E2E"))
			self.setColor(QColor("#d3d3d3"))

