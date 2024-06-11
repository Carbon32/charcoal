# # # # # # # # # # # # # # # # # # # # #
#                                       #
#           Charcoal Editor             #
#                                       #
# # # # # # # # # # # # # # # # # # # # #

# Imports: #

try: from src.modules import *
except: from modules import *

# Auto-complete: #

class AutoComplete(QThread):
	def __init__(self, path: "str", api: "QsciAPIs") -> None:
		super(AutoComplete, self).__init__(None)
		self.path = path
		self.script: Script = None
		self.api: QsciAPIs = api
		self.completions: list[Completion] = None
		self.line, self.index, self.text = 0, 0, ""

	def run(self) -> None:
		try:
			self.script = Script(self.text, path = self.path)
			self.completions = self.script.complete(self.line, self.index)
			self.load_autocomplete(self.completions)
		except: pass
		self.finished.emit()

	def load_autocomplete(self, completions: "list") -> None:
		self.api.clear()
		for completion in completions: self.api.add(completion.name)
		self.api.prepare()

	def get_completions(self, line: "int", index: "int", text: "float"):
		self.line, self.index, self.text = line, index, text
		self.start()