import wx;
import os;
import subprocess;
import re;
import pygtk;
pygtk.require("2.0")
import gtk;

clipboard = gtk.clipboard_get()
processList = ["steam", "chrome"]
killList = ["steam", "chrome", "dota2"]
colorList = [
    "Red",
    "Orange",
    "Yellow",
    "Green",
    "Blue",
    "Purple",
    "Pink",
    "Rainbow-W",
    "Rainbow-L"
]
colorDict = {
    "Pink" : 0x0011,
    "Red" : 0x0012,
    "Orange": 0x0013,
    "Purple": 0x0016,
    "Blue" : 0x0019,
    "Green" : 0x000C,
    "Yellow" : 0x001D
}
rainbow = [
    chr(0x0012),
    chr(0x0013),
    chr(0x001D),
    chr(0x000C),
    chr(0x0019),
    chr(0x0016),
    chr(0x0011)
]


class ProcessHandler:
    def __init__(self):
        self.processes = {}

    def processes(self):
        return self.processes

    def addProcess(self, process, processName):
        self.processes[processName] = process

class FrameHandler(wx.Frame):
    def __init__(self, parent, title, processHandler):
        super(FrameHandler, self).__init__(
            parent=parent,
            title=title,
            size=(450, 550))
        self.processHandler = processHandler
        self.panel = wx.Panel(self, 2)
        self.steamButton = wx.Button(
            self,
            3,
            "Run Steam",
            (50,50),
            (150,50)
        )
        self.chromeButton = wx.Button(
            self,
            4,
            "Run Chrome",
            (250,50),
            (150,50)
        )
        self.mouseComboBox = wx.ComboBox(
            self,
            5,
            "Choose Your Mouse",
            (50,165),
            (150,20),
            getXInputList()
        )
        self.speedMultiplier = wx.TextCtrl(
            self,
            6,
            "Speed Multiplier",
            (250,150),
            (150,50)
        )
        self.changeMouseSensButton = wx.Button(
            self,
            7,
            "Change Sensitivity",
            (150,200),
            (150,50)
        )
        self.killApp = wx.ComboBox(
            self,
            8,
            "Frozen Application",
            (50,315),
            (150,50),
            killList
        )
        self.killButton = wx.Button(
            self,
            9,
            "Kill App",
            (250,315),
            (150,50)
        )
        self.colorChanger = wx.ComboBox(
            self,
            10,
            "Rainbow-L",
            (50, 400),
            (150,50),
            colorList
        )
        self.colorText = wx.TextCtrl(
            self,
            11,
            "Your Text",
            (250, 400),
            (150, 50)
        )
        self.colorButton = wx.Button(
            self,
            12,
            "Copy Text",
            (150,450),
            (150,50)
        )
        self.Show()
        self.initBinds()

    def resetXInputList(self, event):
        self.mouseComboBox.clear();
        for mouse in getXInputList():
            self.mouseComboBox.append(mouse)

    def initBinds(self):
        self.Bind(
            wx.EVT_BUTTON,
            self.runSteam,
            self.steamButton
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.runChrome,
            self.chromeButton
        )
        self.Bind(
            wx.EVT_COMBOBOX,
            self.resetXInputList,
            self.mouseComboBox
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.changeSensitivity,
            self.changeMouseSensButton
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.pkill,
            self.killButton
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.coloredText,
            self.colorButton
        )

    def pkill(self, event):
        application = self.killApp.GetValue()
        if(application == "Frozen Application"):
            self.errorBox("No application given to kill.")
            return
        os.popen("pkill -9 "+application)

    def coloredText(self, event):
        color = self.colorChanger.GetValue()
        if(color != "Rainbow-W" and color != "Rainbow-L"):
            hexCharacter = chr(colorDict[color])
            clipboard.set_text(hexCharacter+self.colorText.GetValue())
        elif(color == "Rainbow-W"):
            coloredString = ""
            stringList = self.colorText.GetValue().split()
            for i in range(0,len(stringList)):
                string = stringList[i]
                rainbowNumber = i
                rainbowCharacter = rainbow[rainbowNumber % 7]
                coloredString += rainbowCharacter + string+ " "
            clipboard.set_text(coloredString)
        else:
            coloredString = ""
            stringList = list(self.colorText.GetValue())
            clipboard.set_text(rainbowify(stringList))
        clipboard.store()

    def changeSensitivity(self, event):
        p = re.compile(ur'\d+')
        matches = re.findall('id=\d+', self.mouseComboBox.GetValue())
        try:
            id = re.findall('\d+', matches[0])[0]
        except IndexError:
            self.errorBox("Please select your mouse.")
            return
        multiplier = self.speedMultiplier.GetValue()
        try:
            multiplier = str(1/float(multiplier))
        except ValueError:
            self.errorBox("Multipler was not a number, change it.")
            return
        if (float(multiplier) > 0.1):
            commandString = "xinput "
            commandString += "--set-prop "
            commandString += str(id)
            commandString += " 'Device Accel Constant Deceleration' "
            commandString += multiplier
            os.popen(commandString)
        else:
            self.errorBox("Multiplier was larger than 10.")

    def errorBox(self, message):
        dialog = wx.MessageDialog(
            self,
            message,
            "Error",
            style=wx.OK,
            pos=wx.DefaultPosition
        )
        dialog.ShowModal()

    def steamButton(self):
        return self.steamButton

    def processHandler(self):
        return self.processHandler

    def runSteam(self, event):
        self.processHandler.addProcess(Execute("steam"),"steam")

    def runChrome(self, event):
        self.processHandler.addProcess(Execute("mchrome tmphome"), "chrome")

def rainbowify(list):
        coloredString = ""
        spaceCounter = 0
        i = 0
        for char in list:
            if char == " ":
                coloredString += " "
                continue
            else:
                rainbowCharacter = rainbow[i % 7]
                coloredString += rainbowCharacter + char
                i += 1
        return coloredString

def Execute(command):
    process = wx.Process()
    wx.Execute(command, wx.EXEC_ASYNC, process)
    return process

def getXInputList():
    fullList = subprocess.check_output(["xinput", "--list", "--short"])
    return [s.strip() for s in fullList.splitlines()]

if __name__ == '__main__':
    dotaSocApp = wx.App()
    procHandle = ProcessHandler()
    mainPanel = FrameHandler(None, 'Dota Soc Control Panel', procHandle)
    dotaSocApp.MainLoop()

