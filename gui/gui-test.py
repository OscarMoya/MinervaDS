#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import subprocess

from entry_dialog import EntryDialog


def print_info(message):
    print "\033[0;34m%s\033[1;0m" % str(message)

class MinervaGUI:

    def __init__(self):

        #main window
        self.app_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.app_window.set_border_width(10)
        self.app_window.set_title("Minerva Demo GUI")

        # Center window and set proper size
        self.app_window.set_position(gtk.WIN_POS_CENTER)
        self.app_window.set_size_request(800, 600)
        self.app_window.set_default_size(min(gtk.gdk.screen_width(), 800), min(600, gtk.gdk.screen_height()))
       
        # Bind Escape to exit
        self.bind_element_to_key_with_method("Escape", self.app_window, gtk.main_quit)
        self.app_window.connect("delete_event", lambda w, e: gtk.main_quit())
        #self.app_window.connect("check-resize", lambda w: w.resize(100, 100))
        self.app_window.set_resizable(False)

        #window layouts
        vbox_app = gtk.VBox(False, 10)
        self.app_window.add(vbox_app)
        vbox_app.show()


        #layouts Table()
        table_layout = gtk.Table(rows=3, columns=10, homogeneous=False)
        table_layout.show()
        vbox_app.add(table_layout)

        table_body = gtk.Table(rows=4, columns=3, homogeneous=True)
        table_body.show()
        vbox_app.add(table_body)

        vbox_frames = gtk.VBox(False, 15)
        vbox_frames.show()
        table_body.attach(vbox_frames, 0, 1, 0, 4, 0, 0, 0, 0)

        vbox_canvas = gtk.VBox(False, 5)
        vbox_canvas.show()
        table_body.attach(vbox_canvas, 1, 2, 0, 4, 0, 0, 0, 0)

        #alignments
        align = gtk.Alignment(0.2, 0.1, 0.7, 0.3)
        vbox_frames.pack_start(align, True, True, 0)
        #align.show()

        #logos
        logo1 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/logo1.png")
        scaled_buf = pixbuf.scale_simple(200, 50, gtk.gdk.INTERP_BILINEAR)
        logo1.set_from_pixbuf(scaled_buf)

        logo2 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/logo2.png")
        scaled_buf = pixbuf.scale_simple(50, 50, gtk.gdk.INTERP_BILINEAR)
        logo2.set_from_pixbuf(scaled_buf)

        logo3 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/logo3.png")
        scaled_buf = pixbuf.scale_simple(110, 50, gtk.gdk.INTERP_BILINEAR)
        logo3.set_from_pixbuf(scaled_buf)

        logo4 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/logo4.png")
        scaled_buf = pixbuf.scale_simple(90, 50, gtk.gdk.INTERP_BILINEAR)
        logo4.set_from_pixbuf(scaled_buf)

        logo5 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/geant.jpg")
        scaled_buf = pixbuf.scale_simple(100, 50, gtk.gdk.INTERP_BILINEAR)
        logo5.set_from_pixbuf(scaled_buf)

        table_layout.attach(logo1, 0, 1, 0, 1, 0, 0, 0, 0)
        logo1.show()

        table_layout.attach(logo2, 2, 3, 0, 1, 0, 0, 0, 0)
        logo2.show()

        table_layout.set_col_spacing(1, 5)
        table_layout.set_col_spacing(2, 30)

        table_layout.attach(logo3, 3, 4, 0, 1, 0, 0, 0, 0)
        logo3.show()

        table_layout.attach(logo4, 4, 5, 0, 1, 0, 0, 1, 0)
        logo4.show()

        table_layout.set_col_spacing(3, 5)
        table_layout.set_col_spacing(4, 170)

        table_layout.attach(logo5, 6, 7, 0, 1, 0, 0, 0, 0)
        logo5.show()

        table_layout.set_row_spacing(0, 10)

        label_app = gtk.Label()
        label_app.set_use_markup(True)
        label_app.set_markup('<span size="16000"><b>MINERVA: Demonstrating resilience over non-secure channels</b></span>')
        table_layout.attach(label_app, 0, 10, 1, 2, 0, 0, 0, 0)
        label_app.show()


        separator = gtk.HSeparator()
        separator.set_size_request(750, 5)
        table_layout.attach(separator, 0, 10, 2, 3, 0, 0, 0, 0)
        separator.show()


        #main frames
        frame_vs = gtk.Frame('VIDEO STREAMING')
        frame_vs.set_label_align(0.5, 1.2)
        frame_ds = gtk.Frame('DISTRIBUTED STORAGE')
        frame_ds.set_label_align(0.5, 1.2)
        frame_vs.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame_ds.set_shadow_type(gtk.SHADOW_ETCHED_IN)

        vbox_frames.add(frame_vs)
        frame_vs.show()

        vbox_frames.add(frame_ds)
        frame_ds.show()

        vbox_vs = gtk.VBox(False, 15)
        vbox_ds = gtk.VBox(False, 15)

        #frame_vs.add(vbox_vs)
        #vbox_vs.show()
        #frame_ds.add(vbox_ds)
        #vbox_ds.show()

        ev_box_vs = gtk.EventBox()
        ev_box_vs.connect("enter-notify-event", self.callback_vs, "enter")
        ev_box_vs.connect("leave-notify-event", self.callback_vs, "leave")

        ev_box_ds = gtk.EventBox()
        ev_box_ds.connect("enter-notify-event", self.callback_ds, "enter")
        ev_box_ds.connect("leave-notify-event", self.callback_ds, "leave")

        ev_box = gtk.EventBox()
        ev_box.connect("enter-notify-event", self.callback, "enter")
        ev_box.connect("leave-notify-event", self.callback, "leave")

        ev_box_ii = gtk.EventBox()
        ev_box_ii.connect("enter-notify-event", self.callback, "enter")
        ev_box_ii.connect("leave-notify-event", self.callback, "leave")

        ev_box_vs.add(vbox_vs)
        ev_box_ds.add(vbox_ds)
        
        vbox_vs.show()
        vbox_ds.show()

        ev_box_vs.show()
        ev_box_ds.show()
        ev_box.show()
        ev_box_ii.show()

        frame_vs.add(ev_box_vs)
        frame_ds.add(ev_box_ds)

        vbox_app.add(ev_box)
        vbox_frames.add(ev_box_ii)
	

        #inner frames
        frame_vs_deploy = gtk.Frame("Deployment / Operation")
        frame_ds_deploy = gtk.Frame("Deployment / Operation")
        frame_vs_failure = gtk.Frame("Failure Simulation")
        frame_ds_failure = gtk.Frame("Failure Simulation")

        frame_vs_deploy.set_shadow_type(gtk.SHADOW_IN)
        frame_ds_deploy.set_shadow_type(gtk.SHADOW_IN)
        frame_vs_failure.set_shadow_type(gtk.SHADOW_IN)
        frame_ds_failure.set_shadow_type(gtk.SHADOW_IN)

        vbox_vs.add(frame_vs_deploy)
        vbox_ds.add(frame_ds_deploy)
        vbox_vs.add(frame_vs_failure)
        vbox_ds.add(frame_ds_failure)
        frame_vs_deploy.show()
        frame_ds_deploy.show()
        frame_vs_failure.show()
        frame_ds_failure.show()


        #canvas space
        frame_canvas = gtk.AspectFrame(None, 0.5, 0.5, 1.0, True)
        #frame_canvas.set_shadow_type(gtk.SHADOW_IN)

        self.canvas = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/goff_topology.png")
        scaled_buf = pixbuf.scale_simple(375, 350, gtk.gdk.INTERP_BILINEAR)
        self.canvas.set_from_pixbuf(scaled_buf)
        vbox_canvas.add(frame_canvas)
        frame_canvas.show()
        frame_canvas.add(self.canvas)
        self.canvas.show()


        #Button tables
        table_vs_deploy = gtk.Table(rows=1, columns=4, homogeneous=True)
        table_vs_deploy.show()
        frame_vs_deploy.add(table_vs_deploy)

        table_ds_deploy = gtk.Table(rows=1, columns=4, homogeneous=True)
        table_ds_deploy.show()
        frame_ds_deploy.add(table_ds_deploy)

        table_vs_failure = gtk.Table(rows=2, columns=6, homogeneous=True)
        table_vs_failure.show()
        frame_vs_failure.add(table_vs_failure)

        table_ds_failure = gtk.Table(rows=2, columns=6, homogeneous=True)
        table_ds_failure.show()
        frame_ds_failure.add(table_ds_failure)


        #Button attachments
        #Deploy buttons
        button_env_start_vs = gtk.Button("ENV START")
        button_env_start_vs.connect("button-press-event", lambda a, b: self.start_vs())
        button_env_stop_vs = gtk.Button("ENV STOP")
        button_env_stop_vs.connect("button-press-event", lambda a, b: self.stop_vs())
        button_play_vs = gtk.Button("PLAY")
        button_play_vs.connect("button-press-event", lambda w, e: self.start_video_vs(w, e))
        button_stop_vs = gtk.Button("STOP")
        button_stop_vs.connect("button-press-event", self.stop_video_vs)
        table_vs_deploy.attach(button_env_start_vs, 0, 1, 0, 1)
        button_env_start_vs.show()
        table_vs_deploy.attach(button_env_stop_vs, 1, 2, 0, 1)
        button_env_stop_vs.show()
        table_vs_deploy.attach(button_play_vs, 2, 3, 0, 1)
        button_play_vs.show()
        table_vs_deploy.attach(button_stop_vs, 3, 4, 0, 1)
        button_stop_vs.show()

        button_env_start_ds = gtk.Button("ENV START")
        button_env_start_ds.connect("button-press-event", lambda a, b: self.start_ds())
        button_env_stop_ds = gtk.Button("ENV STOP")
        button_env_stop_ds.connect("button-press-event", lambda a, b: self.stop_ds())
        button_upload_ds = gtk.Button("UPLOAD")
        button_upload_ds.connect("button-press-event", lambda w, e: self.upload_file_ds(w, e))
        button_download_ds = gtk.Button("DOWNLOAD")
        button_download_ds.connect("button-press-event", lambda a, b: self.download_file_ds(a, b))
        table_ds_deploy.attach(button_env_start_ds, 0, 1, 0, 1)
        button_env_start_ds.show()
        table_ds_deploy.attach(button_env_stop_ds, 1, 2, 0, 1)
        button_env_stop_ds.show()
        table_ds_deploy.attach(button_upload_ds, 2, 3, 0, 1)
        button_upload_ds.show()
        table_ds_deploy.attach(button_download_ds, 3, 4, 0, 1)
        button_download_ds.show()

        #Sim labels
        label_vs_en = gtk.Label()
        label_vs_en.set_use_markup(True)
        label_vs_en.set_markup('<span size="7000">ENABLE FLOW</span>')

        label_ds_en = gtk.Label()
        label_ds_en.set_use_markup(True)
        label_ds_en.set_markup('<span size="7000">ENABLE SERVER</span>')

        label_vs_dis = gtk.Label()
        label_vs_dis.set_use_markup(True)
        label_vs_dis.set_markup('<span size="7000">DISABLE FLOW</span>')

        label_ds_dis = gtk.Label()
        label_ds_dis.set_use_markup(True)
        label_ds_dis.set_markup('<span size="7000">DISABLE SERVER</span>')

        table_vs_failure.attach(label_vs_en, 0, 3, 0, 1, 0, 0, 0, 0)
        label_vs_en.show()
        table_ds_failure.attach(label_ds_en, 0, 3, 0, 1, 0, 0, 0, 0)
        label_ds_en.show()
        table_vs_failure.attach(label_vs_dis, 3, 6, 0, 1, 0, 0, 0, 0)
        label_vs_dis.show()
        table_ds_failure.attach(label_ds_dis, 3, 6, 0, 1, 0, 0, 0, 0)
        label_ds_dis.show()


        #Failure buttons
        button_sim_en_a_vs = gtk.Button("A")
        button_sim_en_a_vs.connect("button-press-event", lambda w, e: self.enable_flow_a_vs(w, e))
        button_sim_en_b_vs = gtk.Button("B")
        button_sim_en_b_vs.connect("button-press-event", lambda w, e: self.enable_flow_b_vs(w, e))
        button_sim_en_c_vs = gtk.Button("AxB")
        button_sim_en_c_vs.connect("button-press-event", lambda w, e: self.enable_flow_axb_vs(w, e))
        button_sim_dis_a_vs = gtk.Button("A")
        button_sim_dis_a_vs.connect("button-press-event", lambda w, e: self.disable_flow_a_vs(w, e))
        button_sim_dis_b_vs = gtk.Button("B")
        button_sim_dis_b_vs.connect("button-press-event", lambda w, e: self.disable_flow_b_vs(w, e))
        button_sim_dis_c_vs = gtk.Button("AxB")
        button_sim_dis_c_vs.connect("button-press-event", lambda w, e: self.disable_flow_axb_vs(w, e))
        table_vs_failure.attach(button_sim_en_a_vs, 0, 1, 1, 2)
        button_sim_en_a_vs.show()
        table_vs_failure.attach(button_sim_en_b_vs, 1, 2, 1, 2)
        button_sim_en_b_vs.show()
        table_vs_failure.attach(button_sim_en_c_vs, 2, 3, 1, 2)
        button_sim_en_c_vs.show()
        table_vs_failure.attach(button_sim_dis_a_vs, 3, 4, 1, 2)
        button_sim_dis_a_vs.show()
        table_vs_failure.attach(button_sim_dis_b_vs, 4, 5, 1, 2)
        button_sim_dis_b_vs.show()
        table_vs_failure.attach(button_sim_dis_c_vs, 5, 6, 1, 2)
        button_sim_dis_c_vs.show()

        button_sim_en_a_ds = gtk.Button("A")
        button_sim_en_a_ds.connect("button-press-event", lambda w, e: self.enable_flow_a_ds(w, e))
        button_sim_en_b_ds = gtk.Button("B")
        button_sim_en_b_ds.connect("button-press-event", lambda w, e: self.enable_flow_b_ds(w, e))
        button_sim_en_c_ds = gtk.Button("AxB")
        button_sim_en_c_ds.connect("button-press-event", lambda w, e: self.enable_flow_axb_ds(w, e))
        button_sim_dis_a_ds = gtk.Button("A")
        button_sim_dis_a_ds.connect("button-press-event", lambda w, e: self.disable_flow_a_ds(w, e))
        button_sim_dis_b_ds = gtk.Button("B")
        button_sim_dis_b_ds.connect("button-press-event", lambda w, e: self.disable_flow_b_ds(w, e))
        button_sim_dis_c_ds = gtk.Button("AxB")
        button_sim_dis_c_ds.connect("button-press-event", lambda w, e: self.disable_flow_axb_ds(w, e))
        table_ds_failure.attach(button_sim_en_a_ds, 0, 1, 1, 2)
        button_sim_en_a_ds.show()
        table_ds_failure.attach(button_sim_en_b_ds, 1, 2, 1, 2)
        button_sim_en_b_ds.show()
        table_ds_failure.attach(button_sim_en_c_ds, 2, 3, 1, 2)
        button_sim_en_c_ds.show()
        table_ds_failure.attach(button_sim_dis_a_ds, 3, 4, 1, 2)
        button_sim_dis_a_ds.show()
        table_ds_failure.attach(button_sim_dis_b_ds, 4, 5, 1, 2)
        button_sim_dis_b_ds.show()
        table_ds_failure.attach(button_sim_dis_c_ds, 5, 6, 1, 2)
        button_sim_dis_c_ds.show()


        #Widget extras (implementation)
        hbox_app = gtk.HBox(True, 0)
        """
        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", lambda w: gtk.main_quit())
        button_close.set_flags(gtk.CAN_DEFAULT)
        hbox_app.pack_end(button_close, False, False, 15)
        """
        label_ver = gtk.Label()
        label_ver.set_use_markup(True)
        label_ver.set_markup('<span size="7000">v. 0.1</span>')
        hbox_app.pack_end(label_ver, False, False, 15)
        label_ver.show()
        """
        extra_layout = gtk.Layout(None, None)
        extra_layout.set_size(800, 300)
        vbox_app.add(extra_layout)
        extra_layout.show()

        extra_layout.put(button_close, 100, 75)

        button_close.show()
        """
        hbox_app.show()
        vbox_app.add(hbox_app)


        #application programs...
        self.app_window.show()
        self.app_window.window.property_change("_NET_WM_STRUT", "CARDINAL", 32,
                                               gtk.gdk.PROP_MODE_REPLACE, [0, 0, 0, 0])
        return


    def bind_element_to_key_with_method(self, key, element, method):
        accelgroup = gtk.AccelGroup()
        key, modifier = gtk.accelerator_parse(key)
        accelgroup.connect_group(key, modifier, gtk.ACCEL_VISIBLE, method)
        getattr(element, "add_accel_group")(accelgroup)

    def run_deploy(self, location, command, arguments=None):
        #process = subprocess.Popen(["python", location, command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        command_list = ["python", location, command]
        if arguments:
            command_list.append(arguments)
        process = subprocess.Popen(command_list, shell=False)
        out, err = process.communicate()
        #print out
        #print err
        error_code = process.returncode
        return error_code

    def run_deploy_ds(self, command, arguments=None):
        location = "/home/MinervaDS/tools/deploy.py"
        return self.run_deploy(location, command, arguments)

    def run_deploy_vs(self, command, arguments=None):
        location = "/home/carolina/minerva/src/deploy/use_cases/1_video_streaming/deploy.py"
        return self.run_deploy(location, command, arguments)

    def run_deploy_ds_upload(self, file_path=None):
        return self.run_deploy_ds("upload", file_path)

    def run_deploy_ds_download(self, file_id):
        return self.run_deploy_ds("download", file_id)

    def run_deploy_vs_startx(self, video_path=None):
        return self.run_deploy_vs("startx", video_path)

    def run_deploy_vs_stopx(self):
        return self.run_deploy_vs("stopx")

    def run_deploy_vs_disable(self, flow="A"):
        return self.run_deploy_vs("disable", flow)

    def run_deploy_vs_enable(self, flow="A"):
        return self.run_deploy_vs("enable", flow)

    def run_deploy_ds_disable(self, flow="A"):
        return self.run_deploy_ds("disable", flow)

    def run_deploy_ds_enable(self, flow="A"):
        return self.run_deploy_ds("enable", flow)

    def start_ds(self):
        location = "/home/MinervaDS/tools/deploy.py"
        return self.run_deploy(location, "start")

    def stop_ds(self):
        location = "/home/MinervaDS/tools/deploy.py"
        return self.run_deploy(location, "shutdown")

    def start_vs(self):
        location = "/home/carolina/minerva/src/deploy/use_cases/1_video_streaming/deploy.py"
        return self.run_deploy(location, "start")

    def stop_vs(self):
        location = "/home/carolina/minerva/src/deploy/use_cases/1_video_streaming/deploy.py"
        return self.run_deploy(location, "stop")

    def upload_file(self, window, event, case_type):
        chooser = gtk.FileChooserDialog(title = "Upload a file",
                                        parent = self.app_window,
                                        action = gtk.FILE_CHOOSER_ACTION_OPEN,
                                        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                   gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        current_dir = os.path.dirname(os.path.realpath(__file__))
        initial_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        chooser.set_current_folder(initial_path)

        if case_type == "vs":
            chooser_filter = gtk.FileFilter()
            chooser_filter.set_name("Videos")
            patterns = ["*", "*.avi", "*.mpeg", "*.mp4", "*.flv", "*.mov", ".3gp", "*.m3u*"]
            for pattern in patterns:
                chooser_filter.add_pattern(pattern)
            chooser.add_filter(chooser_filter)

        result = chooser.run()
        
        filename = None

        if result in [gtk.RESPONSE_ACCEPT, gtk.RESPONSE_OK]:
            filename = chooser.get_filename()
            chooser.destroy()
            return filename

        elif result in [gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL]:
            chooser.destroy()

    def upload_file_ds(self, window, event):
        file_path = self.upload_file(window, event, "ds")
        if file_path:
            print_info("Uploading file...")
            return self.run_deploy_ds_upload(file_path)
        else:
            return

    def download_file_ds(self, window, event):
        file_id = self.set_file_id_ds(window, event)
        if file_id:
            print_info("Downloading file...")
            return self.run_deploy_ds_download(file_id)
        else:
            return

    def start_video_vs(self, window, event):
        file_path = self.upload_file(window, event, "vs")
        if file_path:
            return self.run_deploy_vs_startx(file_path)
        else:
            return

    def stop_video_vs(self, window, event):
        return self.run_deploy_vs_stopx()

    def enable_flow_a_vs(self, window, event):
        print_info("Flow A enabled")
        return self.run_deploy_vs_enable("A")

    def enable_flow_b_vs(self, window, event):
        print_info("Flow B enabled")
        return self.run_deploy_vs_enable("B")

    def enable_flow_axb_vs(self, window, event):
        print_info("Flow AxB enabled")
        return self.run_deploy_vs_enable("AxB")

    def disable_flow_a_vs(self, window, event):
        print_info("Flow A disabled")
        return self.run_deploy_vs_disable("A")

    def disable_flow_b_vs(self, window, event):
        print_info("Flow B disabled")
        return self.run_deploy_vs_disable("B")

    def disable_flow_axb_vs(self, window, event):
        print_info("Flow AxB disabled")
        return self.run_deploy_vs_disable("AxB")

    def enable_flow_a_ds(self, window, event):
        print_info("Flow A enabled")
        return self.run_deploy_ds_enable("A")

    def enable_flow_b_ds(self, window, event):
        print_info("Flow B enabled") 
        return self.run_deploy_ds_enable("B")

    def enable_flow_axb_ds(self, window, event):
        print_info("Flow AxB enabled") 
        return self.run_deploy_ds_enable("AxB")

    def disable_flow_a_ds(self, window, event):
        print_info("Flow A disabled") 
        return self.run_deploy_ds_disable("A")

    def disable_flow_b_ds(self, window, event):
        print_info("Flow B disabled") 
        return self.run_deploy_ds_disable("B")

    def disable_flow_axb_ds(self, window, event):
        print_info("Flow AxB disabled") 
        return self.run_deploy_ds_disable("AxB")

    def set_file_id_ds(self, window, event):
        entry = EntryDialog()
        result = entry.run()
        if result:
            return result
        else:
            return

    def callback_vs(self, widget, event, data):
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/goff_topology_vs.png")
        scaled_buf = pixbuf.scale_simple(375, 350, gtk.gdk.INTERP_BILINEAR)
        self.canvas.set_from_pixbuf(scaled_buf)
        self.canvas.show()

    def callback_ds(self, widget, event, data):
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/goff_topology_ds.png")
        scaled_buf = pixbuf.scale_simple(375, 350, gtk.gdk.INTERP_BILINEAR)
        self.canvas.set_from_pixbuf(scaled_buf)
        self.canvas.show()

    def callback(self, widget, event, data):
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/goff_topology.png")
        scaled_buf = pixbuf.scale_simple(375, 350, gtk.gdk.INTERP_BILINEAR)
        self.canvas.set_from_pixbuf(scaled_buf)
        self.canvas.show()


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
   
    # Cleaning temps
    command = "rm -rf /home/MinervaDS/a_flow_file /home/MinervaDS/b_flow_file /home/MinervaDS/c_flow_file"
    try:
        subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    except:
        subprocess.call(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    MinervaGUI()
    main()
