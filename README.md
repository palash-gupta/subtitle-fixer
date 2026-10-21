# Subtitle Fixer

A little script I whipped up because I was annoyed at all the subtitle files being out of sync. And also all the tools online being very subpar. This script is fairly simple and does exactly what I need it to do.

## Usage
```python main.py```


- **Mode 1:**
This mode just takes a time delta and applies that to all the subtitles in the SRT file.

- **Mode 2:**
Same as mode 1 but for bigger deltas where you might need to specify minutes and seconds both.

- **Mode 3:**
If you're too lazy to calculate the actual time delta (such as myself), just look at what was said in the video, and input a keyword from that, the program will show you a series of matches. If you recognise any of them you can input yes and it will automatically synchronise the SRT to that dialogue at that time stamp.
