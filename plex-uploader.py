import platform
from tkinter import *
from tkinter import messagebox
from paramiko import SSHClient
from scp import SCPClient

# Validate basic formats accepted by Plex
FILE_FORMATS = ["mp4", "mkv", "m4a", "mp3", "mov", "avi"]

def is_mac() -> bool:
    """
    The TkinterDnD library is broken on certain MacOS systems due to incompatible architecture,
    so we do a quick check if the system is "Darwin".
    """
    if platform.system() == "Darwin":
        return True

    return False

# Only import the TkinterDnD library is we're not on MacOS
if not is_mac():
    from tkinterdnd2 import *

def scp_progress(filename, size, sent) -> None:
    """
    Track the progress of the SCP transfer.
    """
    print(f"{filename}'s progress: {float(sent)/float(size)*100:.2f}   \r")

class PlexUploader:
    """
    Plex Upload is a simple desktop application built to upload content to a local Plex server without the need to ever touch a terminal.
    """
    def __init__(self) -> None:
        # TODO: These values could be customizable in the UI
        self.hostname = "192.168.1.0"
        self.username = "root"
        self.password = "root"
        self.remote_path = "/opt/plex"
        self.filename = ""

        if is_mac():
            self.tk_dnd = Tk()
        else:
            self.tk_dnd = TkinterDnD.Tk()

    def get_file_event(self, event) -> None:
        """
        Access the file event from the media file being dropped into the application.
        """
        for format in FILE_FORMATS:
            if event.data.endswith(f".{format}"):
                self.filename = str(event.data)
        
        # Show a warning message if the file format is not one of the accepted formats
        messagebox.showwarning("Media Warning", f"{event.data} is not an accepted format.")
        return None
    
    def configure_ui(self) -> None:
        """
        Primary function for handling the UI for Tkinter.
        """
        self.tk_dnd.title("Plex Uploader")
        self.tk_dnd.geometry("800x600")
        self.tk_dnd.config(bg="#18181b")
        frame = Frame(self.tk_dnd)
        frame.pack()

        # This is where the file name should be displayed after dropping into the media section
        Label(self.tk_dnd, text="Media path", bg="#18181b").pack(anchor=NW, padx=10)
        entry_box = Entry(self.tk_dnd, textvar=self.filename, width=80)
        entry_box.pack(fill=X, padx=10)

        # The user must press "Enter" after dragging and dropping the media file
        # The "Enter" will intiate the upload
        if not is_mac():
            entry_box.drop_target_register(DND_FILES)
            entry_box.dnd_bind('<<DropEnter>>', self.get_file_event)

        # Place to drag and drop the media file
        label_frame = LabelFrame(self.tk_dnd, text="Upload Media", bg="#18181b")
        Label(label_frame, bg="#18181b", text="Drag and drop the media file here.").pack(fill=BOTH, expand=True)
        label_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        Button(
            self.tk_dnd,
            # fg="#FFFFFF",
            bg="#18181b",
            text="Learn More",
            command=lambda: messagebox.showinfo("About", "Created by https://github.com/azazelm3dj3d")
        ).pack(padx=10, pady=20)

    def main(self) -> None:
        """
        Simple function for handling all defined functionality and the actual transferring of the files to a remote host.
        """
        # Configure the Tkinter UI
        self.configure_ui()

        # Only run the SCP transfer if a file is present
        if self.filename:
            ssh_client = SSHClient()
            ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password, timeout=30)
            scp = SCPClient(ssh_client.get_transport(), progress=self.scp_progress)
            scp.put(files=self.filename, recursive=False, remote_path=self.remote_path)
            scp.close()

        self.tk_dnd.mainloop()

if __name__ == '__main__':
    PlexUploader().main()
