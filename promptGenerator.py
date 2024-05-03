import random
import json

with open("json_files/prompts.json", "r") as file:
    all_prompts = json.load(file)


def response_to_prompt(user_responses):
    prompt_words = []
    for question in user_responses:
        response = user_responses[question][0]
        choice_adj_array = all_prompts[question][2][response]
        prompt_word = random.choice(choice_adj_array)
        prompt_words.append(prompt_word)
    prompt_str = ' '.join(prompt_words)
    return (prompt_str)


# class PromptGenerator:
#     # NOTE: Don't forget to generate doc by doing <leader>c on the class name.

#     # Holds all the questions: key is the quetsion and value is the possible answers
#     question_dict = {}

#     # This will be the result
#     result = ''


#     def __str__(self):
#         return str(self.__dict__)
