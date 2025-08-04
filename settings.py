# here you can change some app settings

debugMode = True

def dbg(*args, **kwargs):
    if debugMode is True:
        print("\033[33m\033[1m", *args, "\033[0m", **kwargs)


class Strings():

    def __init__(self, lang=0):
        self.windowTitle = ["Poem Septeractor", "مُقسِم الشطور"][lang]
        self.leftBtn  = ["Copy left", "نسخ الأيسر"][lang]
        self.rightBtn = ["Copy right", "نسخ الأيمن"][lang]
        self.clipbrdckbox = ["to clipboard", "إلى الحافظة"][lang]
        self.logToFileCheckBox = ["Log to file", "في ملف"][lang]
        self.ckeckBoxesLayout = ["output", "النتيجه"][lang]
        self.copyAsTable = ["Copy as table", "نسخ كجدول"][lang]

strings = Strings(1 if not debugMode else 0)