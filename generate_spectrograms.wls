#!/usr/bin/env wolframscript
(* ::Package:: *)

(* generate_spectrograms.wls takes in MP3s from audioDir and exports spectrograms to exportDir as PNGs *)

audioDir="/path/to/audio/"
exportDir="/path/to/spectrograms"

SetDirectory[audioDir]
exportSpectrogram[filename_,exportDir_]:=
	Export[
		FileNameJoin[{exportDir,StringReplace[filename,".mp3"->""]<>".png"}],
		Show[Spectrogram[Import[filename]],ImageSize->Large],
		"PNG"
	]
exportSpectrogram[#,exportDir]&/@FileNames[]
