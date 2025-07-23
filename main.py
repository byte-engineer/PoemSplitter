import sys
# import time
from PyQt6 import QtWidgets 
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTextEdit, QPushButton
from settings import *
import re


#> use this command to run the file
#> uv run python main.py

class App(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUi()
        self.renderUi()


    def initUi(self):
        self.setWindowTitle(strings.windowTitle)
        self.setGeometry(200, 200, 300, 300)
        self.setFixedSize(300, 300)

        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.mainGrid = QtWidgets.QVBoxLayout()
        self.centralWidget.setLayout(self.mainGrid)

        dbg("Rendering UI: initUi()")


    def renderUi(self):
        poemInput = QTextEdit()
        self.mainGrid.addWidget(poemInput)

        hButonsLayout = QtWidgets.QHBoxLayout()
        leftCopyButton = QPushButton(strings.leftBtn) 
        rightCopyButton = QPushButton(strings.rightBtn) 
        hButonsLayout.addWidget(leftCopyButton)
        hButonsLayout.addWidget(rightCopyButton)
        self.mainGrid.addLayout(hButonsLayout)

        def leftCopy():
            self.processText(poemInput.toPlainText(), 'left')

        def rightCopy():
            self.processText(poemInput.toPlainText(), 'right')

        leftCopyButton.clicked.connect(leftCopy)
        rightCopyButton.clicked.connect(rightCopy)

        dbg("Rendering UI: renderUi()")


    def processText(self, text: str, side: str):
        import re
        lines = text.split('\n')
        result_lines = []
        
        for line in lines:
            match = re.match(r'^(.*?)\s*(?:\s{2,}|\.+|~+|-+|=+)\s*(.*)$', line)
            if not match:
                continue  # skip if line doesn't match
            right, left = match.group(1).strip(), match.group(2).strip()
            result_lines.append(left if side == 'left' else right)

        final_output = '\n'.join(result_lines)
        # QtWidgets.QApplication.clipboard().setText(final_output)
        dbg(final_output, "\n--- Copied to Clipboard ---")


    def keyReleaseEvent(self, event):
        if isinstance(event, QKeyEvent) and event.key() == Qt.Key.Key_Escape:
            self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec())
    dbg("Done . . .")

if __name__ == "__main__":
    main()