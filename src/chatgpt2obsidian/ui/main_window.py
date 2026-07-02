from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QSplitter

from src.chatgpt2obsidian.parser import ChatParser
from src.chatgpt2obsidian.ui.navigation_tree import NavigationTree
from src.chatgpt2obsidian.ui.chat_view import ChatView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChatGPT Archive")
        self.resize(1200, 800)

        parser = ChatParser("input/conversations.json")
        self.conversations = parser.load()

        self.tree = NavigationTree(self.conversations)
        self.viewer = ChatView()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.viewer)
        splitter.setSizes([300, 900])

        self.setCentralWidget(splitter)

        self.tree.itemClicked.connect(self.on_item_clicked)

        first = self.tree.first_chat()

        if first:
            self.tree.setCurrentItem(first)
            self.viewer.show_conversation(self.conversations[0])

    def on_item_clicked(self, item):

        index = item.data(0, Qt.UserRole)

        if index is None:
            return

        self.viewer.show_conversation(self.conversations[index])