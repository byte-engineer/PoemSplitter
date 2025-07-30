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

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainGrid = QtWidgets.QVBoxLayout()
        self.centralWidget.setLayout(self.mainGrid)

        dbg("Rendering UI: initUi()")


    def renderUi(self):

        __checkbox_style = """
        QCheckBox {

            border: 1px solid #aaa;
            border-radius: 4px;
            padding: 4px;
            background-color: #222;
            color: white;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        """

        poemInput = QTextEdit()
        self.mainGrid.addWidget(poemInput)

        self.clipboardCkeckBox = QtWidgets.QCheckBox(strings.clipbrdckbox)
        self.logToFileCheckBox = QtWidgets.QCheckBox(strings.logToFileCheckBox) 


        # self.clipboardCkeckBox.setStyleSheet(checkbox_style)
        # self.logToFileCheckBox.setStyleSheet(checkbox_style)
        
        self.clipboardCkeckBox.setChecked(True)
        self.logToFileCheckBox.setChecked(False)

        leftCopyButton = QPushButton(strings.leftBtn) 
        rightCopyButton = QPushButton(strings.rightBtn)

        ckeckBoxesLayout = QtWidgets.QVBoxLayout()

        hButonsLayout = QtWidgets.QHBoxLayout()
        hButonsLayout.addWidget(leftCopyButton)
        hButonsLayout.addWidget(rightCopyButton)
        
        hButonsLayout.addLayout(ckeckBoxesLayout)
        
        ckeckBoxesLayout.addWidget(self.clipboardCkeckBox)
        ckeckBoxesLayout.addWidget(self.logToFileCheckBox)


        self.mainGrid.addLayout(hButonsLayout)

        leftCopyButton.clicked.connect(lambda: self.processText(poemInput.toPlainText(), 'left'))
        rightCopyButton.clicked.connect(lambda: self.processText(poemInput.toPlainText(), 'right'))

        dbg("Rendering UI: renderUi()")

    def processText(self, text: str, side: str):
        lines = text.split('\n')
        result_lines = []

        for lineNumber, line in enumerate(lines):
            match = re.match(r'^(.*?)\s*(?:\s{2,}|\.+|~+|-+|=+)\s*(.*)$', line)

            if match:
                right, left = match.group(1).strip(), match.group(2).strip()
                result_lines.append(left if side == 'left' else right)
            else:
                # If no match, decide based on line number and side
                if lineNumber % 2 == (1 if side == 'left' else 0):
                    result_lines.append(line)

        final_output = '\n'.join(result_lines)

        if self.clipboardCkeckBox.isChecked():
            QtWidgets.QApplication.clipboard().setText(final_output)

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
