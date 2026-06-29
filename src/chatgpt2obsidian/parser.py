import json
from pathlib import Path


class ChatParser:

    def __init__(self, filename):
        self.filename = Path(filename)

    def load(self):

        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data