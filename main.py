import os.path
import time

from pydub import AudioSegment
import math


class ConvertAndSplitAudio:
    def __init__(self, filename):
        self.BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "voice")
        self.filename = filename
        self.extension = filename.split(".")[-1]
        self.folder = filename.split(".")[0].replace(" ", "")
        if not os.path.exists(os.path.join(self.BASE_DIR, self.folder)):
            os.mkdir(os.path.join(self.BASE_DIR, self.folder))

        if self.filename.endswith(".wav"):
            self.wav_filename = filename
        else:
            self.wav_filename = filename.replace(self.extension, "wav")
            self.audio = AudioSegment.from_file(os.path.join(self.BASE_DIR, self.folder, self.filename),
                                                format=self.extension)
            file_handle = self.audio.export(os.path.join(self.BASE_DIR, self.folder, self.wav_filename), format="wav")
            print(file_handle)

        print("File is converting..")
        time.sleep(10)
        try:
            self.audio = AudioSegment.from_wav(os.path.join(self.BASE_DIR, self.folder, self.wav_filename))
            self.duration = self.audio.duration_seconds
            if self.extension != "wav":
                os.remove(os.path.join(self.BASE_DIR, self.folder, self.filename))
            self.multiple_split(1)
            os.remove(os.path.join(self.BASE_DIR, self.folder, self.wav_filename))
        except FileNotFoundError as e1:
            print(str(e1))

    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(os.path.join(self.BASE_DIR, self.folder, split_filename), format="wav")

    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.duration / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.wav_filename
            self.single_split(i, i + min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')


ConvertAndSplitAudio("Ses203.wav")
