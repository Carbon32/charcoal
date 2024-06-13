# # # # # # # # # # # # # # # # # # # # #
#                                       #
#           Charcoal Editor             #
#                                       #
# # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.editor import *

# Window: #

class MainWindow(QMainWindow):
	def __init__(self) -> None:
		super(QMainWindow, self).__init__()
		self.init_ui()
		self.current_file, self.current_tab = None, None
		self.paths = {}
		self.statusBar().setStyleSheet(
		'''
			QStatusBar 
			{
				color: #d6d6d6;
				background-color:  rgb(25, 25, 25);
			}
		''')

	def init_ui(self):
		self.setWindowTitle("Charcoal")
		self.setWindowIcon(QIcon('res/icons/logo.png'))
		self.resize(1280, 720)
		self.setFont(QFont("Ebrima", 12))
		self.sections = {
			'File': self.menuBar().addMenu("File"),
			'Edit': self.menuBar().addMenu("Edit"),
			'Tools': self.menuBar().addMenu("Tools"),
			'Help': self.menuBar().addMenu("Help")
		}
		self.menuBar().setStyleSheet(
		'''
			QMenuBar
			{
				background-color: rgb(25, 25, 25);
				color: #d6d6d6;
			}

			QMenuBar::item
			{
				background-color: rgb(25, 25, 25);
			}

			QMenuBar::item:selected
			{
				background-color: rgb(48, 48, 48);
			}

			QMenu 
			{
				background-color: rgb(25, 25, 25);
				color: #d6d6d6;
			}

			QMenu::item::selected
			{
				background-color: rgb(48, 48, 48);
			}
		''')
		self.frames = {}
		self.init_menu()
		self.init_body()
		self.show()

	def get_editor_instance(self, path: "Path" = None, is_python_file: "bool" = True) -> QsciScintilla:
		editor = Editor(path = path, is_python_file = is_python_file)
		return editor

	def set_cursor_arrow(self, _) -> None: self.setCursor(Qt.ArrowCursor)
	def set_cursor_pointer(self, _) -> None: self.setCursor(Qt.PointingHandCursor)
	def create_new_tab(self, path: Path, is_new_file = False) -> None:
		editor = self.get_editor_instance(path, path.suffix in {".py", ".pyw"})
		if(is_new_file):
			self.tab_view.addTab(editor, "Untitled")
			self.setWindowTitle("Charcoal - Untitled")
			self.statusBar().showMessage("Opened: Untitled")
			self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
			self.current_tab = self.tab_view.count() - 1
			self.current_file = None
			return

		if(not path.is_file()): return
		with open(path, 'rb') as file:
			if(b'\0' in file.read(1024)):
				self.statusBar().showMessage("Cannot open this file.", 5000)
				return

		for i in range(self.tab_view.count()):
			if(self.tab_view.tabText(i) == path.name):
				self.tab_view.setCurrentIndex(i)
				self.current_file = path
				return

		self.tab_view.addTab(editor, path.name)
		editor.setText(path.read_text())
		self.setWindowTitle(f"Charcoal - {path.name}")
		self.current_file = path
		self.paths[self.tab_view.count() - 1] = path
		self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
		self.current_tab = self.tab_view.count() - 1
		self.statusBar().showMessage(f"Opened: {path.name}", 5000)

	def add_frame(self, name: "str") -> QFrame:
		frame = QFrame()
		frame.setFrameShape(QFrame.NoFrame)
		frame.setFrameShadow(QFrame.Plain)
		frame.setMaximumWidth(300)
		frame.setMidLineWidth(200)
		frame.setContentsMargins(0, 0, 0, 0)
		frame.setStyleSheet(
		'''
			QFrame 
			{
				background-color: rgb(38, 38, 38);
				border-radius: 0px;
				border: none;
				padding: 5px;
				color: rgb(211, 211, 211);
			}
		''')
		self.frames[name] = frame
		return frame

	def add_menu_option(self, section: "str", name: "str", shortcut: "str", function: "method", separator: "bool" = False) -> None:
		if(separator): self.sections[section].addSeparator()
		option = self.sections[section].addAction(name)
		option.setShortcut(shortcut)
		option.triggered.connect(function)

	def add_side_bar_item(self, path: "str", size: "QSize", action_type: "str"):
		label = QLabel()
		label.setPixmap(QPixmap(path).scaled(size, transformMode=Qt.SmoothTransformation))
		label.setAlignment(Qt.AlignmentFlag.AlignTop)
		label.setFont(QFont("Ebrima", 12))
		label.mousePressEvent = lambda event: self.handle_side_bar(event, action_type)
		label.enterEvent = self.set_cursor_pointer
		label.leaveEvent = self.set_cursor_arrow
		label.setStyleSheet(
		'''
			QFrame
			{
				border-radius: 20px;
				padding: 15px;
			}

			QFrame:hover
			{
				background-color: rgb(48, 48, 48);
			}
		''')
		self.side_bar_layout.addWidget(label)

	def new_file(self) -> None: self.create_new_tab(Path(""), is_new_file = True)
	def open_file(self) -> None:
		new_file, _ = QFileDialog.getOpenFileName(self, "Choose A File", "", "All Files (*);;Python Files (*.py)")
		if(new_file == ''):
			self.statusBar().showMessage("Action Cancelled", 5000)
			return
		file = Path(new_file)
		self.create_new_tab(file)

	def close_file(self) -> None:
		if(self.current_tab != None):
			if(self.current_tab == 0):
				if(self.tab_view.count() > 1):
					self.tab_view.removeTab(self.current_tab)
					self.paths.pop(self.current_tab)
				else:
					self.tab_view.removeTab(0)
					self.current_file = None
					self.paths = {}
					self.current_tab = None
			else:
				self.tab_view.removeTab(self.current_tab)
				try:
					self.paths.pop(self.current_tab)
					self.current_file = self.paths[self.current_tab - 1]
				except KeyError: pass
				self.current_tab -= 1

	def close_all_files(self) -> None:
		while(self.tab_view.count() != 0): self.tab_view.removeTab(self.tab_view.count() - 1)
		self.paths = {}
		self.current_file = None
		self.current_tab = None

	def open_folder(self) -> None:
		new_folder = QFileDialog.getExistingDirectory(self, "Choose A Folder", "")
		if(new_folder):
			self.model.setRootPath(new_folder)
			self.files_tree_view.setRootIndex(self.model.index(new_folder))
			self.statusBar().showMessage(f"Opened: {new_folder}", 5000)

	def save_file(self) -> None:
		if(self.current_file is None and self.tab_view.count() > 0): self.save_as()
		editor = self.tab_view.currentWidget()
		if(self.current_file is not None):
			self.current_file.write_text(editor.text())
			self.statusBar().showMessage(f"Saved: {self.current_file.name}", 5000)

	def save_as(self) -> None:
		editor = self.tab_view.currentWidget()
		if(editor is None): return
		file_path = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
		if(file_path == ''):
			self.statusBar().showMessage("Action Cancelled", 5000)
			return
		path = Path(file_path)
		path.write_text(editor.text())
		if(path.suffix in {".py", ".pyw"}):
			editor.path = path
			editor.is_python_file = True
			editor.init_lexer()
		self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
		self.statusBar().showMessage(f"Saved: {path.name}", 5000)
		self.current_file = path

	def copy(self) -> None:
		editor = self.tab_view.currentWidget()
		if(editor is not None): editor.copy()

	def cut(self) -> None:
		editor = self.tab_view.currentWidget()
		if(editor is not None): editor.cut()

	def paste(self) -> None:
		editor = self.tab_view.currentWidget()
		if(editor is not None): editor.paste()

	def build(self) -> None:
		if(self.tab_view.count() > 0):
			if(self.current_file is None):
				self.save_as()
				if(self.current_file is None): self.statusBar().showMessage("Save the file first...", 5000)
			else:
				if(self.current_file.suffix in {".py", ".pyw"}): self.save_file()
				else: self.statusBar().showMessage("The file must be a Python file.", 5000)

	def open_src_link(self) -> None: QDesktopServices.openUrl(QUrl("https://github.com/Carbon32/charcoal"))
	def init_menu(self) -> None:
		self.add_menu_option("File", "New", "Ctrl+N", self.new_file)
		self.add_menu_option("File", "Open File", "Ctrl+O", self.open_file)
		self.add_menu_option("File", "Open Folder", "Ctrl+K", self.open_folder)
		self.add_menu_option("File", "Save", "Ctrl+S", self.save_file, True)
		self.add_menu_option("File", "Save As", "Ctrl+Shift+S", self.save_as)
		self.add_menu_option("File", "Close File", "Ctrl+W", self.close_file, True)
		self.add_menu_option("File", "Close All Files", "Ctrl+Shift+W", self.close_all_files)
		self.add_menu_option("Edit", "Copy", "Ctrl+C", self.copy)
		self.add_menu_option("Edit", "Cut", "Ctrl+X", self.cut)
		self.add_menu_option("Edit", "Paste", "Ctrl+V", self.paste)
		self.add_menu_option("Edit", "Search", "Ctrl+F", self.force_search, True)
		self.add_menu_option("Tools", "Build", "Ctrl+B", self.build)
		self.add_menu_option("Help", "Source Code", "", self.open_src_link)

	def init_body(self) -> None:
		self.body_frame = QFrame()
		self.body_frame.setFrameShape(QFrame.NoFrame)
		self.body_frame.setFrameShadow(QFrame.Plain)
		self.body_frame.setLineWidth(0)
		self.body_frame.setMidLineWidth(0)
		self.body_frame.setContentsMargins(0, 0, 0, 0)
		self.body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.body_frame.setStyleSheet(
		'''
			QsciScintilla
			{
				border: none;
				background-color: rgb(40, 44, 52);
				color: rgb(211, 211, 211);
			}
			
			QScrollBar:vertical
			{
				border: none;
				width: 14px;
				margin: 15px 0 15px 0;
				background-color: rgb(45, 45, 45);
				border-radius: 0px;
			}

			QScrollBar:handle:vertical
			{
				background-color: rgb(76, 74, 74);
			}

			QScrollBar:handle:vertical:pressed
			{
				background-color: rgb(92, 91, 91);
			}

			QScrollBar::sub-line::vertical
			{
				border: none;
				background: none;
				height: 15px;
				subcontrol-position: top;
				subcontrol-origin: margin;
				background-color: rgb(92, 91, 91);
			}

			QScrollBar::add-line::vertical
			{
				border: none;
				background: none;
				height: 15px;
				subcontrol-position: bottom;
				subcontrol-origin: margin;
				background-color: rgb(92, 91, 91);
			}

			QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
			{
				background: none;
			}

			QScrollBar:horizontal
			{
				border: none;
				width: 14px;
				margin: 15px 0 15px 0;
				background-color: rgb(45, 45, 45);
				border-radius: 0px;
			}

			QScrollBar:handle:horizontal
			{
				background-color: rgb(76, 74, 74);
			}

			QScrollBar:handle:horizontal:pressed
			{
				background-color: rgb(92, 91, 91);
			}

			QScrollBar::sub-line::horizontal
			{
				border: none;
				background: none;
				height: 15px;
				border-top-left-radius: 7px;
				border-top-right-radius: 7px;
				subcontrol-position: top;
				subcontrol-origin: margin;
			}

			QScrollBar::add-line::horizontal
			{
				border: none;
				background: none;
				height: 15px;
				border-top-left-radius: 7px;
				border-top-right-radius: 7px;
				subcontrol-position: bottom;
				subcontrol-origin: margin;
			}

			QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
			{
				background: none;
			}
		''')

		self.body = QHBoxLayout()
		self.body.setContentsMargins(0, 0, 0, 0)
		self.body.setSpacing(0)

		self.side_bar = QFrame()
		self.side_bar.setFrameShape(QFrame.StyledPanel)
		self.side_bar.setFrameShadow(QFrame.Raised)
		self.side_bar.setContentsMargins(0, 0, 0, 0)
		self.side_bar.setMaximumWidth(128)
		self.side_bar.setStyleSheet(
		'''
			background-color: rgb(25, 25, 25);
			padding: 5px;
		''')
		self.side_bar_layout = QVBoxLayout()
		self.side_bar_layout.setContentsMargins(5, 10, 5, 0)
		self.side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

		self.horizontal_split = QSplitter(Qt.Horizontal)
		self.horizontal_split.setStyleSheet(
		'''
			QSplitter
			{
				background-color: rgb(46, 46, 46);
			}

			QSplitter::handle
			{
				background-color: rgb(38, 38, 38);
			}
		''')

		self.file_manager_frame = self.add_frame("file_manager")
		self.file_manager_layout = QVBoxLayout()
		self.file_manager_layout.setContentsMargins(0, 0, 0, 0)
		self.file_manager_layout.setSpacing(0)
		self.file_manager_frame.setStyleSheet(
		'''
			background-color: rgb(38, 38, 38);
			width: 200px;
		''')

		self.search_frame = self.add_frame("search")

		self.search_layout = QVBoxLayout()
		self.search_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.search_layout.setContentsMargins(0, 10, 0, 0)
		self.search_layout.setSpacing(0)
		self.search_frame.setStyleSheet(
		'''
			background-color: rgb(38, 38, 38);
			width: 200px;
		''')

		self.search_input = QLineEdit()
		self.search_input.setPlaceholderText("Search")
		self.search_input.setFont(QFont("Ebrima", 12))
		self.search_input.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.search_input.setStyleSheet(
		'''
			QLineEdit 
			{
				background-color: rgb(38, 38, 38);
				border-bottom: 2px solid #999999;
  				border-radius: 0;
  				padding-bottom: 10px;
				margin: 10px;
				color: rgb(211, 211, 211);
			}

			QLineEdit:hover
			{
				color: rgb(255, 255, 255);
			}
		''')

		self.search_view = QListWidget()
		self.search_view.setFont(QFont("Ebrima", 12))
		self.search_view.setStyleSheet(
		'''
			QListWidget 
			{
				background-color: rgb(38, 38, 38);
				border-radius: 5px;
				padding: 5px;
				color: rgb(211, 211, 211);
			}
		''')
		self.search_view.itemClicked.connect(self.open_search_item)

		self.search_layout.addWidget(self.search_input)
		self.search_layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum))
		self.search_layout.addWidget(self.search_view)
		self.search_frame.setLayout(self.search_layout)

		self.add_side_bar_item('res/icons/folder.png', QSize(32, 32), "file_manager")
		self.add_side_bar_item('res/icons/search.png', QSize(32, 32), "search")
		self.add_side_bar_item('res/icons/build.png', QSize(32, 32), "build")

		self.model = QFileSystemModel()
		self.model.setRootPath(os.getcwd())
		self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

		self.files_tree_view = QTreeView()
		self.files_tree_view.setFont(QFont("Ebrima", 11))
		self.files_tree_view.setModel(self.model)
		self.files_tree_view.setRootIndex(self.model.index(os.getcwd()))
		self.files_tree_view.setSelectionMode(QTreeView.SingleSelection)
		self.files_tree_view.setSelectionBehavior(QTreeView.SelectRows)
		self.files_tree_view.setEditTriggers(QTreeView.NoEditTriggers)
		self.files_tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
		self.files_tree_view.clicked.connect(self.add_new_file)
		self.files_tree_view.setIndentation(10)
		self.files_tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.files_tree_view.setHeaderHidden(True)
		self.files_tree_view.setColumnHidden(1, True)
		self.files_tree_view.setColumnHidden(2, True)
		self.files_tree_view.setColumnHidden(3, True)
		self.files_tree_view.setStyleSheet(
		'''
			QTreeView
			{
				border: none;
				margin: 10px;
				outline: 0;
			}

			QTreeView::item
			{
				border: none;
				margin-left: 10px;
			}

			QTreeView::item:hover
			{
				background-color: rgb(48, 48, 48);
				color: #d7d7d7;
			}

			QTreeView::item:focus
			{
				background-color: rgb(48, 48, 48);
			}

			QTreeView::item:selected
			{
				background-color: rgb(48, 48, 48);
			}

			QTreeView::item:active
			{
				color: #d7d7d7;
			}

			QTreeView::item:!active 
			{
				background-color: rgb(38, 38, 38);
				color: #d6d6d6;
			}

			QTreeView::branch:open:has-children:!has-siblings,
			QTreeView::branch:open:has-children:has-siblings
			{
				border: none;
				border-image: none;
				image: url(res/icons/arrow_down.png);
			}

			QTreeView::branch:has-children:!has-siblings:closed,
			QTreeView::branch:closed:has-children:has-siblings
			{
				background-color: rgb(38, 38, 38);
				border: none;
				border-image: none;
				image: url(res/icons/arrow_right.png);
			}
		''')

		self.tab_view = QTabWidget()
		self.tab_view.setContentsMargins(0, 0, 0, 0)
		self.tab_view.setTabsClosable(True)
		self.tab_view.setMovable(True)
		self.tab_view.setDocumentMode(True)
		self.tab_view.tabCloseRequested.connect(self.close_tab)
		self.tab_view.tabBarClicked.connect(self.set_current_tab)
		self.tab_view.setStyleSheet(
		'''
			QTabBar
			{
				background-color: rgb(30, 30, 30);
			}

			QTabBar::tab
			{
				background-color: rgb(30, 30, 30);
				color: rgb(116, 116, 116);
				min-width: 10ex;
				min-height: 10ex;
				padding: 10px 20px;
				border: none;
			}

			QTabBar::tab::selected
			{
				color: rgb(211, 211, 211);
				border-style: none;
				background-color: rgb(46, 46, 46);
				border-bottom: 2px solid rgb(211, 211, 211);
			}

			QTabBar::close-button
			{
				image: url(res/icons/close.png);
			}
		''')

		self.side_bar.setLayout(self.side_bar_layout)

		self.searcher = Searcher()
		self.searcher.finished.connect(self.search_finished)
		self.search_input.textChanged.connect(lambda text: self.searcher.update_search(text, self.model.rootDirectory().absolutePath()))

		self.file_manager_layout.addWidget(self.files_tree_view)
		self.file_manager_frame.setLayout(self.file_manager_layout)

		self.horizontal_split.addWidget(self.file_manager_frame)
		self.horizontal_split.addWidget(self.tab_view)

		self.current_side_bar = "file_manager"

		self.body.addWidget(self.side_bar)
		self.body.addWidget(self.horizontal_split)
		self.body_frame.setLayout(self.body)

		self.setCentralWidget(self.body_frame)

	def add_new_file(self, index: "QModelIndex") -> None: self.create_new_tab(Path(self.model.filePath(index)))
	def search_finished(self, items: "list") -> None:
		self.search_view.clear()
		for item in items: self.search_view.addItem(item)

	def open_search_item(self, item: "SearchItem") -> None:
		self.create_new_tab(Path(item.path))
		editor = self.tab_view.currentWidget()
		editor.setCursorPosition(item.line_number, item.end)
		editor.setFocus()

	def set_current_tab(self, index: "int") -> None:  self.current_tab = index
	def close_tab(self, index: "int") -> None: self.tab_view.removeTab(index)
	def force_search(self) -> None:
		self.current_side_bar = "search"
		self.horizontal_split.replaceWidget(0, self.search_frame)
		self.horizontal_split.setSizes([1, 1])
		self.frames[self.current_side_bar].show()

	def handle_side_bar(self, event: "QMouseEvent", action_type: "str"):
		if(self.current_side_bar == action_type):
			self.frames[self.current_side_bar].show()
			return
		self.horizontal_split.setSizes([1, 1])
		if(action_type == "file_manager"):
			if(not(self.file_manager_frame in self.horizontal_split.children())):
				self.horizontal_split.replaceWidget(0, self.file_manager_frame)
				self.current_side_bar = action_type
		elif(action_type == "search"):
			if(not(self.search_frame in self.horizontal_split.children())):
				self.horizontal_split.replaceWidget(0, self.search_frame)
				self.current_side_bar = action_type
		elif(action_type == "build"): self.build()

if __name__ == '__main__':
	application = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
	window = MainWindow()
	sys.exit(application.exec())