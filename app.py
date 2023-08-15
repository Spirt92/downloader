import asyncio
import os
import queue
import threading

import requests
from flask import Flask, Response, jsonify, stream_with_context

app = Flask(__name__)

# List of URLs to download
file_urls: list = [
    "https://bouncer.gentoo.org/fetch/root"
    "/all/releases/amd64/autobuilds/20230611T170207Z/"
    "stage3-amd64-systemd-20230611T170207Z.tar.xz",
    "https://geo.mirror.pkgbuild.com/iso/2023.07.01/archlinux-x86_64.iso",
    "https://stable.release.flatcar-linux.net/amd64-usr/current/flatcar"
    "_production_iso_image.iso",
]


download_lock = threading.Lock() # Lock for synchronizing the download and zip process
downloaded_and_zipped: bool = False
zip_filename: str = "linux-isos.zip"  # Name of the zip file containing the downloaded files


def generate_zip_chunks(zip_filename: str):
    with open(zip_filename, "rb") as zip_file:
        while True:
            chunk = zip_file.read(8192)  # Read chunks of data
            if not chunk:
                break
            yield chunk


async def zip_files(downloaded_filenames: list) -> None:
    # Create a zip file of downloaded files
    with open(zip_filename, "wb") as zip_file:
        for filename in downloaded_filenames:
            with open(filename, "rb") as file:
                zip_file.write(file.read())

    # Remove downloaded individual files
    for filename in downloaded_filenames:
        os.remove(filename)


def download_file(url: str, filename: str) -> None:
    response = requests.get(url, stream=True)
    with open(filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


def download_and_zip_files() -> None:
    global downloaded_and_zipped

    # Create a directory to store downloaded files
    if not os.path.exists("downloaded_files"):
        os.makedirs("downloaded_files")

    downloaded_filenames = []

    # Create a thread queue to manage parallel downloading
    download_queue: queue.Queue = queue.Queue()

    # Create threads for downloading
    for idx, url in enumerate(file_urls):
        filename: str = os.path.join(
            "downloaded_files", f"file_{idx+1}.iso"
        )  # Adjust filename based on index
        downloaded_filenames.append(filename)
        download_queue.put((url, filename))
        threading.Thread(target=download_file, args=(url, filename)).start()

    # Wait for all downloads to complete
    download_queue.join()

    # Initiate zipping asynchronously
    asyncio.run(zip_files(downloaded_filenames))

    downloaded_and_zipped = True


@app.route("/download", methods=["GET"])
def download_endpoint() -> Response | jsonify:
    global downloaded_and_zipped

    if not downloaded_and_zipped:
        with download_lock:
            if not downloaded_and_zipped:
                download_and_zip_files()
                downloaded_and_zipped = True

    if os.path.exists(zip_filename):
        # Serve the existing zip file as a streaming response with "Transfer-Encoding: chunked"
        response = Response(
            stream_with_context(generate_zip_chunks(zip_filename)), content_type="application/zip"
        )
        response.headers["Content-Disposition"] = f"attachment; filename={zip_filename}"
        return response
    else:
        return jsonify({"status": "Please wait have not been downloaded and zipped yet."}), 200


if __name__ == "__main__":
    app.run(debug=True, threaded=True)  # Use multithreading for handling multiple connections
