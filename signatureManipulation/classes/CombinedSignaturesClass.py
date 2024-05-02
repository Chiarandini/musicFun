from SignatureClass import SignatureClass

class CombinedSignatureClass:

    """represents a signature object

    Attributes:
        signature_1: audio object for the raw audio
        signature_2: information on the user whom the signature belongs to
        id: unique identifier
    """

#todo: update once user object is created
    def __init__(self, signature_1: SignatureClass, signature_2: SignatureClass):
        # raw audio file object
        self.signature_1 = signature_1

        # the AI-modified audio
        self.signature_2 = signature_2

        #unique identifier
        self._id: str

    def __str__(self):
        return str(self.__dict__)


