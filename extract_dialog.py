"""
Loads a video file and its corresponding SRT subtitle file and extracts clips where subtitles match
rules defined in dialog_match().
"""

from moviepy.editor import *
import os
from shutil import rmtree
from collections import namedtuple
from itertools import groupby

def dialog_match(line):
    '''Matches dialog satisfying the following conditions. Change as needed.'''
    if "_" in line:
        return True
    if "speaking romulan" in line.lower():
        return True
    if "in romulan" in line.lower():
        return True

def timecode_to_seconds(srt_timecode, ceiling):
    '''Converts srt timecodes to seconds. Truncates milliseconds unless ceiling is set, in which
    case it will round up to the nearest second.'''
    times = srt_timecode.split(':')
    hour = int(times[0])
    minute = int(times[1])
    sec = int(times[2].split(',')[0])
    millisec = int(times[2].split(',')[1])
    if ceiling and millisec > 0:
        sec += 1
    return (hour*3600) + (minute*60) + sec

def subtitle_list(input_srt):
    '''Loads SRT file as a list of Subtitle ( based on https://stackoverflow.com/a/23620587 )'''
    with open(input_srt) as f:
        # "chunk" our input file, delimited by blank lines
        res = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]
    Subtitle = namedtuple('Subtitle', 'number start end content')
    subs = []
    for sub in res:
        if len(sub) >= 3: # not strictly necessary, but better safe than sorry
            sub = [x.strip() for x in sub]
            number, start_end, *content = sub # py3 syntax
            start, end = start_end.split(' --> ')
            subs.append(Subtitle(number, start, end, content))
    return subs

def extract(input_video, input_srt, basename):
    #LOAD SRT
    subs = subtitle_list(input_srt)
    #FILTER MATCHING SUBS
    matches = []
    for sub in subs:
        for line in sub.content:
            if dialog_match(line):
                matches.append(sub)

    #EXTRACT CLIPS OF MATCHED SUB TIMES
    try:
        os.mkdir(basename)
    except FileExistsError:
        print(f"Info: {basename} exists! Deleting.")
        rmtree(basename)
        os.mkdir(basename)
    os.chdir(f"./{basename}")
    for index, sub in enumerate(matches):
        start = timecode_to_seconds(sub.start, False)
        end = timecode_to_seconds(sub.end, True)
        video = VideoFileClip(input_video).subclip(start, end)
        #Overlay starting timestamp
        textoverlay = ( TextClip(str(sub.start), fontsize=70, color='white')
            .set_position(("center","top"))
            .set_duration(end - start) )
        video = CompositeVideoClip([video, textoverlay])
        video.write_videofile(f"{basename}_{index}.mp4")