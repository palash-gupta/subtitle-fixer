from datetime import datetime, timedelta

fname = "s3e18.srt"

class SubtitleFrame:
    def __init__(self, begin, end, text):
        self.begin = begin
        self.end = end
        self.text = text

    def timing_line(self):
        return f"{self.begin.strftime("%H:%M:%S,%f")[:-3]} --> {self.end.strftime("%H:%M:%S,%f")[:-3]}\r\n"

    def __contains__(self, text):
        return text.lower() in ''.join(self.text).lower()

    def __str__(self):
        return f"{self.timing_line()}{''.join(self.text)}"


# parse the file and build the subtitle array
subtitle_array = []
text_buffer = []

stime = 0
etime = 0

with open(fname, 'r') as f:
    lines = f.readlines()

    current_count = 0

    for line in lines:
        if f"{current_count+1}\n" in line:
            subtitle_array.append(SubtitleFrame( stime, etime, text_buffer))
            text_buffer = []
            current_count += 1

        elif "-->" in line:
            start, end = line.split(' --> ')
            stime = datetime.strptime(start, "%H:%M:%S,%f")
            etime = datetime.strptime(end, "%H:%M:%S,%f\n")

        else:
            text_buffer.append(line)
    
    subtitle_array.append(SubtitleFrame( stime, etime, text_buffer))


# main

mode = int(input("Which mode?\n\n1. Time Delta (seconds)\n2. Time Delta (minutes and seconds)\n3. Time Shift\n\n> "))

delta = None

if mode == 1:
    seconds = int(input("Enter time in seconds (negative if you want the subtitles to shift backwards): "))
    delta = timedelta(seconds=seconds)
elif mode == 2:
    minutes, seconds = map(int, input("Enter time in M:S: ").split(':'))
    if minutes < 0:
        seconds = -seconds
    delta = timedelta(minutes=minutes, seconds=seconds)
elif mode == 3:
    minutes, seconds = map(int, input("Enter time stamp on the video (M:S): ").split(':'))
    t1 = datetime(1900, 1, 1, 0, minutes, seconds, 0)

    search_text = input("Enter dialogue that just ended: ")
    matched = False
    for subtitle in subtitle_array:
        if search_text in subtitle:
            print("MATCH FOUND")
            print(subtitle)
            if "n" in input("Confirm? [Y/n] ").lower():
                continue

            matched = True
            t2 = subtitle.end
            delta = t1 - t2  # check if this is t1-t2 or t2-t1
            break

    if not matched:
        print("No matches found.")
        exit()

# we do a little shifting

new_fname = input(f"Enter new filename (default: {fname[:-4]}_synced.srt): ")
if new_fname == '':
    new_fname = f"{fname[:-4]}_synced.srt"


with open(new_fname, 'w') as f:
    subnum = 1
    for i in range(1, current_count+1):
        subtitle = subtitle_array[i]

        subtitle.begin += delta
        subtitle.end += delta

        if subtitle.begin.year < 1900:
            continue

        f.write(str(subnum)+'\r\n')
        f.write(str(subtitle))
        subnum += 1


