import platform, os
from tkinter import *
from tkinter import messagebox
from paramiko import AutoAddPolicy, SSHClient
from scp import SCPClient
from dotenv import load_dotenv

load_dotenv()

def is_mac() -> bool:
    """
    The TkinterDnD library is broken on certain MacOS systems due to incompatible architecture,
    so we do a quick check if the system is "Darwin".
    """
    if platform.system() == "Darwin":
        return True

    return False

def scp_progress(filename, size, sent) -> None:
    """
    Track the progress of the SCP transfer.
    """

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system("clear")

    print(f"File: {filename}\nProgress: {float(sent)/float(size)*100:.2f}\r\n")

# Only import the TkinterDnD library is we're not on MacOS
if not is_mac():
    from tkinterdnd2 import *

if is_mac():
    tk_dnd = Tk()
else:
    tk_dnd = TkinterDnD.Tk()

WIDTH = 400
HEIGHT = 300

# Startup the app in the center of the screen
screen_width = tk_dnd.winfo_screenwidth()
screen_height = tk_dnd.winfo_screenheight()

x = (screen_width/2) - (WIDTH/2)
y = (screen_height/2) - (HEIGHT/2)

tk_dnd.title("Plex Uploader")
tk_dnd.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, x, y))
tk_dnd.config(bg="#18181b")

FILE_NAME = StringVar()
VERSION = "0.1"

class PlexUploader:
    """
    Plex Upload is a simple desktop application built to upload content to a local Plex server without the need to ever touch a terminal.
    """

    def __init__(self) -> None:
        self.hostname = os.getenv("SSH_HOSTNAME")
        self.username = os.getenv("SSH_USERNAME")
        self.password = os.getenv("SSH_PASSWORD")
        self.remote_path = os.getenv("SSH_REMOTE_PATH")

    def get_file_event(self, event) -> None:
        """
        Access the file event from the media file being dropped into the application.
        """

        # The filename shows with parenthesis for some reason, so we need to strip those from the string
        FILE_NAME.set(event.data)

        # Only run the SCP transfer if a file is present
        if FILE_NAME != StringVar() and not is_mac():
            # If unable to connect via SSH with the provided credentials, it times out at 30 seconds
            ssh_client = SSHClient()
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password, timeout=30)
            scp = SCPClient(ssh_client.get_transport(), progress=scp_progress)
            scp.put(files=FILE_NAME.get()[1:-1], recursive=False, remote_path=self.remote_path)
            scp.close()

        return None
    
    def configure_ui(self) -> None:
        """
        Primary function for handling the UI for Tkinter.
        """
        frame = Frame(tk_dnd)
        frame.pack()

        # Place to drag and drop the media file
        label_frame = LabelFrame(tk_dnd, text="Upload Media", fg="#FFFFFF", bg="#18181b")
        Label(label_frame, fg="#FFFFFF", bg="#18181b", text="Drag and drop the media below.").pack(fill=BOTH, expand=True)
        label_frame.pack(fill=BOTH, expand=False, padx=10, pady=10)

        # This is where the file name should be displayed after dropping into the media section
        Label(tk_dnd, text="Media Path", fg="#FFFFFF", bg="#18181b").pack(anchor=NW, padx=10)
        entry_box = Entry(tk_dnd, textvar=FILE_NAME, borderwidth=2, relief="groove")
        entry_box.pack(fill=BOTH, padx=10, expand=True)

        # The user must press "Enter" after dragging and dropping the media file
        if not is_mac():
            entry_box.drop_target_register(DND_FILES)
            entry_box.dnd_bind('<<Drop>>', self.get_file_event)

        # Verison info
        label_frame = LabelFrame(tk_dnd, text="Version", fg="#FFFFFF", bg="#18181b")
        Label(label_frame, fg="#FFFFFF", bg="#18181b", text=f"v{VERSION}\nCreated by battleoverflow").pack(fill=BOTH, expand=True)
        label_frame.pack(fill=BOTH, expand=False, padx=10, pady=10)

    def main(self) -> None:
        """
        Simple function for handling all defined functionality and the actual transferring of the files to a remote host.
        """
        # Configure the Tkinter UI
        self.configure_ui()

        if is_mac():
            messagebox.showwarning("Warning", "MacOS is not supported.")
            return None

        tk_dnd.mainloop()

if __name__ == '__main__':
    PlexUploader().main()
