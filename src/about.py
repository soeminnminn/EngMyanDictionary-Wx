"""
About box with general info

@license: MIT (see LICENSE.txt) - THIS PROGRAM COMES WITH NO WARRANTY
"""

import codecs
import wx
import wx.html
import wx.lib.wxpTag
import common
import os.path

class CreditBox(wx.Dialog):
    text = '''
    <html>
    <body bgcolor="#000000" text="#ffffff">
    <center>
        <p><font color="#00FF00" size="5">Ministry of Education, Union of Myanmar</font></p>
		<p><font color="#FFF895" size="4">Department of Myanmar Language Commission</font></p>
		<p><font color="#00AAE9" size="4">Produced By World Peace IT Co.,Ltd.</font></p>
		<p><font color="#F1956E">Producer</font></p>
		<p>Daw Wah Wah Htun</p>
		<p><font color="#F1956E">Management</font></p>
		<p>U Mg Mg Tin</p>
		<p>Daw Tin Tin Myint</p>
		<p><font color="#F1956E">Programming</font></p>
		<p>Mi Min Myo Minn</p>
		<p>Win Ko</p>
		<p>Moe Khin Mar Lay</p>
		<p>Za Uk Lian</p>
		<p><font color="#F1956E">Designers</font></p>
		<p>Moe Myint</p>
		<p>Aung Maw Oo</p>
		<p>Tandar Soe Myint</p>
		<p><font color="#F1956E">Audio</font></p>
		<p>Kyaw Kyaw Lwin</p>
		<p>Han Minn Soe</p>
		<p>Naw Minn Minn Htun</p>
		<p>Ei Phyu Phyu Win</p>
		<p>&nbsp;</p>
		<p><font color="#288B03" size="5">ပညာရေး ဝန်ကြီးဌာန</font></p>
		<p><font size="4">မြန်မာစာ အဖွဲ့</font></p>
    </center>
    </body>
    </html>
    '''

    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, -1, 'Dictionary Credit')
        html = wx.html.HtmlWindow(self, -1, size=(400, 250))
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
        html.SetPage(self.text)
        szr = wx.BoxSizer(wx.VERTICAL)
        szr.Add(html, 0, wx.TOP|wx.ALIGN_CENTER, 0)
        szr2 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, wx.ID_OK, "OK")
        btn.SetDefault()
        szr2.Add(btn)
        if wx.Platform == '__WXGTK__':
            extra_border = 5  # border around a default button
        else:
            extra_border = 0
        szr.Add(szr2, 0, wx.ALL|wx.ALIGN_RIGHT, 20 + extra_border)
        self.SetAutoLayout(True)
        self.SetSizer(szr)
        szr.Fit(self)
        self.Layout()
        if parent: self.CenterOnParent()
        else: self.CenterOnScreen()


class AboutBox(wx.Dialog):
    text = '''
    <html>
    <body bgcolor="%s">
    <!-- <font size="-1"> -->
    <center>
    <table align="center" border="2" cellspacing="0">
    <tr>
    <td align="center"><img src="%s">
    </td></tr>
    <tr><td bgcolor="#000000" align="center">
    <font color="#ffffff">Version %s on Python %s and wxPython %s</font>
    </td></tr>
    </table>
    </center>
    <!-- </font> -->
    <table border="0" cellpadding="0" cellspacing="0">
    <tr><td width="50"></td><td>
    <!-- <font size="-1"> -->
    <b><p>License: MIT (see <a href="show_license">LICENSE</a>)</b><br>
    <!-- wxPyColourChooser code copyright (c) 2002-2004 <br>Soe Minn Minn 
    (wxWindows license) -->
    <p>Home page:
    <a href="https://soeminnminn.github.io">Soe Minn Minn</a>
    <p>For credits, see
    <a href="show_credits">CREDITS</a>.<!-- </font> --></td>
    </tr></table>
    </body>
    </html>
    '''

    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, -1, 'About Dictionary')
        html = wx.html.HtmlWindow(self, -1, size=(400, 250))
        html.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnLinkClicked)
        # it's recommended at least for GTK2 based wxPython
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
        bgcolor = common.color_to_string(self.GetBackgroundColour())
        icon_path = os.path.join(common.assets_path, 'ic_launcher.png')
        html.SetPage( self.text % (bgcolor, icon_path, common.version, common.py_version, common.wx_version) )
        ir = html.GetInternalRepresentation()
        ir.SetIndent(0, wx.html.HTML_INDENT_ALL)
        html.SetSize((ir.GetWidth(), ir.GetHeight()))
        szr = wx.BoxSizer(wx.VERTICAL)
        szr.Add(html, 0, wx.TOP|wx.ALIGN_CENTER, 10)
        szr.Add(wx.StaticLine(self, -1), 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 20)
        szr2 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, wx.ID_OK, "OK")
        btn.SetDefault()
        szr2.Add(btn)
        if wx.Platform == '__WXGTK__':
            extra_border = 5  # border around a default button
        else:
            extra_border = 0
        szr.Add(szr2, 0, wx.ALL|wx.ALIGN_RIGHT, 20 + extra_border)
        self.SetAutoLayout(True)
        self.SetSizer(szr)
        szr.Fit(self)
        self.Layout()
        if parent: self.CenterOnParent()
        else: self.CenterOnScreen()

    def OnLinkClicked(self, event):
        href = event.GetLinkInfo().GetHref()
        if href == 'show_license':
            if common.license_file:
                from wx.lib.dialogs import ScrolledMessageDialog
                try:
                    license_path = os.path.join(common.working_dir, common.license_file)
                    license_file = codecs.open(license_path, encoding='UTF-8')
                    dlg = ScrolledMessageDialog(self, license_file.read(), "Dictionary - License")
                    license_file.close()
                    dlg.CenterOnParent()
                    dlg.ShowModal()
                    dlg.Destroy()
                except EnvironmentError:
                    wx.MessageBox('Can\'t read the file "LICENSE".\n\nYou can get a license copy at\n'
                          'http://www.opensource.org/licenses/mit-license.php',
                          'Error', wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION)
            else:
                wx.MessageBox('File "LICENSE.txt" not found!\nYou can get a license copy at\n'
                                'http://www.opensource.org/licenses/mit-license.php',
                              'Error', wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION)
        elif href == 'show_credits':
            credit_dialog = CreditBox(self)
            credit_dialog.CenterOnParent()
            credit_dialog.ShowModal()
            credit_dialog.Destroy()
        else:
            import webbrowser
            webbrowser.open(href, new=True)


