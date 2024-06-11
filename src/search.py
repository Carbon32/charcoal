# # # # # # # # # # # # # # # # # # # # #
#                                       #
#           Charcoal Editor             #
#                                       #
# # # # # # # # # # # # # # # # # # # # #

# Import: #

try: from src.autocomplete import *
except: from autocomplete import *

# Search Item: #

class SearchItem(QListWidgetItem):
	def __init__(self, name: "str", path: "str", line_number: "int", end: "int", line: "str") -> None:
		self.name, self.path, self.line_number, self.end, self.line = name, path, line_number, end, line
		super().__init__(f'{self.name}: {self.line_number}:{self.end} - {self.line}...')

	def __str__(self) -> str:
		return f'{self.name}: {self.line_number}:{self.end} - {self.line}...'

	def __repr__(self) -> str:
		return self.__str__()

class Searcher(QThread):
	finished = pyqtSignal(list)
	def __init__(self):
		super(Searcher, self).__init__(None)

	def walk_directory(self, path: "str", excluded_directories: "set", excluded_files: "set") -> None:
		for root, directories, files, in os.walk(path, topdown = True):
			directories[:] = [d for d in directories if d not in excluded_directories]
			files[:] = [f for f in files if Path(f).suffix not in excluded_files]
			yield root, directories, files

	def searching(self) -> None:
		self.items = []
		if(os.path.exists('settings.json')):
			try:
				with open('settings.json', 'r') as settings:
					rules = json.load(settings)
					excluded_directories, excluded_files = set(rules['excluded_folders']), set(rules['excluded_files'])
			except: excluded_directories, excluded_files = set([]), set([])
		else: new_settings = open('settings.json', 'w').close()
		for root, _, files in self.walk_directory(self.search_path, excluded_directories, excluded_files):
			if(len(self.items) > 500): break
			for file_ in files:
				path = os.path.join(root, file_)
				with open(path, 'rb') as f:
					if(b'\0' in f.read(1024)): break
				with open(path, 'r', encoding = 'utf8') as f:
					regex = re.compile(self.search_text, re.IGNORECASE)
					for i, line, in enumerate(f):
						if(c := regex.search(line)):
							self.item = SearchItem( file_, path, i, c.end(), line[c.start():].strip()[:50])
							self.items.append(self.item)
		self.finished.emit(self.items)

	def run(self) -> None:
		self.searching()

	def update_search(self, text: "str", path: "str") -> None:
		self.search_text, self.search_path = text, path
		self.start()