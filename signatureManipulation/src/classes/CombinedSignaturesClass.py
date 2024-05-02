from classes.SignatureClass import SignatureClass

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


