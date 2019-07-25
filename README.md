# producerpy
A hodgepodge of Python scripts for automating tedious music production and programming-related tasks.

## Stem Killer (delete silent files)
Deletes any audio files that are completely silent.  You might export your tracks to stems to:
- mix in a different DAW
- share with a friend your project will contain stems
```
python delete_silent_files.py <top_dir_of_stems>
```
Often, you will find stems that contain no audio content.  These take up significant diskspace, and clutter your work environment/DAW.  This script only deletes files that are truly silent, files with very quiet sounds (reverb, noise, etc) will not be deleted.


## Organize your drum samples
Copies drum files into a directory organized by drum type.  Specify a directory to search, and an export location to copy the files to.  If searching multiples directories, simply leave the same export location to keep everything together.  Will likely not copy files if they are being read from an external harddrive.  On that note, DO NOT SPECIFY your EXPORT LOCATION as a directory within an external harddrive.
```
python organize_drums.py <top_dir_of_drums> <export_location>
```



## Plug-in Rotary Knob Asset Generator
Convert an image of a rotary knob to a asset strip of the knob at every angle.  The input image should be at the knob's lowest position, 0, -1, whatever.  Prior to rotating, all white pixels are made transparent, and the image is converted to square.  If your knob is not symmetrical, I suggest you add a border so the image is not cropped at certain angles.
```
python plugin_rotary_knob_strip_asset.py <image.png> <export_width>
```


## Audio + Image(s) = Video
Useful for Instagram content, eliminates the need to open any video editing software.  Visual component can be a single image, or several images displayed gif style.
```
python audio_plus_image_to_video.py <audio fp> <image(s) fp>
```


## Giffer
Nothing new here, just a script to generate audio-less gif's given the top folder filepath.
```
python giffer.py <image_dir> <fps>
```




## To run:
Install Python via anaconda using the instructions [here](https://www.anaconda.com/distribution/).

You will also need a few open source CLI tools:
```
brew install ffmpeg libav
```
```
pip install ffmpeg opencv-python moviepy librosa soundfile Pillow
```
