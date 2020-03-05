import extract_dialog

import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

#ASK STARTING PARAMETERS
print("Specify video:")
input_video = filedialog.askopenfilename()
print("Specify subtitle file:")
input_srt = filedialog.askopenfilename()
basename = input("Base name of output files? (Defaults to the input video name): ")
if not basename:
    basename = input_video.split('/')[-1]

#EXTRACT DIALOG
extract_dialog.extract(input_video, input_srt, basename)