# here you can change some app settings

debugMode = True

def dbg(*args, **kwargs):
    if debugMode is True:
        print(*args, **kwargs)


class Strings():

    def __init__(self, lang=0):
        self.windowTitle = ["Poem Septeractor", "مُقسِم الشطور"][lang]
        self.leftBtn  = ["Copy left", "نسخ الأيسر"][lang]
        self.rightBtn = ["Copy right", "نسخ الأيمن"][lang]
        self.clipbrdckbox = ["to clipboard", "انسخ إلى الحافظة"][lang]

        self.options = {
            "twoParts" : ["two parts each", "شطرين في كل سطر"][lang],
            "onePart" : ["each part on a line", "شطر في كل سطر"][lang],
        }

strings = Strings(1)