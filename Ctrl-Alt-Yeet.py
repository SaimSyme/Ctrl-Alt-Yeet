from tkinter import *
from tkinter import filedialog
import os
import shutil

directories = {
    # Videos
    ".mp4": "Videos",
    ".MP4": "Videos",
    ".avi": "Videos",
    ".AVI": "Videos",
    ".mov": "Videos",
    ".MOV": "Videos",
    ".mkv": "Videos",
    ".MKV": "Videos",
    ".wmv": "Videos",
    ".flv": "Videos",
    ".webm": "Videos",
    ".gif": "Videos",

    # Audios
    ".mp3": "Audios",
    ".MP3": "Audios",
    ".wav": "Audios",
    ".WAV": "Audios",
    ".ogg": "Audios",
    ".OGG": "Audios",
    ".flac": "Audios",
    ".aac": "Audios",
    ".m4a": "Audios",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".bmp": "Images",
    ".gif": "Images",
    ".tiff": "Images",
    ".webp": "Images",

    # Compressed
    ".zip": "Compressed",
    ".ZIP": "Compressed",
    ".rar": "Compressed",
    ".RAR": "Compressed",
    ".7z": "Compressed",
    ".tar": "Compressed",
    ".gz": "Compressed",
    ".bz2": "Compressed",
    ".xz": "Compressed",

    # Documents
    ".pdf": "Documents",
    ".PDF": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".DOCX": "Documents",
    ".txt": "Documents",
    ".TXT": "Documents",
    ".rtf": "Documents",
    ".odt": "Documents",

    # Programs
    ".exe": "Programs",
    ".EXE": "Programs",
    ".msi": "Programs",
    ".bat": "Programs",
    ".sh": "Programs",

    # Spreadsheets and Presentations
    ".xls": "Documents",
    ".XLS": "Documents",
    ".xlsx": "Documents",
    ".XLSX": "Documents",
    ".csv": "Documents",
    ".ppt": "Documents",
    ".PPT": "Documents",
    ".pptx": "Documents",
    ".PPTX": "Documents",

    # Others (General)
    ".iso": "General",
    ".tar.gz": "General",
    ".html": "General",
    ".css": "General",
    ".js": "General",
    ".php": "General",
    ".py": "General",
    ".java": "General",
    ".cpp": "General",
    ".h": "General",
    ".xml": "General",
    ".json": "General",
    ".log": "General"
}

def openFile():
    filepath = filedialog.askdirectory()
    os.chdir(filepath)
    if filepath:
        print(filepath)
        SillyLilGuy.pack_forget()
        display_label.config(text=f"Organizing  （〜^∇^ )〜  {filepath}")
        display_label.pack() 
        createFolders()
        org_File1(filepath)
        FinishedOrg.pack()

def createFolders():
    for directory in set(directories.values()):
        os.makedirs(directory, exist_ok=True)
    print("Folders Created!")

def org_File1(filepath):
    files = os.listdir(filepath)

    for file in files:
        source_path = os.path.join(filepath, file)
        if os.path.isfile(source_path):
            _, extension = os.path.splitext(file)
            extension_lower = extension.lower()

            if extension_lower in directories:
                target_folder = directories[extension_lower]
            else:
                target_folder = "General"

            destination_folder = os.path.join(filepath, target_folder)

            # Create target folder if it doesn't exist
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # Construct destination path
            destination_path = os.path.join(destination_folder, file)

            # Check if file with same name exists in destination folder
            if os.path.exists(destination_path):
                base, ext = os.path.splitext(file)
                counter = 1
                while True:
                    new_filename = f"{base}_{counter}{ext}"
                    new_destination_path = os.path.join(destination_folder, new_filename)
                    if not os.path.exists(new_destination_path):
                        destination_path = new_destination_path
                        break
                    counter += 1

            try:
                # Move the file to the destination folder
                shutil.move(source_path, destination_path)
                print(f"Moved '{file}' to '{target_folder}' folder.")
            except Exception as e:
                print(f"Failed to move '{file}': {str(e)}")

    print("Files Organized!")

#GUI
window = Tk()
window.geometry("720x300")
window.title("◪_◪ CTRL+ALT+YEET ◪_◪ ")
window.resizable(False,False)

try:
    icon = PhotoImage(file='favicon.png')
    window.iconphoto(True, icon)
except:
    pass
window.config(background="#191825")

label = Label(window,
              text="◪_◪   CTRL+ALT+YEET   ◪_◪",
              font=('Ariel',20,'bold'),
              fg="#865DFF",
              bg="#191825",
              pady=20)
label.pack()

directorySelector = Label(window,
              text="SELECT YOUR DIRECTORY TO ORGANIZE:",
              font=('courier',15,'bold'),
              fg="#865DFF",
              bg="#191825",
              pady=10)
directorySelector.pack()

file_Chooser_Btn = Button(text="Select",command=openFile,pady=5,padx=40,fg="#865DFF",font=('Arial',12,'bold'),bg="white",relief='flat')
file_Chooser_Btn.pack()

display_label = Label(window, text="----------",
             font=('courier',15,'bold'),
             fg="#865DFF",
             bg="#191825",
             pady=10)
#display.pack is up there in the opneFile function

FinishedOrg = Label(window, text="YOUR DIRECTORY HAS BEEN ORGANIZED\n°˖✧◝(⁰▿⁰)◜✧˖°",
             font=('courier',15,'bold'),
             fg="#865DFF",
             bg="#191825",
             pady=10)
#Finished.pack is up there as well with different config

SillyLilGuy = Label(window, text="(ﾉ◕ヮ◕)ﾉ:･ﾟ✧",
             font=('courier',15,'bold'),
             fg="#865DFF",
             bg="#191825",
             pady=10)
SillyLilGuy.pack()
            
window.mainloop()