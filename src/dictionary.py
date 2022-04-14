#!/usr/bin/env python
# -*- coding: utf-8 -*-

import about
import dataaccess
import common

import os, io
import wx, wx.adv, wx.html, wx.lib.newevent
import zipfile

OnSearchSelectEvent, EVT_SEARCH_SELECT = wx.lib.newevent.NewEvent()

class SearchPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        search_sizer = wx.BoxSizer(wx.VERTICAL)
        
        search_h = -1
        if "wxGTK" in wx.PlatformInfo:
            search_h = 30
        self.search_box = wx.SearchCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, size=(-1, search_h))
        self.search_box.ShowCancelButton(True)
        self.search_box.SetDescriptiveText("Search \u2026")
        self.search_box.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        self.search_box.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch)

        search_sizer.Add(self.search_box, flag=wx.EXPAND)

        search_sizer.Add((0, 4), 0, 0, 0)
        
        self.search_list = wx.ListBox(self, wx.ID_ANY, style=wx.LB_SINGLE|wx.LB_ALWAYS_SB)
        self.Bind(wx.EVT_LISTBOX, self.OnItemSelect, self.search_list)
        search_sizer.Add(self.search_list, proportion=1, flag=wx.EXPAND)

        self.SetSizer(search_sizer)

        self.db = dataaccess.DataAccess() 
        self.ids = []
        self.ShowSuggestWord()

    def ShowSuggestWord(self):
        suggest = self.db.SuggestWord()
        self.ids.clear()
        self.search_list.Clear()
        for o in suggest:
            self.search_list.Append(o["word"])
            self.ids.append(o["id"])

    def OnSearch(self, _):
        val = self.search_box.GetValue()
        data = self.db.Word(val)
        self.ids.clear()
        self.search_list.Clear()
        for o in data:
            self.search_list.Append(o["word"])
            self.ids.append(o["id"])

    def OnItemSelect(self, _):
        sel = self.search_list.GetSelection()
        definition = self.db.Definition(self.ids[sel])
        evt = OnSearchSelectEvent(data=definition)
        wx.PostEvent(self, evt)

    def __del__(self):
        self.db.__del__()


class DetailsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.html = wx.html.HtmlWindow(self, wx.ID_ANY)
        self.html.SetStandardFonts(size=12)

        sizer.Add(self.html, 1, wx.EXPAND|wx.ALL, 0)

        self.image_panel = wx.Panel(self, wx.ID_ANY)
        image_sizer = wx.BoxSizer(wx.VERTICAL)
        image_sizer.Add(wx.StaticLine(self.image_panel, wx.HORIZONTAL), 0, wx.EXPAND|wx.ALL, 0)
        
        self.image = wx.StaticBitmap(self.image_panel, wx.ID_ANY, size=(200, 150))
        image_sizer.Add(self.image, 1, wx.TOP|wx.LEFT|wx.ALIGN_CENTER_HORIZONTAL, 10)

        self.image_panel.SetSizer(image_sizer)
        
        sizer.Add(self.image_panel, 0, wx.EXPAND|wx.ALL, 5)
        self.image_panel.Hide()

        self.SetSizer(sizer)
        self.Layout()

    def SetDefinition(self, data):
        _, _, _, title, definition, _, synonym, filename, picture, _ = data
        text = '<html><head><title>%s</title></head><body>' % title
        text += definition

        if synonym:
            text += '<hr /><font size="3">Synonym</font><p>%s</p>' % synonym
        
        if picture:
            zip_path = os.path.join(common.assets_path, common.picture_zip_file)
            if os.path.exists(zip_path):
                try:
                    with zipfile.ZipFile(zip_path, mode="r") as archive:
                        pic_bytes = archive.read('%s.png' % filename)
                        pic_io = io.BytesIO(pic_bytes)
                        pic_img = wx.Image(stream=pic_io, type=wx.BITMAP_TYPE_PNG)
                        self.image.SetBitmap(wx.Bitmap(pic_img))
                        self.image_panel.Show()
                except EnvironmentError as err:
                    print(err)
        else:
            self.image_panel.Hide()    
            
        text += '</body></html>'
        self.html.SetPage(text)
        self.Layout()

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame, app):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        self.app = app
        icon = wx.Icon(frame.icon_path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnOpen)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        open_item = wx.MenuItem(menu, -1, "Open Dictionary")
        menu.Bind(wx.EVT_MENU, self.OnOpen, id=open_item.GetId())
        menu.Append(open_item)

        exit_item = wx.MenuItem(menu, -1, "Exit")
        menu.Bind(wx.EVT_MENU, self.OnQuit, id=exit_item.GetId())
        menu.Append(exit_item)
        return menu

    def OnOpen(self, _):
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()

    def OnQuit(self, event):
        if self.frame:
            self.frame.Quit()
        else:
            self.app.ExitMainLoop()

class MainFrame(wx.Frame):

    def __init__(self, app):
        wx.Frame.__init__(self, None)
        self.SetSize((800, 600))
        self.SetTitle(common.app_title)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.icon_path = os.path.join(common.assets_path, 'icon.ico')
        icon = wx.Icon(self.icon_path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.app = app

        # Menu Bar
        self.menubar = wx.MenuBar()

        file_menu = wx.Menu()
        
        exit_menu = file_menu.Append(wx.ID_ANY, "E&xit", "")
        self.Bind(wx.EVT_MENU, self.OnQuit, exit_menu)
        
        self.menubar.Append(file_menu, "&File")
        
        about_menu = wx.Menu()
        info_menu = about_menu.Append(wx.ID_ANY, "&About \u2026", "")
        self.Bind(wx.EVT_MENU, self.OnAbout, info_menu)
        
        self.menubar.Append(about_menu, "&Help")

        self.SetMenuBar(self.menubar)
        # Menu Bar end

        self.panel = wx.Panel(self, wx.ID_ANY)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        splitter = wx.SplitterWindow(self.panel, wx.ID_ANY, style=wx.SP_3D|wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(120)
        sizer.Add(splitter, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        self.search_pane = SearchPanel(splitter)
        self.search_pane.Bind(EVT_SEARCH_SELECT, self.OnSearchSelect)
        self.details_pane = DetailsPanel(splitter)
        
        splitter.SplitVertically(self.search_pane, self.details_pane, 220)

        self.panel.SetSizer(sizer)
        self.Layout()

        self.setupTaskBarIcon()

    def setupTaskBarIcon(self):
        self.taskbar_icon = None
        if wx.adv.TaskBarIcon.IsAvailable():
            self.taskbar_icon = TaskBarIcon(self, self.app)

    def OnSearchSelect(self, event):
        self.SetTitle("%s - [%s]" % (common.app_title, event.data[1]))
        self.details_pane.SetDefinition(event.data)

    def OnAbout(self, _):
        about_dialog = about.AboutBox(self)
        about_dialog.CenterOnParent()
        about_dialog.ShowModal()
        about_dialog.Destroy()

    def Quit(self):
        self.Close(force=True)
        if self.taskbar_icon:
            self.taskbar_icon.RemoveIcon()
            self.taskbar_icon.Destroy()

        self.Destroy()
        self.app.ExitMainLoop()

    def OnQuit(self, _):
        self.Quit()

    def OnClose(self, event):
        if event.CanVeto():
            self.Hide()
            event.Veto()
        else:
            event.Skip()
        

class EngMyanApp(wx.App):

    def OnInit(self):
        self.frame = MainFrame(self)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True    


def main():
    app = EngMyanApp(False)
    app.MainLoop()