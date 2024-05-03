class User:

    """represents a user object

    Attributes:
        responses: responses of the user to quiz questions
        id: unique identifier
    """

#todo: update once user object is created
    def __init__(self, responses: dict):
        # raw audio file object
        self.responses = responses

        #unique identifier
        self._id: str

    def __str__(self):
        return str(self.__dict__)