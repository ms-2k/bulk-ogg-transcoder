import wx
from os.path import join as join_path
from ffmpeg import ensure_ffmpeg, ffmpeg_path
from encode import encode_all

#main window class
class FrameMain(wx.Frame):

    #init
    def __init__(self, parent = None, *args):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = 'Simple Bulk Encoder', pos = wx.DefaultPosition, size = wx.Size(500,225), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        #size constraints
        self.SetSizeHints(wx.Size(500, 225), wx.Size(500, 225))
        self.SetBackgroundColour(wx.Colour(200, 200, 200))

        self.timer = wx.Timer(self, id=wx.ID_ANY)

        #main container
        container_main = wx.BoxSizer(wx.VERTICAL)
        
        #input folder label
        self.label_input = wx.StaticText(self, wx.ID_ANY, u"Input Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_input.SetLabelMarkup(u"Input Folder")
        self.label_input.Wrap(-1)
        self.label_input.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        container_main.Add(self.label_input, 0, wx.ALL, 5)

        #input folder selection
        self.dir_input = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u'Select a folder', wx.DefaultPosition, wx.Size(475,-1), wx.DIRP_DEFAULT_STYLE)
        container_main.Add(self.dir_input, 0, wx.ALL, 5)


        #output folder label
        self.label_output = wx.StaticText(self, wx.ID_ANY, u"Output Folder", wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_output.Wrap(-1)
        container_main.Add(self.label_output, 0, wx.ALL, 5)

        #output folder selection
        self.dir_output = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u'Select a folder', wx.DefaultPosition, wx.Size(475,-1), wx.DIRP_DEFAULT_STYLE)
        container_main.Add(self.dir_output, 0, wx.ALL, 5)


        #container for execution buttons
        container_start = wx.GridSizer(0, 2, 0, 0)

        #ensure ffmpeg button
        self.button_ffmpeg = wx.Button(self, wx.ID_ANY, u"Ensure FFmpeg", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_ffmpeg.Bind(wx.EVT_BUTTON, self.on_click)
        self.button_ffmpeg.SetName(u'bFFmpeg')
        container_start.Add(self.button_ffmpeg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 5)

        #status text
        self.label_status = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        container_main.Add(self.label_status, 0, wx.ALL, 5)

        #start transcode button
        self.button_start = wx.Button(self, wx.ID_ANY, u"Start Transcode", wx.DefaultPosition, wx.Size(235,-1), 0)
        self.button_start.Bind(wx.EVT_BUTTON, self.on_click)
        self.button_start.SetName(u'bStart')
        container_start.Add(self.button_start, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        container_main.Add(container_start, 1, wx.EXPAND, 5)


        #finalize
        self.SetSizer(container_main)
        self.Layout()
        self.Centre(wx.BOTH)

    #resets the status label
    def reset_status(self):
        self.label_status.SetLabelText(wx.EmptyString)

    #calls encode_all
    def start(self):

        #acquire FFmpeg path
        ffmpeg = ffmpeg_path()

        #input and output paths
        ipath = self.dir_input.GetPath()
        opath = self.dir_output.GetPath()

        #use ipath/output if output path is not specified
        if len(opath) < 1:
            opath = join_path(ipath, 'output')

        #call encode_all
        encode_all(ffmpeg, ipath, opath, 160)

    #called when a button is clicked
    def on_click(self, event):

        #check what was clicked
        clicked = event.GetEventObject().GetName()
        
        #ensure ffmpeg
        if(clicked == 'bFFmpeg'):
            
            #change status label
            self.label_status.SetLabelText('Downloading...')

            #call ensure ffmpeg
            wx.CallLater(100, ensure_ffmpeg)

            #reset status label
            wx.CallLater(200, self.reset_status)

            #instantiate finisher dialog (it just says done!)
            ok = FrameDialog(title = u'Done', parent=wx.GetTopLevelParent(self))
            wx.CallLater(300, ok.Show)

        #start
        elif(clicked == 'bStart'):

            #check if ffmpeg exists
            #let the user know if it's not present
            if ffmpeg_path() == None:
                ok = FrameDialog(title = u'Error', display_text=u'No FFmpeg', parent=wx.GetTopLevelParent(self))
                ok.Show()
                return
            
            #check if input path points to anything (can't encode nothing)
            if len(self.dir_input.GetPath()) < 1:
                ok = FrameDialog(title = u'Error', display_text=u'Invalid input', parent=wx.GetTopLevelParent(self))
                ok.Show()
                return
            
            #change status label
            self.label_status.SetLabelText('Running...')

            #call start
            wx.CallLater(100, self.start)

            #reset status label when it's done
            wx.CallLater(200, self.reset_status)

            #display finisher dialog
            ok = FrameDialog(title = u'Done', parent=wx.GetTopLevelParent(self))
            wx.CallLater(300, ok.Show)


#dialog frame
class FrameDialog (wx.Dialog):

    #initialize
    #parent = the parent window (need to set or it won't close with the parent)
    #display_text = what will be displayed in the main body
    #title = what will be displayed as the title (top bar)
    def __init__(self, parent = None, display_text = u'Done!', title = wx.EmptyString):
        wx.Dialog.__init__ (self, parent, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE)

        #set size
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        #main dialog container
        container_dialog = wx.GridSizer(0, 1, 0, 0)

        #the actual dialog text
        self.text_dialog = wx.StaticText(self, wx.ID_ANY, display_text, wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_dialog.Wrap(-1)
        container_dialog.Add(self.text_dialog, 0, wx.ALL, 5)

        #the exit text (it will say "OK")
        self.button_dialog = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_dialog.Bind(wx.EVT_BUTTON, self.on_click)
        self.confirmed = False
        container_dialog.Add(self.button_dialog, 0, wx.ALIGN_CENTER|wx.ALL, 5)


        #format it
        self.SetSizer(container_dialog)
        self.Layout()
        container_dialog.Fit(self)
        self.Centre(wx.BOTH)
    
    #close the window when OK is clicked
    def on_click(self, event):
        self.Close()


#main
if __name__ == '__main__':

    #create app and start main loop
    app = wx.App(False)
    frame = FrameMain(None)
    frame.Show()
    app.MainLoop()