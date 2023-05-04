import wx

class CustomFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size(500,225), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(500, 225), wx.Size(500, 225))
        self.SetBackgroundColour(wx.Colour(200, 200, 200))

        container_main = wx.BoxSizer(wx.VERTICAL)

        self.label_input = wx.StaticText(self, wx.ID_ANY, u"Input Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_input.SetLabelMarkup(u"Input Folder")
        self.label_input.Wrap(-1)

        self.label_input.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))

        container_main.Add(self.label_input, 0, wx.ALL, 5)

        container_input = wx.GridSizer(0, 2, 0, 0)

        self.text_input = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(325,-1), 0)
        container_input.Add(self.text_input, 0, wx.ALL, 5)

        self.button_input = wx.Button(self, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.Size(125,-1), 0)
        self.button_input.Bind(wx.EVT_BUTTON, self.OnClick)
        self.button_input.SetName(u'bInput')
        container_input.Add(self.button_input, 0, wx.ALIGN_RIGHT|wx.ALL, 5)


        container_main.Add(container_input, 1, wx.EXPAND, 5)

        self.label_output = wx.StaticText(self, wx.ID_ANY, u"Output Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_output.Wrap(-1)

        container_main.Add(self.label_output, 0, wx.ALL, 5)

        container_output = wx.GridSizer(0, 2, 0, 0)

        self.text_output = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(325,-1), 0)
        container_output.Add(self.text_output, 0, wx.ALL, 5)

        self.button_output = wx.Button(self, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.Size(125,-1), 0)
        self.button_output.Bind(wx.EVT_BUTTON, self.OnClick)
        self.button_output.SetName(u'bOutput')
        container_output.Add(self.button_output, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        container_main.Add(container_output, 1, wx.EXPAND, 5)


        container_start = wx.GridSizer(0, 2, 0, 0)

        self.button_ffmpeg = wx.Button(self, wx.ID_ANY, u"Ensure FFmpeg", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_ffmpeg.Bind(wx.EVT_BUTTON, self.OnClick)
        self.button_ffmpeg.SetName(u'bFFmpeg')
        container_start.Add(self.button_ffmpeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 5)

        self.panel_filler = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_filler.SetBackgroundColour(wx.Colour(200, 200, 200))
        container_main.Add(self.panel_filler, 1, wx.EXPAND | wx.ALL, 5)

        self.button_start = wx.Button(self, wx.ID_ANY, u"Start Transcode", wx.DefaultPosition, wx.Size(235,-1), 0)
        self.button_start.Bind(wx.EVT_BUTTON, self.OnClick)
        self.button_start.SetName(u'bStart')
        container_start.Add(self.button_start, 0, wx.ALIGN_CENTER|wx.ALL, 5)


        container_main.Add(container_start, 1, wx.EXPAND, 5)

        self.SetSizer(container_main)
        self.Layout()

        self.Centre(wx.BOTH)
    
    def OnClick(self, event, proc = print):
        proc(event.GetEventObject().GetName())

if __name__ == '__main__':

    app = wx.App(False)
    frame = CustomFrame(None)
    frame.Show()
    app.MainLoop()