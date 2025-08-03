import sys
# import time
from PyQt6 import QtWidgets 
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTextEdit, QPushButton
from PyQt6.QtGui import QTextCharFormat, QTextCursor, QColor
from PyQt6 import QtGui
from PyQt6.QtGui import QTextCursor

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


        ckeckBoxesLayout = QtWidgets.QVBoxLayout()

        # main Text Edit
        self.poemInput = QTextEdit()

        # TODO
        BottomGridLayout = QtWidgets.QGridLayout(self)
        

        self.mainGrid.addWidget(self.poemInput)

        # clipBoard chk box 
        self.clipboardCheckBox = QtWidgets.QCheckBox(strings.clipbrdckbox)
        self.clipboardCheckBox.setChecked(True if not debugMode else False)
        
        self.logToFileCheckBox = QtWidgets.QCheckBox(strings.logToFileCheckBox) 
        self.logToFileCheckBox.setChecked(False)

        leftCopyButton = QPushButton(strings.leftBtn) 
        rightCopyButton = QPushButton(strings.rightBtn)

        hButonsLayout = QtWidgets.QHBoxLayout()
        hButonsLayout.addWidget(leftCopyButton)
        hButonsLayout.addWidget(rightCopyButton)
        hButonsLayout.addLayout(ckeckBoxesLayout)      # Two chk boxs 

        # Adding the chk boxes
        ckeckBoxesLayout.addWidget(self.clipboardCheckBox) 
        ckeckBoxesLayout.addWidget(self.logToFileCheckBox)


        self.mainGrid.addLayout(hButonsLayout)

        leftCopyButton.clicked.connect(lambda: self.processText(self.poemInput.toPlainText(), 'left'))
        rightCopyButton.clicked.connect(lambda: self.processText(self.poemInput.toPlainText(), 'right'))

        dbg("Rendering UI: renderUi()")



    def processText(self, text: str, side: str):
        lines = text.split('\n')
        result_lines = []

        # Clear old highlights and selection
        self.poemInput.setExtraSelections([])
        self.highlights = []
        cursor = self.poemInput.textCursor()
        cursor.clearSelection()
        self.poemInput.setTextCursor(cursor)

        for lineNumber, line in enumerate(lines):
            match = re.match(r'^(.*?)\s*(?:\s{2,}|\.+|~+|-+|=+)\s*(.*)$', line)

            if match:
                dbg(f"Matched '{match.group()}' at index {match.start()} to {match.end()}")
                right, left = match.group(1).strip(), match.group(2).strip()
                result_lines.append(left if side == 'left' else right)
                self.highLightText(match, side)
            else:
                if lineNumber % 2 == (1 if side == 'left' else 0):
                    self.highlight_lines(mode='even' if side == 'left' else 'odd')
                    result_lines.append(line)


        final_output = '\n'.join(result_lines)

        if self.logToFileCheckBox.isChecked():
            with open("OutputFile.txt", 'w') as file:
                file.write(final_output)
                dbg(final_output, "\n--- Logged to a File ---")

        if self.clipboardCheckBox.isChecked():
            QtWidgets.QApplication.clipboard().setText(final_output)
            dbg(final_output, "\n--- Copied to Clipboard ---")


    def highlight_lines(self, mode='even'):    # mode can be 'even' or 'odd'
        self.poemInput.setExtraSelections([])  # clear previous
        self.highlights = []

        fullText = self.poemInput.toPlainText()
        lines = fullText.split('\n')
        pos = 0

        for index, line in enumerate(lines):
            line_len = len(line)

            if mode == 'even' and index % 2 == 0:
                self._addHighlight(pos, pos + line_len)
            elif mode == 'odd' and index % 2 == 1:
                self._addHighlight(pos, pos + line_len)

            pos += line_len + 1  # +1 for '\n'

        self.poemInput.setExtraSelections(self.highlights)

    def _addHighlight(self, start, end):
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("lightgreen"))

        cursor = self.poemInput.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)

        selection = QTextEdit.ExtraSelection()
        selection.cursor = cursor
        selection.format = fmt

        self.highlights.append(selection)

    def highLightText(self, match: re.Match[str], side):
        fullText = self.poemInput.toPlainText()
        matchedText = match.group(1 if side == 'left' else 2)

        startIdx = fullText.find(matchedText)
        if startIdx == -1:
            return  # Not found, skip

        endIdx = startIdx + len(matchedText)

        # Create highlight format
        fmt = QtGui.QTextCharFormat()
        fmt.setBackground(QtGui.QColor("blue"))

        # Create cursor and apply selection
        cursor = self.poemInput.textCursor()
        cursor.setPosition(startIdx)
        cursor.setPosition(endIdx, QTextCursor.MoveMode.KeepAnchor)

        selection = QtWidgets.QTextEdit.ExtraSelection()
        selection.cursor = cursor
        selection.format = fmt

        # Store all highlights (this is important!)
        if not hasattr(self, 'highlights'):
            self.highlights = []

        self.highlights.append(selection)
        self.poemInput.setExtraSelections(self.highlights)



    def keyReleaseEvent(self, event):
        if isinstance(event, QKeyEvent) and event.key() == Qt.Key.Key_Escape:
            self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('windows11')
    win = App()
    win.show()
    sys.exit(app.exec())
    dbg("Done . . .")

if __name__ == "__main__":
    main()
