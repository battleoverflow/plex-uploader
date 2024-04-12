from tkinter import *
from tkinter import messagebox
from tkinterdnd2 import *
from paramiko import SSHClient
from scp import SCPClient

# Validate basic formats accepted by Plex
FILE_FORMATS = ["mp4", "mkv", "m4a", "mp3", "mov", "avi"]

class PlexUploader:
    def __init__(self) -> None:
        # TODO: These values could be customizable in the UI
        self.hostname = "192.168.1.0"
        self.username = "root"
        self.password = "root"
        self.remote_path = "/opt/plex"
        self.filename = ""

    def get_file_event(self, event) -> str:
        for format in FILE_FORMATS:
            if event.data.endswith(f".{format}"):
                return str(event.data)
            
        messagebox.showwarning("About Project", f"{event.data} is not an accepted format.")
        return None

    def main(self) -> None:
        tk_dnd = TkinterDnD.Tk()
        tk_dnd.title("Plex Uploader")
        tk_dnd.geometry("800x600")
        tk_dnd.config(bg="#18181b")
        frame = Frame(tk_dnd)
        frame.pack()

        Label(tk_dnd, text="Media path", bg="#18181b").pack(anchor=NW, padx=10)
        entry_box = Entry(tk_dnd, textvar=self.filename, width=80)
        entry_box.pack(fill=X, padx=10)
        entry_box.drop_target_register(DND_FILES)
        entry_box.dnd_bind('<<Drop>>', self.filename)

        label_frame = LabelFrame(tk_dnd, text="Upload Media", bg="#18181b")
        Label(label_frame, bg="#18181b", text="Drag and drop the media file here.").pack(fill=BOTH, expand=True)
        label_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        Button(
            tk_dnd,
            # fg="#FFFFFF",
            bg="#18181b",
            text="Learn More",
            command=lambda: messagebox.showinfo("About", "Created by https://github.com/azazelm3dj3d")
        ).pack(padx=10, pady=20)

        if PlexUploader.get_file_event:
            ssh_client = SSHClient()
            ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password, timeout=30)
            scp = SCPClient(ssh_client.get_transport())
            scp.put(files=self.filename, recursive=False, remote_path=self.remote_path)
            scp.close()

        tk_dnd.mainloop()

if __name__ == '__main__':
    PlexUploader().main()
