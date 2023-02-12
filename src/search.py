# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                      Charcoal Editor                      #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Import: #

from src.autocomplete import *

# Search Item: #

class SearchItem(QListWidgetItem):
    def __init__(self, name, path, line_number, end, line):

        # Properties:

        self.name, self.path, self.line_number, self.end, self.line = name, path, line_number, end, line
        self.formated_string = f'{self.name}: {self.line_number}:{self.end} - {self.line}...'
        super().__init__(self.formated_string)

    def __str__(self):
        return self.formated_string

    def __repr__(self):
        return self.__str__()

class Searcher(QThread):
    finished = pyqtSignal(list)
    def __init__(self):
        super(Searcher, self).__init__(None)

    def walk_directory(self, path, excluded_directories, excluded_files):
        for root, directories, files, in os.walk(path, topdown = True):
            directories[:] = [dir_ for dir_ in directories if dir_ not in excluded_directories]
            files[:] = [f for f in files if Path(f).suffix not in excluded_files]
            yield root, directories, files

    def searching(self):
        self.items = []
        excluded_directories = set([".git", "__pycache__"])
        excluded_files = set([".exe", ".png", ".jpg", ".jpeg", ".pyc"])

        for root, _, files in self.walk_directory(self.search_path, excluded_directories, excluded_files):
            if(len(self.items) > 500):
                break

            for file_ in files:
                path = os.path.join(root, file_)
                with open(path, 'rb') as f:
                    if(b'\0' in f.read(1024)):
                        break

                with open(path, 'r', encoding = 'utf8') as f:
                    r = re.compile(self.search_text, re.IGNORECASE)
                    for i, line, in enumerate(f):
                        if(c := r.search(line)):
                            self.item = SearchItem(
                                file_,
                                path,
                                i,
                                c.end(),
                                line[c.start():].strip()[:50],
                            )
                            self.items.append(self.item)

        self.finished.emit(self.items)

    def run(self):
        self.searching()

    def update_search(self, text, path):
        self.search_text, self.search_path = text, path
        self.start()