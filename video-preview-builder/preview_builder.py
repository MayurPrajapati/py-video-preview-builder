#! /usr/bin/env python
from moviepy.editor import concatenate, VideoFileClip
import sys
import fnmatch
import os
import os.path

# python video-preview-builder/preview_builder.py folder_name

N_CLIPS = 10
DURATION = 3

# reduce for higher quality
QUALITY = 60

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: vdeoParser INDIR (OUTDIR)')
        exit(1)
    elif len(sys.argv) == 2:
        if not os.path.isdir(sys.argv[1]):
            print("Input {0} is not a valid directory".format(sys.argv[1]))
            exit(1)
        indir = sys.argv[1]
        outdir = sys.argv[1]
    elif len(sys.argv) == 3:
        if (not os.path.isdir(sys.argv[1])) or (not os.path.isdir(sys.argv[2])):
            print("Your inputs must be directories")
            exit(1)
        indir = sys.argv[1]
        outdir = sys.argv[2]
    else:
        print("Usage: vdeoParser INDIR (OUTDIR)")
        exit(1)

    for file in os.listdir(indir):
        if fnmatch.fnmatch(file, '*.mp4'):
            filearray = os.path.splitext(file)
            filename = str(filearray[0])
            try:
                vfc = VideoFileClip(indir+"/"+file)
                dur = vfc.duration
            except:
                print("Video file {0} is improperly formatted".format(file))
                continue

            markers = [dur*x/N_CLIPS-dur/(2*N_CLIPS)
                       for x in range(1, N_CLIPS+1)]

            clips = [vfc.subclip(m, m).set_duration(DURATION) for m in markers]
            video = concatenate(clips)

            video.write_videofile(outdir+"/"+filename + "preview" + ".mp4",threads=16,
                                  audio=True, ffmpeg_params=["-qmax", str(QUALITY)])
