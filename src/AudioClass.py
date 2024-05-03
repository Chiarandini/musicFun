from pydub import AudioSegment


class Audio:
    """raw audio information

    Attributes:
        raw_audio (AudioSegment): The base audio-file generated manually
        raw_audio_description (str): The text associated with the raw audio
        id: unique identifier
    """

    def __init__(self, raw_audio: AudioSegment, raw_audio_description: str = ''):
        # raw audio file saved
        self.raw_audio = raw_audio

        # description acompanying audio file
        self.raw_audio_description = raw_audio_description

        # unique identifier
        self._id: str

    def __str__(self):
        return str(self.__dict__)
