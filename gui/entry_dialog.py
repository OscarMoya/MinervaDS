#!/usr/bin/env python

import gtk


class EntryDialog(gtk.MessageDialog):
    def __init__(self, *args, **kwargs):
        """
        Creates a new EntryDialog. Takes all the arguments of the usual
        MessageDialog constructor plus one optional named argument 
        "default_value" to specify the initial contents of the entry.
        """
        
        if "default_value" in kwargs:
            default_value = kwargs["default_value"]
            del kwargs["default_value"]
        else:
            default_value = ""
        
        super(EntryDialog, self).__init__(*args, **kwargs)

        self.hbox = gtk.HBox()
        self.set_markup("Set the ID of the uploaded file: ")

        entry = gtk.Entry()        
        entry.set_text(str(default_value))
        entry.connect("activate", lambda ent, dlg, resp: dlg.response(resp),
                      self, gtk.RESPONSE_OK)

        button_cancel = gtk.Button("Cancel")
        self.hbox.pack_end(button_cancel, False, False, 0)
        button_cancel.connect("button-press-event", lambda a, b, c, d: self.destroy(),
                              self, gtk.RESPONSE_CANCEL)
        button_cancel.show()        

        button_ok = gtk.Button("Ok")
        self.hbox.pack_end(button_ok, False, False, 0)
        button_ok.connect("button-press-event", lambda a, b, c, d: self.text_callback(),
                      self, gtk.RESPONSE_OK)
        button_ok.show()

        self.vbox.pack_start(entry, True, True, 0)
        self.vbox.add(self.hbox)
        self.hbox.show()
        self.vbox.show_all()
        self.entry = entry

    def do_button_press_event(self, event):
        """
        The button press event virtual method
        """
        if event.button == -5:
            print "..."
        return True

    def set_value(self, text):
        self.entry.set_text(text)

    def run(self):
        result = super(EntryDialog, self).run()

#        if result in [gtk.RESPONSE_ACCEPT, gtk.RESPONSE_OK]:
        try:
            text = self.entry_text
            return text
            #elif result in [gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL]:
        except:
            pass

    def text_callback(self):
        self.entry_text = self.entry.get_text()
        #print "Entry contents:", self.entry_text
        self.destroy()
