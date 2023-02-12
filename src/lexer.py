# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                      Charcoal Editor                      #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.search import *

# Lexer: #

class PythonLexer(QsciLexerCustom):
    def __init__(self, parent):
        super(PythonLexer, self).__init__(parent)

        # Properties:

        self.setDefaultColor(QColor("#abb2bf"))
        self.setDefaultPaper(QColor("#2E2E2E"))
        self.setDefaultFont(QFont("Consolas", 14))

        # Keywords:

        self.keywords = keyword.kwlist

        # Built-in Functions:

        self.builtin_functions = [name for name, _object in vars(builtins).items() if isinstance(_object, types.BuiltinFunctionType)]

        # Color IDs:

        self.ids = {
                    "Default": [0, "#abb2bf", "#2E2E2E"], "Keyword": [1, "#c678dd", "#2E2E2E"], "Types": [2, "#56b6c2", "#2E2E2E"], "String": [3, "#98c379", "#2E2E2E"],
                    "Keyargs": [4, "#c678dd", "#2E2E2E"], "Brackets": [5, "#c678dd", "#2E2E2E"], "Comments": [6, "#777777", "#2E2E2E"], "Constants": [7, "#d19a5e", "#2E2E2E"],
                    "Functions": [8, "#61afd1", "#2E2E2E"], "Classes": [9, "#C68F55", "#2E2E2E"], "Define": [10, "#61afd1", "#2E2E2E"]
        }
        # Styles: 

        for item in self.ids:
            self.setColor(QColor(self.ids[item][1]), self.ids[item][0])
            self.setPaper(QColor(self.ids[item][2]), self.ids[item][0])
            if(item == "Default" or item == "Keyword" or item == "Classes" or item == "Define"):
                self.setFont(QFont("Consolas", 14, weight = QFont.Bold), self.ids[item][0])

    def language(self) -> str:
        return "PythonLexer"

    def description(self, style: int) -> str:
        for item in self.ids:
            if(style == self.ids[item][0]):
                return item

        return ""

    def get_tokens(self, text) -> list[str, int]:
        p  = re.compile(r"[*]\/|\/[*]|\s+|\w+|\W")
        return [(token, len(bytearray(token, "utf-8"))) for token in p.findall(text)]

    def styleText(self, start: int, end: int) -> None:
        self.startStyling(start)
        editor: QsciScintilla = self.parent()

        text = editor.text()[start:end]
        token_list = self.get_tokens(text)
        string_flag = False

        if(start > 0):
            previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if(previous_style == self.ids["String"][0]):
                string_flag = False

        def next_token(skip: int = None):
            if(len(token_list) > 0):
                if(skip is not None and skip != 0):
                    for _ in range(skip - 1):
                        if(len(token_list) > 0):
                            token_list.pop(0)
                return token_list.pop(0)
            else:
                return None

        def peek_token(n = 0):
            try:
                return token_list[n]
            except IndexError:
                return ['']

        def skip_space_peek(skip = None):
            i = 0
            token = (' ')
            if(skip is not None):
                i = skip
            while token[0].isspace():
                token = peek_token(i)
                i += 1
            return token, i

        while(True):
            current_token = next_token()
            if(current_token is None):
                break

            token: str = current_token[0]
            token_length: int = current_token[1]

            if(string_flag):
                self.setStyling(token_length, self.ids["String"][0])
                if(token == '"' or token == "'"):
                    string_flag = False
                continue

            if(token == "class"):
                name, n = skip_space_peek()
                bracket_colon, _ = skip_space_peek(n)
                if(name[0].isidentifier() and bracket_colon[0] in (":", "(")):
                    self.setStyling(token_length, self.ids["Keyword"][0])
                    _ = next_token(n)
                    self.setStyling(name[1] + 1, self.ids["Classes"][0])
                    continue
                else:
                    self.setStyling(token_length, self.ids["Keyword"][0])
                    continue

            elif(token == "def"):
                name, n = skip_space_peek()
                if(name[0].isidentifier()):
                    self.setStyling(token_length, self.ids["Keyword"][0])
                    _ = next_token(n)
                    self.setStyling(name[1] + 1, self.ids["Define"][0])
                    continue
                else:
                    self.setStyling(token_length, self.ids["Keyword"][0])
                    continue

            elif(token in self.keywords):
                self.setStyling(token_length, self.ids["Keyword"][0])
            
            elif(token.isnumeric() or token == 'self'):
                self.setStyling(token_length, self.ids["Constants"][0])
            
            elif(token  in ["(", ")", "{", "}", "[", "]"]):
                self.setStyling(token_length, self.ids["Brackets"][0])
            
            elif(token == '"' or token == "'"):
                self.setStyling(token_length, self.ids["String"][0])
                string_flag = True
            
            elif(token in self.builtin_functions or token in ['+', '-', '*', '/', '%', '=', '<', '>']):
                self.setStyling(token_length, self.ids["Types"][0])
            else:
                self.setStyling(token_length, self.ids["Default"][0])