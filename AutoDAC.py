import wx
import numpy as np
import MicroscopeInterface.src.Main as Run


class UI(wx.Frame):

    def __init__(self, parent, title):
        super(UI, self).__init__(parent, title=title,
            size=(750, 500))

        self.InitUI()
        self.Centre()
        self.Show()

        self.lif_path = None
        self.save_path = None

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(5, 5)

        text1 = wx.StaticText(panel, label="Welcome to AutoDAC")
        sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM,
            border=15)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        text3 = wx.StaticText(panel, label="Absolute LIF file path")
        sizer.Add(text3, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

        button1 = wx.Button(panel, label="Browse...")
        sizer.Add(button1, pos=(3, 1), flag=wx.TOP|wx.RIGHT, border=5)
        button1.Bind(wx.EVT_BUTTON, self.LIFBrowse)

        # text4 = wx.StaticText(panel, label="Absolute directory path to store the images")
        # sizer.Add(text4, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)

        # button2 = wx.Button(panel, label="Browse...")
        # sizer.Add(button2, pos=(4, 1), flag=wx.TOP|wx.RIGHT, border=5)
        # button2.Bind(wx.EVT_BUTTON, self.ImageBrowse)

        button4 = wx.Button(panel, label="Start")
        sizer.Add(button4, pos=(7, 3))
        button4.Bind(wx.EVT_BUTTON, self.Start)

        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

    def Start(self, e):
        scores = Run.start_analysis(self.lif_path, self.save_path)

        total = np.ndarray.sum(scores)
        formatted_result = 'Number of cells of interest: ' + str(total) + '\n'

        if total != 0:
            formatted_result += 'Number of rejects: ' + str(scores[0]) + '\n'
            for i, score in enumerate(scores[1:]):
                formatted_result += 'Number of cells scoring ' + str(i + 1) + '/8: ' + str(score) + ' (' + str(int((score / total) * 100)) + '%)' + '\n'

        wx.MessageBox(formatted_result, 'Results', wx.OK | wx.ICON_INFORMATION)

    def LIFBrowse(self, e):
        dialog = wx.FileDialog(None, 'Select', style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, wildcard="*.lif")

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        else:
            path = None

        dialog.Destroy()
        self.lif_path = path

    def ImageBrowse(self, e):
        dialog = wx.DirDialog(None, "Choose directory to save images to", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        else:
            path = None

        dialog.Destroy()
        self.save_path = path


if __name__ == '__main__':

    # Create application object
    app = wx.App()
    # Container widget
    UI(None, title='AutoDAC')
    # Display application
    app.MainLoop()
