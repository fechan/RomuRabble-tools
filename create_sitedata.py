"""
Ingests a list of Romulan audio file names (without extension) and outputs site data JSON
"""
import json

filename_file = open("filelist.txt", "r")
filenames = [filename.replace("\n", "") for filename in filename_file.readlines()]
filename_file.close()

site_data = []
for filename in filenames:
    site_data.append(
        {
            "audio_file":       filename + ".mp3",
            "spectrogram_file": filename + ".png"
        }
    )

with open("site_data.json", "w") as f:
    json.dump(site_data, f, indent=2)