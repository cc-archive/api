"""
rest-wx-client.py
$Id$

Sample implementation of REST client using wxPython.
(c) 2004, Nathan R. Yergler, Creative Commons

"""

import urllib2
import libxml2
import libxslt

import wx
import wx.lib.dialogs

class CcRest:
    """Wrapper class to decompose REST XML responses into Python objects."""
    
    def __init__(self, root):
        self.root = root

        self.__lc_doc = None

    def license_classes(self, lang='en'):
        """Returns a dictionary whose keys are license IDs, with the
        license label as the value."""

        lc_url = '%s/%s' % (self.root, 'classes')

        # retrieve the licenses document and store it
        self.__lc_doc = urllib2.urlopen(lc_url).read()

        # parse the document and return a dictionary
        lc = {}
        d = libxml2.parseMemory(self.__lc_doc, len(self.__lc_doc))
        c = d.xpathNewContext()

        licenses = c.xpathEval('//licenses/license')

        for l in licenses:
            lc[l.xpathEval('@id')[0].content] = l.content
            
        return lc
        
    def fields(self, license, lang='en'):
        """Retrieves details for a particular license."""

        l_url = '%s/license/%s' % (self.root, license)

        # retrieve the license source document
        self.__l_doc = urllib2.urlopen(l_url).read()

        d = libxml2.parseMemory(self.__l_doc, len(self.__l_doc))
        c = d.xpathNewContext()
        
        self._cur_license = {}

        fields = c.xpathEval('//field')

        for field in fields:
            f_id = field.xpathEval('@id')[0].content
            self._cur_license[f_id] = {}

            self._cur_license[f_id]['label'] = \
                              field.xpathEval('label')[0].content
            self._cur_license[f_id]['description'] = \
                              field.xpathEval('description')[0].content
            self._cur_license[f_id]['type'] = \
                              field.xpathEval('type')[0].content
            self._cur_license[f_id]['enum'] = {}

            # extract the enumerations
            enums = field.xpathEval('enum')
            for e in enums:
                e_id = e.xpathEval('@id')[0].content
                self._cur_license[f_id]['enum'][e_id] = \
                     e.xpathEval('label')[0].content
            
        return self._cur_license

    def issue(self, license, answers, lang='en'):
        l_url = '%s/license/%s/issue' % (self.root, license)

        # construct the answers.xml document from the answers dictionary
        answer_xml = """
        <answers>
          <license-%s>""" % license

        for key in answers:
            answer_xml = """%s
            <%s>%s</%s>""" % (answer_xml, key, answers[key], key)

        answer_xml = """%s
          </license-%s>
        </answers>
        """ % (answer_xml, license)

        
        # retrieve the license source document
        self.__a_doc = urllib2.urlopen(l_url,
                                       data='answers=%s' % answer_xml).read()

        return self.__a_doc
        
class LicenseFrame(wx.Frame):
    REST_ROOT = 'http://api.creativecommons.org/rest'
    
    def __init__(self, parent, title=None):
        wx.Frame.__init__(self, None, title=title)

        # initialize tracking attributes
        self.__license = ''
        self.__fields = []
        self.__fieldinfo = {}

        # create the web services proxy
        self.__cc_server = CcRest(self.REST_ROOT)
        
        # create the primary frame sizer
        self.sizer = wx.GridBagSizer(5, 5)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(1)
        self.SetSizer(self.sizer)

        # create the basic widgets
        self.cmbLicenses = wx.ComboBox(self,
                                       style=wx.CB_DROPDOWN|wx.CB_READONLY
                                       )
        self.sizer.Add(self.cmbLicenses, (0,0),
                       flag=wx.EXPAND|wx.ALL)

        # set up a call later to update the license class list
        wx.CallAfter(self.getLicenseClasses)

        # create the panel for the fields
        self.pnlFields = wx.Panel(self)
        self.sizer.Add(self.pnlFields, (1,0),
                       flag=wx.EXPAND|wx.ALL)

        self.cmdLicense = wx.Button(self, label="Get License")
        self.sizer.Add(self.cmdLicense, (2,0), flag = wx.ALIGN_RIGHT)

        # set up the field panel sizer
        self.fieldSizer = wx.FlexGridSizer(0, 2, 5, 5)
        self.fieldSizer.AddGrowableCol(1)
        self.pnlFields.SetSizer(self.fieldSizer)

        # bind event handlers
        self.Bind(wx.EVT_COMBOBOX, self.onSelectLicenseClass, self.cmbLicenses)
        self.Bind(wx.EVT_BUTTON,   self.onLicense,       self.cmdLicense)

    def getLicenseClasses(self):
        """Calls the SOAP API via proxy to get a list of all available
        license class identifiers."""

        self.__l_classes = self.__cc_server.license_classes()
        self.cmbLicenses.AppendItems(self.__l_classes.values())

    def onLicense(self, event):
        """Submit selections and display license info."""
        answers = {}

        for field in self.__fields:
            if self.__fieldinfo[field]['type'] == 'enum':
                answer_key = [n for n in self.__fieldinfo[field]['enum'] if
                              self.__fieldinfo[field]['enum'][n] ==
                              self.__fieldinfo[field]['control'].GetValue()][0]

                answers[field] = self.__fieldinfo[field]['enum'][answer_key]

        wx.lib.dialogs.alertDialog(self,
                       self.__cc_server.issue(self.__license, answers),
                       'License Results')
        
    def onSelectLicenseClass(self, event):
        if event.GetString() == '' or event.GetString() == self.__license:
            # bail out if there's no change; we'll get called again momentarily
            return
        
        # get the new license ID
        self.__license = [n for n in self.__l_classes.keys()
                          if self.__l_classes[n] == event.GetString()][0]
        
        # clear the sizer
        self.pnlFields.GetSizer().Clear(True)

        # retrieve the fields
        fields = self.__cc_server.fields(self.__license)
        self.__fields = fields.keys()
        self.__fieldinfo = fields

        for field in self.__fields:
            # update the UI
            self.updateFieldDetails(field)

    def updateFieldDetails(self, fieldid):
        
        field = fieldid
        self.__fieldinfo[field] = dict(self.__fieldinfo[field])

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
            self.__fieldinfo[field]['control'] = \
                 wx.ComboBox(self.pnlFields,
                             style=wx.CB_DROPDOWN|wx.CB_READONLY,
                             choices = self.__fieldinfo[field]['enum'].values()
                             )
            self.__fieldinfo[field]['control'].SetSelection(0)
            self.pnlFields.GetSizer().Add(
                self.__fieldinfo[field]['control'],
                flag = wx.EXPAND | wx.ALL)

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
