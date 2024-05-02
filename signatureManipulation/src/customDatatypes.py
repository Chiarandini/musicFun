from pydub import AudioSegment

# representation of an audio file with its description

class AudioClass:

    """raw audio information

    Attributes:
        raw_audio: The base audio-file generated manually
        raw_audio_description: The text associated with the raw audio        
        id: unique identifier
    """

    def __init__(self, raw_audio: AudioSegment, raw_audio_description: str = ''):
        # raw audio file saved
        self.raw_audio = raw_audio

        # description acompanying audio file
        self.raw_audio_description = raw_audio_description

        #unique identifier
        self._id: str


    def __str__(self):
        return str(self.__dict__)

# representation of a user

class UserClass:

    """represents a user object

    Attributes:
        responses: responses of the user to quiz questions
        id: unique identifier
    """

    def __init__(self, responses: dict):
        # raw audio file object
        self.responses = responses

        #unique identifier
        self._id: str

    def __str__(self):
        return str(self.__dict__)


# a signature object with a lot of information

class SignatureClass:

    """represents a signature object

    Attributes:
        raw_audio: audio object for the raw audio
        user: information on the user whom the signature belongs to
        signature_audio: the AI generated audio information
        ai_prompt: The text-prompt used to generate the signature
        id: unique identifier
    """

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


# combined signature class
class CombinedSignatureClass:

    """represents a signature object

    Attributes:
        signature_1: signature object for first user
        signature_2: signature object for second user
        combined_signature: combined signature object of the two users
        id: unique identifier
    """

#todo: update once user object is created
    def __init__(self, signature_1: SignatureClass, signature_2: SignatureClass, combined_signature: SignatureClass):
        # signature object for first user
        self.signature_1 = signature_1

        # signature object for second user
        self.signature_2 = signature_2

        # combined signature object of the two people
        self.combined_signature = combined_signature

        #unique identifier
        self._id: str

    def __str__(self):
        return str(self.__dict__)


