# Imports
"""
MODULES USED:
1. tkinter
2. customtkinter
3. requests
4. piloow
5. os
"""

from tkinter import *
import customtkinter as ctk
from tkinter import messagebox
import requests as req
from PIL import Image, ImageTk
import os


# Innitialisation of class AppWindow (Init. the main screen...)

class AppWindow:
    def __init__(self, window):
        # Super class init.
        super(AppWindow, self).__init__()
        # --------------------------------------------------------------------------------------------------------------
        # Settings

        self.root = window # Init. window as main screen
        self.bg = "#141526" # Background colour (Shade of black and blue)
        self.font = "Leelawadee UI Semilight" # Font

        # --------------------------------------------------------------------------------------------------------------
        # Configurations

        self.root.config(bg=self.bg)

        # --------------------------------------------------------------------------------------------------------------
        # Functions

        def get_movie():
            """
            Exceptions: 
                        1. HTTPSError
                        2. RequestsError
                        (1 & 2 occur if you are not connected any network)
                        3. tkinter._tckError (has been completely resolved)
            """
            
            try:
                # Clearing mechanism
                self.status_label.place(x=5000, y=50)
                self.name_label.place(x=6000, y=50)
                
                self.show_user_label.place(x=6000, y=180)
                
                self.enter_choice_label.place(x=6000, y=200+70)
                self.choice_entry.place(x=6800, y=207+70)
                
                self.download_button.place(x=9000, y=202+70)
                
                # Getting User enterd Search data
                search = self.text_box.get()
                y = search.split(" ") # :type <list>
                p = "+".join(y)  # :type <str>

                # Requesting API for data
                
                link = f"https://yts.mx/api/v2/list_movies.json?query_term={p}"
                response = req.get(link).json()  # :type <json file>

                # checking for null-search
                
                if response['data']['movie_count'] != 0: # If movies found in search name
                    
                    # Placing the menu for movie results
                    
                    self.movie_menu.place(x=50, y=200)
                    self.movie_menu.delete(0, END)

                    datas = response['data']['movies'] # Extracting only required data

                    # Extracting data from response file
                    """
                    1. movie_titles: List of movie titles based on search
                    2. movie_runtime: List of movie runtimes
                    3. movie year: Year of Release
                    4. movie_torrent: Torrent info for movies
                    """
                    
                    movie_title = [datas[_]['title_long'] for _ in range(len(datas))]  # <List comprehension>
                    movie_runtime = [datas[_]['runtime'] for _ in range(len(datas))]  # <List comprehension>
                    movie_year = [datas[_]['year'] for _ in range(len(datas))]  # <List comprehension>
                    movie_torrent = [datas[_]['torrents'] for _ in range(len(datas))]  # <List comprehension>
                   
                    # displaying movies in self.moviemenu
                    for title in movie_title:
                        # Displays --> <Movie title>--<Movie year>--<Movie runtime>
                        self.movie_menu.insert(END, f"{movie_title.index(title)+1}--{title[:-7:]}--{movie_year[movie_title.index(title)]}--({movie_runtime[movie_title.index(title)]} minutes)")
                    # -------------------------------------------------------------------------------------------------
                    """
                    Function: get_choice: To download movie based on user choice
                    :returns download status & adds link to qbittorrent for download
                    """
                    
                    def get_choice():    
                        """
                        Exceptions: 
                        1. HTTPSError
                        2. RequestsError
                        (1 & 2 occur if you are not connected any network)
                        3. tkinter._tckError (has been completely resolved)
                        4. ListIndexError (Has been completely resolved)
                        5. SearchOutOfListIndexError
                        """
                        try:
                            choose_movie = int(self.choice_entry.get()) # Getting user input choice :type <int>
                            for dll in movie_torrent[choose_movie-1]:
                                
                                # Checking for 1080p quality
                                if dll['quality'] == '1080p':
                                    view = dll
                                    break
                                else:
                                    view = dll
                            
                            # Configuration and placing of Movie name that is being downloaded
                            self.name_label.place(x=600, y=400)
                            self.name_label.config(text=f"Downloading: {movie_title[choose_movie - 1]}")

                            torrent_hash = view['hash'] # Torrent hashcode 

                            # Magnetin link generation
                            """
                            Trackers Used:
                            1. - udp://glotorrents.pw:6969/announce
                            2. - udp://tracker.opentrackr.org:1337/announce
                            3. - udp://torrent.gresille.org:80/announce
                            4. - udp://tracker.openbittorrent.com:80
                            5. - udp://tracker.coppersurfer.tk:6969
                            6. - udp://tracker.leechers-paradise.org:6969
                            7. - udp://p4p.arenabg.ch:1337
                            8. - udp://tracker.internetwarriors.net:1337
                            """
                            magnet_link = f"magnet:?xt=urn:btih:{torrent_hash}&dn={movie_title[choose_movie - 1]}+{view['quality']}+{view['type']}+YTS.MX&tr=udp://track.two:80&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://glotorrents.pw:6969/announce&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://torrent.gresille.org:80/announce&tr=udp://p4p.arenabg.com:1337&tr=udp://tracker.leechers-paradise.org:6969"

                            # Status Label init. and configuration
                            self.status_label.place(x=600, y=600)
                            self.status_label.config(text="STATUS: Magnetic link generated")

                            # Sending query to QbitTorrent via command prompt
                            command = f'qbt torrent add url "{magnet_link}" --username admin --password adminadmin --url http://localhost:8080'
                            os.system(command)

                            self.status_label.config(text=f"STATUS: Download Started") # To show when downloas has started...
                            
                        except Exception:
                            messagebox.showerror("MoviTorrnt", "STATUS: ERROR 6969")  # Error message

                    # Label configurations and placing...
                    self.show_user_label.place(x=600, y=180) # Instruciton Label
                    
                    self.enter_choice_label.place(x=600, y=200+70) # For choice entry
                    self.choice_entry.place(x=680, y=207+70)
                    
                    self.download_button.place(x=900, y=202+70) # For Downloading
                    self.download_button.configure(command=get_choice)
                    

                else:
                    messagebox.showwarning("MOVI", f"Movie Search '{search.capitalize()}' not found...")
            except Exception as e:
                messagebox.showerror("MoviTorrnt", f"STATUS ERROR: [{e}]")
            

        # --------------------------------------------------------------------------------------------------------------
        # Images
        
        """
        Images Used:
        1. logo_img --> Logo image
        2. search_bar_img --> Search Bar
        3. search_button_img --> Search Button
        4. enter_choice_img --> Enter choice bar image
        
        **NOTE**
        Image.Resampling.LANCZOS used instead of Image.ANTIALIAS
        
        Reason: Image.ANTIALIAS is not going to be supported in the newer python versions
                
        Error Message: (DeprecationWarning: ANTIALIAS is deprecated and will be removed in Pillow 10 (2023-07-01). Use LANCZOS or Resampling.LANCZOS instead.)
        """

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
        """
        Labels Used:
        1. Logo Label
        2. Logo Text Label
        (No identifiers assigned to 1 & 2)
        3. search_bar_label --> Search Bar
        4. enter_choice_label --> Download choice number bar
        5. show_user_label --> Just an indication label
        6. status_label --> Shows status of download 
        """

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

        """
        1. search_button --> Button init. for search
        2. download_button --> Download button
        """
        
        self.search_button = Button(self.root, image=self.search_button_img, command=get_movie, bg="white", bd=0).place(x=966, y=23) # Search Button init

        self.download_button = ctk.CTkButton(self.root, text="Download", bg_color="white", height=38) # Download Button init.

        # --------------------------------------------------------------------------------------------------------------
        # Text Entry

        """
        1. text_box --> To Enter your movie search
        2. choice_entry --> To Enter your choice
        """
        
        self.text_box = Entry(self.root, bg="white", bd=0, fg=self.bg, font=(self.font, 15))
        self.text_box.place(x=738, y=27)

        self.choice_entry = Entry(self.root, bg="white", fg="black", bd=0, font=(self.font, 12))

        # ---------------------------------------------------------------------------------------------------------------
        # Text Box
        self.movie_menu = Listbox(self.root, width=75, height=30, bg=self.bg, fg="white", bd=0, borderwidth=0) # To List generated search based on user request.


# Driver/Run Code
if __name__ == '__main__':
    window = Tk()  # Initialising tkinter Window
    window.geometry("1080x720+100+100")  # Setting Geometry
    window.title("Movie-Downloader.io")  # Setting main window title
    window.resizable(False, False)  # Setting rigid size settings (Full Screen Disabled...)
    window.iconbitmap('Images/messageboxlogo.ico')  # Seeting mainwindow icon Bitmap :type <ico file>
    x = AppWindow(window)
    window.mainloop()
