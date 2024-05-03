# Import the AudioSegment class for processing audio and the
from pydub import AudioSegment
from pydub.silence import split_on_silence
# import pyrubberband as pyrb

import numpy as np
from SignatureClass import Signature
from CombinedSignaturesClass import CombinedSignature
from AudioClass import Audio
# from UserClass import User


class CombineSignatureFactory:
    """Takes two signatures and combines them. There are various different methods of
    combinations, and so there is a class to keep all ways of combining and tweaking of
    two signatures.

    Attributes:
        signature1: 1st signature. Must be a wav file
        signature2: 2nd signature. Must be a wav file
        splits_signature_1: List containing the segments that the 1st signature was split into
        splits_signature_2: List containing the segments that the 1st signature was split into
        combined_signature: output of the combine function (change which method used to get different results)
    """

    def __init__(self, signature1: Signature, signature2: Signature):
        self.signature_1 = signature1
        self.signature_2 = signature2
        # store the two signatures after the splitting method has been executed
        self.splits_signature_1 = []
        self.splits_signature_2 = []

        # stores resulting combined signatture (i.e., the output of the program)
        self.combined_signature: CombinedSignature

    # maybe this: https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-implement-multiple-constructors

    def __str__(self):
        return str(self.__dict__)

    # helper functions for split

    def _split_method_1(self, audio: Audio, silence_len=10,
                        silence_tresh=-56):
        """split the audio where there are silences

        Returns:
            list containing AudioSegment segments.
        """
        return split_on_silence(
            # Use the loaded audio.
            audio.raw_audio,
            # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
            min_silence_len=silence_len,
            # Consider a chunk silent if it's quieter than -16 dBFS.
            # (You may want to adjust this parameter.)
            silence_thresh=silence_tresh,
            # keep as much silence as possible
            keep_silence=500
        )

    # helper functions for combination

    def _match_target_amplitude(self, aChunk, target_dBFS):
        ''' Normalize given audio chunk '''
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)

    # def _audio_speed(self, audiosegment: AudioSegment, speed=1.0):
    #     y = np.array(audiosegment.get_array_of_samples())
    #     if audiosegment.channels == 2:
    #         y = y.reshape((-1, 2))
    #
    #     sample_rate = audiosegment.frame_rate
    #     y_fast = pyrb.time_stretch(y, sample_rate, speed)
    #
    #     channels = 2 if (y_fast.ndim == 2 and y_fast.shape[1] == 2) else 1
    #     y = np.int16(y_fast * 2 ** 15)
    #
    #     return AudioSegment(y.tobytes(), frame_rate=sample_rate, sample_width=2, channels=channels)

    def _combine_method_1(self, split_1: list[AudioSegment], split_2: list[AudioSegment]):
        """Take two split signatures, and tries to choose the combination that is as
        close as half as possible, then combine those, and normalize their length

        Args:
            split_1: 1st split audio segments
            split_2: 2nd spit audio segments

        TODO:
            currently, if forward and backward tally are the same, the first is chosen
            since it executes first. You may want slightly different behavior.
        """
        # NOTE : These are for testing purposes (don't know how to mock objects in python yet)
        # lengths_1 = [2, 2, 0.25, 4.75]
        # lengths_2 = [2, 2, 2, 2, 2]
        lengths_1 = [len(v) / 1000 for v in split_1]
        lengths_2 = [len(v) / 1000 for v in split_2]

        half = sum([len(v) / 1000 for v in split_2]) / 2

        # Find what is the closest the segments gets to the half-way point

        def find_mid_point(lengths: list[float], forward: bool):
            # going forward or backward through the list
            tally = 0
            prev = 0
            if forward:
                iter = 0
            else:
                iter = 1
            # NOTE: python doesn't have a do-while loop, so had to jank it
            while True:
                prev = tally
                if forward:
                    tally += lengths[iter]
                else:
                    tally += lengths[-iter]
                iter += 1
                if tally >= half:
                    break
            return (tally, prev, iter)

        forward_tally_1, forward_prev_1, forward_iter_1 = find_mid_point(lengths_1, True)
        forward_tally_2, forward_prev_2, forward_iter_2 = find_mid_point(lengths_2, True)
        backward_tally_1, backward_prev_1, backward_iter_1 = find_mid_point(lengths_1, False)
        backward_tally_2, backward_prev_2, backward_iter_2 = find_mid_point(lengths_2, False)

        # conditionals for finding the best splitting

        def combine_segments(options, split, f_iter, b_iter):
            min_val = min(options, key=lambda x: abs(x - half))

            if min_val == options[0]:
                return sum(split[0:f_iter])
            elif min_val == options[1]:
                return sum(split[0:f_iter - 1])
            elif min_val == options[2]:
                return sum(split[-b_iter + 1:])
            else:
                return sum(split[-b_iter + 2:])

        all_options_1 = [forward_tally_1, forward_prev_1, backward_tally_1, backward_prev_1]
        all_options_2 = [forward_tally_2, forward_prev_2, backward_tally_2, backward_prev_2]

        part_1 = combine_segments(all_options_1, split_1, forward_iter_1, backward_iter_1)
        part_2 = combine_segments(all_options_2, split_2, forward_iter_2, backward_iter_2)

        # TODO: normalize the lengths so that they are each half length
        # normalized_1 = self._audio_speed(part_1, part_1.duration_seconds / half)
        # normalized_2 = self._audio_speed(part_2, part_2.duration_seconds / half)

        # self.combined_signature = normalized_1 + normalized_2
        return part_1 + part_2

    def _combine_method_2(self, split_1: list[AudioSegment], split_2: list[AudioSegment]):
        """Take two split signatures, take the longest ones, and combine them.

        Args:
            split_1: 1st split audio segments
            split_2: 2nd spit audio segments
        """
        longest_clip_1 = max(split_1, key=len)
        longest_clip_2 = max(split_2, key=len)
        return longest_clip_1 + longest_clip_2

    def split(self, signature_1: Signature, signature_2: Signature, method=_split_method_1):
        """Splits signature_1 and signature_2 bassed off of the desired method
           (default method provided)

        Args:
            method (func): the method of audio splitting
        """
        return (method(self, signature_1.audio_obj), method(self, signature_2.audio_obj))

    def combine(self,
                split_1: list[AudioSegment],
                split_2: list[AudioSegment], method=_combine_method_1) -> AudioSegment:
        return method(self, split_1, split_2)

    def build(self) -> CombinedSignature:
        self.splits_signature_1, self.splits_signature_2 = self.split(self.signature_1, self.signature_2)
        combo = self.combine(self.splits_signature_1, self.splits_signature_2)
        # TODO: This will have to be AI-ed
        ai_combo = combo  # post-AI
        # WARN: This shows we need to think more about he CombinedSignature Object
        combo_sig = Signature(Audio(combo, ''), ai_combo,
                              self.signature_1.user)
        return CombinedSignature(self.signature_1, self.signature_2, combo_sig)


# def save_splits(path: str, chunks: list[AudioSegment]):
#
#     # Process each chunk with your parameters
#     for i, chunk in enumerate(chunks):
#         # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
#         # silence_chunk = AudioSegment.silent(duration=500)
#
#         # Add the padding chunk to beginning and end of the entire chunk.
#         # audio_chunk = silence_chunk + chunk + silence_chunk
#
#         # Normalize the entire chunk.
#         normalized_chunk = self._match_target_amplitude(chunk, -20.0)
#
#         # Export the audio chunk with new bitrate.
#         print("Exporting chunk{0}.mp3.".format(i))
#         normalized_chunk.export(
#             path + "/chunk{0}.mp3".format(i),
#             bitrate="192k",
#             format="mp3"
#         )

# if __name__ == "__main__":
#     number1, number2 = '001', '002'
#     # number1, number2 = '033', '020'
#     # number1, number2 = '034', '050'
#     sig1, sig2 = '../signatures/Signature-4_' + number1 + '.mp3', '../signatures/Signature-4_' + number2 + '.mp3'
#     test = CombinedSignature(sig1, sig2)
#     test.execute()

#     audio1, audio2 = AudioSegment.from_file(sig1), AudioSegment.from_file(sig2)
#     play(audio1)
#     play(AudioSegment.silent(500))
#     play(audio2)
#     play(AudioSegment.silent(900))
#     play(test.combined_signature)
