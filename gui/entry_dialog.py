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

        self.set_markup("Se the ID of the uploaded file:")
        self.add_buttons("OK",True,"Cancel",False)

        entry = gtk.Entry()        
        entry.set_text(str(default_value))
        entry.connect("activate", 
                      lambda ent, dlg, resp: dlg.response(resp), 
                      self, gtk.RESPONSE_OK)
#        button_cancel = gtk.Button("Cancel")
#        self.vbox.pack_end(button_cancel, True, True, 0)
#        button_cancel.connect("button-press-event",
#                      lambda a, b, c, d: gtk.main_quit(),
#                      self, gtk.RESPONSE_CANCEL)
#        button_ok = gtk.Button("Ok")
#        self.vbox.pack_end(button_ok, True, True, 0)
#        button_ok.connect("button-press-event",
#                      lambda a, b, c, d: gtk.main_quit(),
#                      self, gtk.RESPONSE_OK)
        self.vbox.pack_end(entry, True, True, 0)
        self.vbox.show_all()
        self.entry = entry

    # XXX Check this
    def do_button_press_event(self, event):
        """
        The button press event virtual method
        """
        if event.button == -5:
        return True

    def set_value(self, text):
        self.entry.set_text(text)

    def run(self):
        result = super(EntryDialog, self).run()
        if result in [gtk.RESPONSE_ACCEPT, gtk.RESPONSE_OK]:
            text = self.entry.get_text()
        else:
            text = None
        return text
