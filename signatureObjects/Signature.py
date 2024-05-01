

from pydub import AudioSegment


class Signature:

    """Holds all information a single signature would need

    Attributes:
        raw_audio: The audio-file which will be processed by the AI
        raw_audio_description: The text associated with the raw audio
        signature: the processed audio information
        text_prompt: The text-prompt used to generate the signature
    """

    def __init__(self, path: str, description: str = ''):
        # raw audio file saved
        self.base_audio = AudioSegment.from_file(path)

        # description acompanying audio file
        self.raw_audio_description = description

        # text prompt used to generate signature
        self.text_promt = ''

        # Processed Signature (Post AI)
        self.signature = None

        # HACK: This REALLY shouldn't be here. temporary hack for AI object!
        # original path
        self.path = path

    def __str__(self):
        return str(self.__dict__)


if __name__ == "__main__":
    sig = Signature('./../signatures/Signature-4_002.mp3', 'test')
    print(sig)
