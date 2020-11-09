# Imports
import os
from random import shuffle
from random import seed
from random import randint
from math import floor
from math import ceil
import time
import moviepy.editor as mpe
import moviepy.video as mpv
import moviepy.audio.fx.audio_fadein as mpafi
import moviepy.audio.fx.audio_fadeout as mpafo
import moviepy.video.fx.fadein as mpfxi
import moviepy.video.fx.fadeout as mpfxo
from assets.overlayWords.words import word_list

# Classes
class Sequence:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

class InputAgent:
    def generate_test_input(self):
        self.movie_file_name = "assets/vids/HTF.mp4"
        self.music_file_name = "assets/music/Depression.mp3"
        self.overlay_video_clip_name = 'assets/overlayVids/OverlayVid1.mp4'
        self.overlay_picture_name = 'assets/overlayPics/OverlayPic1.png'  
        self.output_file_name = 'output/SadVideo.mp4'   
        self.desired_duration = 60
        self.desired_minimum_cuts_length = 3
        self.desired_maximum_cuts_length = 4
        self.offset_start = 24
        self.offset_end = 17
        self.fadeInLevel = 50
        self.clip = mpe.VideoFileClip(self.movie_file_name)
        self.audio = mpe.AudioFileClip(self.music_file_name)   

    def gather_input_from_console(self):
        self.movie_file_name = input('Filename of movie?')
        self.music_file_name = input('Filename of music?')
        self.overlay_video_clip_name = input('Filename of overlay video?')
        self.overlay_picture_name = input('Filename of overlay picture?')
        self.output_file_name = input('Output filename?')         
        self.desired_duration = int(input('Desired edit duration in seconds?'))
        self.desired_minimum_cuts_length = int(input('Desired minimum cuts length in seconds?'))
        self.desired_maximum_cuts_length = int(input('Desired maximum cuts length in seconds?'))
        self.offset_start = int(input('Offset from start in seconds?'))
        self.offset_end = int(input('Offset from end in seconds?'))
        self.fadeInLevel = int(input('Fade in level in %?'))
        self.clip = mpe.VideoFileClip(self.movie_file_name)
        self.audio = mpe.AudioFileClip(self.music_file_name)        

class SequenceManager:
    def generate_non_overlapping_sequences(self, offset_start, total_input_length, min_segment_length, max_segment_length, total_output_length):
        result = []

        if (total_output_length > total_input_length):
            total_output_length = total_input_length

        random_intervals = self.generate_random_intervals(min_segment_length, max_segment_length, total_output_length)    
        empty_space_step = floor((total_input_length - total_output_length) / (len(random_intervals) + 1))

        current_pointer = empty_space_step

        for random_interval in random_intervals:
            result.append(Sequence(offset_start + current_pointer, offset_start + current_pointer + random_interval))
            current_pointer += random_interval + empty_space_step

        return result

    def generate_random_intervals(self, min_segment_length, max_segment_length, total_output_length):
        result = []

        current_length = 0

        while (current_length < total_output_length):
            current_segment_length = randint(min_segment_length, max_segment_length)

            if (current_length + current_segment_length > total_output_length):
                current_segment_length = total_output_length - current_length

            result.append(current_segment_length)
            current_length += current_segment_length

        return result

    def print_sequence(self, sequence):
        print('Begin: ' + str(sequence.begin) + '; End: ' + str(sequence.end) + '; Length: ' + str(sequence.end - sequence.begin))

    def print_results(self, non_overlapping_sequences):
        total_length = 0

        for non_overlapping_sequence in non_overlapping_sequences:
            self.print_sequence(non_overlapping_sequence)
            total_length += non_overlapping_sequence.end - non_overlapping_sequence.begin

        print('Total length: ' + str(total_length))

    def generate_sequence(self, inputAgent, shuffled, printResult):
        self.sequence = self.generate_non_overlapping_sequences(inputAgent.offset_start, inputAgent.clip.duration - inputAgent.offset_start - inputAgent.offset_end, inputAgent.desired_minimum_cuts_length, inputAgent.desired_maximum_cuts_length, inputAgent.desired_duration)                

        if (shuffled):
            shuffle(self.sequence)
        
        if (printResult):
            print('Sequence:')
            self.print_results(self.sequence)

class WordsGenerator:
    def getWord(self):
        word = word_list[randint(0, len(word_list))]
        spaced_word = '  '.join([e for e in word])

        return spaced_word

class VideoCreator:
    def createVideo(self, inputAgent, sequenceManager, wordsGenerator):
        final_clip_list = []
        final_total_length = 0
        distance_between_fadein_clips = 3
        clips_since_last_fadein = 0
        clip_number = 1
        clipSize = inputAgent.clip.size
        audioFadeInOutInterval = 3
        videoFadeInOutDelimiter = 3
        textClipDuration = 2

        for non_overlapping_sequence in sequenceManager.sequence:
            rand = randint(1, 100)
            sequenceLength = non_overlapping_sequence.end - non_overlapping_sequence.begin            
            subclip = inputAgent.clip.subclip(non_overlapping_sequence.begin, non_overlapping_sequence.end)            

            if (clip_number == len(sequenceManager.sequence)):
                final_clip_list.append(mpfxo.fadeout(subclip, sequenceLength / videoFadeInOutDelimiter))
            elif (clip_number == 1 or (rand <= inputAgent.fadeInLevel and clips_since_last_fadein >= distance_between_fadein_clips and clip_number < len(sequenceManager.sequence) - 2)):
                clips_since_last_fadein = 0
                final_clip_list.append(mpfxi.fadein(subclip, sequenceLength / videoFadeInOutDelimiter))
            else:
                clips_since_last_fadein += 1
                final_clip_list.append(subclip)

            final_total_length += sequenceLength
            clip_number += 1

        overlayClip = mpe.VideoFileClip(inputAgent.overlay_video_clip_name)
        overlayClips = []
        i = 1

        while i <= ceil(final_total_length / overlayClip.duration):
            overlayClips.append(overlayClip)
            i += 1

        finalWordClip = mpe.TextClip(wordsGenerator.getWord(), fontsize = 35, color = 'white', size = clipSize, bg_color = 'black', method = 'caption', align = 'center').set_duration(textClipDuration)
        finalSequenceClip = mpe.concatenate_videoclips(final_clip_list)
        finalOverlayClip = mpe.concatenate_videoclips(overlayClips).resize(clipSize).set_opacity(0.40).set_duration(final_total_length)

        # The composition is done here in this convoluted way, becasue for some reason it didn't work normally when I tried concatenate TextClip with VideoClips first and then place Overlay on top of all of them with CompositeVideoClip
        composedOverlayClip = mpe.CompositeVideoClip([finalSequenceClip, finalOverlayClip])

        finalOverlayImage = mpe.ImageClip(inputAgent.overlay_picture_name).resize(clipSize).set_opacity(0.30).set_duration(final_total_length + textClipDuration)
        finalAudio = mpafo.audio_fadeout(mpafi.audio_fadein(inputAgent.audio.set_duration(final_total_length + textClipDuration), audioFadeInOutInterval), audioFadeInOutInterval)

        mpe.CompositeVideoClip([mpe.concatenate_videoclips([finalWordClip, composedOverlayClip]), finalOverlayImage]).set_audio(finalAudio).write_videofile(inputAgent.output_file_name, codec = "libx264", audio_codec = "aac")

        # Have this here to avoid "OSError: [WinError 6] The handle is invalid" error at the end
        overlayClip.close()

# Main
seed(int(round(time.time() * 1000)))

inputAgent = InputAgent()
inputAgent.generate_test_input()
# inputAgent.gather_input_from_console() # Uncomment to provide your own input

sequenceManager = SequenceManager()
sequenceManager.generate_sequence(inputAgent, False, True)

wordsGenerator = WordsGenerator()

videoCreator = VideoCreator()
videoCreator.createVideo(inputAgent, sequenceManager, wordsGenerator)