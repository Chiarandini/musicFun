from pydub import AudioSegment
from classes.AudioClass import AudioClass
from classes.UserClass import UserClass

class SignatureClass:

    """represents a signature object

    Attributes:
        raw_audio: audio object for the raw audio
        user: information on the user whom the signature belongs to
        signature_audio: the AI generated audio information
        ai_prompt: The text-prompt used to generate the signature
        id: unique identifier
    """

#TODO: update once user object is created
    def __init__(self, audio_obj: AudioClass, signature_audio: AudioSegment, user: UserClass, ai_prompt: str =''):
        # raw audio file object
        self.audio_obj = audio_obj

        # the AI-modified audio
        self.signature_audio = signature_audio

        # text prompt used to generate signature
        self.ai_prompt = ai_prompt

        # user object information
        self.user= user

        #unique identifier
        self._id: str

    def __str__(self):
        return str(self.__dict__)


