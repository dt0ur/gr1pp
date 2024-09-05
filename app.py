#!/usr/bin/env python
from flask import Flask
from flask import request, redirect, url_for, send_from_directory
from markupsafe import escape
import subprocess
import os

app = Flask(__name__)

ydl_opts = {}
SAVEDIR = "/var/www/html/dl"

@app.route('/dl/<file>')
def download(file):
    print("downloading " + file)
    return send_from_directory(SAVEDIR, file, as_attachment=True)


@app.route('/watch')
def ripaudio():

    videoID = ""
    try:
        videoID = request.args.get('v')
    except:
        return "error"

    if videoID == "":
        return "error"

    p = subprocess.Popen(["yt-dlp", videoID, "--get-filename", "--restrict-filenames", "-x", "--audio-format", "mp3",
            "--ffmpeg-location", "/usr/local/bin/","--no-continue", "--no-mtime", "--user-agent",
            "foo_browser", "--no-cache-dir", "-o", "%(title)s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    filename, errors = p.communicate()
    if errors is not None and len(errors) > 0:
        return errors

    decoded_filename = filename.decode()[:len(filename.decode())-1]
    print(decoded_filename)
    full_path = SAVEDIR + "/" + decoded_filename + ".mp3"
    p = subprocess.Popen(["yt-dlp", videoID, "--restrict-filenames", "-x", "--audio-format", "mp3",
            "--ffmpeg-location", "/usr/local/bin/","--no-continue", "--no-mtime", "--user-agent",
            "foo_browser", "--no-cache-dir", "-o", SAVEDIR + "/%(title)s.%(ext)s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()
    if errors is not None and len(errors) > 0:
        return errors

    print(output.decode())
    to_download = decoded_filename + ".mp3"
    return redirect(url_for("download", file=to_download))


