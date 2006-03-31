"""
soap-wx-client.py
$Id$

Sample implementation of SOAP client using wxPython.
(c) 2004, Nathan R. Yergler, Creative Commons

TODO:
 * SOAP progress feedback
   * convert SOAP calls to two-part (start, then get result in different func)
 
"""

import threading

import wx
import wx.lib.dialogs
import SOAPpy

myEVT_FINISHED_EVENT = wx.NewEventType()
EVT_FINISHED_EVENT = wx.PyEventBinder(myEVT_FINISHED_EVENT, 1)

class ThreadFinishedEvent(wx.PyCommandEvent):
    def __init__(self, id):
        evtType = myEVT_FINISHED_EVENT
        wx.PyCommandEvent.__init__(self, evtType, id)
        
class SoapThread(threading.Thread):
    def __init__(self, parent, method, params, callback, server_proxy):
        threading.Thread.__init__(self)
        self.parent = parent
        self.__server = server_proxy
        self.__callback = callback
        self.__method = method
        self.__params = params

        self.start()

    def run(self):
        """Make the call to the SOAP Proxy"""
        method = getattr(self.__server, self.__method)
        result = method(*self.__params)
        self.__callback(self, result)

        wx.PostEvent(self.parent, ThreadFinishedEvent(self.parent.GetId()))
        
    def abort(self):
        self.__want_abort = True
        
class wxSoapProxy(wx.Gauge):
    DELAY = 100
    GAUGE_MAX = 50
    
    def __init__(self, parent, server):
        wx.Gauge.__init__(self, parent, -1, self.GAUGE_MAX)

        # store a reference to the actual SOAP Proxy
        self.__server = SOAPpy.SOAPProxy(server)

        # create the timer object we'll use
        self.timer = wx.Timer(self)

        # bind to events
        self.Bind(EVT_FINISHED_EVENT, self.onFinished)
        self.Bind(wx.EVT_TIMER,       self.onIncrement)
        
    def onFinished(self, event):
        self.timer.Stop()
        self.resetGauge()

    def resetGauge(self):
        self.SetValue(0)
        
    def onIncrement(self, event):
        self.SetValue(self.__count)

        if self.__count == self.GAUGE_MAX - 1:
            self.__count = 0
        else:
            self.__count = self.__count + 1
    
    def call(self, method, params, callback):
        self.__count = 0
        self.__thread = SoapThread(self, method, params,
                                   callback, self.__server)
        self.timer.Start(self.DELAY)
        
class LicenseFrame(wx.Frame):
    def __init__(self, parent, title=None):
        wx.Frame.__init__(self, None, title=title)

        # create the SOAP proxy
        self.__cc_server = SOAPpy.SOAPProxy(
            'http://api.creativecommons.org/soap')

        # initialize tracking attributes
        self.__license = ''
        self.__fields = []
        self.__fieldinfo = {}
        
        # create the sizer
        self.sizer = wx.GridBagSizer(5, 5)
        self.SetSizer(self.sizer)

        # create the basic widgets
        self.cmbLicenses = wx.ComboBox(self,
                                       style=wx.CB_DROPDOWN|wx.CB_READONLY,
                                       choices=self.__cc_server.licenses())
        self.sizer.Add(self.cmbLicenses, (0,0))

        # create the panel for the fields
        self.pnlFields = wx.Panel(self)
        self.sizer.Add(self.pnlFields, (1,0))

        self.cmdLicense = wx.Button(self, label="Get License")
        self.sizer.Add(self.cmdLicense, (2,0))

        # set up the field panel sizer
        self.fieldSizer = wx.FlexGridSizer(0, 2, 5, 5)
        self.fieldSizer.AddGrowableCol(1)
        self.pnlFields.SetSizer(self.fieldSizer)

        # bind event handlers
        self.Bind(wx.EVT_COMBOBOX, self.onChangeLicense, self.cmbLicenses)
        self.Bind(wx.EVT_BUTTON,   self.onLicense,       self.cmdLicense)

        # do final initialization

        # SOAP PROXY TEST CODE
        self.proxy = wxSoapProxy(self, 'http://api.creativecommons.org/soap')
        # self.__cc_server)
        self.sizer.Add(self.proxy, (3,0))
        foo = wx.Button(self, label="test")
        self.sizer.Add(foo, (4,0))

        self.Bind(wx.EVT_BUTTON, self.OnTest, foo)

    def OnTest(self, event):
        self.proxy.call('licenses', [], self.OnTestFinished)
        
    def OnTestFinished(self, thread, result):
        print thread
        print result
        
    def onLicense(self, event):
        """Submit selections and display license info."""
        answers = {}

        for field in self.__fields:
            if self.__fieldinfo[field]['type'] == 'enum':
                answers[field] = self.__fieldinfo[field]['enum'][
                    self.__fieldinfo[field]['control'].GetValue()]

        wx.lib.dialogs.alertDialog(self,
                       self.__cc_server.getLicense(self.__license, answers),
                       'License Results')
        
    def onChangeLicense(self, event):
        if event.GetString() == '' or event.GetString() == self.__license:
            # bail out if there's no change; we'll get called again momentarily
            return
        
        # get the new license ID
        self.__license = event.GetString()
        print self.__license

        # clear the sizer
        self.pnlFields.GetSizer().Clear(True)
        
        # create the new fields
        self.__fields = self.__cc_server.fields(self.__license)
        self.__fieldinfo = {}
        
        for field in self.__fields:
            # get the field details
            self.__fieldinfo[field] = dict(
                self.__cc_server.fieldDetail(self.__license, field)
                )

            # make sure we have a label
            if self.__fieldinfo[field]['label'] == '':
                self.__fieldinfo[field]['label'] = field

            # add the label text
            self.__fieldinfo[field]['label_ctrl'] = wx.StaticText(
                self.pnlFields,
                label=self.__fieldinfo[field]['label'])

            self.pnlFields.GetSizer().Add(self.__fieldinfo[field]['label_ctrl'])
            # add the control
            if self.__fieldinfo[field]['type'] == 'enum':
                # enumeration field; retrieve the possibilities
                self.__fieldinfo[field]['enum'] = dict(
                    [(dict(n)['label'], dict(n)['id']) for n in
                     self.__cc_server.fieldEnum(self.__license, field)]
                    )

                self.__fieldinfo[field]['control'] = \
                     wx.ComboBox(self.pnlFields,
                                 style=wx.CB_DROPDOWN|wx.CB_READONLY,
                                 choices = self.__fieldinfo[field]['enum'].keys()
                                 )
                self.__fieldinfo[field]['control'].SetSelection(0)
                self.pnlFields.GetSizer().Add(
                    self.__fieldinfo[field]['control'])
                
            # add tooltip help
            wx.HelpProvider.Get().AddHelp(self.__fieldinfo[field]['control'],
                                          self.__fieldinfo[field]['description'])
            wx.HelpProvider.Get().AddHelp(self.__fieldinfo[field]['label_ctrl'],
                                          self.__fieldinfo[field]['description'])

                    
        self.Fit()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    wx.HelpProvider.Set(wx.SimpleHelpProvider())
    main = LicenseFrame(None, title="Chooser")
    main.Show()
    app.MainLoop()
