#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk

class MinervaGUI:

    def __init__(self):

        #main window
        app_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        app_window.set_size_request(800, 600)
        app_window.set_border_width(10)
        app_window.set_title("Minerva Demo GUI")
        app_window.connect("delete_event", lambda w, e: gtk.main_quit())


        #window layouts
        vbox_app = gtk.VBox(False, 10)
        app_window.add(vbox_app)
        vbox_app.show()


        #layouts Table()
        table_layout = gtk.Table(rows=3, columns=10, homogeneous=False)
        table_layout.show()
        vbox_app.add(table_layout)

        table_body = gtk.Table(rows=5, columns=3, homogeneous=True)
        table_body.show()
        vbox_app.add(table_body)

        vbox_frames = gtk.VBox(False, 5)
        vbox_frames.show()
        table_body.attach(vbox_frames, 0, 1, 0, 4, 0, 0, 0, 0)

        vbox_canvas = gtk.VBox(False, 5)
        valign = gtk.Alignment(0, 1, 0, 0)
        vbox_canvas.pack_start(valign)
        vbox_canvas.show()
        table_body.attach(vbox_canvas, 1, 2, 0, 4, 0, 0, 0, 0)


        #logos
        logo1 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/logo1.png")
        scaled_buf = pixbuf.scale_simple(150, 50, gtk.gdk.INTERP_BILINEAR)
        logo1.set_from_pixbuf(scaled_buf)

        logo2 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/logo2.png")
        scaled_buf = pixbuf.scale_simple(60, 60, gtk.gdk.INTERP_BILINEAR)
        logo2.set_from_pixbuf(scaled_buf)

        logo3 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/logo3.png")
        scaled_buf = pixbuf.scale_simple(110, 50, gtk.gdk.INTERP_BILINEAR)
        logo3.set_from_pixbuf(scaled_buf)

        logo4 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/logo4.png")
        scaled_buf = pixbuf.scale_simple(90, 60, gtk.gdk.INTERP_BILINEAR)
        logo4.set_from_pixbuf(scaled_buf)

        logo5 = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/geant.jpg")
        scaled_buf = pixbuf.scale_simple(100, 50, gtk.gdk.INTERP_BILINEAR)
        logo5.set_from_pixbuf(scaled_buf)

        table_layout.attach(logo1, 0, 1, 0, 1, 0, 0, 0, 0)
        logo1.show()

        table_layout.attach(logo2, 2, 3, 0, 1, 0, 0, 0, 0)
        logo2.show()

        table_layout.set_col_spacing(1, 10)
        table_layout.set_col_spacing(2, 30)

        table_layout.attach(logo3, 3, 4, 0, 1, 0, 0, 0, 0)
        logo3.show()

        table_layout.attach(logo4, 4, 5, 0, 1, 0, 0, 1, 0)
        logo4.show()

        table_layout.set_col_spacing(3, 10)
        table_layout.set_col_spacing(4, 210)

        table_layout.attach(logo5, 6, 7, 0, 1, 0, 0, 0, 0)
        logo5.show()

        table_layout.set_row_spacing(0, 20)

        label_app = gtk.Label()
        label_app.set_use_markup(gtk.TRUE)
        label_app.set_markup('<span size="16000"><b>MINERVA: Demonstrating resilience over non-secure channels</b></span>')
        table_layout.attach(label_app, 0, 10, 1, 2, 0, 0, 0, 0)
        label_app.show()


        separator = gtk.HSeparator()
        separator.set_size_request(750, 5)
        table_layout.attach(separator, 0, 10, 2, 3, 0, 0, 0, 0)
        separator.show()


        #main frames
        frame_vs = gtk.Frame("Video Streaming")
        frame_ds = gtk.Frame("Distributed Storage")
        frame_vs.set_shadow_type(gtk.SHADOW_IN)
        frame_ds.set_shadow_type(gtk.SHADOW_IN)

        vbox_frames.add(frame_vs)
        frame_vs.show()

        vbox_frames.add(frame_ds)
        frame_ds.show()

        vbox_vs = gtk.VBox(False, 5)
        vbox_ds = gtk.VBox(False, 5)

        frame_vs.add(vbox_vs)
        vbox_vs.show()
        frame_ds.add(vbox_ds)
        vbox_ds.show()


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

        canvas = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("images/backup.png")
        scaled_buf = pixbuf.scale_simple(375, 350, gtk.gdk.INTERP_BILINEAR)
        canvas.set_from_pixbuf(scaled_buf)
        vbox_canvas.add(frame_canvas)
        frame_canvas.show()
        frame_canvas.add(canvas)
        canvas.show()


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
        button_env_stop_vs = gtk.Button("ENV STOP")
        button_play_vs = gtk.Button("PLAY")
        button_stop_vs = gtk.Button("STOP")
        table_vs_deploy.attach(button_env_start_vs, 0, 1, 0, 1)
        button_env_start_vs.show()
        table_vs_deploy.attach(button_env_stop_vs, 1, 2, 0, 1)
        button_env_stop_vs.show()
        table_vs_deploy.attach(button_play_vs, 2, 3, 0, 1)
        button_play_vs.show()
        table_vs_deploy.attach(button_stop_vs, 3, 4, 0, 1)
        button_stop_vs.show()

        button_env_start_ds = gtk.Button("ENV START")
        button_env_stop_ds = gtk.Button("ENV STOP")
        button_upload_ds = gtk.Button("UPLOAD")
        button_download_ds = gtk.Button("DOWNLOAD")
        table_ds_deploy.attach(button_env_start_ds, 0, 1, 0, 1)
        button_env_start_ds.show()
        table_ds_deploy.attach(button_env_stop_ds, 1, 2, 0, 1)
        button_env_stop_ds.show()
        table_ds_deploy.attach(button_upload_ds, 2, 3, 0, 1)
        button_upload_ds.show()
        table_ds_deploy.attach(button_download_ds, 3, 4, 0, 1)
        button_download_ds.show()

        #Sim labels
        label_vs_en = gtk.Label("ENABLE SERVER")
        label_ds_en = gtk.Label("ENABLE SERVER")
        label_vs_dis = gtk.Label("DISABLE SERVER")
        label_ds_dis = gtk.Label("DISABLE SERVER")

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
        button_sim_en_b_vs = gtk.Button("B")
        button_sim_en_c_vs = gtk.Button("AxB")
        button_sim_dis_a_vs = gtk.Button("A")
        button_sim_dis_b_vs = gtk.Button("B")
        button_sim_dis_c_vs = gtk.Button("AxB")
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
        button_sim_en_b_ds = gtk.Button("B")
        button_sim_en_c_ds = gtk.Button("AxB")
        button_sim_dis_a_ds = gtk.Button("A")
        button_sim_dis_b_ds = gtk.Button("B")
        button_sim_dis_c_ds = gtk.Button("AxB")
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



        """
        #hbox_app.add(table_layout)
        hbox_app = gtk.HBox(True, 0)
        vbox_app.add(hbox_app)

        button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_close.connect("clicked", lambda w: gtk.main_quit())
        button_close.set_flags(gtk.CAN_DEFAULT)
        #hbox_app.pack_end(button_close, False, False, 0)

        extra_layout = gtk.Layout(None, None)
        extra_layout.set_size(800, 300)
        app_window.add(extra_layout)
        extra_layout.show()

        extra_layout.put(button_close, 700, 75)
        button_close.show()

        hbox_app.show()
        vbox_app.add(hbox_app)
        """

        #application programs...
        """
        button_close.grab_default()
        """
        app_window.show()

        return


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    MinervaGUI()
    main()

