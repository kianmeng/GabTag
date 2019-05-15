from gi import require_version
require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, GLib
from PIL import Image
import io
import math

class View:


    class __View:

        def __init__(self, tree_view, title, album, artist, genre, cover, track, year, length, size):

            self.tree_view = tree_view
            self.title = title
            self.album = album
            self.artist = artist
            self.genre = genre
            self.cover = cover
            self.track = track
            self.year = year
            self.length = length
            self.size = size
            self.cover_width = 300
            self.cover_height = 300

        def erase(self):
            self.genre.set_text("")
            self.album.set_text("")
            self.title.set_text("")
            self.artist.set_text("")
            self.year.set_text("")
            self.track.set_text("")


        def set_editibility_title(self, multiline, title):
            if multiline == 1 :
                self.title.set_text("")
                self.title.set_editable(0)
            else :
                self.title.set_editable(1)
                self.title.set_text(title)

        def set_editability_size(self, multiline, size):
            if multiline == 1 :
                self.size.set_text("")
            else :
                self.size.set_text(size)

        def set_editability_length(self, multiline, length):
            if multiline == 1 :
                self.length.set_text("")
            else :
                self.length.set_text(length)

        def show(self,tagdico, multiline):
            self.set_editibility_title(multiline,tagdico["title"]["value"])
            self.set_editability_size(multiline,tagdico["size"]["value"])
            self.set_editability_length(multiline,tagdico["length"]["value"])
            self.genre.set_text(tagdico["genre"]["value"])
            self.album.set_text(tagdico["album"]["value"])
            self.artist.set_text(tagdico["artist"]["value"])
            self.year.set_text(tagdico["year"]["value"])
            self.track.set_text(tagdico["track"]["value"])


            if tagdico["cover"]["value"] != None and tagdico["cover"]["value"] != "":
                if len(tagdico["cover"]["value"])>100 :
                     with  Image.open(io.BytesIO(tagdico["cover"]["value"])) as img :
                        glibbytes = GLib.Bytes.new(img.tobytes())

                        print("A :",glibbytes.get_size())

                        #print("B :",img.width/math.sqrt(3)," ", img.height/math.sqrt(3))

                        width = img.width  ##The best fix i could find for the moment
                        height = img.height
                        if glibbytes.get_size() < width * height * 3 :
                             width = math.sqrt(glibbytes.get_size()/3)
                             height = math.sqrt(glibbytes.get_size()/3)

                        pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(glibbytes, #ERROR HAPPENS WITH SOME COVER
                                                                GdkPixbuf.Colorspace.RGB,
                                                                False,
                                                                8,
                                                                width,
                                                                height,
                                                                len(img.getbands())*img.width)

                        pixbuf = pixbuf.scale_simple(self.cover_width, self.cover_height, GdkPixbuf.InterpType.BILINEAR)

                        self.cover.set_from_pixbuf(pixbuf)
                else:
                    with  Image.open(tagdico["cover"]["value"]) as img :
                        glibbytes = GLib.Bytes.new(img.tobytes())

                        pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(glibbytes,
                                                                GdkPixbuf.Colorspace.RGB,
                                                                False,
                                                                8,
                                                                img.width,
                                                                img.height,
                                                                len(img.getbands())*img.width)

                        pixbuf = pixbuf.scale_simple(self.cover_width, self.cover_height, GdkPixbuf.InterpType.BILINEAR)

                        self.cover.set_from_pixbuf(pixbuf)
            else :

                self.cover.set_from_icon_name(None,32)


        def update_cover(self,cover_value):
            with  Image.open(cover_value) as img :
                glibbytes = GLib.Bytes.new(img.tobytes())

                pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(glibbytes,
                                                        GdkPixbuf.Colorspace.RGB,
                                                        False,
                                                        8,
                                                        img.width,
                                                        img.height,
                                                        len(img.getbands())*img.width)


                pixbuf = pixbuf.scale_simple(self.cover_width, self.cover_height, GdkPixbuf.InterpType.BILINEAR)

                self.cover.set_from_pixbuf(pixbuf)




        def add_column(self, name):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(name, renderer, text=0)
            self.tree_view.append_column(column)



    __instance = None

    def __init__(self, tree_view, title, album, artist, genre, cover, track, year, length, size):
        """ Virtually private constructor. """
        if View.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            View.__instance = View.__View(tree_view, title, album, artist, genre, cover, track, year, length, size)


    @staticmethod
    def getInstance():
        """ Static access method. """
        if View.__instance == None:
            View(None,None,None,None,None, None, None, None, None, None)
        return View.__instance

