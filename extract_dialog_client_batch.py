import extract_dialog

#episodes is a list of tuples ("EPISODE_NAME", "EPISODE_FILEPATH", "SRT_FILEPATH")
episodes = []

for episode in episodes:
    name = episode[0]
    input_video = episode[1]
    input_srt = episode[2]
    extract_dialog.extract(input_video, input_srt, name)