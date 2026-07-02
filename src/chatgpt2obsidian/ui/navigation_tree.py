from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class NavigationTree(QTreeWidget):

    def __init__(self, conversations):
        super().__init__()

        self.conversations = conversations

        self.setHeaderHidden(True)

        self.projects_item = QTreeWidgetItem(["📁 Projects"])
        self.chats_item = QTreeWidgetItem(["💬 Chats"])

        self.addTopLevelItem(self.projects_item)
        self.addTopLevelItem(self.chats_item)

        for index, conversation in enumerate(conversations):
            item = QTreeWidgetItem([conversation.title])
            item.setData(0, Qt.UserRole, index)
            self.chats_item.addChild(item)

        self.projects_item.setExpanded(True)
        self.chats_item.setExpanded(True)

    def first_chat(self):
        if self.chats_item.childCount():
            return self.chats_item.child(0)
        return None