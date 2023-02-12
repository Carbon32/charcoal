# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                      Charcoal Editor                      #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Auto-complete: #

class AutoComplete(QThread):
    def __init__(self, path, api):
        super(AutoComplete, self).__init__(None)

        # Properties:

        self.path = path
        self.script: Script = None
        self.api: QsciAPIs = api
        self.completions: list[Completion] = None
        self.line, self.index, self.text = 0, 0, ""

    def run(self):
        try:
            self.script = Script(self.text, path = self.path)
            self.completions = self.script.complete(self.line, self.index)
            self.load_autocomplete(self.completions)
        except:
            pass
            
        self.finished.emit()

    def load_autocomplete(self, completions):
        self.api.clear()
        for completion in completions:
            self.api.add(completion.name)

        self.api.prepare()

    def get_completions(self, line, index, text):
        self.line, self.index, self.text = line, index, text
        self.start()

