from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollBar
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QSizePolicy,
)


class MessageWidget(QWidget):

    def __init__(self, role: str, text: str):
        super().__init__()

        root = QHBoxLayout(self)

        if role == "user":
            root.addStretch()

        bubble = QWidget()

        if role == "user":
            bubble.setStyleSheet("""
                QWidget{
                    background:#2b5278;
                    border-radius:12px;
                    padding:8px;
                }
            """)
        else:
            bubble.setStyleSheet("""
                QWidget{
                    background:#343541;
                    border-radius:12px;
                    padding:8px;
                }
            """)

        bubble.setMaximumWidth(700)

        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(12, 10, 12, 10)

        author = QLabel("👤 You" if role == "user" else "🤖 ChatGPT")
        author.setStyleSheet("""
            color:#9cdcfe;
            font-weight:bold;
            font-size:14px;
        """)

        message = QLabel(text)

        message.setWordWrap(True)

        message.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        message.setStyleSheet("""
            color:white;
            font-size:14px;
        """)

        bubble_layout.addWidget(author)
        bubble_layout.addWidget(message)

        root.addWidget(bubble)

        if role != "user":
            root.addStretch()


class ChatView(QScrollArea):

    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

        self.container = QWidget()

        self.layout = QVBoxLayout(self.container)

        self.layout.setAlignment(Qt.AlignTop)

        self.layout.setSpacing(14)

        self.setWidget(self.container)

        def clear(self):

        while self.layout.count():

            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def show_conversation(self, conversation):

        self.clear()

        title = QLabel(conversation.title)

        title.setStyleSheet("""
            color:white;
            font-size:28px;
            font-weight:bold;
            padding:10px;
        """)

        self.layout.addWidget(title)

        for message in conversation.messages:

            widget = MessageWidget(
                message.role,
                message.text
            )

            self.layout.addWidget(widget)

        self.layout.addStretch()

        self.verticalScrollBar().setValue(0)