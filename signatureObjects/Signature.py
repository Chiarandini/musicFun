

from pydub import AudioSegment


class Signature:

    """Holds all information a single signature would need

    Attributes:
        raw_audio: The audio-file which will be processed by the AI
        raw_audio_description: The text associated with the raw audio
        signature: the processed audio information
        text_prompt: The text-prompt used to generate the signature
    """
    # raw audio file saved
    base_audio = None

    # Processed Signature (Post AI)
    signature = None

    # text prompt used to generate signature
    text_prompt = ''

    # The text used to help find the right signature
    raw_audio_description = ''

    def __init__(self, path: str, description: str = ''):
        self.base_audio = AudioSegment.from_file(path)
        self.raw_audio_description = description

    def __str__(self):
        return str(self.__dict__)


if __name__ == "__main__":
    sig = Signature('./../signatures/Signature-4_002.mp3', 'test')
    print(sig)
