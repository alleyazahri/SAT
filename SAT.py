import sys
import tkinter
from tkinter import *
import glob
import os
import random
import pygame
from tkinter.filedialog import askopenfilename, askdirectory
from shutil import copyfile

# Initialize the music program
pygame.mixer.init()

# Stylizing Variables:
HEADER_FONT = ("Verdana", 14)
SUB_HEADER_FONT = ("Verdana",12)
STANDARD_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
BG_BUTTON = "black"
HOVER_BUTTON = "yellow"
DP_TEXT_BUTTON = "white"

# Default Music Directory
DEFAULT_MUSIC_DIRECTORY = '/home/pi/Music/*'

# Variables the main code needs access to
global about
global app
global swindow

about = None
swindow = None


def aboutMessage():
    """
    This method displays a Tkinter window with information
    about this application and it's creator.
    """
    global about

    # Have only one about window open at a time
    try:
        about.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass

    about = tkinter.Tk()

    about.wm_title("About")
    # Header Labels
    label = tkinter.Label(about, text="About S.A.T.", font=HEADER_FONT)
    label.pack(side="top", padx=5, pady=(10, 0))
    label4=tkinter.Label(about,text="(Simple Audio Thing)", font = HEADER_FONT)
    label4.pack(side="top", padx=5, pady=(0, 10))

    # Informational Labels
    label2 = tkinter.Label(about, text="Author: Megan Francis")
    label2.pack(side="top")
    label3 = tkinter.Label(about, text="Created in Spring 2016")
    label3.pack(side="top")

    # Exit Button
    B1 = tkinter.Button(about,text="Close", command=about.destroy)
    B1.pack(pady=(12,10))

    # Main loop for about window
    about.mainloop()

def exitSAT():
    """
    This method contains all the code to close all windows in the
    application, as well as close and exit the music player
    """
    # Close Search Window
    global swindow
    try:
        swindow.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass
    
    # Close About Window
    global about
    try:
        about.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass
    
    # Close Import Window
    global importS
    try:
        importS.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass

    # Close Overview Window
    global qoWindow
    try:
        qoWindow.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass

    # Close Play A Song Window
    global pasWindow
    try:
        pasWindow.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass

    # Close Loop & Shuffle Button Window
    global lasbWindow
    try:
        lasbWindow.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass

    # Close Search Button Window
    global sbWindow
    try:
        sbWindow.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass

    # Close Import Songs Window
    global isWindow
    try:
        isWindow.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass

    # Close Music Directory Window
    global tmdWindow
    try:
        tmdWindow.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass

    # Close Unanswered Questions Window
    global uqWindow
    try:
        uqWindow.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass
    
    # Close Main Application Window
    global app
    try:
        app.destroy()
    except NameError:
        pass
    except AttributeError:
        pass
    except tkinter.TclError:
        pass

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    
    pygame.mixer.quit()
    sys.exit()

def importMusic():
    """
    This method calls the ImportMusic class which imports a song or
    a directory of songs based on user input.
    """
    ImportMusic()


class ImportMusic():
    def __init__(self):
        """
        Sets up the Import window for importing music into the music
        directory. From the import file window a single .mp3 file
        can be imported. From the import directory window, a directory
        of files canbe imported, it will only import .mp3 files.
        """
        # Tkinter Window
        global importS
        # SongSearch Object
        global ss

        # Have only one import window open at a time
        try:
            importS.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Tkinter Label Variables
        self.songPath = None
        self.compLab = None
        self.artLab = None
        self.songLab = None
        self.countLab = None

        # Tkinter Button Variables
        self.B3 = None
        self.B4 = None

        # Tkinter Entry Variables
        self.songTitle = None
        self.artistName = None

        # Song Display and Calculation Variables
        self.songToImport = ''
        self.songArray = []
        self.count = 0
        self.total = 0

        # Initialize Tkinter Window
        importS = tkinter.Tk()
        importS.wm_title("Import")

        # Import Buttons in Window
        B1 = tkinter.Button(importS,text="Import File", command=self.openFile)
        B1.grid(column=0, row=0, pady=(10,2), padx=10, columnspan=2)
        B2 = tkinter.Button(importS,text="Import Directory", command=self.openDir)
        B2.grid(column=0, row=1, pady=(2,10), padx=10, columnspan=2)

        # Main loop for import window
        importS.mainloop()

    def openFile(self):
        """
        Opens a file dialog box searching for a .mp3 file. Once a file
        is selected, the user is asked for the artist and title. Then
        it is downloaded to the music directory.
        """
        # Tkinter Import Window
        global importS

        # Reset Variables
        if self.compLab is not None:
            self.compLab.configure(text='') #should be irrelevant? had issues before adding it though
            self.compLab.destroy()
            self.compLab=None

        # Obtain File Path from file dialog
        importS.fileName = filedialog.askopenfilename(filetypes=(("MP3 files","*.mp3"),("All files","*.*")))
        self.songToImport = importS.fileName

        # Do a file check TEST!?
        if type(self.songToImport) is not str or self.songToImport == "":
            self.songToImport = ""
            return
        elif os.path.splitext(self.songToImport)[1] != '.mp3':
            self.songToImport = ""
            self.compLab = tkinter.Label(importS, text="File is not .mp3 format", font=SUB_HEADER_FONT, fg='red')
            self.compLab.grid(column=0, row=8, columnspan=2, padx=10, pady=(2,10))
            return

        # File Path
        self.songPath = tkinter.Label(importS, text=self.songToImport, font=STANDARD_FONT)
        self.songPath.grid(column=0, row=4, columnspan=2)

        # Artist & Song Labels & Entry Boxes
        self.artLab = tkinter.Label(importS, text="Artist Name:", font=STANDARD_FONT)
        self.artistName = tkinter.Entry(importS)
        self.songLab = tkinter.Label(importS, text="Song Title:", font=STANDARD_FONT)
        self.songTitle = tkinter.Entry(importS)
        # Appending Labels to Window
        self.artLab.grid(column=0, row=5)
        self.artistName.grid(column=1, row=5)
        self.songLab.grid(column=0, row=6)
        self.songTitle.grid(column=1, row=6)

        # Import Button
        self.B3 = tkinter.Button(importS,text="Import", command=self.importSong)
        self.B3.grid(column=0, row=7, pady=(10,2), padx=10, columnspan=2)

        # Insert best guess for a song title
        tempSong = StartPage.splitArtSong(self.songToImport)
        self.songTitle.insert(0,tempSong[1])

    def openDir(self):
        """
        Opens a file dialog box searching for a directory. Once a directory
        is selected, the user will be asked for an artist name and song title
        for each file in the directory. It will ignore all files not ending in
        .mp3
        """
        # Tkinter Import Window
        global importS

        # Reset Complete Label
        if self.compLab is not None:
            self.compLab.destroy()
            self.compLab=None

        # Opens File Dialog Box
        importS.fileDir = filedialog.askdirectory()

        # Makes sure a directory was selected
        if type(importS.fileDir) is str and importS.fileDir != "":
            # Create Array of Directory Files
            self.songArray = glob.glob((importS.fileDir + "/*"))

            # Grab File
            self.songToImport = self.songArray.pop()
            self.count = 1
            self.total = len(self.songArray)+1

            # Check for .mp3 format
            while os.path.splitext(self.songToImport)[1] != '.mp3':
                # Go Through Array until .mp3 file is found
                if len(self.songArray) > 0:
                    self.songToImport = self.songArray.pop()
                    self.count += 1
                # No .mp3 file was found
                else:
                    self.compLab = tkinter.Label(importS, text="No .mp3 Files to Import", font=SUB_HEADER_FONT, fg='red')
                    self.compLab.grid(column=0, row=8, columnspan=2, padx=10, pady=(2,10))
                    return
                # Check might have to be written more like this:
                # filename, file_extension = os.path.splitext('path.ext')
                # then file_extension will be the extension

            # Label for telling user how many songs will be imported
            self.countLab = tkinter.Label(importS, text=("Importing " + str(self.count) + " of " + str(self.total) + ":"), font=STANDARD_FONT)
            self.countLab.grid(column=0, row=3, columnspan=2)

            # File Path Label
            self.songPath = tkinter.Label(importS, text=self.songToImport, font=STANDARD_FONT)
            self.songPath.grid(column=0, row=4, columnspan=2)

            # Import & Skip Buttons
            self.B3 = tkinter.Button(importS,text="Import", command=self.importSong)
            self.B3.grid(column=0, row=7, pady=(10,2), padx=10)
            self.B4 = tkinter.Button(importS,text="Skip", command=self.skip)
            self.B4.grid(column=1, row=7, pady=(10,2), padx=10)

            # Song & Artist Labels & Entry Boxes
            self.artLab = tkinter.Label(importS, text="Artist Name:", font=STANDARD_FONT)
            self.artistName = tkinter.Entry(importS)
            self.songLab = tkinter.Label(importS, text="Song Title:", font=STANDARD_FONT)
            self.songTitle = tkinter.Entry(importS)
            # Placing on Window
            self.artLab.grid(column=0, row=5)
            self.artistName.grid(column=1, row=5)
            self.songLab.grid(column=0, row=6)
            self.songTitle.grid(column=1, row=6)

            # Insert best guess for a song title
            tempSong = StartPage.splitArtSong(self.songToImport)
            self.songTitle.insert(0,tempSong[1])

    def skip(self):
        """
        Called by B4 Button, the Skip Button. This method skips a file
        for importing at the request of the user.
        """
        # Tkinter Import Window
        global importS

        # Make sure there's another song to skip to
        if len(self.songArray) > 0:
            # Increment songs dealt with
            self.count += 1
            self.countLab.config(text="Importing " + str(self.count) + " of " + str(self.total) + ":")

            # Select a new song from the array
            self.songToImport = self.songArray.pop()

            # Testing file for MP3 format
            isMP3 = True
            while os.path.splitext(self.songToImport)[1] != '.mp3':
                # Go through array until .mp3 file is found
                if len(self.songArray) > 0:
                    self.songToImport = self.songArray.pop()
                    self.count += 1
                # No .mp3 file was found
                else:
                    isMP3 = False
                    break

            # It is an MP3
            if isMP3:
                self.songPath.config(text=self.songToImport)

                # Insert best guess for song title
                tempSong = StartPage.splitArtSong(self.songToImport)
                self.songTitle.delete(0, END)
                self.songTitle.insert(0,tempSong[1])
            # It isn't an MP3 and it's the last element in the array
            else:
                # Destroy Useless GUI Variables
                self.closeLabels()

                # Let User know import is complete
                self.compLab = tkinter.Label(importS, text="Import Complete!", font=SUB_HEADER_FONT, fg='green')
                self.compLab.grid(column=0, row=8, columnspan=2, padx=10, pady=(2,10))

        # No more songs in array
        else:
            # Destroy Labels
            self.countLab.destroy()
            self.artLab.destroy()
            self.songLab.destroy()
            self.songPath.destroy()

            # Destroy Entry Boxes
            self.artistName.destroy()
            self.songTitle.destroy()

            # Reset Count & Total Variables
            self.count = 0
            self.total = 0

            # Destroy Buttons
            self.B3.destroy()
            if self.B4 is not None:
                self.B4.destroy()

            # Let User know import is complete
            self.compLab = tkinter.Label(importS, text="Import Complete!", font=SUB_HEADER_FONT, fg='green')
            self.compLab.grid(column=0, row=8, columnspan=2, padx=10, pady=(2,10))

    def importSong(self):
        """
        Method which handles the copying of files and creating of
        sub-directories based on user input from the openFile and openDir
        methods.
        """
        # Tkinter Import Window
        global importS
        # SongSearch Variable
        global ss

        # Get the filepath for the music directory
        direct = ss.getFilePath()
        direct = direct[0:(len(direct)-1)]

        # Retrieve Artist & Song Variables
        artist = self.artistName.get()
        song = self.songTitle.get()

        # Add artist to music directory
        direct = direct+artist

        # Multiple Songs to import
        if len(self.songArray) > 0:
            # Update what's left to import
            self.count += 1
            self.countLab.config(text="Importing " + str(self.count) + " of " +
                                      str(self.total) + ":")

            # Check If The Artist Exists
            if not os.path.exists(direct):
                os.makedirs(direct)

            # Copy File to direct path
            direct = direct +'/'+song+'.mp3'
            copyfile(self.songToImport,direct)

            # Get next song from array
            self.songToImport = self.songArray.pop()

            # Testing file for MP3 format
            isMP3 = True
            while os.path.splitext(self.songToImport)[1] != '.mp3':
                if len(self.songArray) > 0:
                    self.songToImport = self.songArray.pop()
                    self.count += 1
                else:
                    isMP3 = False
                    break
            if isMP3:
                # Destroy old variables
                self.artLab.destroy()
                self.artistName.destroy()
                self.songLab.destroy()
                self.songTitle.destroy()

                # Insert New Song Info
                self.songPath.config(text=self.songToImport)
                self.artLab = tkinter.Label(importS, text="Artist Name:", font=STANDARD_FONT)
                self.artistName = tkinter.Entry(importS)
                self.songLab = tkinter.Label(importS, text="Song Title:", font=STANDARD_FONT)
                self.songTitle = tkinter.Entry(importS)

                # Post to GUI, Insert best guess for Artist & Song Names
                tempSong = StartPage.splitArtSong(self.songToImport)
                self.artLab.grid(column=0, row=5)
                self.artistName.grid(column=1, row=5)
                self.artistName.insert(0, artist)
                self.songLab.grid(column=0, row=6)
                self.songTitle.grid(column=1, row=6)
                self.songTitle.insert(0,tempSong[1])
            else:
                # Destroy useless GUI Variables
                self.closeLabels()

                # Let user know import is complete
                self.compLab = tkinter.Label(importS, text="Import Complete!", font=SUB_HEADER_FONT, fg='green')
                self.compLab.grid(column=0, row=8, pady=(2,10), padx=10, columnspan=2)

        # Only one song to import
        else:
            # Import Last Song
            if not os.path.exists(direct):
                os.makedirs(direct)
            direct = direct +'/'+song+'.mp3'
            copyfile(self.songToImport,direct)

            # Destroy useless GUI Variables
            self.closeLabels()

            # Let User know import is complete
            self.compLab = tkinter.Label(importS, text="Import Complete!", font=SUB_HEADER_FONT,fg='green')
            self.compLab.grid(column=0, row=3, pady=(2,10), padx=10, columnspan=2)

    def closeLabels(self):
        """
        Removes GUI labels that are no longer useful for the current
        user interaction pane
        """
        # Destroy Labels
        self.artLab.destroy()
        self.songLab.destroy()
        self.songPath.destroy()

        # Destroy Entry Boxes
        self.artistName.destroy()
        self.songTitle.destroy()

        # Reset Counting Variables
        if self.count > 0:
            self.countLab.destroy()
            self.count = 0
            self.total = 0

        # Destroy Buttons
        self.B3.destroy()
        if self.B4 is not None:
            self.B4.destroy()
            self.B4 = None


class SAT(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        """
        This method initializes frames and pages for the application as well
        as the menu bar.
        :param args: variables
        :param kwargs: dictionaries
        """

        # Initialize Tkinter
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.protocol('WM_DELETE_WINDOW',self.closeSAT)
        self.wm_title("S.A.T.")
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Contains the frames for the application
        self.frames = {}

        # Sets up each frame in the main tkinter window
        for Frame in (StartPage, Documentation):
            frame = Frame(container, self)
            self.frames[Frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Menu
        menubar = tkinter.Menu(container)
        # File Sub-Menu
        filemenu = tkinter.Menu(menubar,tearoff=0)
        filemenu.add_command(label="Import", command=lambda: importMusic())
        filemenu.add_command(label="Exit", command = lambda: exitSAT())
        menubar.add_cascade(label="File", menu=filemenu)
        # Help Sub-Menu
        helpmenu = tkinter.Menu(menubar,tearoff=0)
        helpmenu.add_separator()
        helpmenu.add_command(label="About",command= lambda: aboutMessage())
        helpmenu.add_command(label="Help Topics", command = lambda: self.show_frame(Documentation))
        menubar.add_cascade(label="Help",menu=helpmenu)

        # Configure the menu for the main Tkinter window
        tkinter.Tk.config(self,menu=menubar)

        # Start off by showing the Start Page
        self.show_frame(StartPage)

    def closeSAT(self):
        """
        This method contains all the code to close all windows in the
        application, as well as close and exit the music player
        """
        # Close Search Window
        global swindow
        try:
            swindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass
        
        # Close About Window
        global about
        try:
            about.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass
        
        # Close Import Window
        global importS
        try:
            importS.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Close Overview Window
        global qoWindow
        try:
            qoWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Close Play A Song Window
        global pasWindow
        try:
            pasWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Close Loop & Shuffle Button Window
        global lasbWindow
        try:
            lasbWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Close Search Button Window
        global sbWindow
        try:
            sbWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Close Import Songs Window
        global isWindow
        try:
            isWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Close Music Directory Window
        global tmdWindow
        try:
            tmdWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Close Unanswered Questions Window
        global uqWindow
        try:
            uqWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass
        
        # Close Main Application Window
        try:
            self.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        pygame.mixer.quit()
        sys.exit()
        
    def show_frame(self, cont):
        """
        show_frame raises the indicated frame to the top of the main Tkinter window.
        :param cont: A Tkinter frame that has been initialized in init
        """
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tkinter.Frame):

    def __init__(self, parent, controller):
        """
        Initializes the Start Page of the application.
        :param parent: Main tkinter container passed from the SAT object
        :param controller: The SAT object that created an instance of StartPage
        """
        # Song Variables
        global continuePlaying
        global songList
        global prevSongs
        global loopButton
        global shuffleButton
        global nowPlaying
        global randomButton

        # Display Variables
        global artDisplay
        global songDisplay

        # Variable for SongSearch
        global ss

        # Initializing Song Variables
        songList = []
        prevSongs = []
        nowPlaying = None
        continuePlaying = False
        self.initVol = 1

        # Initializing SongSearch variable
        ss = SongSearch('')

        # Initialize the tkinter window
        tkinter.Frame.__init__(self,parent)

        # Beginning labels
        title = tkinter.Label(self, text = "Simple Audio Thing", font=HEADER_FONT)
        title.grid(column=0,row=0, columnspan=5, sticky="W", pady=10, padx=10)
        music = tkinter.Label(self, text="Now Playing", font=SUB_HEADER_FONT)
        music.grid(column=0,row=1, columnspan=5, sticky="W", padx=15)

        # Display Artist & Song
        artistTitle = tkinter.Label(self, text="Artist:", font=STANDARD_FONT)
        artistTitle.grid(column=0, row=2, pady=(3,0), padx=20, columnspan = 2, sticky="W")
        songTitle = tkinter.Label(self, text="Song:", font=STANDARD_FONT)
        songTitle.grid(column=0,row=3, pady=(3,0), padx=20, columnspan = 2, sticky="W")
        artDisplay = tkinter.Label(self, text = "", font=STANDARD_FONT)
        songDisplay = tkinter.Label(self, text = "", font=STANDARD_FONT)
        artDisplay.grid(column=2, row=2, pady=(3,0), columnspan=5, sticky="W")
        songDisplay.grid(column=2, row=3, pady=(3,0), columnspan=5, sticky="W")

        # First Row of Buttons (Play, Previous, Next, Pause, & Stop)
        prevButton = tkinter.Button(self, text="Prev", command=lambda: self.previous(), width=6)
        prevButton.grid(column=1,row=4,sticky="E", pady=(5, 0))
        playButton = tkinter.Button(self, text="Play", command=lambda: self.play(), width=6)
        playButton.grid(column=2,row=4,sticky="W", pady=(5, 0))
        nextButton = tkinter.Button(self, text="Next", command=lambda: self.next(), width=6)
        nextButton.grid(column=3,row=4,sticky="W", pady=(5, 0))
        pauseButton = tkinter.Button(self, text="Pause", command=lambda: self.pause(), width=6)
        pauseButton.grid(column=4,row=4,sticky="W", pady=(5, 0))
        stopButton = tkinter.Button(self, text="Stop", command=lambda: self.stop(), width=6)
        stopButton.grid(column=5,row=4,sticky="W", pady=(5, 0))

        # Second Row of Buttons (Search, Randomize, Shuffle, & Loop)
        searchButton = tkinter.Button(self, text="Search", command=lambda: self.search())
        searchButton.grid(column=1,row=5,sticky="W",pady=10, padx=(30, 0))
        randomButton =tkinter.Button(self, text="Randomize", command=lambda: self.random())
        randomButton.grid(column=2,row=5,sticky="W",pady=10, columnspan=2)
        loopButton = self.lsButton("Loop", self, 0, 1)
        shuffleButton = self.lsButton("Shuffle", self, 0, 2)

        '''
        # Rooms Section (May be irrelevant?)
        roomsTitle = tkinter.Label(self, text="Active Rooms", font=SUB_HEADER_FONT)
        roomsTitle.grid(column=0, row=6, sticky="W", padx=10, pady=(30, 10), columnspan=5)
        livingRoom = self.RoomButton("Living Room", self, 1, 1)
        kitchen = self.RoomButton("Kitchen", self, 0, 2)'''

        # Volume Button
        self.volume = tkinter.Scale(self, command=self.changeVolume, length=200, width=18, from_=100, to=0)
        self.volume.grid(row=0, column=8, rowspan=18, sticky="W", padx=15)
        volTitle = tkinter.Label(self, text="Volume", font=SMALL_FONT)
        volTitle.grid(column=8, row=18, sticky="E", padx=(20,15))

    def play(self):
        """
        Function called when Play is pressed, it selects a song, displays
        it in the window, and plays it.
        """
        # Song Variables
        global continuePlaying
        global songList
        global shuffleButton
        global artDisplay
        global songDisplay
        global nowPlaying

        # Finds and plays a song since nothing was playing
        if nowPlaying is None or not pygame.mixer.music.get_busy():
            # Populate the list of songs to play
            if shuffleButton.isPressed:
                songList = ss.populate('s')
            else:
                songList = ss.populate(None)

            # Play the first song in the list
            nowPlaying = songList.pop(0)
            pygame.mixer.music.load(nowPlaying)
            pygame.mixer.music.play()

            # Display song info to app
            artSong = StartPage.splitArtSong()
            artDisplay.config(text=artSong[0])
            songDisplay.config(text=artSong[1])

            # Let next() know it can work now
            continuePlaying = True

        # Un-pause the song that's already playing
        else:
            pygame.mixer.music.unpause()

    def playSpecSong(self,song):
        """
        Plays a specific song based on input
        :param song: file path of the song to be played
        """
        # Song Variables
        global continuePlaying
        global songList
        global shuffleButton
        global artDisplay
        global songDisplay
        global nowPlaying
        global prevSongs

        # Append what was playing to previous
        if nowPlaying is not None:
            prevSongs.append(nowPlaying)
            
        # Load the song to be played
        nowPlaying = song
        pygame.mixer.music.load(nowPlaying)
        pygame.mixer.music.play()

        # Display the song to the app window
        artSong = StartPage.splitArtSong()
        artDisplay.config(text=artSong[0])
        songDisplay.config(text=artSong[1])

        #Let next() know it can continue playing
        continuePlaying = True

        # Populate the song list for future songs to be played
        if shuffleButton.isPressed:
            songList = ss.populate('s')
        else:
            songList = ss.populate(nowPlaying)

    def playSpecSongtDest(self,index,songDict):
        """
        Plays a specific song from a dictionary of songs and buttons, then
        destroys the buttons on the search window
        :param index: index of the song to be played given the dictionary
        :param songDict: Dictionary of songs/buttons
        """
        # Song Variables
        global continuePlaying
        global songList
        global shuffleButton
        global artDisplay
        global songDisplay
        global nowPlaying

        # Append what was playing to previous
        if nowPlaying is not None:
            prevSongs.append(nowPlaying)
            
        # Load the song to play
        nowPlaying = songDict[index][1]
        pygame.mixer.music.load(nowPlaying)
        pygame.mixer.music.play()

        # Display the song to the application window
        artSong = StartPage.splitArtSong()
        artDisplay.config(text=artSong[0])
        songDisplay.config(text=artSong[1])

        # Let next() know it can continue to play songs
        continuePlaying = True

        # Populate the song list
        if shuffleButton.isPressed:
            songList = ss.populate('s')
        else:
            songList = ss.populate(nowPlaying)

        for i in range(len(songDict)):
            songDict[i][0].destroy()

    @staticmethod
    def splitArtSong(song=None):
        """
        Takes a filepath and returns the Artist and Song name
        :param song: the file path to be parsed, if None, it will parse the
        nowPlaying global variable
        :return: [Artist, Song]
        """
        if song is None:
            global nowPlaying
            tempArray= nowPlaying.split('/')
        else:
            tempArray= song.split('/')
        tempsong = tempArray[len(tempArray)-1]
        tempsong = tempsong.split('.')

        return (tempArray[len(tempArray)-2],tempsong[0])

    def pause(self):
        """
        Function called when the Pause button is pressed in the
        application window, it pauses the music being played.
        """
        pygame.mixer.music.pause()

    @staticmethod
    def next():
        """
        Function called by the Next button in the application window as well
        as every second by the waiting() function below.
        This function calls the next song in the song list.
        :return:
        """
        # Make sure the next button should be called
        global continuePlaying
        if continuePlaying:
            # Song Variables
            global songList
            global prevSongs
            global nowPlaying
            # Display Variables
            global artDisplay
            global songDisplay
            # Button & Search Variables
            global loopButton
            global shuffleButton
            global ss

            # Repopulates songList if it is empty and Loop is pressed
            if len(songList) == 0:
                if loopButton.isPressed:
                    if shuffleButton.isPressed:
                        songList = ss.populate('s')
                    else:
                        songList = ss.populate(nowPlaying)
                # Clears display and stops music if Loop isn't pressed
                else:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    nowPlaying = None
                    artDisplay.config(text='')
                    songDisplay.config(text='')
                    continuePlaying = False
                    songList = []
                    prevSongs = []
                    return

            # Select song and play, append last song to prevSongs
            prevSongs.append(nowPlaying)
            nowPlaying = songList.pop(0)
            pygame.mixer.music.load(nowPlaying)
            pygame.mixer.music.play()

            # Change display on
            artSong = StartPage.splitArtSong()
            artDisplay.config(text=artSong[0])
            songDisplay.config(text=artSong[1])


    def previous(self):
        """
        Function called by the previous button in the application window.
        This function will replay the last song that was played.
        """
        # Song Variables
        global prevSongs
        global songList
        global artDisplay
        global songDisplay
        global nowPlaying

        # Makes sure there's a previous song to play, then plays it
        if len(prevSongs)>0:
            songList.insert(0,nowPlaying)
            nowPlaying = prevSongs.pop()
            pygame.mixer.music.load(nowPlaying)
            pygame.mixer.music.play()
            artSong = StartPage.splitArtSong()
            artDisplay.config(text=artSong[0])
            songDisplay.config(text=artSong[1])

    def stop(self):
        """
        Function called by the stop button in the application window.
        This function will stop the playing of music.
        """
        # Song Variables
        global continuePlaying
        global songList
        global prevSongs
        global artDisplay
        global songDisplay
        global nowPlaying

        # Makes sure there's already a song playing, then stops it
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            nowPlaying = None
            artDisplay.config(text='')
            songDisplay.config(text='')
            continuePlaying = False
            songList = []
            prevSongs = []

    def changeVolume(self, vol):
        """
        Function called by the volume scale in the application window.
        This function will change the volume of the music being played.
        :param vol: integer value between 0 and 100 for the volume
        """
        # Song Variable
        global nowPlaying

        # Change the volume if it can be changed
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(int(vol)/100.0)

        # Set initial volume
        if self.initVol == 1:
            self.volume.set(100)
            pygame.mixer.music.set_volume(1)
            self.initVol = 0

    def activateRoom(self, roomButton):
        """
        Function to set up the on and off ability of a room button
        :param roomButton: Tkinter button variable
        """
        # Removes the original button from the window
        roomButton.button.destroy()

        # Checks current state of button, then changes it
        if roomButton.isPressed == 0:
            roomButton.button = tkinter.Button(self, text=roomButton.buttonName, command=lambda: self.activateRoom(roomButton))
            roomButton.isPressed = 1
        else:
            roomButton.button = tkinter.Button(self, text=roomButton.buttonName, command=lambda: self.activateRoom(roomButton), bg=BG_BUTTON,
                                      fg=DP_TEXT_BUTTON)
            roomButton.isPressed = 0

        # Placement of button and associated variables
        span = 2
        roomButton.button.grid(column=(roomButton.buttonNumber+1+(span*(roomButton.buttonNumber-1))), row=8, sticky="W", columnspan=span)

    def loopShuffle(self, lsButton):
        """
        Similar to the activateRoom function, this function sets up the on
        and off ability of the loop and shuffle buttons as well as handles
        the functionality of the two buttons.
        :param lsButton: Loop or Shuffle button
        """
        # Removes the first button from the application window
        lsButton.button.destroy()

        # Song Variables
        global continuePlaying
        global songList
        global ss

        # Checks current state of button, then changes it
        if lsButton.isPressed == 1:
            # Changes button state (on/off)
            lsButton.button = tkinter.Button(self, text=lsButton.buttonName, command=lambda: self.loopShuffle(lsButton))
            lsButton.isPressed = 0

            # Repopulates song list if shuffle button is pressed
            if continuePlaying and lsButton.buttonName == "Shuffle":
                songList = []
                songList = ss.populate(nowPlaying)

        else:
            # Changes button state (on/off)
            lsButton.button = tkinter.Button(self, text=lsButton.buttonName, command=lambda: self.loopShuffle(lsButton), bg=BG_BUTTON,
                                      fg=DP_TEXT_BUTTON)
            lsButton.isPressed = 1

            # Repopulates song list if shuffle button is pressed
            if continuePlaying and lsButton.buttonName == "Shuffle":
                songList = []
                songList = ss.populate('s')

        # Placement of button and associated variables
        span = 1
        if lsButton.buttonNumber % 2 == 1:
            stick = "E"
        else:
            stick = "W"
        lsButton.button.grid(column=(lsButton.buttonNumber+3), row=5, sticky=stick, columnspan=span)

    def random(self):
        """
        Function called by the randomize button in the application window.
        Plays a random song in the music directory.
        """
        global ss
        ss.reInit('')
        self.playSpecSong(ss.callBestMethod())

    def search(self):
        """
        Function called by the search button in the application window.
        Pulls up a new Tkinter window used for searching the song directory.
        Plays the song it finds after the search.
        """
        # SongSearch Variable
        global ss

        # Search window (made global so exit() function can remove it)
        global swindow

        # Have only one search window open at a time
        try:
            swindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Variable for an error message in the Tkinter search window
        self.errorm = None

        # Variable to hold songs found in search
        self.songArray = []

        def funct():
            """
            This function handles the search when the search button is pressed.
            """
            # Resets the error message to nothing
            if self.errorm is not None:
                self.errorm.destroy()

            # Removes the button variables in the songArray
            if len(self.songArray)>0:
                for i in range(len(self.songArray)):
                    self.songArray[i][0].destroy()
                self.songArray = []
                

            # Grabs the artist and song variables from the entry boxes
            artVar = artist.get()
            songVar = song.get()

            # Determines which fields were filled out,
            if songVar != '':
                args = 's'
                if artVar != '':
                    args += 'a'
                    ss.reInit(args,songVar,artVar)
                else:
                    ss.reInit(args,songVar)
            elif artVar != '':
                args = 'a'
                ss.reInit(args,None,artVar)

            # Calls the SearchSong class which returns songs based on search
            result = ss.callBestMethod()

            # A single song was returned, play it
            if type(result) is str:
                self.playSpecSong(result)
            # Nothing was returned, display error message
            elif result == -1:
                self.errorm = tkinter.Label(swindow, text="Couldn't find it...try again", font=SUB_HEADER_FONT, fg='red')
                self.errorm.grid(column=0, row=7, columnspan=3)
            # A list was returned, display options
            else:
                for i in range(len(result)):
                    temp = StartPage.splitArtSong(result[i])
                    newButton = tkinter.Button(swindow, text=(temp[1] + " by " + temp[0]), width=50, command=lambda i=i: self.playSpecSongtDest(i, self.songArray))
                    self.songArray.append((newButton,result[i]))
                    newButton.grid(column=0, row=7+i, columnspan=2, padx=10)

        # Instruction Labels
        swindow = tkinter.Tk()
        swindow.wm_title("Search")
        searchHeader = tkinter.Label(swindow, text="Search", font=HEADER_FONT)
        searchHeader.grid(column=0, row=0, pady=(10,5), padx=10, columnspan=3)
        searchInst = tkinter.Label(swindow, text="Fill out the fields that you want, ignore the rest and press search!", font=SMALL_FONT)
        searchInst2 = tkinter.Label(swindow, text="We'll handle it from there!", font=SMALL_FONT)
        # Putting labels in window
        searchInst.grid(column=0,row=1, padx=10, columnspan=3)
        searchInst2.grid(column=0,row=2, pady=(0,10), padx=10, columnspan=3)

        # Entry and Labels
        artLab = tkinter.Label(swindow, text="Artist:", font=STANDARD_FONT)
        artist = tkinter.Entry(swindow)
        songLab = tkinter.Label(swindow, text="Song:", font=STANDARD_FONT)
        song = tkinter.Entry(swindow)
        butt = tkinter.Button(swindow, text="Search", command=lambda: funct())
        # Putting labels in window
        artLab.grid(column=0, row=4)
        artist.grid(column=1, row=4)
        songLab.grid(column=0, row=5)
        song.grid(column=1, row=5)
        butt.grid(column=0, row=6, columnspan=3, pady=(0,10))

        # Window loop
        swindow.mainloop()

    class RoomButton(tkinter.Tk):

        def __init__(self, name, parent, initVal, buttonNum):
            """
            Class used to keep track of variables associated with room buttons.
            :param name: String, button name
            :param parent: Parent object creating this object
            :param initVal: integer variable 1 or 0 for ON/OFF
            :param buttonNum: integer variable with sequence number
            """
            # Button variables
            self.button = tkinter.Button(parent, text=name, command=lambda: parent.activateRoom(self))
            self.isPressed = initVal
            self.buttonNumber = buttonNum
            self.buttonName = name

            # Calls the activateRoom() function after button is created.
            parent.activateRoom(self)

    class lsButton(tkinter.Tk):

        def __init__(self, name, parent, initVal, buttonNum):
            """
            Class used to keep track of variables associated with loop and
            shuffle buttons.
            :param name: String, button name ("Loop"/"Shuffle")
            :param parent: Parent object creating this object
            :param initVal: integer variable 1 or - for ON/OFF
            :param buttonNum: integer variable with sequence number
            """
            # Button Variables
            self.button = tkinter.Button(parent, text=name, command=lambda: parent.loopShuffle(self))
            self.isPressed = initVal
            self.buttonNumber = buttonNum
            self.buttonName = name

            # Calls the loopShuffle() function after button is created.
            parent.loopShuffle(self)


class Documentation(tkinter.Frame):

    def __init__(self, parent, controller):
        """
        Initializes the Documentation page of the application.
        :param parent: Main Tkinter container passed from the SAT object
        :param controller: The SAT object that created an instance of Documentation
        """
        # Initializes the Tkinter frame
        tkinter.Frame.__init__(self,parent)

        # Header Label
        label = tkinter.Label(self, text = "Help Topics", font=HEADER_FONT)
        label.grid(column=0, row=0, columnspan=2, pady=10,padx=10, sticky="W")

        # Topic Buttons, first column
        mainPage = tkinter.Label(self, text = "Main Interface Help", font=SUB_HEADER_FONT)
        mainPage.grid(column=0, row=1, padx=10, sticky="W")
        b1 = tkinter.Button(self,text="Overview", command = lambda: self.qo(), width=25)
        b1.grid(column=0,row=2,padx=10)
        b2 = tkinter.Button(self,text="Playing A Song", command = lambda: self.pas(), width=25)
        b2.grid(column=0,row=3,padx=10)
        b3 = tkinter.Button(self,text="Loop & Shuffle Buttons", command = lambda: self.lasb(), width=25)
        b3.grid(column=0,row=4,padx=10)
        b5 = tkinter.Button(self,text="Search Button", command = lambda: self.sb(), width=25)
        b5.grid(column=0,row=5,padx=10)

        # Topic Buttons, second column
        addTops = tkinter.Label(self, text = "Additional Topics", font=SUB_HEADER_FONT)
        addTops.grid(column=1, row=1, sticky="W")
        b6 = tkinter.Button(self,text="Importing Songs", command = lambda: self.iS(), width=25)
        b6.grid(column=1, row=2, padx=(0,10))
        b7 = tkinter.Button(self,text="The Music Directory", command = lambda: self.tmd(), width=25)
        b7.grid(column=1, row=3, padx=(0,10))
        b8 = tkinter.Button(self,text="Unanswered Questions?", command = lambda: self.uq(), width=25)
        b8.grid(column=1, row=4, padx=(0,10))
        # Button to return to original page
        button1 = tkinter.Button(self,text="Home", command = lambda: controller.show_frame(StartPage))
        button1.grid(column=1,row=6, columnspan=2, padx=(0,10), pady=(5,0), sticky="E")

    def qo(self):
        """
        Opens the Quick Overview informational window when the button is pressed in the
        Help Documentation page.
        """
        global qoWindow

        # Only One qoWindow open at a time
        try:
            qoWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Create Window
        qoWindow = tkinter.Tk()
        qoWindow.wm_title("Overview")

        # Header Label
        header = tkinter.Label(qoWindow, text = "Overview", font=HEADER_FONT)
        header.grid(column=0, row=0, pady=10,padx=10, sticky="W", columnspan=2)

        # Information Layout Section
        tkinter.Label(qoWindow, text = "Layout",
                      font=SUB_HEADER_FONT).grid(column=0, row=1, padx=10, sticky="W", columnspan=2)
        # Now Playing Section
        tkinter.Label(qoWindow, text = "Now Playing: ",
                      font=STANDARD_FONT).grid(column=0, row=2, padx=(20,3), sticky="W")
        tkinter.Label(qoWindow, text = "This section is the main section in the upper left corner of the main",
                      font=STANDARD_FONT).grid(column=1, row=2, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "window. It will display the artist and song title for the song that is",
                      font=STANDARD_FONT).grid(column=1, row=3, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "currently being played in the music player.",
                      font=STANDARD_FONT).grid(column=1, row=4, padx=(2,10), pady=(0,5), sticky="W")
        # Button Description
        tkinter.Label(qoWindow, text = "Buttons: ",
                      font=STANDARD_FONT).grid(column=0, row=5, padx=(20,3), sticky="W")
        tkinter.Label(qoWindow, text = "This is the section just below the Now Playing section. It contains all",
                      font=STANDARD_FONT).grid(column=1, row=5, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "the buttons for control of the MP3 player. Each button will be described",
                      font=STANDARD_FONT).grid(column=1, row=6, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "below in more detail.",
                      font=STANDARD_FONT).grid(column=1, row=7, padx=(2,10), pady=(0,5), sticky="W")
        # Volume Slider
        tkinter.Label(qoWindow, text = "Volume Slider: ",
                      font=STANDARD_FONT).grid(column=0, row=8, padx=(20,3), sticky="W")
        tkinter.Label(qoWindow, text = "This is located in the right-most column of the MP3 player. The volume",
                      font=STANDARD_FONT).grid(column=1, row=8, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "starts at 100, simply slide the nutton up or down for higher or lower",
                      font=STANDARD_FONT).grid(column=1, row=9, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "volume respectively.",
                      font=STANDARD_FONT).grid(column=1, row=10, padx=(2,10), sticky="W")

        # Buttons Row 1 Section
        tkinter.Label(qoWindow, text = "Buttons - Row 1 (Prev, Play, Next, Pause, Stop)",
                      font=SUB_HEADER_FONT).grid(column=0, row=12, padx=10, pady=(0,5), sticky="W", columnspan=2)
        # Previous Button
        tkinter.Label(qoWindow, text = "Prev: ",
                      font=STANDARD_FONT).grid(column=0, row=13, padx=(20,3), sticky="W")
        tkinter.Label(qoWindow, text = "Previous Button. This will play the last song that played if it is",
                      font=STANDARD_FONT).grid(column=1, row=13, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "available. If no song has yet been played or the Stop button has",
                      font=STANDARD_FONT).grid(column=1, row=14, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "been pressed, this button will do nothing.",
                      font=STANDARD_FONT).grid(column=1, row=15, padx=(2,10), pady=(0,5), sticky="W")
        # Play Button
        tkinter.Label(qoWindow, text = "Play: ",
                      font=STANDARD_FONT).grid(column=0, row=16, padx=(20,3), sticky="W")
        tkinter.Label(qoWindow, text = "Play Button. If nothing is playing, this button will select a random",
                      font=STANDARD_FONT).grid(column=1, row=16, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "song from the music library to play. If something has been paused, it",
                      font=STANDARD_FONT).grid(column=1, row=17, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "will resume playback. If a song is already playing, this button will do",
                      font=STANDARD_FONT).grid(column=1, row=18, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "nothing.",
                      font=STANDARD_FONT).grid(column=1, row=19, padx=(2,10), pady=(0,5), sticky="W")
        # Next Button
        tkinter.Label(qoWindow, text = "Next: ",
                      font=STANDARD_FONT).grid(column=0, row=20, padx=(20,3), sticky="W")
        tkinter.Label(qoWindow, text = "Next Button. This will play the next song lined up in the music queue",
                      font=STANDARD_FONT).grid(column=1, row=20, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "which is based on the loop and shuffle buttons.",
                      font=STANDARD_FONT).grid(column=1, row=21, padx=(2,10), pady=(0,5), sticky="W")
        # Pause Button
        tkinter.Label(qoWindow, text = "Pause: ",
                      font=STANDARD_FONT).grid(column=0, row=22, padx=(20,3), sticky="W")
        tkinter.Label(qoWindow, text = "Pause Button. If a song is playing, this button will pause it for later",
                      font=STANDARD_FONT).grid(column=1, row=22, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "playback. If nothing is playing, this button will do nothing.",
                      font=STANDARD_FONT).grid(column=1, row=23, padx=(2,10), pady=(0,5), sticky="W")
        # Stop Button
        tkinter.Label(qoWindow, text = "Stop: ",
                      font=STANDARD_FONT).grid(column=0, row=24, padx=(20,3), sticky="W")
        tkinter.Label(qoWindow, text = "Stop Button. If nothing is playing, this button will do nothing. Otherwise",
                      font=STANDARD_FONT).grid(column=1, row=24, padx=(2,10), sticky="W")
        tkinter.Label(qoWindow, text = "it will stop music playback and clear the music queue.",
                      font=STANDARD_FONT).grid(column=1, row=25, padx=(2,10), pady=(0,5), sticky="W")

        # Buttons Row 2 Section
        tkinter.Label(qoWindow, text = "Buttons - Row 2 (Search, Randomize, Loop, & Shuffle)",
                      font=SUB_HEADER_FONT).grid(column=0, row=26, padx=10, pady=(0,5), sticky="W", columnspan=2)
        # Previous Button
        tkinter.Label(qoWindow, text = "Randomize: ",
                      font=STANDARD_FONT).grid(column=0, row=27, padx=(20,3), pady=(0,5), sticky="W")
        tkinter.Label(qoWindow, text = "This button will play a random song from the music library.",
                      font=STANDARD_FONT).grid(column=1, row=27, padx=(2,10), pady=(0,5), sticky="W")
        tkinter.Label(qoWindow, text = "All other buttons in these sections are described individually in detail. For the Search",
                      font=STANDARD_FONT).grid(column=0, row=28, padx=(20,10), sticky="W", columnspan=2)
        tkinter.Label(qoWindow, text = "button, see 'Search Button' in the Help Topics Menu, for the Loop and Shuffle buttons see",
                      font=STANDARD_FONT).grid(column=0, row=29, padx=(20,10), sticky="W", columnspan=2)
        tkinter.Label(qoWindow, text = "the 'Loop & Shuffle Buttons' in the Help Topics Menu.",
                      font=STANDARD_FONT).grid(column=0, row=30, padx=(20,10), sticky="W", columnspan=2)
  
        # Close Button
        B1 = tkinter.Button(qoWindow,text="Close", command=qoWindow.destroy)
        B1.grid(column=0, row=31, pady=10, columnspan = 2)

        # Main Loop for Window
        qoWindow.mainloop()

    def pas(self):
        """
        Opens the 'Play A Song' informational window when the button is pressed in the
        Help Documentation page.
        """
        global pasWindow

        # Only One pasWindow open at a time
        try:
            pasWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Create Window
        pasWindow = tkinter.Tk()
        pasWindow.wm_title("Play A Song")

        # Header Label
        header = tkinter.Label(pasWindow, text = "Playing A Song", font=HEADER_FONT)
        header.grid(column=0, row=0, pady=10,padx=10, sticky="W", columnspan=2)

        # The Play Button Described
        tkinter.Label(pasWindow, text = "The Play Button",
                      font=SUB_HEADER_FONT).grid(column=0, row=1, padx=10, pady=5, sticky="W", columnspan=2)
        tkinter.Label(pasWindow, text = "You can press this button at any time. It will play a song at random ",
                      font=STANDARD_FONT).grid(column=0, row=2, padx=(20,10), sticky="W")
        tkinter.Label(pasWindow, text = "if nothing is currently playing. Otherwise it will do nothing, or",
                      font=STANDARD_FONT).grid(column=0, row=3, padx=(20,10), sticky="W")
        tkinter.Label(pasWindow, text = "unpause a paused song.",
                      font=STANDARD_FONT).grid(column=0, row=4, padx=(20,10), sticky="W")

        # The Randomize Button
        tkinter.Label(pasWindow, text = "The Randomize Button",
                      font=SUB_HEADER_FONT).grid(column=0, row=5, padx=10, pady=(10,5), sticky="W", columnspan=2)
        tkinter.Label(pasWindow, text = "This is the perfect button for you when you get sick of whatever is",
                      font=STANDARD_FONT).grid(column=0, row=6, padx=(20,10), sticky="W")
        tkinter.Label(pasWindow, text = "playing and just want to be surprised. It will play a random song at",
                      font=STANDARD_FONT).grid(column=0, row=7, padx=(20,10), sticky="W")
        tkinter.Label(pasWindow, text = "any time. Even if nothing has been previously playing.",
                      font=STANDARD_FONT).grid(column=0, row=8, padx=(20,10), sticky="W")

        # The Search Button
        tkinter.Label(pasWindow, text = "Searching For Songs",
                      font=SUB_HEADER_FONT).grid(column=0, row=9, padx=10, pady=(10,5), sticky="W", columnspan=2)
        tkinter.Label(pasWindow, text = "The Search button handles this functionality and is described in",
                      font=STANDARD_FONT).grid(column=0, row=10, padx=(20,10), sticky="W")
        tkinter.Label(pasWindow, text = "detail in the 'Search Button' section of the Help Topics menu.",
                      font=STANDARD_FONT).grid(column=0, row=11, padx=(20,10), sticky="W")

        # Close Button
        B1 = tkinter.Button(pasWindow,text="Close", command=pasWindow.destroy)
        B1.grid(column=0, row=12, pady=10, columnspan = 2)

        # Main Loop for Window
        pasWindow.mainloop()

    def lasb(self):
        """
        Opens the 'Loop & Shuffle Buttons' informational window when the button is pressed in the
        Help Documentation page.
        """

        global lasbWindow

        # Only One lasbWindow open at a time
        try:
            lasbWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Create Window
        lasbWindow = tkinter.Tk()
        lasbWindow.wm_title("Loop & Shuffle Buttons")

        # Header Label
        header = tkinter.Label(lasbWindow, text = "Loop & Shuffle Buttons", font=HEADER_FONT)
        header.grid(column=0, row=0, pady=10,padx=10, sticky="W", columnspan=2)

        # The Loop Button
        tkinter.Label(lasbWindow, text = "The Loop Button",
                      font=SUB_HEADER_FONT).grid(column=0, row=1, padx=10, pady=5, sticky="W", columnspan=2)
        tkinter.Label(lasbWindow, text = "This button initializes as being on. When turned on, it will tell the",
                      font=STANDARD_FONT).grid(column=0, row=2, padx=(20,10), sticky="W")
        tkinter.Label(lasbWindow, text = "music player to continually play, even if it has ran through every",
                      font=STANDARD_FONT).grid(column=0, row=3, padx=(20,10), sticky="W")
        tkinter.Label(lasbWindow, text = "song in the music directory. If Shuffle is also on, these songs will",
                      font=STANDARD_FONT).grid(column=0, row=4, padx=(20,10), sticky="W")
        tkinter.Label(lasbWindow, text = "be re-shuffled every time it plays through all the songs in the",
                      font=STANDARD_FONT).grid(column=0, row=5, padx=(20,10), sticky="W")
        tkinter.Label(lasbWindow, text = "directory. If it is not selected, the player will loop through artists",
                      font=STANDARD_FONT).grid(column=0, row=6, padx=(20,10), sticky="W")
        tkinter.Label(lasbWindow, text = "in alphabetical order and the songs in each artist directory also in",
                      font=STANDARD_FONT).grid(column=0, row=7, padx=(20,10), sticky="W")
        tkinter.Label(lasbWindow, text = "alphabetical order.",
                      font=STANDARD_FONT).grid(column=0, row=8, padx=(20,10), sticky="W")

        # The Shuffle Button
        tkinter.Label(lasbWindow, text = "The Shuffle Button",
                      font=SUB_HEADER_FONT).grid(column=0, row=9, padx=10, pady=(10,5), sticky="W", columnspan=2)
        tkinter.Label(lasbWindow, text = "This button shuffles the songs in the music queue for songs that will",
                      font=STANDARD_FONT).grid(column=0, row=10, padx=(20,10), sticky="W")
        tkinter.Label(lasbWindow, text = "play next. It initializes as on, if turned off, the player will go",
                      font=STANDARD_FONT).grid(column=0, row=11, padx=(20,10), sticky="W")
        tkinter.Label(lasbWindow, text = "through the artists in alphabetical order starting at what was currently",
                      font=STANDARD_FONT).grid(column=0, row=12, padx=(20,10), sticky="W")
        tkinter.Label(lasbWindow, text = "playing.",
                      font=STANDARD_FONT).grid(column=0, row=13, padx=(20,10), sticky="W")



        # Close Button
        B1 = tkinter.Button(lasbWindow,text="Close", command=lasbWindow.destroy)
        B1.grid(column=0, row=14, pady=10, columnspan = 2)

        # Main Loop for Window
        lasbWindow.mainloop()

    def sb(self):
        """
        Opens the 'Search Button' informational window when the button is pressed in the
        Help Documentation page.
        """
        global sbWindow

        # Only One sbWindow open at a time
        try:
            sbWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Create Window
        sbWindow = tkinter.Tk()
        sbWindow.wm_title("Search Window")

        # Header Label
        header = tkinter.Label(sbWindow, text = "Search Button", font=HEADER_FONT)
        header.grid(column=0, row=0, pady=10,padx=10, sticky="W", columnspan=2)

        # The Loop Button
        tkinter.Label(sbWindow, text = "Using the Search Window",
                      font=SUB_HEADER_FONT).grid(column=0, row=1, padx=10, pady=5, sticky="W", columnspan=2)
        tkinter.Label(sbWindow, text = "The search button opens a search window where two fields are available",
                      font=STANDARD_FONT).grid(column=0, row=2, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "for user input. The user can fill out either the artist field, the song",
                      font=STANDARD_FONT).grid(column=0, row=3, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "field, or both. If both are filled out it will be looking for a specific",
                      font=STANDARD_FONT).grid(column=0, row=4, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "song by a specific artist.",
                      font=STANDARD_FONT).grid(column=0, row=5, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "The search window will stay open even after it starts a song playing,",
                      font=STANDARD_FONT).grid(column=0, row=6, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "simply click the x at the top of the window to get rid of the search",
                      font=STANDARD_FONT).grid(column=0, row=7, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "window.",
                      font=STANDARD_FONT).grid(column=0, row=8, padx=(20,10), sticky="W")

        # The Shuffle Button
        tkinter.Label(sbWindow, text = "Multiple Results",
                      font=SUB_HEADER_FONT).grid(column=0, row=9, padx=10, pady=(10,5), sticky="W", columnspan=2)
        tkinter.Label(sbWindow, text = "The search window will pull up multiple results as click-able buttons",
                      font=STANDARD_FONT).grid(column=0, row=10, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "if there is more than one song that matches the search. To play one of",
                      font=STANDARD_FONT).grid(column=0, row=11, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "those songs, simply click the button with the name of the song you wish",
                      font=STANDARD_FONT).grid(column=0, row=12, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "to play.",
                      font=STANDARD_FONT).grid(column=0, row=13, padx=(20,10), sticky="W")

        # The Shuffle Button
        tkinter.Label(sbWindow, text = "Searching Tips",
                      font=SUB_HEADER_FONT).grid(column=0, row=14, padx=10, pady=(10,5), sticky="W", columnspan=2)
        tkinter.Label(sbWindow, text = "The search will match a partial artist or song name. So if you are",
                      font=STANDARD_FONT).grid(column=0, row=15, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "unsure of a spelling in the directory, you can type the first few letters",
                      font=STANDARD_FONT).grid(column=0, row=16, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "and it should pull up in the search results. The search is not case",
                      font=STANDARD_FONT).grid(column=0, row=17, padx=(20,10), sticky="W")
        tkinter.Label(sbWindow, text = "sensitive.",
                      font=STANDARD_FONT).grid(column=0, row=18, padx=(20,10), sticky="W")

        # Close Button
        B1 = tkinter.Button(sbWindow,text="Close", command=sbWindow.destroy)
        B1.grid(column=0, row=19, pady=10, columnspan = 2)

        # Main Loop for Window
        sbWindow.mainloop()

    def iS(self):
        """
        Opens the 'Importing Songs' informational window when the button is pressed in the
        Help Documentation page.
        """
        global isWindow

        # Only One isWindow open at a time
        try:
            isWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Create Window
        isWindow = tkinter.Tk()
        isWindow.wm_title("Importing Songs")

        # Header Label
        header = tkinter.Label(isWindow, text = "Importing Songs", font=HEADER_FONT)
        header.grid(column=0, row=0, pady=10,padx=10, sticky="W", columnspan=2)

        # Importing Songs Window
        tkinter.Label(isWindow, text = "The Importing Songs Window",
                      font=SUB_HEADER_FONT).grid(column=0, row=1, padx=10, pady=5, sticky="W", columnspan=2)
        tkinter.Label(isWindow, text = "To import songs, click File, then Import. This will open the import songs",
                      font=STANDARD_FONT).grid(column=0, row=2, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "window where you have two options: 'Import File' or 'Import Directory'.",
                      font=STANDARD_FONT).grid(column=0, row=3, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "This player will only import .mp3 files as that is the only file type",
                      font=STANDARD_FONT, fg='red').grid(column=0, row=4, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "it currently plays.",
                      font=STANDARD_FONT, fg='red').grid(column=0, row=5, padx=(20,10), sticky="W")

        # Single File
        tkinter.Label(isWindow, text = "Import A Single File",
                      font=SUB_HEADER_FONT).grid(column=0, row=9, padx=10, pady=(10,5), sticky="W", columnspan=2)
        tkinter.Label(isWindow, text = "In the Import Window, click the 'Import File' Button. Navigate to the .mp3",
                      font=STANDARD_FONT).grid(column=0, row=10, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "file you wish to import. Click open. From there you will be asked what the",
                      font=STANDARD_FONT).grid(column=0, row=11, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "Artist Name and Song Title are. The import box will put in a default value",
                      font=STANDARD_FONT).grid(column=0, row=12, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "for the song title under the assumption that the file name is the song name.",
                      font=STANDARD_FONT).grid(column=0, row=13, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "When you have the two fields filled out, click 'Import' and the song will be",
                      font=STANDARD_FONT).grid(column=0, row=14, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "added to the song library.",
                      font=STANDARD_FONT).grid(column=0, row=15, padx=(20,10), sticky="W")

        # Directory
        tkinter.Label(isWindow, text = "Import A Directory of Music Files",
                      font=SUB_HEADER_FONT).grid(column=0, row=16, padx=10, pady=(10,5), sticky="W", columnspan=2)
        tkinter.Label(isWindow, text = "In the Import Window, click the 'Import Directory' Button. Navigate to the ",
                      font=STANDARD_FONT).grid(column=0, row=17, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "directory you wish to import. Click open. From there the import window will",
                      font=STANDARD_FONT).grid(column=0, row=18, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "tell you how many files it found in the directory and which file you're",
                      font=STANDARD_FONT).grid(column=0, row=19, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "currently importing. It will automatically skip any file that is not a .mp3",
                      font=STANDARD_FONT).grid(column=0, row=20, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "file. For each that is an MP3, it will ask you for an Artist Name and Song",
                      font=STANDARD_FONT).grid(column=0, row=21, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "Title. The Song Title is filled with a default value under the assumption that",
                      font=STANDARD_FONT).grid(column=0, row=22, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "the file name is the song title. The Artist Name field will automatically",
                      font=STANDARD_FONT).grid(column=0, row=23, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "populate with the last value the user inputs as the artist name. Click import",
                      font=STANDARD_FONT).grid(column=0, row=24, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "after editing the two fields, and the next song will appear in the window to",
                      font=STANDARD_FONT).grid(column=0, row=25, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "be imported. When it is done importing a 'Import Complete' message will appear.",
                      font=STANDARD_FONT).grid(column=0, row=26, padx=(20,10), sticky="W")

        # Troubleshooting
        tkinter.Label(isWindow, text = "Troubleshooting",
                      font=SUB_HEADER_FONT).grid(column=0, row=27, padx=10, pady=(10,5), sticky="W", columnspan=2)
        tkinter.Label(isWindow, text = "Question: How do I play the file I just imported?",
                      font=STANDARD_FONT).grid(column=0, row=28, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "Answer: Use the Search Window. For more information about this window see",
                      font=STANDARD_FONT).grid(column=0, row=29, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "'Search Button' in the Help Topics menu.",
                      font=STANDARD_FONT).grid(column=0, row=30, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "Question: Why wasn't my file imported?",
                      font=STANDARD_FONT).grid(column=0, row=31, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "Answer: Is it a .mp3 file? No other file formats are supported in this media",
                      font=STANDARD_FONT).grid(column=0, row=32, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "player. Were you importing a directory? If so it only imports songs that are",
                      font=STANDARD_FONT).grid(column=0, row=33, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "immediatly in the directory, it will not import songs that are in a folder in",
                      font=STANDARD_FONT).grid(column=0, row=34, padx=(20,10), sticky="W")
        tkinter.Label(isWindow, text = "that directory.",
                      font=STANDARD_FONT).grid(column=0, row=35, padx=(20,10), sticky="W")

        # Close Button
        B1 = tkinter.Button(isWindow,text="Close", command=isWindow.destroy)
        B1.grid(column=0, row=37, pady=10, columnspan = 2)

        # Main Loop for Window
        isWindow.mainloop()

    def tmd(self):
        """
        Opens the Music Directory informational window when the button is pressed in the
        Help Documentation page.
        """
        global tmdWindow

        # Only One tmdWindow open at a time
        try:
            tmdWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Create Window
        tmdWindow = tkinter.Tk()
        tmdWindow.wm_title("Music Directory")

        # Header Label
        header = tkinter.Label(tmdWindow, text = "The Music Directory", font=HEADER_FONT)
        header.grid(column=0, row=0, pady=10,padx=10, sticky="W", columnspan=2)

        # Overview
        tkinter.Label(tmdWindow, text = "Overview",
                      font=SUB_HEADER_FONT).grid(column=0, row=1, padx=10, pady=5, sticky="W", columnspan=2)
        tkinter.Label(tmdWindow, text = "The default music directory is currently located in /home/pi/Music.",
                      font=STANDARD_FONT).grid(column=0, row=2, padx=(20,10), sticky="W")
        tkinter.Label(tmdWindow, text = "The way this music player stores music in the directory is to have",
                      font=STANDARD_FONT).grid(column=0, row=3, padx=(20,10), sticky="W")
        tkinter.Label(tmdWindow, text = "a folder titled with the Artist Name and under that folder all the",
                      font=STANDARD_FONT).grid(column=0, row=4, padx=(20,10), sticky="W")
        tkinter.Label(tmdWindow, text = "music files (in .mp3 format) by that artist named with the song title.",
                      font=STANDARD_FONT).grid(column=0, row=5, padx=(20,10), sticky="W")
        tkinter.Label(tmdWindow, text = "This allows the player to correctly display the artist name and song title",
                      font=STANDARD_FONT).grid(column=0, row=6, padx=(20,10), sticky="W")
        tkinter.Label(tmdWindow, text = "in the Now Playing section of the player.",
                      font=STANDARD_FONT).grid(column=0, row=7, padx=(20,10), sticky="W")

        # Changing the Directory
        tkinter.Label(tmdWindow, text = "Changing the Default Directory",
                      font=SUB_HEADER_FONT).grid(column=0, row=8, padx=10, pady=(10,5), sticky="W", columnspan=2)
        tkinter.Label(tmdWindow, text = "This option is currently not supported but will be coming soon!",
                      font=STANDARD_FONT).grid(column=0, row=9, padx=(20,10), sticky="W")


        # Close Button
        B1 = tkinter.Button(tmdWindow,text="Close", command=tmdWindow.destroy)
        B1.grid(column=0, row=10, pady=10, columnspan = 2)

        # Main Loop for Window
        tmdWindow.mainloop()

    def uq(self):
        """
        Opens the Music Directory informational window when the button is pressed in the
        Help Documentation page.
        """
        global uqWindow

        # Only One tmdWindow open at a time
        try:
            uqWindow.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        except tkinter.TclError:
            pass

        # Create Window
        uqWindow = tkinter.Tk()
        uqWindow.wm_title("Unanswered Questions")

        # Header Label
        header = tkinter.Label(uqWindow, text = "Unanswered Questions? Improvement Ideas?", font=HEADER_FONT)
        header.grid(column=0, row=0, pady=10,padx=10, sticky="W", columnspan=2)

        # Importing Songs Window
        tkinter.Label(uqWindow, text = "Email me at francis.megan301@gmail.com",
                      font=SUB_HEADER_FONT).grid(column=0, row=1, padx=10, pady=5, sticky="W", columnspan=2)

        # Close Button
        B1 = tkinter.Button(uqWindow,text="Close", command=uqWindow.destroy)
        B1.grid(column=0, row=14, pady=10, columnspan = 2)

        # Main Loop for Window
        uqWindow.mainloop()


class SongSearch:

    def __init__(self, inputs, song=None, artist=None, filePath=None):
        """
        Class used to search a song directory with a layout such that folders
        containing songs are labeled with the songs' artist.
        :param inputs: character value ('a','s', and/or 'f') to indicate which
        parameters have been included. a=artist, s=song, f=filePath.
        :param song: String, a song title being searched for. Defaults to None
        :param artist: String, an artist being searched for. Defaults to None
        :param filePath: A directory being searched in. Defaults to '/home/pi/Music/*'
        """
        self.inputs = inputs
        if 'f' in inputs:
            self.filePath = filePath
        else:
            self.filePath = DEFAULT_MUSIC_DIRECTORY
        if 'a' in inputs:
            self.artist = artist
        else:
            self.artist = None
        if 's' in inputs:
            self.song = song
        else:
            self.song = None

    def reInit(self,inputs,song=None,artist=None):
        """
        Re-Initializes the variables
        :param inputs: character value ('a','s', and/or 'f') to indicate which
        parameters have been included. a=artist, s=song, f=filePath.
        :param song: String, a song title being searched for. Defaults to None
        :param artist: String, an artist being searched for. Defaults to None
        """
        self.inputs = inputs
        if 's' in inputs:
            self.song = song
        else:
            self.song = None
        if 'a' in inputs:
            self.artist = artist
        else:
            self.artist = None

    def changeFilePath(self,filePath):
        """
        Changes the file path being searched in.
        :param filePath: String, file path of directory one wishes to search in.
        Directory must have a layout such that folders containing songs must be
        labeled with the songs' artist. It does not search deeper than the one
        sub-directory.
        """
        self.filePath = filePath

    def getFilePath(self):
        return self.filePath

    def findWord(self, word, searchList):
        """
        Case insensitive search between a string and elements in a list.
        :param word: String, word being searched for in the list
        :param searchList: String[], list to be searched through
        :return: Integer, index value of the string containing the word. Returns -1
        if the word is not found.
        """
        sW = word.lower()
        for l in searchList:
            sL = l.lower()
            for start in range(len(self.filePath)-2,len(sL)):
                templ=start
                tempw=0
                while(tempw < len(sW) and templ < len(sL) and sW[tempw]==sL[templ]):
                    templ+=1
                    tempw+=1
                    if(tempw == len(sW)):
                        return l
        return -1

    def search(self):
        """
        Searches for a given song by a given artist in the music directory.
        :return: Returns the file path of the song being searched for. Returns -1
        if the song is not found.
        """
        path = glob.glob(self.filePath)
        authDir = self.findWord(self.artist, path)
        if authDir != -1:
            path= glob.glob(authDir + '/*')
            thing = self.findWord(self.song,path)
            return thing

    def songSearch(self):
        """
        Searches for a given song in the music directory.
        :return: (String, String[], Integer) Returns the file path of the song
        being searched for. If there is more than one song that match the query
        an array of songs matching the query is returned. If no song is found,
        it returns -1.
        """
        path = glob.glob(self.filePath)
        songs = []
        for n in path:
            subPath = glob.glob(n + '/*')
            thing = self.findWord(self.song,subPath)
            if thing is not -1:
                songs.append(thing)
        if len(songs) < 1:
            return -1
        elif len(songs) == 1:
            return songs[0]
        else:
            return songs

    def randAuth(self):
        """
        Searches for the given author in the music directory If there is more than one
        song in the directory, it returns an array
        :return: (String, String[], Integer) Returns the file path of a song if there
        is only one song in the artist directory, returns an array with the file
        paths of the songs by the given artist, or returns -1 if no such artist is
        found in the music directory.
        """
        path = glob.glob(self.filePath)
        songs = []
        authDir = self.findWord(self.artist,path)

        if authDir != -1:
            while authDir != -1:
                songs += glob.glob(authDir + '/*')
                path.remove(authDir)
                authDir = self.findWord(self.artist,path)

            if len(songs) > 1:
                return songs
            else:
                return songs[0]
        else:
            return -1

    def randomSong(self):
        """
        Searches for a random song in the music directory.
        :return: String, returns the filepath of a random song.
        """
        authDir = glob.glob(self.filePath)
        authDir = authDir[random.randint(0,len(authDir)-1)]
        authDir = glob.glob(authDir + '/*')
        return authDir[random.randint(0,len(authDir)-1)]

    def callBestMethod(self):
        """
        Calls the best search method based on the arguments given in 'inputs'
        :return: (String, String[], Integer) returns the value being returned
        by the given method.
        """
        if 's' in self.inputs and 'a' in self.inputs:
            return self.search()
        elif 's' in self.inputs:
            return self.songSearch()
        elif 'a' in self.inputs:
            return self.randAuth()
        else:
            return self.randomSong()

    def populate(self, shuff):
        """
        Populates an array with songs in the music directory based on whether they
        should be shuffled.
        :param shuff: String, 's' indicates that the songs should be shuffled, None
        indicates that they should not be shuffled, a file path indicates that
        the songs should not be shuffled and should start from the given song in the
        file path.
        :return: String[], an array of file paths of all songs in the music directory
        based on if they should be shuffled, and where they should start from.
        """
        # Array being populated and returned
        sArray = []

        # Array of all artists in the music directory
        authDir = glob.glob(self.filePath)

        # Don't shuffle the songs, start from a random song in the directory
        if shuff is None:
            # Finding random song & appending to list
            authStart = random.randint(0,len(authDir)-1)
            songDir = glob.glob(authDir[authStart] + '/*')
            songStart = random.randint(0,len(songDir)-1)
            sArray.append(songDir[songStart])
            authOrig = authStart
            songOrig = songStart

            # Increment song in order to append next song
            songStart += 1
            while (songStart != songOrig or authStart != authOrig):
                # There's another song in the sub-directory, append it
                if songStart < len(songDir):
                    sArray.append(songDir[songStart])
                    songStart += 1
                # No more songs in this sub-directory, switch artist directories
                else:
                    songStart = 0
                    authStart = (authStart+1)%len(authDir)
                    songDir = glob.glob(authDir[authStart] + '/*')
        # Shuffle the songs (nice and easy)
        elif shuff is 's':
            songDir = []
            for i in authDir:
                songDir = songDir + glob.glob(i + '/*')
            while len(songDir)>0:
                sArray.append(songDir.pop(random.randint(0,len(songDir)-1)))
        # A file path was given, find it, then populate the list
        else:
            # Variables to keep track of position in search
            authStart = 0
            songStart = 0
            songDir = None
            temp = False

            # Search directories one by one
            for i in authDir:
                songDir = glob.glob(authDir[authStart] + '/*')
                for j in songDir:
                    # Found the song
                    if j == shuff:
                        temp = True
                        break
                    songStart += 1
                if temp:
                    break
                # Increment variables
                authStart += 1
                songStart = 0

            # Keep track of where we started
            authOrig = authStart
            songOrig = songStart
            songStart += 1

            # Populate the list without shuffling
            while (songStart != songOrig or authStart != authOrig):
                if songStart < len(songDir):
                    sArray.append(songDir[songStart])
                    songStart += 1
                else:
                    songStart = 0
                    authStart = (authStart+1)%len(authDir)
                    songDir = glob.glob(authDir[authStart] + '/*')
        return sArray


def waiting():
    """
    Call the next() method in the start page class every second. Used to
    continue playing songs after one has finished.
    """
    if not pygame.mixer.music.get_busy():
        StartPage.next()
    app.after(1000, waiting)

# Create the application
app = SAT()
# Call waiting() so next() is properly implemented
waiting()
# Loop until finished with app.
app.mainloop()

# Closing the music variables so songs don't play after hitting the x
if pygame.mixer.music.get_busy():
    pygame.mixer.music.stop()

pygame.mixer.quit()
