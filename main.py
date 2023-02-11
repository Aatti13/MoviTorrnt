# Imports

from tkinter import *
import customtkinter as ctk
from tkinter import messagebox
import requests as req
from PIL import Image, ImageTk
import os


class AppWindow:
    def __init__(self, window):
        super(AppWindow, self).__init__()

        self.root = window
        self.bg = "#141526"
        self.font = "Leelawadee UI Semilight"

        # --------------------------------------------------------------------------------------------------------------
        # Configurations

        self.root.config(bg=self.bg)

        # --------------------------------------------------------------------------------------------------------------
        # Functions

        def get_movie():

            try:
                self.status_label.place(x=5000, y=50)
                self.name_label.place(x=6000, y=50)
                self.show_user_label.place(x=6000, y=180)
                self.enter_choice_label.place(x=6000, y=200+70)
                self.choice_entry.place(x=6800, y=207+70)
                self.download_button.place(x=9000, y=202+70)
                
                search = self.text_box.get()
                y = search.split(" ")
                p = "+".join(y)

                link = f"https://yts.mx/api/v2/list_movies.json?query_term={p}"
                response = req.get(link).json()

                if response['data']['movie_count'] != 0:

                    self.movie_menu.place(x=50, y=200)
                    self.movie_menu.delete(0, END)

                    datas = response['data']['movies']

                    movie_title = [datas[_]['title_long'] for _ in range(len(datas))]
                    movie_runtime = [datas[_]['runtime'] for _ in range(len(datas))]
                    movie_year = [datas[_]['year'] for _ in range(len(datas))]
                    movie_torrent = [datas[_]['torrents'] for _ in range(len(datas))]
                    # file_size = [datas[_]['torrents'][_]['size']]

                    for title in movie_title:
                        self.movie_menu.insert(END, f"{movie_title.index(title)+1}--{title[:-7:]}--{movie_year[movie_title.index(title)]}--({movie_runtime[movie_title.index(title)]} minutes)")

                    def get_choice():    
                        try:
                            choose_movie = int(self.choice_entry.get())
                            for dll in movie_torrent[choose_movie-1]:
                                if dll['quality'] == '1080p':
                                    view = dll
                                    break
                                else:
                                    view = dll
                            self.name_label.place(x=600, y=400)
                            self.name_label.config(text=f"Downloading: {movie_title[choose_movie - 1]}")

                            torrent_hash = view['hash']

                            magnet_link = f"magnet:?xt=urn:btih:{torrent_hash}&dn={movie_title[choose_movie - 1]}+{view['quality']}+{view['type']}+YTS.MX&tr=udp://track.two:80&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://glotorrents.pw:6969/announce&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://torrent.gresille.org:80/announce&tr=udp://p4p.arenabg.com:1337&tr=udp://tracker.leechers-paradise.org:6969"

                            self.status_label.place(x=600, y=600)
                            self.status_label.config(text="STATUS: Magnetic link generated")

                            command = f'qbt torrent add url "{magnet_link}" --username admin --password adminadmin --url http://localhost:8080'
                            os.system(command)

                            self.status_label.config(text=f"STATUS: Download Started:")
                            
                        except Exception:
                            messagebox.showerror("MoviTorrnt", "STATUS: ERROR 6969")

                    self.show_user_label.place(x=600, y=180)
                    self.enter_choice_label.place(x=600, y=200+70)
                    self.choice_entry.place(x=680, y=207+70)
                    self.download_button.place(x=900, y=202+70)
                    self.download_button.configure(command=get_choice)
                    

                else:
                    messagebox.showwarning("MOVI", f"Movie Search '{search.capitalize()}' not found...")
            except Exception as e:
                messagebox.showerror("MoviTorrnt", f"STATUS ERROR: [{e}]")
            

        # --------------------------------------------------------------------------------------------------------------
        # Images

        self.logo_img = Image.open("Images/image.jpg")
        self.logo_img = self.logo_img.resize((60, 60), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)

        self.search_bar_img = Image.open("Images/search bar.png")
        self.search_bar_img = self.search_bar_img.resize((369, 55), Image.Resampling.LANCZOS)
        self.search_bar_img = ImageTk.PhotoImage(self.search_bar_img)

        self.search_button_img = Image.open("Images/searchbutton.png")
        self.search_button_img = self.search_button_img.resize((35, 35), Image.Resampling.LANCZOS)
        self.search_button_img = ImageTk.PhotoImage(self.search_button_img)

        self.enter_choice_img = Image.open("Images/search bar light.png")
        self.enter_choice_img = ImageTk.PhotoImage(self.enter_choice_img)

        # --------------------------------------------------------------------------------------------------------------
        # Labels

        Label(self.root, image=self.logo_img, bd=0, bg=self.bg).place(x=10, y=10)
        Label(self.root, text="MoviTorrnt", font=(self.font, 35), bd=0, bg=self.bg, fg="white").place(x=90, y=10)

        self.search_bar_label = Label(self.root, image=self.search_bar_img, bd=0, bg=self.bg).place(relx=0.6, rely=0.02)

        self.enter_choice_label = Label(self.root, image=self.enter_choice_img, bd=0, bg=self.bg)

        self.show_user_label = Label(self.root, text="Enter Choice number: ",
        font=(self.font, 18), bg=self.bg, fg="white")

        self.name_label = Label(self.root, bg=self.bg, fg="white", bd=0, font=(self.font, 12))

        self.status_label = Label(self.root, bg=self.bg, fg="white", bd=0, font=(self.font, 16))


        # --------------------------------------------------------------------------------------------------------------
        # Buttons

        self.search_button = Button(self.root, image=self.search_button_img, command=get_movie, bg="white", bd=0).place(x=966, y=23)

        self.download_button = ctk.CTkButton(self.root, text="Download", bg_color="white", height=38)

        # --------------------------------------------------------------------------------------------------------------
        # Text Entry

        self.text_box = Entry(self.root, bg="white", bd=0, fg=self.bg, font=(self.font, 15))
        self.text_box.place(x=738, y=27)

        self.choice_entry = Entry(self.root, bg="white", fg="black", bd=0, font=(self.font, 12))

        # ---------------------------------------------------------------------------------------------------------------
        # Text Box
        self.movie_menu = Listbox(self.root, width=75, height=30, bg=self.bg, fg="white", bd=0, borderwidth=0)


if __name__ == '__main__':
    window = Tk()
    window.geometry("1080x720+100+100")
    window.title("Movie-Downloader.io")
    window.resizable(False, False)
    window.iconbitmap('Images/messageboxlogo.ico')
    x = AppWindow(window)
    window.mainloop()
