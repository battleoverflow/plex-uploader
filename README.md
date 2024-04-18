# Plex Uploader
Plex Uploader is a simple desktop application built with the SSH & SCP protocols to upload media to a local Plex server utilizing a graphical interface. The Plex Uploader utilizes the Tkinter and TkinterDnD packages to provide a simple drag and drop interface for media files.

For this application to properly work, you must have SSH configured on both systems. At the end of the day, this is essentially just an SSH/SCP wrapper with a graphical interface, so it can be used for transferring any file from one system to another. I have only tested select media file formats (mp4, png, wav, etc.).

I have a couple ideas on expanding the app, but for now, this version should work for transferring single files quickly.

## Configuration

This specific configuration requires a username and password configuration. I may eventually add in RSA authentication, but for now, this is the current setup. You can add your SSH credentials within the `.env` file. You can see how to format the environment variables by comparing the `.env.example` to your current configuration.

## How To Run

> [!IMPORTANT]
> This project is currently only available for Windows due to the TkinterDnD package.

An executable is available to download under the Releases tab. Please note that the `.env` file must be in the same directory as the executable.

You can simple double-click the executable or run via the terminal:

```bash
./plex_uploader
```

If you're interested in working with the source code, you'll need to make sure Tkinter is installed on your system and all packages are installed. After everything is installed, you can run the code.

```bash
pip3 install -r requirements.txt
python3 plex-uploader.py
```

There is also a progress counter in the terminal while the application is running.
