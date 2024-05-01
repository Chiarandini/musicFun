class PromptGenerator:
    # NOTE: Don't forget to generate doc by doing <leader>c on the class name.

    # Holds all the questions: key is the quetsion and value is the possible answers
    question_dict = {}

    # This will be the result
    result = ''

    def __str__(self):
        return str(self.__dict__)
