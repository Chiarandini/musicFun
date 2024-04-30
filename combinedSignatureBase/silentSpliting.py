# Import the AudioSegment class for processing audio and the
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.playback import play

# Define a function to normalize a chunk to a target amplitude.


class CombinedSignature:
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
    # stores signatures that need to be combined
    signature_1 = None
    signature_2 = None

    # store the two signatures after the splitting method has been executed
    splits_signature_1 = []
    splits_signature_2 = []

    #stores resulting combined signatture (i.e., the output of the program)
    combined_signature = None

    def __init__(self, signature1, signature2):
        try:
            self.signature_1 = AudioSegment.from_file(signature1)
            self.signature_2 = AudioSegment.from_file(signature2)
            if round(self.signature_1.duration_seconds) != round(self.signature_2.duration_seconds):
                raise AttributeError("Both audiofiles must have the same duration")
        except FileNotFoundError:
            raise FileNotFoundError("File not Found")

    def __str__(self):
        return str(self.__dict__)

    def _match_target_amplitude(self, aChunk, target_dBFS):
        ''' Normalize given audio chunk '''
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)

    def _split_method_1(self, audio, silence_len=10, silence_tresh=-56) -> list[AudioSegment]:
        """split the audio where there are silences

        Returns:
            list containing AudioSegment segments.
        """
        return split_on_silence(
            # Use the loaded audio.
            audio,
            # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
            min_silence_len=silence_len,
            # Consider a chunk silent if it's quieter than -16 dBFS.
            # (You may want to adjust this parameter.)
            silence_thresh=silence_tresh,
            # keep as much silence as possible
            keep_silence=500
        )

    def split(self, method=_split_method_1) -> None:
        """Splits signature_1 and signature_2 bassed off of the desired method
           (default method provided)

        Args:
            method (func): the method of audio splitting
        """
        self.splits_signature_1 = method(self, self.signature_1)
        self.splits_signature_2 = method(self, self.signature_2)

    def _combine_method_1(self, split_1: list[AudioSegment], split_2: list[AudioSegment]):
        """Take two split signatures, and tries to choose the combination that is as
        close as half as possible, then combine those, and normalize their length

        Args:
            split_1: 1st split audio segments
            split_2: 2nd spit audio segments
        """
        lengths_1 = [len(v) / 1000 for v in split_1]
        lengths_2 = [len(v) / 1000 for v in split_2]
        half = sum([len(v) / 1000 for v in split_2]) / 2
        print(lengths_1)
        print(lengths_2)
        print(half)

        # Find what is the closest the segments gets to the half-way point
        forward_tally_1 = 0
        forward_prev_1 = 0
        forward_iter_1 = 0
        while forward_tally_1 < half:
            forward_prev_1 = forward_tally_1
            forward_tally_1 += lengths_1[forward_iter_1]
            forward_iter_1 += 1

        forward_tally_2 = 0
        forward_prev_2 = 0
        forward_iter_2 = 0
        while forward_tally_2 < half:
            forward_prev_2 = forward_tally_2
            forward_tally_2 += lengths_2[forward_iter_2]
            forward_iter_2 += 1

        backward_tally_1 = 0
        backward_prev_1 = 0
        backward_iter_1 = 1
        while backward_tally_1 < half:
            backward_prev_1 = backward_tally_1
            backward_tally_1 += lengths_1[-backward_iter_1]
            backward_iter_1 += 1

        backward_tally_2 = 0
        backward_prev_2 = 0
        backward_iter_2 = 1
        while backward_tally_2 < half:
            backward_prev_2 = backward_tally_2
            backward_tally_2 += lengths_2[-backward_iter_2]
            backward_iter_2 += 1

        # conditionals for finding the best splitting
        all_options_1 = [forward_tally_1, forward_prev_1, backward_tally_1, backward_prev_1]
        min_val_1 = min(all_options_1, key=lambda x: abs(x - half))

        # TODO: Now that you know where to split the signatures, combine the segments.
        if min_val_1 == forward_tally_1:
            print('best split for split_1 is forward_tally_1: ' + str(forward_tally_1))
            part_1 = sum(split_1[0:iter])
        elif min_val_1 == forward_prev_1:
            print('best split for split_1 is forward_prev_1: ' + str(forward_prev_1))
            part_1 = sum(split_1[0:(iter - 1)])
        elif min_val_1 == backward_tally_1:
            print('best split for split_1 is backward_tally_1: ' + str(backward_tally_1))
            part_1 = sum(split_1[-1:-iter])
        else:
            print('best split for split_1 is backward_prev_1: ' + str(backward_tally_1))

        all_options_2 = [forward_tally_2, forward_prev_2, backward_tally_2, backward_prev_2]
        min_val_2 = min(all_options_2, key=lambda x: abs(x - half))

        if min_val_2 == forward_tally_2:
            print('best split for split_2 is forward_tally_2: ' + str(forward_tally_2))
        elif min_val_2 == forward_prev_2:
            print('best split for split_2 is forward_prev_2: ' + str(forward_prev_2))
        elif min_val_2 == backward_tally_2:
            print('best split for split_2 is backward_tally_2: ' + str(backward_tally_2))
        else:
            print('best split for split_2 is backward_prev_2: ' + str(backward_prev_2))

        # TODO: normalize the lengths so that they are each half length

        # TODO: Combine normalized_part_1 and normalized_part_2
    def _combine_method_2(self, split_1: list[AudioSegment], split_2: list[AudioSegment]):
        """Take two split signatures, take the longest ones, and combine them.

        Args:
            split_1: 1st split audio segments
            split_2: 2nd spit audio segments
        """
        longest_clip_1 = max(split_1, key=len)
        longest_clip_2 = max(split_2, key=len)

        self.combined_signature = longest_clip_1 + longest_clip_2

    def combine(self, method=_combine_method_1):
        method(self, self.splits_signature_1, self.splits_signature_2)

    def execute(self):
        self.split()
        self.combine()

    def save_splits(self, path: str, chunks):

        # Process each chunk with your parameters
        for i, chunk in enumerate(chunks):
            # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
            # silence_chunk = AudioSegment.silent(duration=500)

            # Add the padding chunk to beginning and end of the entire chunk.
            # audio_chunk = silence_chunk + chunk + silence_chunk

            # Normalize the entire chunk.
            normalized_chunk = self._match_target_amplitude(chunk, -20.0)

            # Export the audio chunk with new bitrate.
            print("Exporting chunk{0}.mp3.".format(i))
            normalized_chunk.export(
                path + "/chunk{0}.mp3".format(i),
                bitrate="192k",
                format="mp3"
            )


if __name__ == "__main__":
    # number1, number2 = '001', '002'
    # number1, number2 = '033', '020'
    number1, number2 = '034', '050'
    sig1, sig2 = '../signatures/Signature-4_' + number1 + '.mp3', '../signatures/Signature-4_' + number2 + '.mp3'
    test = CombinedSignature(sig1, sig2)
    test.execute()
    play(test.combined_signature)
    play(AudioSegment.silent(900))
    audio1, audio2 = AudioSegment.from_file(sig1), AudioSegment.from_file(sig2)
    play(audio1)
    play(AudioSegment.silent(500))
    play(audio2)
