"""
Ingests a list of Romulan audio file names (without extension) and outputs site data JSON
"""
import json

filename_file = open("filelist.txt", "r")
filenames = [filename.replace("\n", "") for filename in filename_file.readlines()]
filename_file.close()

utterances = []
id = 0
for filename in filenames:
    tokens = filename.split("_")
    utterances.append(
        {
            "id":           id,
            "season":       int(filename[1]),
            "episode":      int(filename[3]),
            "discourse":    int(tokens[1].replace("discourse", "")),
            "time":         float(tokens[2]),
            "audio":        filename + ".mp3",
            "spectrogram":  filename + ".png",
            "meaning":      ""
        }
    )
    id = id + 1

site_data = {}
for utterance in utterances:
    episode_name = f"PIC {utterance['season']}x{str(utterance['episode']).zfill(2)}"
    if episode_name in site_data:
        site_data[episode_name]["utterances"].append(utterance)
    else:
        site_data[episode_name] = {
            "episode_name": episode_name,
            "utterances": []
        }

sorted_site_data = {}
for episodeName, episodeData in site_data.items():
    episodeData["utterances"] = sorted(episodeData["utterances"], key=lambda utterance: utterance["time"])
    sorted_site_data[episodeName] = episodeData

with open("site_data.json", "w") as f:
    json.dump(list(sorted_site_data.values()), f, indent=2)