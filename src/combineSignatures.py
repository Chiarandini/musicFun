from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.playback import play
import pyrubberband as pyrb

import numpy as np
from classes.SignatureClass import Signature
from classes.SignatureClass import Signature
from classes.AudioClass import Audio
from classes.UserClass import User


def _split_method_1(audio, silence_len=10, silence_tresh=-56) -> list[AudioSegment]:
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


# helper functions for combination

def _match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


def _audio_speed(audiosegment, speed=1.0):
    y = np.array(audiosegment.get_array_of_samples())
    if audiosegment.channels == 2:
        y = y.reshape((-1, 2))

    sample_rate = audiosegment.frame_rate
    y_fast = pyrb.time_stretch(y, sample_rate, speed)

    channels = 2 if (y_fast.ndim == 2 and y_fast.shape[1] == 2) else 1
    y = np.int16(y_fast * 2 ** 15)

    return AudioSegment(y.tobytes(), frame_rate=sample_rate, sample_width=2, channels=channels)


def _combine_method_1(split_1: list[AudioSegment], split_2: list[AudioSegment]):
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
    # NOTE: python doesn't have a do-while loop, so had to jank it
    forward_tally_1 = 0
    forward_prev_1 = 0
    forward_iter_1 = 0
    while True:
        forward_prev_1 = forward_tally_1
        forward_tally_1 += lengths_1[forward_iter_1]
        forward_iter_1 += 1
        if forward_tally_1 >= half:
            break

    forward_tally_2 = 0
    forward_prev_2 = 0
    forward_iter_2 = 0
    while True:
        forward_prev_2 = forward_tally_2
        forward_tally_2 += lengths_2[forward_iter_2]
        forward_iter_2 += 1
        if forward_tally_2 >= half:
            break

    backward_tally_1 = 0
    backward_prev_1 = 0
    backward_iter_1 = 1
    while True:
        backward_prev_1 = backward_tally_1
        backward_tally_1 += lengths_1[-backward_iter_1]
        backward_iter_1 += 1
        if backward_tally_1 >= half:
            break

    backward_tally_2 = 0
    backward_prev_2 = 0
    backward_iter_2 = 1
    while True:
        backward_prev_2 = backward_tally_2
        backward_tally_2 += lengths_2[-backward_iter_2]
        backward_iter_2 += 1
        if backward_tally_2 >= half:
            break

    # conditionals for finding the best splitting
    all_options_1 = [forward_tally_1, forward_prev_1, backward_tally_1, backward_prev_1]
    min_val_1 = min(all_options_1, key=lambda x: abs(x - half))

    if min_val_1 == forward_tally_1:
        part_1 = sum(split_1[0:forward_iter_1])
    elif min_val_1 == forward_prev_1:
        part_1 = sum(split_1[0:forward_iter_1 - 1])
    elif min_val_1 == backward_tally_1:
        part_1 = sum(split_1[-backward_iter_1 + 1:])
    else:
        part_1 = sum(split_1[-backward_iter_1 + 2:])

    all_options_2 = [forward_tally_2, forward_prev_2, backward_tally_2, backward_prev_2]
    min_val_2 = min(all_options_2, key=lambda x: abs(x - half))

    if min_val_2 == forward_tally_2:
        part_2 = sum(split_2[0:forward_iter_2])
    elif min_val_2 == forward_prev_2:
        part_2 = sum(split_2[0:forward_iter_2 - 1])
    elif min_val_2 == backward_tally_2:
        part_2 = sum(split_2[-backward_iter_2 + 1:])
    else:
        part_2 = sum(split_2[-backward_iter_2 + 2:])

    # TODO: normalize the lengths so that they are each half length
    normalized_1 = _audio_speed(part_1, part_1.duration_seconds / half)
    normalized_2 = _audio_speed(part_2, part_2.duration_seconds / half)

    # combine_signatures = part_1 + part_2
    combine_signatures = normalized_1 + normalized_2

    return combine_signatures

    # TODO: Combine normalized_part_1 and normalized_part_2


# execution of the functionalities

def split(signature_audio_1: Audio, signature_audio_2: Audio, method=_split_method_1) -> list:
    return ([method(signature_audio_1), method(signature_audio_2)])


def combine(splits_1: list, splits_2: list, method=_combine_method_1):
    return method(splits_1, splits_2)


def execute(signature1: Signature, signature2: Signature):
    split_arrays = split(signature1.audio_obj, signature2.audio_obj)
    return combine(split_arrays[0], split_arrays[1])
